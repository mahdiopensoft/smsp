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

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

logger = logging.getLogger("omr.api")

# مخزن مؤقت للنتائج (demo mode — لا قاعدة بيانات)
_RESULT_CACHE: dict = {}


@csrf_exempt
@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([permissions.AllowAny])
def grade_sheet(request):
    """
    رفع ورقة OMR وتصحيحها — Template-Driven Architecture.

    Form-data:
        sheet_image   (file)    — صورة الورقة (PNG/JPG)
        answer_key    (str, optional) — JSON: {"1":"A","2":"C",...}
        template_id   (str, optional) — معرّف القالب (default: OMR_YEMEN_180)
        dpi           (int, optional) — دقة الصورة (default: 300)

    إذا تم تحديد template_id، يتم استخدام المحرك الاحترافي (OpenCVOMREngine)
    الذي يقرأ الإحداثيات من القالب. وإلا يُستخدم المحرك القديم (svg_omr_engine) كـ fallback.
    """
    image_file = request.FILES.get("sheet_image")
    if not image_file:
        return Response({"error": "sheet_image مطلوب"}, status=status.HTTP_400_BAD_REQUEST)

    # تحليل مفتاح الإجابات والربط بالاختبار
    answer_key = {}
    raw_key = request.data.get("answer_key", "")
    if raw_key:
        try:
            parsed = json.loads(raw_key)
            answer_key = {int(k): v for k, v in parsed.items()}
        except (json.JSONDecodeError, ValueError) as e:
            return Response({"error": f"answer_key غير صحيح: {e}"}, status=status.HTTP_400_BAD_REQUEST)

    # التحقق من وجود معرف الاختبار أو النموذج لجلب مفتاح الإجابة تلقائياً
    exam_id = request.data.get("exam_id") or request.data.get("exam")
    version_id = request.data.get("version_id")
    version_code = request.data.get("version_code") or request.data.get("version")
    target_version = None

    if exam_id or version_id:
        try:
            from exams.models.ExamVersion import ExamVersion
            if version_id:
                target_version = ExamVersion.objects.filter(id=version_id, is_deleted=False).prefetch_related('question_orders__question__options').first()
                if target_version and not exam_id:
                    exam_id = target_version.exam_id
            elif exam_id and version_code:
                target_version = ExamVersion.objects.filter(exam_id=exam_id, versionCode=version_code, is_deleted=False).prefetch_related('question_orders__question__options').first()
            elif exam_id:
                target_version = ExamVersion.objects.filter(exam_id=exam_id, is_deleted=False).prefetch_related('question_orders__question__options').first()

            # جلب مفتاح الحل تلقائياً من النموذج إذا لم يُمرر يدوياً
            if target_version and not answer_key:
                for qo in target_version.question_orders.filter(is_deleted=False).order_by('orderIndex'):
                    opts = list(qo.question.options.filter(is_deleted=False))
                    ans_letter = 'A'
                    for idx, opt in enumerate(opts):
                        if opt.isTrue:
                            ans_letter = chr(65 + idx)
                            break
                    answer_key[qo.orderIndex] = ans_letter
        except Exception as e_key:
            logger.warning(f"Could not auto-fetch answer key from ExamVersion: {e_key}")

    dpi = int(request.data.get("dpi", 300))
    template_id = request.data.get("template_id", "").strip()

    # حفظ الصورة مؤقتاً
    suffix = os.path.splitext(image_file.name)[1] or ".png"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        for chunk in image_file.chunks():
            tmp.write(chunk)
        tmp_path = tmp.name

    try:
        if template_id:
            # ═══ المحرك الاحترافي (Template-Driven) ═══
            result = _grade_with_template(tmp_path, template_id, answer_key, dpi, original_filename=image_file.name)
        else:
            # ═══ Fallback: المحرك القديم (svg_omr_engine) ═══
            result = _grade_with_legacy(tmp_path, answer_key, dpi)
    except Exception as e:
        logger.exception("خطأ في التصحيح")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        os.unlink(tmp_path)

    # تحويل الصورة المُعلَّقة إلى base64
    annotated_b64 = base64.b64encode(result.pop("annotated_image")).decode()

    # توليد معرّف النتيجة وتخزينها
    result_id = str(uuid.uuid4())
    _RESULT_CACHE[result_id] = {
        "meta": {k: v for k, v in result.items() if k != "questions"},
        "questions": result["questions"],
        "annotated_b64": annotated_b64,
    }

    # ═══ حفظ النتيجة آلياً في قاعدة البيانات في نموذج Submission و OMRSheetResult ═══
    try:
        from submissions.models.Submission import Submission
        from omr.models.OMRSheetResult import OMRSheetResult

        student_info = result.get("student_info", {})
        s_name = student_info.get("name") or "طالب اختبار"
        seat_num = student_info.get("seat_number") or result.get("barcode") or ""
        total_q = result.get("total_questions", len(result.get("questions", [])))
        total_c = result.get("total_correct", 0)

        # حساب نسبة الثقة الكلية
        qs = result.get("questions", [])
        if qs:
            avg_conf = sum(float(q.get("final_confidence") or q.get("confidence") or 0.95) for q in qs) / len(qs)
        else:
            avg_conf = 0.95
        confidence = float(result.get("overall_confidence") or result.get("confidence") or avg_conf)

        # ربط الاختبار والنموذج في التسليم
        from exams.models.Exam import Exam
        from exams.models.StudentExamRegistration import StudentExamRegistration
        exam_obj = None
        if exam_id:
            exam_obj = Exam.objects.filter(id=exam_id, is_deleted=False).first()
        if not exam_obj:
            exam_obj = Exam.objects.filter(is_deleted=False).order_by('-created_at').first()
        if not exam_obj:
            exam_obj, _ = Exam.objects.get_or_create(title="اختبار عام OMR", defaults={"total_score": 100})

        # محاولة مطابقة تسجيل الطالب آلياً عبر رقم الجلوس أو الباركود
        barcode_val = result.get("barcode") or ""
        qr_val = result.get("qr") or ""
        matched_reg = None
        if exam_obj:
            reg_qs = StudentExamRegistration.objects.filter(examVersion__exam=exam_obj, is_deleted=False).select_related('student', 'student_profile__organization', 'examVersion')
            if seat_num:
                matched_reg = reg_qs.filter(seatNumber=str(seat_num)).first()
            if not matched_reg and barcode_val:
                matched_reg = reg_qs.filter(seatNumber=barcode_val.split("_")[-1] if "SEAT_" in barcode_val else barcode_val).first()
            if not matched_reg and qr_val and "|" in qr_val:
                parts = qr_val.split("|")
                if len(parts) >= 3:
                    matched_reg = reg_qs.filter(seatNumber=parts[2]).first()

        inst_name = ""
        if matched_reg:
            if not target_version:
                target_version = matched_reg.examVersion
            if not s_name or s_name == "طالب اختبار":
                if matched_reg.student_profile and matched_reg.student_profile.name_ar:
                    s_name = matched_reg.student_profile.name_ar
                elif matched_reg.student:
                    s_name = matched_reg.student.first_name or matched_reg.student.username
            if not seat_num:
                seat_num = matched_reg.seatNumber
            if matched_reg.student_profile and matched_reg.student_profile.organization:
                inst_name = matched_reg.student_profile.organization.name_ar

        sub_kwargs = {
            "exam": exam_obj,
            "status": Submission.Status.COMPLETED,
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
            }
        }
        if target_version:
            sub_kwargs["exam_version"] = target_version
        if matched_reg and not Submission.objects.filter(registration=matched_reg).exists():
            sub_kwargs["registration"] = matched_reg

        sub_record = Submission.objects.create(**sub_kwargs)

        OMRSheetResult.objects.create(
            submission=sub_record,
            status="success",
            confidence=confidence,
            total_questions=total_q,
            answered_questions=result.get("total_answered", 0),
            correct_answers=total_c,
            wrong_answers=result.get("total_wrong", 0),
            unanswered=result.get("total_empty", 0),
            mcq_score=result.get("score", 0),
            mcq_max_score=result.get("max_score", total_q),
            provider_used=result.get("engine_used", "opencv_omr"),
            processing_time_ms=result.get("processing_ms", 0.0),
        )
        result_id = str(sub_record.id)
        _RESULT_CACHE[result_id] = _RESULT_CACHE[list(_RESULT_CACHE.keys())[-1]]
    except Exception as db_err:
        logger.warning(f"Could not persist submission record to DB: {db_err}")

    return Response({
        "result_id":       result_id,
        "total_questions": result.get("total_questions", len(result.get("questions", []))),
        "score":           result["score"],
        "max_score":       result["max_score"],
        "score_percent":   result["score_percent"],
        "total_correct":   result["total_correct"],
        "total_wrong":     result["total_wrong"],
        "total_answered":  result["total_answered"],
        "total_empty":     result["total_empty"],
        "ai_corrections":  result.get("ai_corrections", 0),
        "processing_ms":   result["processing_ms"],
        "questions":       result["questions"],
        "annotated_image": annotated_b64,
        "engine_used":     result.get("engine_used", "legacy"),
        "template_id":     result.get("template_id") or template_id or "svg_hardcoded",
        "template_name":   result.get("template_name", ""),
        "barcode":         result.get("barcode", ""),
        "qr":              result.get("qr", ""),
        "student_info":    result.get("student_info", {}),
        "switched_notice": result.get("switched_notice", ""),
    }, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([permissions.AllowAny])
def detect_template_api(request):
    """
    التعرف التلقائي الفوري على القالب من الورقة المرفوعة مباشرة.
    يرجع معرّف القالب المطابق، اسمه، وعدد الأسئلة دون الحاجة لاختيار يدوي من المستخدم.
    """
    image_file = request.FILES.get("sheet_image")
    if not image_file:
        return Response({"error": "sheet_image مطلوب"}, status=status.HTTP_400_BAD_REQUEST)

    suffix = os.path.splitext(image_file.name)[1] or ".png"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        for chunk in image_file.chunks():
            tmp.write(chunk)
        tmp_path = tmp.name

    try:
        db_obj, detected_code, detected_qs = _detect_template_from_sheet(tmp_path, original_filename=image_file.name)
        if not db_obj:
            return Response({"error": "تعذر التعرف على القالب من الورقة"}, status=status.HTTP_404_NOT_FOUND)

        td = db_obj.template_data or {}
        q_count = detected_qs or td.get("questions", {}).get("metadata", {}).get("num_questions", 50)
        return Response({
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

    # ── 4. فحص هيئة وأبعاد الورقة (A4 طولي مقابل A5 عرضي) ───────────
    is_portrait = h > w * 1.15
    if is_portrait:
        db_obj = ExamTemplate.objects.filter(
            Q(template_data__paper__size__iexact="A4") | Q(name__icontains="180"),
            is_active=True
        ).order_by("-created_at").first()
        return db_obj, detected_code, 180

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


def _grade_with_template(image_path: str, template_id: str, answer_key: dict, dpi: int, original_filename: str = "") -> dict:
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

    engine_result = engine._process(
        input_data={"image_path": image_path},
        context={
            "template": template,
            "dpi": effective_dpi,
            "answer_key": {
                "mcq_answers": {str(k): v for k, v in answer_key.items()},
                "mcq_marks_per_question": 1,
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
        if not barcode_val:
            barcode_val = td.get("barcode", {}).get("value", "")
        qr_val = td.get("qr", {}).get("value", "")
        student_info = td.get("header", {})

    return {
        "total_questions": total_questions,
        "total_answered":  total_answered,
        "total_correct":   total_correct,
        "total_wrong":     total_answered - total_correct,
        "total_empty":     total_questions - total_answered,
        "score":           round(data.get("total_score", total_correct), 2),
        "max_score":       float(data.get("max_score", total_questions)),
        "score_percent":   round((total_correct / max(total_questions, 1)) * 100, 1),
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


def _grade_with_legacy(image_path: str, answer_key: dict, dpi: int) -> dict:
    """Fallback: المحرك القديم svg_omr_engine (إحداثيات ثابتة)."""
    from omr.providers.svg_omr_engine import grade_sheet as _grade
    result = _grade(
        image_path=image_path,
        answer_key=answer_key if answer_key else None,
        dpi=dpi,
        use_ai=True,
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


