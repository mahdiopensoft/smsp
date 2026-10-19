"""
apps/omr/api.py — OMR API Endpoints
=====================================
POST /api/omr/grade/          رفع ورقة + تصحيح فوري (demo أو حقيقي)
GET  /api/omr/results/<id>/   عرض نتيجة محفوظة
GET  /api/omr/annotated/<id>/ صورة الورقة المُعلَّقة (PNG)
"""

import base64
import json
import logging
import os
import tempfile
import uuid
import io
import zipfile

from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

logger = logging.getLogger("omr.api")

# مخزن مؤقت للنتائج (demo mode — لا قاعدة بيانات)
_RESULT_CACHE: dict = {}


def _process_and_grade_image_file(
    image_path: str,
    original_filename: str = "",
    template_id: str = "",
    answer_key: dict = None,
    marks_map: dict = None,
    dpi: int = 300,
    exam_id=None,
    version_id=None,
    version_code=None,
    target_version=None,
    exam_obj=None,
    batch_obj=None,
    page_number: int = 1,
    request_user=None,
) -> dict:
    """
    الدالة المركزية لتصحيح ورقة إجابة واحدة (صورة أو صفحة مفردة من PDF)،
    مطابقة بيانات الطالب ورقم الجلوس، التحقق الصارم من عدم انتهاك قفل الكنترول المركزي،
    وحفظ النتيجة في قاعدة البيانات.
    """
    answer_key = answer_key or {}
    marks_map = marks_map or {}

    # ═══ التصحيح بالمحرك المناسب ═══
    if template_id or template_id == "":
        result = _grade_with_template(
            image_path, template_id or "AUTO", answer_key, dpi,
            original_filename=original_filename or os.path.basename(image_path),
            marks_map=marks_map
        )
    else:
        result = _grade_with_legacy(image_path, answer_key, dpi, marks_map=marks_map)

    from exams.models.Exam import Exam
    from exams.models.StudentExamRegistration import StudentExamRegistration
    from exams.models.ExamVersion import ExamVersion
    from submissions.models.Submission import Submission
    from omr.models.OMRSheetResult import OMRSheetResult
    from omr.models.OMRQuestionResult import OMRQuestionResult
    from omr.providers.opencv_omr import normalize_choice
    from django.core.files.base import ContentFile

    student_info = result.get("student_info", {})
    s_name = student_info.get("name") or "طالب اختبار"
    seat_num = student_info.get("seat_number") or result.get("barcode") or ""
    total_q = result.get("total_questions", len(result.get("questions", [])))

    if not exam_obj:
        if exam_id:
            try:
                exam_obj = Exam.objects.filter(id=int(exam_id), is_deleted=False).first()
            except (ValueError, TypeError):
                pass
        if not exam_obj and target_version and hasattr(target_version, "exam"):
            exam_obj = target_version.exam

    # مطابقة الاختبار والطالب ورقم جلوسه آلياً من الباركود والـ QR وقاعدة البيانات
    import re
    barcode_val = result.get("barcode") or ""
    qr_val = result.get("qr") or ""

    # استخراج معرف الاختبار من الباركود إذا وجد (مثال: EXAM_7_VER_A_SEAT_418485)
    if barcode_val and "EXAM_" in barcode_val:
        try:
            ex_part = barcode_val.split("EXAM_")[1].split("_")[0]
            if ex_part.isdigit():
                found_ex = Exam.objects.filter(id=int(ex_part), is_deleted=False).first()
                if found_ex:
                    exam_obj = found_ex
        except Exception:
            pass

    # تجهيز قائمة بأرقام الجلوس المحتملة من الباركود والـ QR
    candidate_seats = []
    if seat_num:
        candidate_seats.append(str(seat_num).strip())
    if barcode_val:
        if "_SEAT_" in barcode_val:
            candidate_seats.append(barcode_val.split("_SEAT_")[-1].split("_")[0].strip())
        clean_b = barcode_val.strip()
        candidate_seats.append(clean_b)
        if len(clean_b) >= 6:
            candidate_seats.append(clean_b[:6])
    if qr_val:
        tokens = [t.strip() for t in re.split(r'[-|_/]', qr_val) if t.strip().isdigit()]
        candidate_seats.extend(tokens)

    matched_reg = None
    if exam_obj:
        reg_qs = StudentExamRegistration.objects.filter(examVersion__exam=exam_obj, is_deleted=False).select_related('student', 'student_profile__organization', 'examVersion')
        for c_seat in candidate_seats:
            if c_seat:
                matched_reg = reg_qs.filter(seatNumber=c_seat).first()
                if matched_reg:
                    break
        if not matched_reg and barcode_val:
            for r in reg_qs:
                if r.seatNumber and (r.seatNumber in barcode_val or barcode_val.startswith(r.seatNumber)):
                    matched_reg = r
                    break

    inst_name = ""
    if matched_reg:
        if not target_version:
            target_version = matched_reg.examVersion
        if matched_reg.student_profile and matched_reg.student_profile.name_ar:
            s_name = matched_reg.student_profile.name_ar
        elif matched_reg.student:
            s_name = matched_reg.student.first_name or matched_reg.student.username
        if not seat_num:
            seat_num = matched_reg.seatNumber
        if matched_reg.student_profile and matched_reg.student_profile.organization:
            inst_name = matched_reg.student_profile.organization.name_ar

    # ═══ قفل وحماية الكنترول المركزي الصارم (Control Lock Enforcement) ═══
    # يمنع منعاً باتاً تعديل أو إعادة تصحيح أي ورقة لطالب تم ترحيلها واعتمادها رسمياً في الكنترول
    existing_locked_sub = None
    if matched_reg:
        existing_locked_sub = Submission.objects.filter(
            exam=exam_obj, registration=matched_reg, is_deleted=False
        ).first()
    elif seat_num and exam_obj:
        existing_locked_sub = Submission.objects.filter(
            exam=exam_obj, layout_result__seat_number=str(seat_num), is_deleted=False
        ).first()

    if existing_locked_sub:
        lr_check = existing_locked_sub.layout_result or {}
        if lr_check.get("dispatched_to_control"):
            receipt = lr_check.get("control_receipt_code", "CTL-CONFIRMED")
            disp_date = lr_check.get("dispatched_at", "")
            raise PermissionError(
                f"درجات الطالب '{s_name}' (رقم الجلوس: {seat_num}) معتمدة ومقفلة رسمياً بنظام الكنترول المركزي (إيصال: {receipt} بتاريخ: {disp_date}). يمنع منعاً باتاً إعادة تصحيح أو تعديل الورقة."
            )

    # مطابقة النموذج المحدد من الباركود إذا لم يكن محدداً
    if not target_version and barcode_val and "_VER_" in barcode_val and exam_obj:
        try:
            v_code = barcode_val.split("_VER_")[1].split("_")[0]
            target_version = ExamVersion.objects.filter(exam=exam_obj, versionCode=v_code, is_deleted=False).prefetch_related('question_orders__question__options').first()
        except Exception:
            pass

    # إذا تم كشف نموذج معتمد بدقة، يتم إعادة احتساب الدرجات بمفتاح النموذج الفعلي
    if target_version:
        v_key = {}
        v_marks = {}
        for qo in target_version.question_orders.filter(is_deleted=False).order_by('orderIndex'):
            q = qo.question
            opts = list(q.options.filter(is_deleted=False))
            ans_letter = 'A'
            for idx, opt in enumerate(opts):
                if opt.isTrue:
                    ans_letter = chr(65 + idx)
                    break
            if (q.questionType in ['True/False', 'true_false', 'صح وخطأ']) or (q.isTrue is not None):
                ans_letter = 'A' if q.isTrue is True else ('B' if q.isTrue is False else ans_letter)
            v_key[str(qo.orderIndex)] = ans_letter
            v_marks[str(qo.orderIndex)] = float(q.defaultMark or 1.0)

        re_score = 0.0
        re_max = 0.0
        re_correct = 0
        for q_item in result.get("questions", []):
            q_id_str = str(q_item.get("question_id") or q_item.get("q") or 1)
            exp = v_key.get(q_id_str)
            w = float(v_marks.get(q_id_str, 1.0))
            re_max += w
            q_item["correct_choice"] = exp
            q_item["max_mark"] = w
            m_choice = q_item.get("marked_choice") or q_item.get("marked")
            if m_choice and exp:
                if normalize_choice(m_choice) == normalize_choice(exp):
                    q_item["is_correct"] = True
                    q_item["marks_awarded"] = w
                    re_score += w
                    re_correct += 1
                else:
                    q_item["is_correct"] = False
                    q_item["marks_awarded"] = 0.0
            else:
                q_item["is_correct"] = False if m_choice else None
                q_item["marks_awarded"] = 0.0

        result["score"] = round(re_score, 2)
        result["max_score"] = round(re_max if re_max > 0 else float(total_q), 2)
        result["total_correct"] = re_correct
        result["total_wrong"] = result.get("total_answered", 0) - re_correct
        result["score_percent"] = round((result["score"] / max(result["max_score"], 1.0)) * 100.0, 1)

    total_c = result.get("total_correct", 0)
    qs = result.get("questions", [])
    if qs:
        avg_conf = sum(float(q.get("final_confidence") or q.get("confidence") or 0.95) for q in qs) / len(qs)
    else:
        avg_conf = 0.95
    confidence = float(result.get("overall_confidence") or result.get("confidence") or avg_conf)

    ambiguous_cnt = sum(1 for q in qs if q.get("bubble_state") in ["ambiguous", "multiple"])
    if ambiguous_cnt == 0:
        ambiguous_cnt = result.get("ai_corrections", 0)

    initial_sub_status = Submission.Status.NEEDS_REVIEW if (ambiguous_cnt > 0 or confidence < 0.85) else Submission.Status.COMPLETED
    initial_sheet_status = "needs_review" if (ambiguous_cnt > 0 or confidence < 0.85) else "success"

    annotated_raw = result.pop("annotated_image", b"")
    annotated_b64 = base64.b64encode(annotated_raw).decode() if annotated_raw else ""

    if not exam_obj:
        # لم يتم تحديد أي اختبار: نرجع النتيجة الفورية بدون إنشاء أي اختبار أو حشو قاعدة البيانات
        result_id = str(uuid.uuid4())
        _RESULT_CACHE[result_id] = {
            "meta": {k: v for k, v in result.items() if k != "questions"},
            "questions": result["questions"],
            "annotated_b64": annotated_b64,
        }
        return {
            "result_id":       result_id,
            "submission_id":   None,
            "page_number":     page_number,
            "student_name":    s_name,
            "seat_number":     seat_num,
            "status":          initial_sub_status,
            "confidence":      confidence,
            "total_questions": total_q,
            "score":           result["score"],
            "max_score":       result["max_score"],
            "score_percent":   result["score_percent"],
            "total_correct":   total_c,
            "total_wrong":     result.get("total_wrong", 0),
            "total_answered":  result.get("total_answered", 0),
            "total_empty":     result.get("total_empty", 0),
            "ai_corrections":  ambiguous_cnt,
            "processing_ms":   result["processing_ms"],
            "questions":       result["questions"],
            "annotated_image": annotated_b64,
            "engine_used":     result.get("engine_used", "legacy"),
            "template_id":     result.get("template_id") or template_id or "svg_hardcoded",
            "template_name":   result.get("template_name", ""),
            "barcode":         barcode_val,
            "qr":              qr_val,
            "student_info":    result.get("student_info", {}),
            "switched_notice": result.get("switched_notice", ""),
        }

    sub_kwargs = {
        "exam": exam_obj,
        "batch": batch_obj,
        "status": initial_sub_status,
        "current_engine": result.get("engine_used", "opencv_omr"),
        "mcq_score": result.get("score", 0),
        "total_score": result.get("score", 0),
        "overall_confidence": confidence,
        "processing_time_ms": result.get("processing_ms", 0.0),
        "omr_result": result.get("questions", []),
        "layout_result": {
            "student_name": s_name,
            "seat_number": seat_num,
            "institution_name": inst_name,
            "template_id": result.get("template_id"),
            "template_name": result.get("template_name"),
            "barcode": barcode_val,
            "qr": qr_val,
            "total_questions": total_q,
            "score_percent": result.get("score_percent", 0),
            "ambiguous_count": ambiguous_cnt,
            "page_number": page_number,
        }
    }
    if target_version:
        sub_kwargs["exam_version"] = target_version

    if existing_locked_sub:
        # تحديث السجل غير المقفل القائم لمنع التكرار في المظروف الامتحاني
        sub_record = existing_locked_sub
        for k, v in sub_kwargs.items():
            setattr(sub_record, k, v)
        if matched_reg:
            sub_record.registration = matched_reg
        OMRSheetResult.objects.filter(submission=sub_record).delete()
    else:
        if matched_reg and not Submission.objects.filter(registration=matched_reg, exam=exam_obj, is_deleted=False).exists():
            sub_kwargs["registration"] = matched_reg
        sub_record = Submission(**sub_kwargs)

    try:
        with open(image_path, "rb") as f_img:
            sub_record.original_image.save(os.path.basename(original_filename or image_path), ContentFile(f_img.read()), save=False)
    except Exception as img_save_err:
        logger.warning(f"Could not save original image to submission: {img_save_err}")

    if annotated_raw:
        try:
            sub_record.aligned_image.save(f"annotated_sub_{sub_record.id or 'scan'}.png", ContentFile(annotated_raw), save=False)
        except Exception as img_save_err:
            logger.warning(f"Could not save aligned image to submission: {img_save_err}")

    sub_record.save()

    sheet_obj = OMRSheetResult.objects.create(
        submission=sub_record,
        status=initial_sheet_status,
        confidence=confidence,
        total_questions=total_q,
        answered_questions=result.get("total_answered", 0),
        correct_answers=total_c,
        wrong_answers=result.get("total_wrong", 0),
        unanswered=result.get("total_empty", 0),
        ambiguous_count=ambiguous_cnt,
        mcq_score=result.get("score", 0),
        mcq_max_score=result.get("max_score", total_q),
        provider_used=result.get("engine_used", "opencv_omr"),
        processing_time_ms=result.get("processing_ms", 0.0),
    )

    for q_item in result.get("questions", []):
        q_num = int(q_item.get("question_id") or q_item.get("q") or 1)
        OMRQuestionResult.objects.create(
            sheet_result=sheet_obj,
            question_number=q_num,
            marked_choice=q_item.get("marked_choice") or q_item.get("marked"),
            correct_choice=q_item.get("correct_choice") or q_item.get("correct"),
            is_correct=q_item.get("is_correct"),
            bubble_state=q_item.get("bubble_state") or ("filled" if q_item.get("marked_choice") else "empty"),
            choice_confidences=q_item.get("choice_confidences") or {},
            final_confidence=float(q_item.get("final_confidence") or q_item.get("confidence") or 0.95),
            marks_awarded=float(q_item.get("marks_awarded", q_item.get("score_awarded", 1.0 if q_item.get("is_correct") else 0.0))),
        )

    result_id = str(sub_record.id)
    _RESULT_CACHE[result_id] = {
        "meta": {k: v for k, v in result.items() if k != "questions"},
        "questions": result["questions"],
        "annotated_b64": annotated_b64,
    }

    return {
        "result_id":       result_id,
        "submission_id":   sub_record.id,
        "page_number":     page_number,
        "student_name":    s_name,
        "seat_number":     seat_num,
        "status":          initial_sub_status,
        "confidence":      confidence,
        "total_questions": total_q,
        "score":           result["score"],
        "max_score":       result["max_score"],
        "score_percent":   result["score_percent"],
        "total_correct":   result["total_correct"],
        "total_wrong":     result["total_wrong"],
        "total_answered":  result["total_answered"],
        "total_empty":     result["total_empty"],
        "ai_corrections":  ambiguous_cnt,
        "processing_ms":   result["processing_ms"],
        "questions":       result["questions"],
        "annotated_image": annotated_b64,
        "engine_used":     result.get("engine_used", "legacy"),
        "template_id":     result.get("template_id") or template_id or "svg_hardcoded",
        "template_name":   result.get("template_name", ""),
        "barcode":         barcode_val,
        "qr":              qr_val,
        "student_info":    result.get("student_info", {}),
        "switched_notice": result.get("switched_notice", ""),
    }


