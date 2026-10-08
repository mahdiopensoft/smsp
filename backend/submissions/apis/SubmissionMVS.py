from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from submissions.models.Submission import Submission
from submissions.serializers.Submission import SubmissionSerializer
from bank.models.AuditLog import AuditLog
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from django.db.models import Q, Count, Avg

class SubmissionMVS(AllMVS):
    """
    Dedicated ModelViewSet for OMR Submissions & Processed Answer Sheets.
    Endpoint: /api/submissions/submissions/
    Used by: OMRSubmissionsView.vue
    """
    queryset = Submission.objects.select_related(
        'batch',
        'exam__subject',
        'exam_version',
        'registration__student',
        'registration__student_profile'
    ).all().distinct()
    serializer_class = SubmissionSerializer
    filterset_fields = {
        'status': ['exact'],
        'batch': ['exact'],
        'exam': ['exact'],
        'exam_version': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        inst_type = self.request.query_params.get('institution_type')
        if inst_type and inst_type != 'all':
            qs = qs.filter(exam__institution_type=inst_type)

        exam_id = self.request.query_params.get('exam') or self.request.query_params.get('exam_id')
        if exam_id:
            qs = qs.filter(exam_id=exam_id)

        version_id = self.request.query_params.get('exam_version') or self.request.query_params.get('examVersion')
        if version_id:
            qs = qs.filter(exam_version_id=version_id)

        subject_id = self.request.query_params.get('subject') or self.request.query_params.get('subject_id')
        if subject_id:
            qs = qs.filter(
                Q(exam__subject_id=subject_id) |
                Q(exam__versions__question_orders__question__lesson__unit__class_subject__subject_id=subject_id) |
                Q(exam__versions__question_orders__question__lesson__unit__semester_subject__fk_subject_id=subject_id)
            )

        # School Filters
        stage_id = self.request.query_params.get('stage') or self.request.query_params.get('stage_id')
        if stage_id:
            qs = qs.filter(
                Q(exam__versions__question_orders__question__lesson__unit__class_subject__class_track__level__stage_id=stage_id) |
                Q(exam__subject__class_subjects__class_track__level__stage_id=stage_id)
            )

        class_track_id = self.request.query_params.get('class_track') or self.request.query_params.get('class_track_id')
        if class_track_id:
            qs = qs.filter(
                Q(exam__versions__question_orders__question__lesson__unit__class_subject__class_track_id=class_track_id) |
                Q(exam__subject__class_subjects__class_track_id=class_track_id)
            )

        level_id = self.request.query_params.get('level') or self.request.query_params.get('level_id')
        if level_id:
            qs = qs.filter(
                Q(exam__versions__question_orders__question__lesson__unit__class_subject__class_track__level_id=level_id) |
                Q(exam__subject__class_subjects__class_track__level_id=level_id)
            )

        track_id = self.request.query_params.get('track') or self.request.query_params.get('track_id') or self.request.query_params.get('branch')
        if track_id:
            qs = qs.filter(
                Q(exam__versions__question_orders__question__lesson__unit__class_subject__class_track__track_id=track_id) |
                Q(exam__subject__class_subjects__class_track__track_id=track_id)
            )

        # University Filters
        college_id = self.request.query_params.get('college') or self.request.query_params.get('fk_college')
        if college_id:
            qs = qs.filter(
                Q(exam__versions__question_orders__question__lesson__unit__semester_subject__fk_specialization__fk_college_id=college_id) |
                Q(exam__subject__semester_subjects__fk_specialization__fk_college_id=college_id)
            )

        dept_id = self.request.query_params.get('department') or self.request.query_params.get('fk_department') or self.request.query_params.get('section')
        if dept_id:
            qs = qs.filter(
                Q(exam__versions__question_orders__question__lesson__unit__semester_subject__fk_specialization__fk_section_id=dept_id) |
                Q(exam__subject__semester_subjects__fk_specialization__fk_section_id=dept_id)
            )

        spec_id = self.request.query_params.get('specialization') or self.request.query_params.get('fk_specialization')
        if spec_id:
            qs = qs.filter(
                Q(exam__versions__question_orders__question__lesson__unit__semester_subject__fk_specialization_id=spec_id) |
                Q(exam__subject__semester_subjects__fk_specialization_id=spec_id)
            )

        sem_sub_id = self.request.query_params.get('semester_subject') or self.request.query_params.get('fk_semester_subject')
        if sem_sub_id:
            qs = qs.filter(
                Q(exam__versions__question_orders__question__lesson__unit__semester_subject_id=sem_sub_id) |
                Q(exam__subject__semester_subjects__id=sem_sub_id)
            )

        submission_status = self.request.query_params.get('status')
        if submission_status:
            qs = qs.filter(status=submission_status)

        batch_id = self.request.query_params.get('batch') or self.request.query_params.get('batch_id')
        if batch_id:
            qs = qs.filter(batch_id=batch_id)

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(registration__seatNumber__icontains=search) |
                Q(registration__student__first_name__icontains=search) |
                Q(registration__student__last_name__icontains=search) |
                Q(registration__student__username__icontains=search) |
                Q(registration__student_profile__name_ar__icontains=search) |
                Q(registration__student_profile__academic_number__icontains=search) |
                Q(exam__title__icontains=search) |
                Q(exam__uniqueCode__icontains=search)
            )

        return qs.order_by('-id').distinct()

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Calculates aggregate OMR processing statistics directly in database."""
        qs = self.get_queryset()
        aggregates = qs.aggregate(
            total=Count('id'),
            completed=Count('id', filter=Q(status=Submission.Status.COMPLETED)),
            needs_review=Count('id', filter=Q(status=Submission.Status.NEEDS_REVIEW)),
            failed=Count('id', filter=Q(status=Submission.Status.FAILED)),
            pending=Count('id', filter=Q(status__in=[Submission.Status.PENDING, Submission.Status.ALIGNING, Submission.Status.OMR_PROCESSING])),
            avg_score=Avg('total_score', filter=Q(status=Submission.Status.COMPLETED))
        )
        return Response({
            "total": aggregates['total'] or 0,
            "completed": aggregates['completed'] or 0,
            "needs_review": aggregates['needs_review'] or 0,
            "failed": aggregates['failed'] or 0,
            "pending": aggregates['pending'] or 0,
            "average_score": round(float(aggregates['avg_score'] or 0), 2)
        })

    @action(detail=False, methods=['post'], url_path='bulk-upload', parser_classes=[MultiPartParser, FormParser])
    def bulk_upload(self, request):
        """
        المسح الضوئي الجماعي المتقدم (Bulk / Batch OMR Scanning)
        يستقبل:
        1. مجموعة صور فردية (Multiple images): files أو images
        2. أو ملف مضغوط (ZIP archive) يحتوي على أوراق الإجابة
        3. أو ملف PDF متعدد الصفحات (Multipage PDF) من الماسح الضوئي (ADF)
        """
        import os
        import io
        import zipfile
        import tempfile
        import logging
        from django.core.files.base import ContentFile
        from django.utils import timezone
        from omr.api import _grade_with_template, _detect_template_from_sheet
        from omr.models.OMRSheetResult import OMRSheetResult
        from omr.models.OMRQuestionResult import OMRQuestionResult
        from submissions.models.SubmissionBatch import SubmissionBatch
        from exams.models.Exam import Exam
        from exams.models.ExamVersion import ExamVersion
        from exams.models.StudentExamRegistration import StudentExamRegistration

        try:
            import fitz
        except ImportError:
            fitz = None

        logger = logging.getLogger("omr.bulk")

        # جمع الملفات المرفوعة
        uploaded_files = request.FILES.getlist('files') or request.FILES.getlist('images') or []
        single_file = request.FILES.get('file')
        if single_file and not uploaded_files:
            uploaded_files = [single_file]

        if not uploaded_files:
            return Response({"success": False, "message": "لم يتم العثور على أي ملفات أو صور للمعالجة"}, status=status.HTTP_400_BAD_REQUEST)

        exam_id = request.data.get('exam_id') or request.data.get('exam')
        template_id = request.data.get('template_id', 'AUTO')
        batch_name = request.data.get('title') or request.data.get('name') or f"دفعة مسح ضوئي {timezone.now().strftime('%Y-%m-%d %H:%M')}"

        exam_obj = None
        if exam_id:
            exam_obj = Exam.objects.filter(id=exam_id, is_deleted=False).first()
        if not exam_obj:
            exam_obj = Exam.objects.filter(is_deleted=False).order_by('-created_at').first()

        # إنشاء سجل الدفعة
        batch_record = SubmissionBatch.objects.create(
            name=batch_name,
            exam=exam_obj,
            uploaded_by=request.user if request.user.is_authenticated else None,
            status=SubmissionBatch.Status.PROCESSING,
        )

        # استخراج الصور الفردية من PDF أو ZIP أو الصور العادية
        extracted_images = []  # list of (filename, file_bytes)

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
                    logger.warning(f"Error reading ZIP file {up_file.name}: {ze}")
            elif fn_lower.endswith('.pdf'):
                if fitz is not None:
                    try:
                        doc = fitz.open(stream=file_bytes, filetype="pdf")
                        for page_idx in range(len(doc)):
                            page = doc[page_idx]
                            pix = page.get_pixmap(dpi=300)
                            img_data = pix.tobytes("png")
                            extracted_images.append((f"{os.path.splitext(up_file.name)[0]}_page_{page_idx+1}.png", img_data))
                    except Exception as pe:
                        logger.warning(f"Error rendering PDF {up_file.name}: {pe}")
                else:
                    logger.warning("PyMuPDF (fitz) is not installed; skipping PDF decomposition.")
            elif fn_lower.endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff', '.webp')):
                extracted_images.append((up_file.name, file_bytes))

        if not extracted_images:
            batch_record.status = SubmissionBatch.Status.FAILED
            batch_record.notes = "لم يتم العثور على صور أوراق صالحة داخل الملفات المرفوعة"
            batch_record.save()
            return Response({"success": False, "message": "لم يتم العثور على صور أوراق صالحة داخل الملفات المرفوعة"}, status=status.HTTP_400_BAD_REQUEST)

        # تجهيز مفاتيح الإجابة لجميع نماذج الاختبار
        versions_keys = {}
        if exam_obj:
            for v in exam_obj.versions.filter(is_deleted=False).prefetch_related('question_orders__question__options'):
                v_key = {}
                for qo in v.question_orders.filter(is_deleted=False).order_by('orderIndex'):
                    opts = list(qo.question.options.filter(is_deleted=False))
                    ans_letter = 'A'
                    for idx, opt in enumerate(opts):
                        if opt.isTrue:
                            ans_letter = chr(65 + idx)
                            break
                    v_key[qo.orderIndex] = ans_letter
                versions_keys[v.versionCode] = (v, v_key)

        default_version = list(versions_keys.values())[0][0] if versions_keys else None
        default_answer_key = list(versions_keys.values())[0][1] if versions_keys else {}

        # معالجة الأوراق بالكامل
        processed_sheets = []
        success_count = 0
        needs_review_count = 0
        failed_count = 0
        total_scores = 0.0

        for img_name, img_bytes in extracted_images:
            suffix = os.path.splitext(img_name)[1] or ".png"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(img_bytes)
                tmp_path = tmp.name

            try:
                # الكشف والتصحيح بالمحرك
                grading_result = _grade_with_template(
                    tmp_path,
                    template_id=template_id,
                    answer_key=default_answer_key,
                    dpi=300,
                    original_filename=img_name
                )

                score_val = float(grading_result.get("score", 0.0))
                total_q = grading_result.get("total_questions", 40)
                total_c = grading_result.get("total_correct", 0)
                barcode_val = grading_result.get("barcode") or ""
                qr_val = grading_result.get("qr") or ""
                student_info = grading_result.get("student_info", {})
                seat_num = student_info.get("seat_number") or ""
                s_name = student_info.get("name") or "طالب اختبار"

                # مطابقة نموذج الاختبار إن وجد في الباركود
                target_version = default_version
                if barcode_val and "_VER_" in barcode_val:
                    try:
                        v_code = barcode_val.split("_VER_")[1].split("_")[0]
                        if v_code in versions_keys:
                            target_version = versions_keys[v_code][0]
                    except Exception:
                        pass

                # مطابقة الطالب من رقم الجلوس أو الباركود
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

                if matched_reg:
                    target_version = matched_reg.examVersion
                    if matched_reg.student_profile and matched_reg.student_profile.name_ar:
                        s_name = matched_reg.student_profile.name_ar
                    elif matched_reg.student:
                        s_name = matched_reg.student.first_name or matched_reg.student.username
                    if not seat_num:
                        seat_num = matched_reg.seatNumber

                # تحديد حالة الورقة بناء على الثقة والالتباس
                ambiguous_c = grading_result.get("ambiguous_count", 0)
                avg_conf = float(grading_result.get("overall_confidence") or 0.95)
                sheet_status = Submission.Status.NEEDS_REVIEW if (ambiguous_c > 0 or avg_conf < 0.82) else Submission.Status.COMPLETED

                # إنشاء كائن التسليم
                sub_record = Submission(
                    batch=batch_record,
                    exam=exam_obj,
                    exam_version=target_version,
                    registration=matched_reg if (matched_reg and not Submission.objects.filter(registration=matched_reg).exists()) else None,
                    status=sheet_status,
                    current_engine="opencv_omr",
                    mcq_score=score_val,
                    total_score=score_val,
                    overall_confidence=avg_conf,
                    processing_time_ms=grading_result.get("processing_ms", 0.0),
                    omr_result=grading_result.get("questions", []),
                    layout_result={
                        "student_name": s_name,
                        "seat_number": seat_num,
                        "template_id": grading_result.get("template_id"),
                        "template_name": grading_result.get("template_name"),
                        "barcode": barcode_val,
                        "qr": qr_val,
                        "score_percent": grading_result.get("score_percent", 0),
                        "total_questions": total_q,
                    }
                )
                sub_record.original_image.save(img_name, ContentFile(img_bytes), save=False)
                sub_record.save()

                # حفظ النتيجة التفصيلية في OMRSheetResult و OMRQuestionResult
                sheet_res = OMRSheetResult.objects.create(
                    submission=sub_record,
                    status="success",
                    confidence=avg_conf,
                    total_questions=total_q,
                    answered_questions=grading_result.get("total_answered", 0),
                    correct_answers=total_c,
                    wrong_answers=grading_result.get("total_wrong", 0),
                    unanswered=grading_result.get("total_empty", 0),
                    ambiguous_count=ambiguous_c,
                    mcq_score=score_val,
                    mcq_max_score=total_q,
                    provider_used=grading_result.get("engine_used", "opencv_omr"),
                    processing_time_ms=grading_result.get("processing_ms", 0.0),
                )

                for q_item in grading_result.get("questions", []):
                    OMRQuestionResult.objects.create(
                        sheet_result=sheet_res,
                        question_number=q_item.get("question_id") or q_item.get("q") or 1,
                        marked_choice=q_item.get("marked_choice") or q_item.get("marked"),
                        correct_choice=q_item.get("correct_choice") or q_item.get("correct"),
                        is_correct=q_item.get("is_correct"),
                        bubble_state=q_item.get("bubble_state") or q_item.get("mode", "empty"),
                        choice_confidences=q_item.get("choice_confidences") or {},
                        final_confidence=q_item.get("final_confidence") or q_item.get("confidence") or 0.95,
                        marks_awarded=1.0 if q_item.get("is_correct") else 0.0,
                    )

                if sheet_status == Submission.Status.COMPLETED:
                    success_count += 1
                else:
                    needs_review_count += 1
                total_scores += score_val

                processed_sheets.append({
                    "id": sub_record.id,
                    "filename": img_name,
                    "seat_number": seat_num or "—",
                    "student_name": s_name,
                    "model_code": target_version.versionCode if target_version else "A",
                    "score": score_val,
                    "max_score": total_q,
                    "percentage": round((score_val / float(max(1, total_q))) * 100, 1),
                    "confidence": avg_conf,
                    "status": sheet_status,
                    "ambiguous_count": ambiguous_c,
                })

            except Exception as e_sheet:
                logger.error(f"Error processing sheet {img_name}: {e_sheet}")
                failed_count += 1
                processed_sheets.append({
                    "id": None,
                    "filename": img_name,
                    "seat_number": "—",
                    "student_name": "خطأ في المعالجة",
                    "model_code": "—",
                    "score": 0,
                    "max_score": 0,
                    "percentage": 0,
                    "confidence": 0,
                    "status": Submission.Status.FAILED,
                    "error": str(e_sheet),
                })
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

        # تحديث كائن الدفعة
        total_p = len(extracted_images)
        batch_record.total_papers = total_p
        batch_record.processed_papers = success_count + needs_review_count
        batch_record.failed_papers = failed_count
        batch_record.status = SubmissionBatch.Status.COMPLETED if failed_count == 0 else SubmissionBatch.Status.PARTIALLY_COMPLETED
        batch_record.save()

        AuditLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action=AuditLog.ActionChoices.CREATE,
            resource_type='SubmissionBatch',
            resource_id=str(batch_record.id),
            description=f"مسح ومعالجة جماعية لدفعة أوراق OMR: {total_p} ورقة (نجاح: {success_count}، تدقيق: {needs_review_count}، فشل: {failed_count})"
        )

        return Response({
            "success": True,
            "message": f"اكتملت المعالجة الجماعية بنجاح ({batch_record.processed_papers}/{total_p} ورقة)",
            "batch_id": batch_record.id,
            "batch_name": batch_record.name,
            "total_papers": total_p,
            "completed_count": success_count,
            "needs_review_count": needs_review_count,
            "failed_count": failed_count,
            "average_score": round(total_scores / float(max(1, success_count + needs_review_count)), 2),
            "sheets": processed_sheets,
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reprocess(self, request, pk=None):
        """
        إعادة معالجة وتصحيح حقيقية للورقة عبر استدعاء محرك OMR مجدداً على الصورة الأصلية.
        """
        import os
        from omr.api import _grade_with_template
        from omr.models.OMRSheetResult import OMRSheetResult
        from omr.models.OMRQuestionResult import OMRQuestionResult

        submission = self.get_object()

        if not submission.original_image or not os.path.exists(submission.original_image.path):
            submission.status = Submission.Status.PENDING
            submission.error_message = ""
            submission.save(update_fields=['status', 'error_message'])
            return Response({
                "success": True,
                "id": submission.id,
                "status": submission.status,
                "message": "تم تحويل الورقة إلى وضع قيد الانتظار (لم يتم العثور على ملف الصورة الأصلية على القرص)"
            })

        try:
            # استخراج مفتاح الحل للاختبار
            answer_key = {}
            if submission.exam_version:
                for qo in submission.exam_version.question_orders.filter(is_deleted=False).order_by('orderIndex'):
                    opts = list(qo.question.options.filter(is_deleted=False))
                    ans_letter = 'A'
                    for idx, opt in enumerate(opts):
                        if opt.isTrue:
                            ans_letter = chr(65 + idx)
                            break
                    answer_key[qo.orderIndex] = ans_letter

            template_id = (submission.layout_result or {}).get("template_id") or "AUTO"
            grading_result = _grade_with_template(
                submission.original_image.path,
                template_id=template_id,
                answer_key=answer_key,
                dpi=300,
                original_filename=os.path.basename(submission.original_image.name)
            )

            score_val = float(grading_result.get("score", 0.0))
            total_q = grading_result.get("total_questions", 40)
            ambiguous_c = grading_result.get("ambiguous_count", 0)
            avg_conf = float(grading_result.get("overall_confidence") or 0.95)

            new_status = Submission.Status.NEEDS_REVIEW if (ambiguous_c > 0 or avg_conf < 0.82) else Submission.Status.COMPLETED

            submission.mcq_score = score_val
            submission.total_score = score_val
            submission.status = new_status
            submission.overall_confidence = avg_conf
            submission.processing_time_ms = grading_result.get("processing_ms", 0.0)
            submission.omr_result = grading_result.get("questions", [])
            submission.save()

            # تحديث OMRSheetResult
            sheet_res, _ = OMRSheetResult.objects.get_or_create(submission=submission)
            sheet_res.confidence = avg_conf
            sheet_res.total_questions = total_q
            sheet_res.answered_questions = grading_result.get("total_answered", 0)
            sheet_res.correct_answers = grading_result.get("total_correct", 0)
            sheet_res.wrong_answers = grading_result.get("total_wrong", 0)
            sheet_res.unanswered = grading_result.get("total_empty", 0)
            sheet_res.ambiguous_count = ambiguous_c
            sheet_res.mcq_score = score_val
            sheet_res.mcq_max_score = total_q
            sheet_res.save()

            # إعادة حفظ الأسئلة
            OMRQuestionResult.objects.filter(sheet_result=sheet_res).delete()
            for q_item in grading_result.get("questions", []):
                OMRQuestionResult.objects.create(
                    sheet_result=sheet_res,
                    question_number=q_item.get("question_id") or q_item.get("q") or 1,
                    marked_choice=q_item.get("marked_choice") or q_item.get("marked"),
                    correct_choice=q_item.get("correct_choice") or q_item.get("correct"),
                    is_correct=q_item.get("is_correct"),
                    bubble_state=q_item.get("bubble_state") or q_item.get("mode", "empty"),
                    choice_confidences=q_item.get("choice_confidences") or {},
                    final_confidence=q_item.get("final_confidence") or q_item.get("confidence") or 0.95,
                    marks_awarded=1.0 if q_item.get("is_correct") else 0.0,
                )

            AuditLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                action=AuditLog.ActionChoices.UPDATE,
                resource_type='Submission',
                resource_id=str(submission.id),
                description=f"إعادة تصحيح ورقة الإجابة #{submission.id}: النتيجة ({score_val}/{total_q})"
            )

            return Response({
                "success": True,
                "id": submission.id,
                "status": submission.status,
                "score": score_val,
                "max_score": total_q,
                "confidence": avg_conf,
                "message": "تمت إعادة تصحيح الورقة وتحديث الدرجات بنجاح"
            })

        except Exception as e:
            return Response({"success": False, "message": f"فشلت إعادة التصحيح: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def update_review(self, request, pk=None):
        """
        Human reviewer manual override for MCQ / Essay score.
        Body:
            mcq_score: float (optional)
            essay_score: float (optional)
            total_score: float (optional)
            status: str (default 'completed')
        """
        submission = self.get_object()
        mcq_score = request.data.get('mcq_score')
        essay_score = request.data.get('essay_score')
        new_status = request.data.get('status', Submission.Status.COMPLETED)

        with transaction.atomic():
            if mcq_score is not None:
                submission.mcq_score = mcq_score
            if essay_score is not None:
                submission.essay_score = essay_score

            # Auto calculate total if not explicitly given
            calc_mcq = float(submission.mcq_score or 0)
            calc_essay = float(submission.essay_score or 0)
            submission.total_score = request.data.get('total_score', calc_mcq + calc_essay)
            submission.status = new_status
            submission.save()

            AuditLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                action=AuditLog.ActionChoices.UPDATE,
                resource_type='Submission',
                resource_id=str(submission.id),
                description=f"مراجعة واعتماد يدوي لدرجة الورقة #{submission.id}: المجموع ({submission.total_score})"
            )

        return Response({
            "success": True,
            "id": submission.id,
            "status": submission.status,
            "total_score": submission.total_score,
            "message": "تم حفظ نتائج المراجعة البشرية بنجاح"
        })