@csrf_exempt
@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([permissions.AllowAny])
def grade_sheet(request):
    """
    رفع ورقة OMR وتصحيحها الفوري — يدعم الصور والـ PDF (صفحة واحدة أو متعدد الصفحات).
    """
    image_file = request.FILES.get("sheet_image")
    if not image_file:
        return Response({"error": "sheet_image مطلوب"}, status=status.HTTP_400_BAD_REQUEST)

    answer_key = {}
    marks_map = {}
    raw_key = request.data.get("answer_key", "")
    if raw_key:
        try:
            parsed = json.loads(raw_key) if isinstance(raw_key, str) else raw_key
            answer_key = {str(k): v for k, v in parsed.items()}
        except (json.JSONDecodeError, ValueError) as e:
            return Response({"error": f"answer_key غير صحيح: {e}"}, status=status.HTTP_400_BAD_REQUEST)

    raw_marks = request.data.get("marks_map", "") or request.data.get("question_marks", "")
    if raw_marks:
        try:
            parsed_marks = json.loads(raw_marks) if isinstance(raw_marks, str) else raw_marks
            marks_map = {str(k): float(v) for k, v in parsed_marks.items()}
        except (json.JSONDecodeError, ValueError):
            pass

    exam_id = request.data.get("exam_id") or request.data.get("exam")
    version_id = request.data.get("version_id")
    version_code = request.data.get("version_code") or request.data.get("version")
    target_version = None
    exam_obj = None

    if exam_id or version_id:
        try:
            from exams.models.Exam import Exam
            from exams.models.ExamVersion import ExamVersion
            if version_id:
                target_version = ExamVersion.objects.filter(id=version_id, is_deleted=False).prefetch_related('question_orders__question__options').first()
                if target_version and not exam_id:
                    exam_id = target_version.exam_id
            elif exam_id and version_code:
                target_version = ExamVersion.objects.filter(exam_id=exam_id, versionCode=version_code, is_deleted=False).prefetch_related('question_orders__question__options').first()
            elif exam_id:
                target_version = ExamVersion.objects.filter(exam_id=exam_id, is_deleted=False).prefetch_related('question_orders__question__options').first()

            if exam_id:
                exam_obj = Exam.objects.filter(id=exam_id, is_deleted=False).first()
            elif target_version:
                exam_obj = target_version.exam

            if target_version:
                for qo in target_version.question_orders.filter(is_deleted=False).order_by('orderIndex'):
                    q = qo.question
                    opts = list(q.options.filter(is_deleted=False))
                    ans_letter = 'A'
                    for idx, opt in enumerate(opts):
                        if opt.isTrue:
                            ans_letter = chr(65 + idx)
                            break
                    if (q.questionType in ['True/False', 'true_false', 'صح وخطأ']) or (q.isTrue is not None):
                        ans_letter = 'A' if q.isTrue is True else ('B' if q.isTrue is False else ans_letter)
                    
                    q_num_str = str(qo.orderIndex)
                    if not answer_key or q_num_str not in answer_key:
                        answer_key[q_num_str] = ans_letter
                    if q_num_str not in marks_map:
                        marks_map[q_num_str] = float(q.defaultMark or 1.0)
        except Exception as e_key:
            logger.warning(f"Could not auto-fetch answer key from ExamVersion: {e_key}")

    dpi = int(request.data.get("dpi", 300))
    template_id = request.data.get("template_id", "").strip()

    suffix = os.path.splitext(image_file.name)[1] or ".png"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        for chunk in image_file.chunks():
            tmp.write(chunk)
        tmp_path = tmp.name

    try:
        # فحص ما إذا كان الملف PDF
        if image_file.name.lower().endswith(".pdf"):
            if fitz is None:
                return Response({"error": "مكتبة معالجة الـ PDF (PyMuPDF) غير متوفرة بالسيرفر"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            doc = fitz.open(tmp_path)
            num_pages = len(doc)
            if num_pages == 0:
                return Response({"error": "ملف الـ PDF فارغ لا يحتوي على أي صفحات"}, status=status.HTTP_400_BAD_REQUEST)

            if num_pages == 1:
                # PDF صفحة واحدة
                page = doc[0]
                pix = page.get_pixmap(dpi=dpi)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as p_tmp:
                    p_tmp.write(pix.tobytes("png"))
                    p_img_path = p_tmp.name
                try:
                    res = _process_and_grade_image_file(
                        p_img_path,
                        original_filename=f"{os.path.splitext(image_file.name)[0]}_page_1.png",
                        template_id=template_id,
                        answer_key=answer_key,
                        marks_map=marks_map,
                        dpi=dpi,
                        exam_id=exam_id,
                        version_id=version_id,
                        version_code=version_code,
                        target_version=target_version,
                        exam_obj=exam_obj,
                        request_user=request.user if request.user.is_authenticated else None,
                    )
                    return Response(res, status=status.HTTP_200_OK)
                finally:
                    if os.path.exists(p_img_path):
                        os.unlink(p_img_path)
            else:
                # PDF متعدد الصفحات
                from submissions.models.SubmissionBatch import SubmissionBatch
                batch_name = f"مسح PDF متعدد ({num_pages} ص) - {image_file.name} - {timezone.now().strftime('%H:%M')}"
                batch_record = SubmissionBatch.objects.create(
                    name=batch_name,
                    exam=exam_obj,
                    uploaded_by=request.user if request.user.is_authenticated else None,
                    status=SubmissionBatch.Status.PROCESSING,
                    total_papers=num_pages,
                )

                pages_results = []
                for p_idx in range(num_pages):
                    page = doc[p_idx]
                    pix = page.get_pixmap(dpi=dpi)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as p_tmp:
                        p_tmp.write(pix.tobytes("png"))
                        p_img_path = p_tmp.name
                    try:
                        p_res = _process_and_grade_image_file(
                            p_img_path,
                            original_filename=f"{os.path.splitext(image_file.name)[0]}_page_{p_idx+1}.png",
                            template_id=template_id,
                            answer_key=answer_key,
                            marks_map=marks_map,
                            dpi=dpi,
                            exam_id=exam_id,
                            version_id=version_id,
                            version_code=version_code,
                            target_version=target_version,
                            exam_obj=exam_obj,
                            batch_obj=batch_record,
                            page_number=p_idx + 1,
                            request_user=request.user if request.user.is_authenticated else None,
                        )
                        pages_results.append(p_res)
                    except PermissionError as p_err:
                        pages_results.append({
                            "page_number": p_idx + 1,
                            "student_name": "مقفل بالكنترول",
                            "error": str(p_err),
                            "status": "locked_in_control",
                        })
                    except Exception as p_err:
                        logger.warning(f"Error grading page {p_idx+1}: {p_err}")
                        pages_results.append({
                            "page_number": p_idx + 1,
                            "student_name": f"خطأ ص {p_idx+1}",
                            "error": str(p_err),
                            "status": "failed",
                        })
                    finally:
                        if os.path.exists(p_img_path):
                            os.unlink(p_img_path)

                from submissions.models.Submission import Submission
                completed_cnt = sum(1 for p in pages_results if p.get("status") == Submission.Status.COMPLETED)
                needs_rev_cnt = sum(1 for p in pages_results if p.get("status") == Submission.Status.NEEDS_REVIEW)
                batch_record.processed_papers = completed_cnt + needs_rev_cnt
                batch_record.failed_papers = num_pages - (completed_cnt + needs_rev_cnt)
                batch_record.status = SubmissionBatch.Status.COMPLETED if batch_record.failed_papers == 0 else SubmissionBatch.Status.PARTIALLY_COMPLETED
                batch_record.save()

                first_valid = next((p for p in pages_results if "score" in p), pages_results[0])
                resp_payload = {
                    "is_batch": True,
                    "batch_id": batch_record.id,
                    "total_pages": num_pages,
                    "completed_count": completed_cnt,
                    "needs_review_count": needs_rev_cnt,
                    "pages": pages_results,
                    "result_id": first_valid.get("result_id"),
                    "score": first_valid.get("score", 0),
                    "max_score": first_valid.get("max_score", 0),
                    "score_percent": first_valid.get("score_percent", 0),
                    "total_correct": first_valid.get("total_correct", 0),
                    "total_wrong": first_valid.get("total_wrong", 0),
                    "total_answered": first_valid.get("total_answered", 0),
                    "total_empty": first_valid.get("total_empty", 0),
                    "questions": first_valid.get("questions", []),
                    "annotated_image": first_valid.get("annotated_image", ""),
                    "engine_used": first_valid.get("engine_used", "template_driven"),
                    "template_id": first_valid.get("template_id", ""),
                    "template_name": first_valid.get("template_name", ""),
                    "barcode": first_valid.get("barcode", ""),
                    "qr": first_valid.get("qr", ""),
                    "student_info": first_valid.get("student_info", {}),
                }
                return Response(resp_payload, status=status.HTTP_200_OK)

        else:
            # صورة منفردة (PNG / JPG / TIFF)
            res = _process_and_grade_image_file(
                tmp_path,
                original_filename=image_file.name,
                template_id=template_id,
                answer_key=answer_key,
                marks_map=marks_map,
                dpi=dpi,
                exam_id=exam_id,
                version_id=version_id,
                version_code=version_code,
                target_version=target_version,
                exam_obj=exam_obj,
                request_user=request.user if request.user.is_authenticated else None,
            )
            return Response(res, status=status.HTTP_200_OK)

    except PermissionError as perm_err:
        return Response({"error": str(perm_err)}, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        logger.exception("خطأ في التصحيح")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@csrf_exempt
@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([permissions.AllowAny])
def batch_scan_api(request):
    """
    المسح والتصحيح الجماعي المباشر (Multi-file / Multipage Batch Scan API)
    يستقبل ملفات متعددة (صور فردية، PDF متعدد الصفحات، ZIP).
    """
    from submissions.models.SubmissionBatch import SubmissionBatch
    from exams.models.Exam import Exam

    uploaded_files = request.FILES.getlist('files') or request.FILES.getlist('images') or []
    single_file = request.FILES.get('file') or request.FILES.get('sheet_image')
    if single_file and not uploaded_files:
        uploaded_files = [single_file]

    if not uploaded_files:
        return Response({"error": "لم يتم العثور على أي ملفات أو صور للمعالجة"}, status=status.HTTP_400_BAD_REQUEST)

    exam_id = request.data.get('exam_id') or request.data.get('exam')
    template_id = request.data.get('template_id', 'AUTO')
    dpi = int(request.data.get('dpi', 300))
    batch_title = request.data.get('title') or request.data.get('name') or f"دفعة مسح ضوئي {timezone.now().strftime('%Y-%m-%d %H:%M')}"

    exam_obj = None
    if exam_id:
        try:
            exam_obj = Exam.objects.filter(id=int(exam_id), is_deleted=False).first()
        except (ValueError, TypeError):
            pass
    if not exam_obj:
        return Response({"error": "يرجى تحديد الاختبار المطلوب قبل بدء المسح الجماعي"}, status=status.HTTP_400_BAD_REQUEST)

    batch_record = SubmissionBatch.objects.create(
        name=batch_title,
        exam=exam_obj,
        uploaded_by=request.user if request.user.is_authenticated else None,
        status=SubmissionBatch.Status.PROCESSING,
    )

    extracted_images = []
    for up_file in uploaded_files:
        fn_lower = up_file.name.lower()
        file_bytes = up_file.read()
        if fn_lower.endswith('.zip'):
            try:
                with zipfile.ZipFile(io.BytesIO(file_bytes)) as z:
                    for zinfo in z.infolist():
                        if zinfo.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff', '.webp')):
                            extracted_images.append((os.path.basename(zinfo.filename), z.read(zinfo.filename)))
            except Exception as ze:
                logger.warning(f"Error reading ZIP: {ze}")
        elif fn_lower.endswith('.pdf'):
            if fitz is not None:
                try:
                    doc = fitz.open(stream=file_bytes, filetype="pdf")
                    for p_idx in range(len(doc)):
                        pix = doc[p_idx].get_pixmap(dpi=dpi)
                        extracted_images.append((f"{os.path.splitext(up_file.name)[0]}_page_{p_idx+1}.png", pix.tobytes("png")))
                except Exception as pe:
                    logger.warning(f"Error rendering PDF {up_file.name}: {pe}")
        elif fn_lower.endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff', '.webp')):
            extracted_images.append((up_file.name, file_bytes))

    if not extracted_images:
        batch_record.status = SubmissionBatch.Status.FAILED
        batch_record.save()
        return Response({"error": "لم يتم العثور على أوراق صالحة داخل الملفات المرفوعة"}, status=status.HTTP_400_BAD_REQUEST)

    batch_record.total_papers = len(extracted_images)
    batch_record.save()

    from submissions.models.Submission import Submission
    processed_sheets = []
    success_count = 0
    needs_review_count = 0
    locked_count = 0
    failed_count = 0

    for idx, (img_name, img_bytes) in enumerate(extracted_images):
        suffix = os.path.splitext(img_name)[1] or ".png"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_f:
            tmp_f.write(img_bytes)
            tmp_p = tmp_f.name

        try:
            res = _process_and_grade_image_file(
                tmp_p,
                original_filename=img_name,
                template_id=template_id,
                dpi=dpi,
                exam_obj=exam_obj,
                batch_obj=batch_record,
                page_number=idx + 1,
                request_user=request.user if request.user.is_authenticated else None,
            )
            processed_sheets.append(res)
            if res.get("status") == Submission.Status.COMPLETED:
                success_count += 1
            else:
                needs_review_count += 1
        except PermissionError as perm_e:
            locked_count += 1
            processed_sheets.append({
                "page_number": idx + 1,
                "filename": img_name,
                "student_name": "مقفل بالكنترول",
                "status": "locked_in_control",
                "error": str(perm_e),
            })
        except Exception as sheet_e:
            failed_count += 1
            processed_sheets.append({
                "page_number": idx + 1,
                "filename": img_name,
                "student_name": "خطأ في المعالجة",
                "status": Submission.Status.FAILED,
                "error": str(sheet_e),
            })
        finally:
            if os.path.exists(tmp_p):
                os.unlink(tmp_p)

    batch_record.processed_papers = success_count + needs_review_count
    batch_record.failed_papers = failed_count
    batch_record.status = SubmissionBatch.Status.COMPLETED if failed_count == 0 else SubmissionBatch.Status.PARTIALLY_COMPLETED
    batch_record.save()

    return Response({
        "success": True,
        "message": f"اكتملت المعالجة الجماعية بنجاح ({batch_record.processed_papers}/{len(extracted_images)} ورقة)",
        "batch_id": batch_record.id,
        "batch_name": batch_record.name,
        "total_papers": len(extracted_images),
        "completed_count": success_count,
        "needs_review_count": needs_review_count,
        "locked_count": locked_count,
        "failed_count": failed_count,
        "sheets": processed_sheets,
    }, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([permissions.AllowAny])
def detect_template_api(request):
    """
    التعرف التلقائي الفوري على القالب من الورقة المرفوعة مباشرة (يدعم الصور والـ PDF).
    """
    image_file = request.FILES.get("sheet_image")
    if not image_file:
        return Response({"error": "sheet_image مطلوب"}, status=status.HTTP_400_BAD_REQUEST)

    suffix = os.path.splitext(image_file.name)[1] or ".png"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        for chunk in image_file.chunks():
            tmp.write(chunk)
        tmp_path = tmp.name

    sheet_to_check = tmp_path
    cleanup_sheet = False

    try:
        if image_file.name.lower().endswith(".pdf"):
            if fitz is not None:
                doc = fitz.open(tmp_path)
                if len(doc) > 0:
                    pix = doc[0].get_pixmap(dpi=300)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as p_tmp:
                        p_tmp.write(pix.tobytes("png"))
                        sheet_to_check = p_tmp.name
                        cleanup_sheet = True

        db_obj, detected_code, detected_qs = _detect_template_from_sheet(sheet_to_check, original_filename=image_file.name)
        if not db_obj:
            return Response({
                "found": False,
                "template_id": None,
                "total_questions": detected_qs or None,
                "barcode": detected_code or "",
                "message": "تعذر التعرف على القالب من الورقة تلقائياً"
            }, status=status.HTTP_200_OK)

        td = db_obj.template_data or {}
        q_count = detected_qs or td.get("questions", {}).get("metadata", {}).get("num_questions", 50)
        return Response({
            "found": True,
            "template_id": db_obj.id,
            "template_name": db_obj.name,
            "total_questions": q_count,
            "barcode": detected_code or td.get("barcode", {}).get("value", ""),
            "qr": td.get("qr", {}).get("value", ""),
            "paper_size": td.get("paper", {}).get("size", "A5"),
            "student_fields": td.get("header", {}),
        }, status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception("خطأ في كشف القالب")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        if cleanup_sheet and os.path.exists(sheet_to_check):
            os.unlink(sheet_to_check)
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)



def _detect_template_from_sheet(image_path: str, requested_template_id: str = "", original_filename: str = ""):
    """
    التعرف التلقائي الذكي والشامل على أي قالب مباشرة من محتوى وهندسة ورقة الإجابة:
    1. التحقق المباشر من القالب المطلوب صراحة (إذا لم يكن AUTO).
    2. مطابقة اسم القالب المباشرة من اسم الملف المرفوع (مثل: بببببببب_600DPI_UltraHD.png).
    3. كشف الباركود والـ QR المشفر للقالب (zxingcpp / pyzbar / OpenCV).
    4. فحص هيئة وأبعاد الورقة (A4 طولي 180 سؤال مقابل A5 عرضي).
    5. محاذاة الزوايا الأربع (Fiducial Marks) إلى الفضاء القياسي 300 DPI.
    6. بصمة شبكة الدوائر الفلكية (Universal Bubble Footprint Scorer):
       يقوم بمطابقة إحداثيات الدوائر الفعلية لكل القوالب النشطة في النظام بالدوائر الفيزيائية المكتشفة في الورقة.
    7. فحص التوزيع الهندسي للأعمدة والصفوف (Fallback للمقاييس الكلاسيكية).
    """
    import cv2
    import numpy as np
    try:
        from templates_engine.models.ExamTemplate import ExamTemplate
    except ImportError:
        from templates_engine.models import ExamTemplate
    from django.db.models import Q

    # ── 1. التحقق من القالب إذا كان محدداً صراحة يدوياً ──────────────
    if requested_template_id and str(requested_template_id).strip().upper() not in ("AUTO", "", "NONE", "UNDEFINED", "OMR_AUTO"):
        try:
            req_obj = ExamTemplate.objects.filter(id=int(requested_template_id), is_active=True).first()
            if req_obj:
                td = req_obj.template_data or {}
                q_cnt = (
                    td.get("questions", {}).get("metadata", {}).get("num_questions") or
                    len(td.get("mcq_questions", [])) or
                    req_obj.total_mcq or 40
                )
                logger.info("Using explicitly requested template: %s (id=%s, qs=%d)", req_obj.name, req_obj.id, q_cnt)
                return req_obj, None, q_cnt
        except (ValueError, TypeError):
            pass

    img = cv2.imread(image_path)
    if img is None:
        return None, None, 0

    h, w = img.shape[:2]
    fname = (original_filename or os.path.basename(image_path)).strip()
    active_templates = list(
        ExamTemplate.objects.filter(is_active=True)
        .exclude(name__icontains="سلة المهملات")
        .order_by("-id")
    )

    # ── 2. مطابقة مباشرة بالاسم من اسم الملف المرفوع ──────────────────
    for tpl in active_templates:
        clean_name = tpl.name.strip() if tpl.name else ""
        if len(clean_name) >= 3 and clean_name in fname:
            td = tpl.template_data or {}
            q_cnt = (
                td.get("questions", {}).get("metadata", {}).get("num_questions") or
                len(td.get("mcq_questions", [])) or
                tpl.total_mcq or 40
            )
            logger.info("Direct template match by filename '%s': %s (id=%s, qs=%d)", fname, tpl.name, tpl.id, q_cnt)
            return tpl, None, q_cnt

    # ── 3. كشف الباركود والـ QR ─────────────────────────────────────
    detected_code = None
    try:
        import zxingcpp
        for zr in zxingcpp.read_barcodes(img):
            if zr.text:
                detected_code = zr.text.strip()
                logger.info("Auto-detected barcode via zxingcpp: %s (%s)", detected_code, zr.format)
                break
    except Exception as z_err:
        logger.debug("zxingcpp scan error: %s", z_err)

    if not detected_code:
        try:
            from pyzbar import pyzbar
            for b in pyzbar.decode(img):
                c = b.data.decode("utf-8", errors="ignore").strip()
                if c:
                    detected_code = c
                    logger.info("Auto-detected barcode via pyzbar: %s", detected_code)
                    break
        except Exception as b_err:
            logger.debug("pyzbar scan error: %s", b_err)

    if not detected_code:
        try:
            qr_detector = cv2.QRCodeDetector()
            data, _, _ = qr_detector.detectAndDecode(img)
            if data:
                detected_code = data.strip()
                logger.info("Auto-detected QR via cv2: %s", detected_code)
        except Exception as q_err:
            logger.debug("cv2 QR scan error: %s", q_err)

    import re
    if not detected_code:
        try:
            import pytesseract
            # فحص حجرة الباركود النصية أسفل يسار الورقة (OCR Barcode Text Fallback)
            bc_roi = img[int(h * 0.65):int(h * 0.98), int(w * 0.03):int(w * 0.40)]
            ocr_txt = pytesseract.image_to_string(bc_roi).strip()
            m_ocr = re.search(r"EXAM_\d+_VER_[A-Za-z0-9]+(_SEAT_\d+)?", ocr_txt)
            if m_ocr:
                detected_code = m_ocr.group(0)
                logger.info("Auto-detected exam barcode via OCR fallback: %s", detected_code)
        except Exception as ocr_err:
            logger.debug("OCR barcode fallback error: %s", ocr_err)

    # ── 3.1 مطابقة باركود جلسات الاختبار EXAM_{id}_VER_{code}...
    if detected_code:
        exam_bar_m = re.search(r"EXAM_(\d+)_VER_([A-Za-z0-9]+)", detected_code)
        if exam_bar_m:
            try:
                ex_id = int(exam_bar_m.group(1))
                v_code = exam_bar_m.group(2)
                from exams.models.ExamVersion import ExamVersion
                v_match = ExamVersion.objects.filter(exam_id=ex_id, versionCode=v_code, is_deleted=False).prefetch_related('question_orders').first()
                if not v_match:
                    v_match = ExamVersion.objects.filter(exam_id=ex_id, is_deleted=False).prefetch_related('question_orders').first()
                if v_match:
                    v_q_cnt = v_match.question_orders.filter(is_deleted=False).count()
                    if v_q_cnt > 0:
                        tpl_match = None
                        for tpl in active_templates:
                            t_td = tpl.template_data or {}
                            t_qs = (
                                t_td.get("questions", {}).get("metadata", {}).get("num_questions") or
                                len(t_td.get("mcq_questions", [])) or
                                getattr(tpl, "total_mcq", None)
                            )
                            if t_qs == v_q_cnt or f"({v_q_cnt} سؤال)" in tpl.name or f"({v_q_cnt}سؤال)" in tpl.name:
                                tpl_match = tpl
                                break
                        if not tpl_match:
                            try:
                                from templates_engine.builder import TemplateBuilderService
                                builder = TemplateBuilderService()
                                tf_orders = [qo for qo in v_match.question_orders.filter(is_deleted=False).order_by('orderIndex') if (qo.question.questionType in ['True/False', 'true_false', 'صح وخطأ']) or (qo.question.isTrue is not None)]
                                mcq_orders = [qo for qo in v_match.question_orders.filter(is_deleted=False).order_by('orderIndex') if qo not in tf_orders]
                                sections = []
                                if tf_orders:
                                    sections.append({
                                        "id": "sec_tf",
                                        "title": "صح وخطأ",
                                        "from_q": tf_orders[0].orderIndex,
                                        "to_q": tf_orders[-1].orderIndex,
                                        "type": "true_false",
                                        "choices": ["صح", "خطأ"]
                                    })
                                if mcq_orders:
                                    sections.append({
                                        "id": "sec_mcq",
                                        "title": "اختيار من متعدد",
                                        "from_q": mcq_orders[0].orderIndex,
                                        "to_q": mcq_orders[-1].orderIndex,
                                        "type": "mcq",
                                        "choices": ["1", "2", "3", "4"]
                                    })
                                dyn_cfg = {
                                    "template_id": f"EXAM_{ex_id}_AUTO",
                                    "template_name": f"{v_match.exam.title} ({v_q_cnt} سؤال)",
                                    "name": f"{v_match.exam.title} ({v_q_cnt} سؤال)",
                                    "paper": {"size": "A5", "dpi": 300},
                                    "paper_size": "A5",
                                    "total_mcq": v_q_cnt,
                                    "questions": {
                                        "metadata": {"num_questions": v_q_cnt},
                                        "layout": {"columns_count": 4},
                                        "sections": sections
                                    }
                                }
                                dyn_contract = builder.build_from_designer_config(dyn_cfg)
                                dyn_cfg["mcq_questions"] = [q.model_dump() for q in dyn_contract.mcq_questions]
                                tpl_match, _ = ExamTemplate.objects.get_or_create(
                                    name=f"{v_match.exam.title} ({v_q_cnt} سؤال)",
                                    defaults={"template_data": dyn_cfg, "is_active": True}
                                )
                            except Exception as dyn_err:
                                logger.warning("Could not auto-generate dynamic template: %s", dyn_err)
                        if not tpl_match and active_templates:
                            tpl_match = active_templates[0]
                        if tpl_match:
                            logger.info("Auto-bound sheet via exam barcode %s to template: %s (%d Qs)", detected_code, tpl_match.name, v_q_cnt)
                            return tpl_match, detected_code, v_q_cnt
            except Exception as ex_err:
                logger.debug("Error resolving exam barcode: %s", ex_err)

        # ── 3.2 مطابقة رمز QR المشفر بصيغة {uniqueCode}|{versionCode}|{seatNumber}
        if "|" in detected_code:
            parts = [p.strip() for p in detected_code.split("|")]
            if len(parts) >= 2:
                u_code, v_code = parts[0], parts[1]
                try:
                    from exams.models.Exam import Exam
                    from exams.models.ExamVersion import ExamVersion
                    ex_match = Exam.objects.filter(uniqueCode=u_code, is_deleted=False).first()
                    if ex_match:
                        v_match = ExamVersion.objects.filter(exam=ex_match, versionCode=v_code, is_deleted=False).prefetch_related('question_orders').first()
                        if not v_match:
                            v_match = ExamVersion.objects.filter(exam=ex_match, is_deleted=False).prefetch_related('question_orders').first()
                        if v_match:
                            v_q_cnt = v_match.question_orders.filter(is_deleted=False).count()
                            if v_q_cnt > 0:
                                tpl_match = None
                                for tpl in active_templates:
                                    t_td = tpl.template_data or {}
                                    t_qs = (
                                        t_td.get("questions", {}).get("metadata", {}).get("num_questions") or
                                        len(t_td.get("mcq_questions", [])) or
                                        getattr(tpl, "total_mcq", None)
                                    )
                                    if t_qs == v_q_cnt or f"({v_q_cnt} سؤال)" in tpl.name or f"({v_q_cnt}سؤال)" in tpl.name:
                                        tpl_match = tpl
                                        break
                                if not tpl_match and active_templates:
                                    tpl_match = active_templates[0]
                                if tpl_match:
                                    logger.info("Auto-bound sheet via QR %s to template: %s (%d Qs)", detected_code, tpl_match.name, v_q_cnt)
                                    return tpl_match, detected_code, v_q_cnt
                except Exception as qr_err:
                    logger.debug("Error resolving exam QR: %s", qr_err)

    # التحقق مما إذا كان الباركود يطابق قالباً فريداً غير باركود الوزارة العام
    is_generic_ministry_code = (
        detected_code in ("41848501164148", "YE-MOE-1444-418485-SUB1") or
        (detected_code and ("YE-MOE" in detected_code or "418485" in detected_code))
    )

    if detected_code and not is_generic_ministry_code:
        match_obj = ExamTemplate.objects.filter(
            Q(template_data__barcode__value=detected_code) |
            Q(template_data__qr__value=detected_code) |
            Q(template_data__template_id=detected_code),
            is_active=True
        ).order_by("-created_at").first()
        if match_obj:
            q_cnt = (
                match_obj.template_data.get("questions", {}).get("metadata", {}).get("num_questions") or
                match_obj.total_mcq or
                len(match_obj.template_data.get("mcq_questions", [])) or 50
            )
            logger.info("Auto-detected custom template by unique barcode: %s (%d Qs)", match_obj.name, q_cnt)
            return match_obj, detected_code, q_cnt

    # ── 4. فحص هيئة وأبعاد الورقة وتصحيح التدوير (A4 طولي مقابل A5 عرضي) ───────────
    is_portrait = h > w * 1.15
    if is_portrait:
        def _check_fiducials_simple(test_im):
            th_h, th_w = test_im.shape[:2]
            t_scale = max(th_w / 210.0, th_h / 148.5)
            exp_sz = 5.5 * t_scale
            mn_sz, mx_sz = max(4.0, exp_sz * 0.35), max(exp_sz * 2.2, 12.0)
            t_gr = cv2.cvtColor(test_im, cv2.COLOR_BGR2GRAY) if len(test_im.shape) == 3 else test_im
            try:
                _, t_ot = cv2.threshold(t_gr, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            except Exception:
                return 0
            q_boxes = [
                (0, 0, th_w // 4, th_h // 4),
                (3 * th_w // 4, 0, th_w, th_h // 4),
                (0, 3 * th_h // 4, th_w // 4, th_h),
                (3 * th_w // 4, 3 * th_h // 4, th_w, th_h),
            ]
            f_hits = 0
            for qx1, qy1, qx2, qy2 in q_boxes:
                roi = t_ot[qy1:qy2, qx1:qx2]
                cnts, _ = cv2.findContours(roi, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                for c in cnts:
                    bx, by, bw, bh = cv2.boundingRect(c)
                    if mn_sz <= bw <= mx_sz and mn_sz <= bh <= mx_sz and 0.55 <= bw / float(bh) <= 1.80:
                        c_roi = roi[by:by+bh, bx:bx+bw]
                        if cv2.countNonZero(c_roi) / float(bw * bh) > 0.50:
                            f_hits += 1
                            break
            return f_hits

        cw_hits = _check_fiducials_simple(cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE))
        ccw_hits = _check_fiducials_simple(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))

        if cw_hits >= 3:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            h, w = img.shape[:2]
            logger.info("Auto-rotated sheet 90° CW to match A5 landscape layout (fiducials=%d)", cw_hits)
        elif ccw_hits >= 3:
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
            h, w = img.shape[:2]
            logger.info("Auto-rotated sheet 90° CCW to match A5 landscape layout (fiducials=%d)", ccw_hits)
        else:
            db_obj = ExamTemplate.objects.filter(
                Q(template_data__paper__size__iexact="A4") | Q(name__icontains="180") | Q(paper_height_mm__gt=250),
                is_active=True
            ).order_by("-created_at").first()
            q_cnt = 180
            if db_obj:
                td = db_obj.template_data or {}
                q_cnt = (
                    td.get("questions", {}).get("metadata", {}).get("num_questions") or
                    len(td.get("mcq_questions", [])) or
                    getattr(db_obj, "total_mcq", None) or
                    (180 if "180" in db_obj.name else 50)
                )
            logger.info("Auto-detected portrait A4 sheet -> Bound Template: %s (%d Qs)", db_obj.name if db_obj else "None", q_cnt)
            return db_obj, detected_code, q_cnt

    # ── 5. ورقة A5 عرضية: محاذاة الزوايا الأربع (Fiducials) ──────────
    canon_w, canon_h = 2480, 1754
    canon_scale = 300.0 / 25.4

    img_scale = max(w / 210.0, h / 148.5)
    expected_size_px = 5.5 * img_scale
    min_sz = max(4.0, expected_size_px * 0.35)
    max_sz = max(expected_size_px * 2.2, 12.0)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img

    thresholds_to_try = []
    try:
        _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        thresholds_to_try.append(otsu)
    except Exception:
        pass
    for th_val in [70, 100, 130, 160]:
        _, th = cv2.threshold(gray, th_val, 255, cv2.THRESH_BINARY_INV)
        thresholds_to_try.append(th)

    quads = {
        'TL': (0, 0, w // 4, h // 4),
        'TR': (3 * w // 4, 0, w, h // 4),
        'BL': (0, 3 * h // 4, w // 4, h),
        'BR': (3 * w // 4, 3 * h // 4, w, h),
    }
    detected_centers = {}
    for thresh_img in thresholds_to_try:
        for q_id, (qx1, qy1, qx2, qy2) in quads.items():
            if q_id in detected_centers:
                continue
            roi = thresh_img[qy1:qy2, qx1:qx2]
            cnts, _ = cv2.findContours(roi, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            candidates = []
            for c in cnts:
                bx, by, bw, bh = cv2.boundingRect(c)
                if min_sz <= bw <= max_sz and min_sz <= bh <= max_sz:
                    ratio = bw / float(bh)
                    if 0.55 <= ratio <= 1.80:
                        c_roi = roi[by:by+bh, bx:bx+bw]
                        fill = cv2.countNonZero(c_roi) / (bw * bh)
                        if fill > 0.50:
                            center = (float(qx1 + bx + bw / 2.0), float(qy1 + by + bh / 2.0))
                            candidates.append((center, fill, abs(bw - expected_size_px)))
            if candidates:
                candidates.sort(key=lambda item: (item[2], -item[1]))
                detected_centers[q_id] = candidates[0][0]
        if len(detected_centers) == 4:
            break

    if len(detected_centers) == 3:
        if "TL" not in detected_centers and all(k in detected_centers for k in ("TR", "BL", "BR")):
            detected_centers["TL"] = (
                detected_centers["TR"][0] + detected_centers["BL"][0] - detected_centers["BR"][0],
                detected_centers["TR"][1] + detected_centers["BL"][1] - detected_centers["BR"][1]
            )
        elif "TR" not in detected_centers and all(k in detected_centers for k in ("TL", "BL", "BR")):
            detected_centers["TR"] = (
                detected_centers["TL"][0] + detected_centers["BR"][0] - detected_centers["BL"][0],
                detected_centers["TR"][1] + detected_centers["BR"][1] - detected_centers["BL"][1]
            )
        elif "BL" not in detected_centers and all(k in detected_centers for k in ("TL", "TR", "BR")):
            detected_centers["BL"] = (
                detected_centers["TL"][0] + detected_centers["BR"][0] - detected_centers["TR"][0],
                detected_centers["TL"][1] + detected_centers["BR"][1] - detected_centers["TR"][1]
            )
        elif "BR" not in detected_centers and all(k in detected_centers for k in ("TL", "TR", "BL")):
            detected_centers["BR"] = (
                detected_centers["TR"][0] + detected_centers["BL"][0] - detected_centers["TL"][0],
                detected_centers["TR"][1] + detected_centers["BL"][1] - detected_centers["TL"][1]
            )

    if len(detected_centers) == 4:
        dst_pts = np.float32([
            [(6.0 + 2.75) * canon_scale, (6.0 + 2.75) * canon_scale],
            [(198.5 + 2.75) * canon_scale, (6.0 + 2.75) * canon_scale],
            [(6.0 + 2.75) * canon_scale, (137.0 + 2.75) * canon_scale],
            [(198.5 + 2.75) * canon_scale, (137.0 + 2.75) * canon_scale],
        ])
        src_pts = np.float32([
            detected_centers['TL'],
            detected_centers['TR'],
            detected_centers['BL'],
            detected_centers['BR'],
        ])
        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        aligned = cv2.warpPerspective(img, M, (canon_w, canon_h), borderValue=(255, 255, 255))
    else:
        aligned = cv2.resize(img, (canon_w, canon_h))

    # ── 6. بصمة شبكة الدوائر الفلكية (Universal Bubble Footprint Scorer) ─────────
    # يقارن كل قالب نشط في قاعدة البيانات مع الدوائر الفيزيائية المكتشفة في الورقة بدقة فائقة
    aligned_gray = cv2.cvtColor(aligned, cv2.COLOR_BGR2GRAY) if len(aligned.shape) == 3 else aligned
    _, aligned_th = cv2.threshold(aligned_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    qx1, qx2 = int(10.0 * canon_scale), int(130.0 * canon_scale)
    qy1, qy2 = int(20.0 * canon_scale), int(105.0 * canon_scale)
    q_roi = aligned_th[qy1:qy2, qx1:qx2]
    q_cnts, _ = cv2.findContours(q_roi, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    sheet_bubbles = sum(1 for c in q_cnts if 14 <= cv2.boundingRect(c)[2] <= 55 and 14 <= cv2.boundingRect(c)[3] <= 55)

    raw_stats = []
    for tpl in active_templates:
        td = tpl.template_data or {}
        mcq_qs = td.get('mcq_questions', [])
        if not mcq_qs:
            continue
        found = 0
        total = 0
        missing = 0
        for q in mcq_qs:
            for ch in q.get('choices', []):
                total += 1
                br = ch.get('bubble_region', {})
                cx = int((br.get('dx_mm', 0) + br.get('width_mm', 3.6)/2.0) * canon_scale)
                cy = int((br.get('dy_mm', 0) + br.get('height_mm', 3.6)/2.0) * canon_scale)
                r = int(2.5 * canon_scale)
                roi = aligned_th[max(0, cy-r):min(canon_h, cy+r), max(0, cx-r):min(canon_w, cx+r)]
                cnts, _ = cv2.findContours(roi, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                has_circ = any(10 <= cv2.boundingRect(c)[2] <= 55 and 10 <= cv2.boundingRect(c)[3] <= 55 for c in cnts)
                if has_circ:
                    found += 1
                else:
                    missing += 1
        raw_stats.append((tpl, found, missing, total))

    if raw_stats:
        max_found = max(s[1] for s in raw_stats)
        scored = []
        for tpl, found, missing, total in raw_stats:
            td = tpl.template_data or {}
            mcq_qs = td.get('mcq_questions', [])
            p_fit = (found / float(total)) - 2.5 * (missing / float(total))
            coverage = found / float(max(1, max_found))
            score = p_fit * coverage
            if tpl.name and tpl.name.strip() in fname:
                score += 10.0
            q_cnt = td.get('questions', {}).get('metadata', {}).get('num_questions') or len(mcq_qs) or 40
            scored.append((score, tpl, q_cnt, found, missing, total))

        scored.sort(key=lambda x: -x[0])
        best = scored[0]
        if best[0] > 0.15:
            logger.info(
                "Universal Bubble Footprint Match: Bound to Template %s (id=%s, qs=%d) [score=%.3f, found=%d/%d, max_found=%d]",
                best[1].name, best[1].id, best[2], best[0], best[3], best[5], max_found
            )
            return best[1], detected_code, best[2]

    # ── 7. Fallback: التحليل الهندسي التقليدي للأعمدة والصفوف ──────────────────
    def analyze_roi(x_start_mm, x_end_mm, y_start_mm, y_end_mm):
        x1_roi = max(0, int(x_start_mm * canon_scale))
        x2_roi = min(canon_w, int(x_end_mm * canon_scale))
        y1_roi = max(0, int(y_start_mm * canon_scale))
        y2_roi = min(canon_h, int(y_end_mm * canon_scale))
        roi = aligned[y1_roi:y2_roi, x1_roi:x2_roi]
        if roi.size == 0:
            return 0, 0.0
        r_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY) if len(roi.shape) == 3 else roi
        _, r_thresh = cv2.threshold(r_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        cnts, _ = cv2.findContours(r_thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        b_cnt = sum(
            1 for c in cnts
            if 14 <= cv2.boundingRect(c)[2] <= 65
            and 14 <= cv2.boundingRect(c)[3] <= 65
            and 0.70 <= cv2.boundingRect(c)[2] / float(max(1, cv2.boundingRect(c)[3])) <= 1.40
        )
        density = cv2.countNonZero(r_thresh) / float(roi.shape[0] * roi.shape[1])
        return b_cnt, density

    col12_bot_b, _ = analyze_roi(72.0, 128.0, 78.0, 105.0)
    col34_bot_b, _ = analyze_roi(12.0, 68.0, 78.0, 98.0)
    mid_total_b, _ = analyze_roi(10.0, 130.0, 40.0, 74.0)
    top_total_b, _ = analyze_roi(10.0, 130.0, 20.0, 38.0)
    col4_mid_b, _ = analyze_roi(12.0, 38.0, 40.0, 74.0)

    if col12_bot_b >= 8:
        detected_qs = 60
    elif col34_bot_b >= 8:
        detected_qs = 50
    elif mid_total_b >= 15:
        if col4_mid_b >= 4:
            detected_qs = 40
        else:
            detected_qs = 30
    else:
        if top_total_b >= 30:
            detected_qs = 10
        elif top_total_b >= 8:
            detected_qs = 4
        else:
            detected_qs = 40

    detected_tf_count = 0
    if detected_qs == 40:
        c1_b, _ = analyze_roi(100.0, 130.0, 22.0, 74.0)
        c2_b, _ = analyze_roi(70.0, 100.0, 22.0, 74.0)
        c3_b, _ = analyze_roi(40.0, 70.0, 22.0, 74.0)
        c4_b, _ = analyze_roi(10.0, 40.0, 22.0, 74.0)
        tf_cols = sum(1 for c in [c1_b, c2_b, c3_b, c4_b] if c < 60)
        detected_tf_count = tf_cols * 10

    def _get_template_tf_mcq_counts(tpl):
        td = tpl.template_data or {}
        sections = td.get("questions", {}).get("sections", [])
        if sections:
            tf_cnt, mcq_cnt = 0, 0
            for s in sections:
                is_tf = s.get("type") == "true_false" or (
                    s.get("choices") and len(s.get("choices")) == 2 and
                    ("صح" in s.get("choices") or "T" in s.get("choices"))
                )
                tot = max(1, (s.get("to_q", 1) - s.get("from_q", 1) + 1))
                if is_tf:
                    tf_cnt += tot
                else:
                    mcq_cnt += tot
            return tf_cnt, mcq_cnt
        if tpl.id == 31 or "30 صح" in tpl.name or "30صح" in tpl.name:
            return 30, 10
        if tpl.id == 29 or "20 صح" in tpl.name or "20صح" in tpl.name:
            return 20, 20
        return 0, 40

    matching_templates = []
    for tpl in active_templates:
        td = tpl.template_data or {}
        q_cnt = (
            td.get("questions", {}).get("metadata", {}).get("num_questions") or
            len(td.get("mcq_questions", [])) or
            td.get("total_mcq")
        )
        if q_cnt == detected_qs or f"({detected_qs} سؤال)" in tpl.name or f"({detected_qs}سؤال)" in tpl.name:
            matching_templates.append(tpl)

    db_obj = None
    if detected_qs == 40:
        for tpl in matching_templates:
            tf_c, mcq_c = _get_template_tf_mcq_counts(tpl)
            if tf_c == detected_tf_count:
                db_obj = tpl
                break
        if not db_obj and matching_templates:
            db_obj = matching_templates[0]
    elif matching_templates:
        db_obj = matching_templates[0]

    if not db_obj:
        db_obj = active_templates[0] if active_templates else None

    logger.info(
        "Fallback geometric detection: %d questions (TF=%d) -> Bound Template: %s (id=%s)",
        detected_qs, detected_tf_count, db_obj.name if db_obj else "None", db_obj.id if db_obj else "None"
    )

    return db_obj, detected_code, detected_qs


def _grade_with_template(image_path: str, template_id: str, answer_key: dict, dpi: int, original_filename: str = "", marks_map: dict = None) -> dict:
    """
    التصحيح باستخدام المحرك الاحترافي (OpenCVOMREngine + Template).
    يتعرف تلقائياً على القالب المطابق مباشرة من محتوى الورقة (40 سؤال أو 50 سؤال أو 60 أو 180).
    """
    import time
    import cv2

    t0 = time.time()
    template = None
    db_obj = None
    detected_code = None

    try:
        try:
            from templates_engine.models.ExamTemplate import ExamTemplate
        except ImportError:
            from templates_engine.models import ExamTemplate
        from core.contracts import TemplateContract
        from django.db.models import Q

        # فحص وتحليل بصري مسبق لتحديد كثافة الأسئلة في الورقة بدقة (40 vs 50 vs 60 vs 180)
        detected_db_obj, detected_code, detected_qs = _detect_template_from_sheet(
            image_path, template_id, original_filename=original_filename or os.path.basename(image_path)
        )
        switched_notice = ""

        # هل يُطلب التعرف التلقائي الذكي؟
        is_auto = (
            not template_id or
            str(template_id).strip().upper() in ("AUTO", "OMR_AUTO")
        )

        if is_auto:
            db_obj = detected_db_obj
        else:
            # تم تمرير معرّف صريح من المستخدم - نلتزم باختيار المستخدم تماماً دون تبديل!
            if str(template_id).isdigit():
                db_obj = ExamTemplate.objects.filter(id=int(template_id), is_active=True).first()
            if not db_obj:
                import uuid as _uuid
                try:
                    _uuid.UUID(template_id)
                    db_obj = ExamTemplate.objects.filter(id=template_id, is_active=True).first()
                except (ValueError, AttributeError):
                    pass
            if not db_obj:
                db_obj = ExamTemplate.objects.filter(
                    Q(template_data__template_id=template_id) | Q(name__icontains=str(template_id)),
                    is_active=True
                ).first()
            # إذا لم يُعثر عليه بالمعرف الصريح فقط، نلجأ للتعرف التلقائي
            if not db_obj:
                db_obj = detected_db_obj

        if db_obj and db_obj.template_data:
            logger.info("Loading template from DB: %s (id=%s)", db_obj.name, db_obj.id)
            from templates_engine.builder import TemplateBuilderService
            builder = TemplateBuilderService()
            try:
                template = builder.build_from_designer_config(db_obj.template_data)
            except Exception as build_err:
                logger.warning("Dynamic template build failed (%s) - falling back to raw contract", build_err)
                if isinstance(db_obj.template_data, dict) and "fiducial_marks" in db_obj.template_data:
                    template = TemplateContract(**db_obj.template_data)

    except Exception as e:
        logger.warning("DB template lookup/detection failed (%s) — trying fallback", e)

    # ── 2. Fallback: built-in ministry builder (based on detected question count) ─
    if template is None:
        from templates_engine.builder import TemplateBuilderService
        builder = TemplateBuilderService()

        _fb_qs = locals().get("detected_qs", 0)

        if _fb_qs == 60:
            logger.info("Fallback → build_yemeni_ministry_60_template")
            template = builder.build_yemeni_ministry_60_template(
                template_id="YEMEN_MINISTRY_60",
            )
        elif _fb_qs == 40:
            logger.info("Fallback → build_yemeni_ministry_40_template")
            template = builder.build_yemeni_ministry_40_template(
                template_id="YEMEN_MINISTRY_40",
                paper_size="A5",
            )
        elif _fb_qs == 50:
            logger.info("Fallback → build_yemeni_ministry_50_template")
            template = builder.build_yemeni_ministry_50_template(
                template_id="YEMEN_MINISTRY_50",
                paper_size="A5",
            )
        else:
            logger.info("Fallback → build_multigraphics_yemen_template (omr_yemen_180)")
            template = builder.build_multigraphics_yemen_template(
                template_id="OMR_YEMEN_180",
                config_name="omr_yemen_180",
            )



    # 2. تحديد دقة الصورة (DPI) تلقائياً بناء على أبعاد الصورة وحجم الورقة في القالب
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"تعذر قراءة صورة ورقة الإجابة: {image_path}")
    img_h, img_w = img.shape[:2]

    template_dict = template.model_dump() if hasattr(template, 'model_dump') else (template if isinstance(template, dict) else {})
    paper_size = str(template_dict.get("paper_size", "A5")).upper()
    if "A4" in paper_size:
        pw_mm = 297.0 if img_w >= img_h else 210.0
    else:
        pw_mm = 210.0 if img_w >= img_h else 148.5

    calc_dpi = int(round(img_w / (pw_mm / 25.4)))
    effective_dpi = calc_dpi if (72 <= calc_dpi <= 2400) else (dpi or 300)
    logger.info("OMR Image resolution: %sx%s px, Paper: %s -> Effective DPI: %s", img_w, img_h, paper_size, effective_dpi)

    # استرجاع مفتاح الإجابة تلقائياً من بيانات القالب المخزن إذا لم يتم إرساله من الواجهة
    if not answer_key and db_obj and isinstance(db_obj.template_data, dict):
        tpl_key = db_obj.template_data.get("answer_key") or db_obj.template_data.get("model_answers")
        if isinstance(tpl_key, dict):
            if "mcq_answers" in tpl_key and isinstance(tpl_key["mcq_answers"], dict):
                answer_key = {str(k): v for k, v in tpl_key["mcq_answers"].items()}
            else:
                answer_key = {str(k): v for k, v in tpl_key.items()}
            logger.info("Loaded answer key from template_data: %s items", len(answer_key))

    if not answer_key and template:
        mcq_qs = getattr(template, "mcq_questions", []) if not isinstance(template, dict) else template.get("mcq_questions", [])
        extracted_key = {}
        for q in mcq_qs:
            q_id = getattr(q, "question_id", None) or (q.get("question_id") if isinstance(q, dict) else None)
            c_ans = getattr(q, "correct_answer", None) or (q.get("correct_answer") if isinstance(q, dict) else None)
            if q_id and c_ans:
                extracted_key[str(q_id)] = c_ans
        if extracted_key:
            answer_key = extracted_key
            logger.info("Loaded answer key from template questions: %s items", len(answer_key))

    if hasattr(template, "expected_scan_dpi"):
        template.expected_scan_dpi = effective_dpi
    elif isinstance(template, dict):
        template["expected_scan_dpi"] = effective_dpi

    # 3. تمرير الصورة + القالب إلى OpenCVOMREngine
    from omr.providers.opencv_omr import OpenCVOMREngine
    engine = OpenCVOMREngine()

    marks_by_q = {str(k): float(v) for k, v in (marks_map or {}).items()}
    engine_result = engine._process(
        input_data={"image_path": image_path},
        context={
            "template": template,
            "dpi": effective_dpi,
            "answer_key": {
                "mcq_answers": {str(k): v for k, v in (answer_key or {}).items()},
                "marks_by_question": marks_by_q,
                "mcq_marks_per_question": 1.0,
            },
        },
    )

    elapsed_ms = (time.time() - t0) * 1000

    # 4. تحويل النتيجة لتتوافق مع واجهة الـ API الحالية
    data = engine_result.data or {}
    questions_raw = data.get("questions", [])
    scan_dpi_used = data.get("detected_dpi", effective_dpi)
    aligned_img = data.pop("aligned_image", img)

    # رسم الصورة المُعلَّقة
    annotated = _draw_template_annotated(aligned_img, questions_raw, template, scan_dpi_used)
    _, buf = cv2.imencode('.png', annotated)

    total_questions = data.get("total_questions", len(questions_raw))
    total_answered = sum(1 for q in questions_raw if q.get("marked_choice"))
    total_correct = sum(1 for q in questions_raw if q.get("is_correct"))

    barcode_val = detected_code or ""
    qr_val = ""
    student_info = {}
    if db_obj and isinstance(db_obj.template_data, dict):
        td = db_obj.template_data
        student_info = td.get("header", {})

    final_score = float(data.get("total_score", total_correct))
    final_max = float(data.get("max_score", total_questions))
    score_pct = round((final_score / max(final_max, 1.0)) * 100, 1)

    return {
        "total_questions": total_questions,
        "total_answered":  total_answered,
        "total_correct":   total_correct,
        "total_wrong":     total_answered - total_correct,
        "total_empty":     total_questions - total_answered,
        "score":           round(final_score, 2),
        "max_score":       round(final_max, 2),
        "score_percent":   score_pct,
        "ai_corrections":  data.get("ambiguous_count", 0),
        "processing_ms":   round(elapsed_ms, 1),
        "questions":       questions_raw,
        "annotated_image": buf.tobytes(),
        "engine_used":     "template_driven",
        "barcode":         barcode_val,
        "qr":              qr_val,
        "template_id":     str(db_obj.id if db_obj else template_id),
        "template_name":   db_obj.name if db_obj else "النموذج المعياري",
        "switched_notice": locals().get("switched_notice", ""),
    }


def _grade_with_legacy(image_path: str, answer_key: dict, dpi: int, marks_map: dict = None) -> dict:
    """Fallback: المحرك القديم svg_omr_engine (إحداثيات ثابتة)."""
    from omr.providers.svg_omr_engine import grade_sheet as _grade
    result = _grade(
        image_path=image_path,
        answer_key=answer_key if answer_key else None,
        dpi=dpi,
        use_ai=True,
        marks_map=marks_map
    )
    result["engine_used"] = "legacy_svg"
    return result


def _draw_template_annotated(img, questions, template, dpi):
    """رسم نتائج التصحيح على الصورة باستخدام إحداثيات القالب."""
    import cv2
    scale = dpi / 25.4

    template_data = template.model_dump() if hasattr(template, 'model_dump') else template
    mcq_questions = template_data.get("mcq_questions", [])

    # بناء خريطة الإحداثيات من القالب
    for q_result in questions:
        q_id = q_result.get("question_id")
        marked = q_result.get("marked_choice")
        correct = q_result.get("correct_choice")
        is_correct = q_result.get("is_correct")

        # إيجاد السؤال في القالب
        q_template = None
        for mq in mcq_questions:
            if mq["question_id"] == q_id:
                q_template = mq
                break
        if not q_template:
            continue

        actual_centers = q_result.get("actual_centers", {})

        for choice_data in q_template["choices"]:
            ch = choice_data["choice"]
            bubble = choice_data.get("bubble_region", {})
            if ch in actual_centers:
                cx, cy = int(actual_centers[ch][0]), int(actual_centers[ch][1])
            else:
                cx = int((bubble["dx_mm"] + bubble["width_mm"] / 2) * scale)
                cy = int((bubble["dy_mm"] + bubble["height_mm"] / 2) * scale)
            r = int(bubble.get("width_mm", 3.6) / 2 * scale)
            mk = max(6, int(r * 0.9))

            ai_state = q_result.get("ai_results", {}).get(ch, "empty")

            if ai_state in ("filled", "half_filled"):
                if ch == marked:
                    if is_correct is True:
                        cv2.circle(img, (cx, cy), mk, (0, 210, 0), 3)
                    elif is_correct is False:
                        cv2.circle(img, (cx, cy), mk, (0, 0, 220), -1)
                        cv2.line(img, (cx-int(r*.4), cy-int(r*.4)), (cx+int(r*.4), cy+int(r*.4)), (255,255,255), 2)
                        cv2.line(img, (cx+int(r*.4), cy-int(r*.4)), (cx-int(r*.4), cy+int(r*.4)), (255,255,255), 2)
                    else:
                        cv2.circle(img, (cx, cy), mk, (255, 180, 0), 2)
            else:
                # إظهار إطار الدائرة المكتشفة باللون الأزرق الفاتح لإثبات مسح وموضع الدائرة
                cv2.circle(img, (cx, cy), mk, (240, 160, 40), 1)

            cv2.circle(img, (cx, cy), 2, (80, 80, 80), -1)

        if correct and marked and marked != correct and is_correct is False:
            for cd in q_template["choices"]:
                if cd["choice"] == correct:
                    if correct in actual_centers:
                        cxc, cyc = int(actual_centers[correct][0]), int(actual_centers[correct][1])
                    else:
                        bb = cd["bubble_region"]
                        cxc = int((bb["dx_mm"] + bb["width_mm"] / 2) * scale)
                        cyc = int((bb["dy_mm"] + bb["height_mm"] / 2) * scale)
                    rc = int(cd.get("bubble_region", {}).get("width_mm", 3.6) / 2 * scale)
                    cv2.circle(img, (cxc, cyc), max(6, int(rc * 0.9)), (0, 210, 0), 2)
                    break

    return img



@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_result(request, result_id: str):
    """عرض نتيجة محفوظة في الكاش."""
    cached = _RESULT_CACHE.get(result_id)
    if not cached:
        return Response({"error": "النتيجة غير موجودة أو انتهت صلاحيتها"}, status=status.HTTP_404_NOT_FOUND)
    return Response(cached)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_annotated_image(request, result_id: str):
    """إرجاع الصورة المُعلَّقة كـ PNG مباشرة."""
    cached = _RESULT_CACHE.get(result_id)
    if not cached:
        return HttpResponse(status=404)
    img_bytes = base64.b64decode(cached["annotated_b64"])
    return HttpResponse(img_bytes, content_type="image/png")


