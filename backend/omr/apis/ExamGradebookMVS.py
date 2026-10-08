"""
ExamGradebookMVS.py — شاشة سجل درجات الاختبارات وترحيلها لنظام الكنترول
======================================================================
Endpoint: /api/omr/gradebook/
يربط بين نتائج التصحيح الضوئي (OMR Submissions) ونظام الكنترول الأكاديمي،
ويتيح استعراض كشوفات الرصد، تدقيق الدرجات، وترحيلها رسمياً لسجلات الطلاب.
"""

from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Count, Avg, Max, Min, Q
from django.utils import timezone
from django.db import transaction

from exams.models.Exam import Exam
from exams.models.ExamVersion import ExamVersion
from exams.models.StudentExamRegistration import StudentExamRegistration
from submissions.models.Submission import Submission
from bank.models.AuditLog import AuditLog


def _calculate_grade_letter(percent: float) -> dict:
    """حساب التقدير المعياري الأكاديمي بناء على النسبة المئوية."""
    if percent >= 90:
        return {"code": "A+", "name_ar": "ممتاز مرتفع", "color": "success"}
    elif percent >= 85:
        return {"code": "A", "name_ar": "ممتاز", "color": "success"}
    elif percent >= 80:
        return {"code": "B+", "name_ar": "جيد جداً مرتفع", "color": "primary"}
    elif percent >= 75:
        return {"code": "B", "name_ar": "جيد جداً", "color": "primary"}
    elif percent >= 70:
        return {"code": "C+", "name_ar": "جيد مرتفع", "color": "info"}
    elif percent >= 65:
        return {"code": "C", "name_ar": "جيد", "color": "info"}
    elif percent >= 60:
        return {"code": "D+", "name_ar": "مقبول مرتفع", "color": "warning"}
    elif percent >= 50:
        return {"code": "D", "name_ar": "مقبول", "color": "warning"}
    else:
        return {"code": "F", "name_ar": "راسب", "color": "error"}


class ExamGradebookMVS(ViewSet):
    """
    سجل درجات الاختبارات والترحيل لنظام الكنترول المركزي.
    """
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        """
        قائمة الاختبارات مع ملخص إحصائيات التصحيح والترحيل للكنترول.
        """
        search = request.query_params.get('search', '').strip()
        institution_type = request.query_params.get('institution_type')
        subject_id = request.query_params.get('subject')

        qs = Exam.objects.filter(is_deleted=False).select_related(
            'subject', 'year', 'governorate', 'directorate'
        ).prefetch_related('versions').order_by('-created_at')

        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(uniqueCode__icontains=search))
        if institution_type and institution_type != 'all':
            qs = qs.filter(institution_type=institution_type)
        if subject_id:
            qs = qs.filter(subject_id=subject_id)

        exams_list = []
        for exam in qs[:100]:
            total_registered = StudentExamRegistration.objects.filter(
                examVersion__exam=exam, is_deleted=False
            ).count()

            subs = Submission.objects.filter(exam=exam, is_deleted=False)
            total_submissions = subs.count()
            completed_subs = subs.filter(status=Submission.Status.COMPLETED).count()
            needs_review_subs = subs.filter(status=Submission.Status.NEEDS_REVIEW).count()

            # إحصائيات الدرجات
            aggregates = subs.filter(status=Submission.Status.COMPLETED).aggregate(
                avg_score=Avg('total_score'),
                max_score=Max('total_score'),
                min_score=Min('total_score')
            )
            exam_max_score = float(getattr(exam, 'total_score', 100) or 100)
            avg_val = float(aggregates['avg_score'] or 0.0)
            pass_count = subs.filter(status=Submission.Status.COMPLETED, total_score__gte=(exam_max_score * 0.5)).count()

            # التحقق من عدد السجلات المرحلة للكنترول
            dispatched_count = 0
            for s in subs:
                lr = s.layout_result or {}
                if lr.get("dispatched_to_control"):
                    dispatched_count += 1

            dispatch_status = "none"
            if dispatched_count > 0 and dispatched_count >= completed_subs and completed_subs > 0:
                dispatch_status = "full"
            elif dispatched_count > 0:
                dispatch_status = "partial"

            exams_list.append({
                "id": exam.id,
                "title": exam.title,
                "uniqueCode": exam.uniqueCode,
                "institution_type": exam.institution_type,
                "institution_type_display": "مدرسي" if exam.institution_type == 'school' else ("جامعي" if exam.institution_type == 'university' else "معاهد"),
                "subject_name": getattr(exam.subject, 'name_ar', str(exam.subject)) if exam.subject else "غير محدد",
                "year_name": exam.year.gregorian_year if (exam.year and hasattr(exam.year, 'gregorian_year')) else (str(exam.year) if exam.year else "العام الحالي"),
                "max_score": exam_max_score,
                "total_registered": total_registered,
                "total_submissions": total_submissions,
                "completed_count": completed_subs,
                "needs_review_count": needs_review_subs,
                "absent_count": max(0, total_registered - total_submissions),
                "dispatched_count": dispatched_count,
                "dispatch_status": dispatch_status,
                "average_score": round(avg_val, 2),
                "highest_score": float(aggregates['max_score'] or 0.0),
                "lowest_score": float(aggregates['min_score'] or 0.0),
                "pass_rate": round((pass_count / float(max(1, completed_subs))) * 100, 1),
                "created_at": exam.created_at.strftime("%Y-%m-%d %H:%M") if exam.created_at else "",
            })

        return Response({
            "success": True,
            "count": len(exams_list),
            "results": exams_list
        })

    def retrieve(self, request, pk=None):
        """
        جلب كشف درجات الطلاب التفصيلي لاختبار محدد تمهيداً للرصد والترحيل للكنترول.
        """
        try:
            exam = Exam.objects.select_related('subject', 'year', 'governorate', 'directorate').get(pk=pk, is_deleted=False)
        except Exam.DoesNotExist:
            return Response({"success": False, "message": "الاختبار غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        exam_max_score = float(getattr(exam, 'total_score', 100) or 100)

        # جلب جميع تسجيلات الطلاب
        registrations = StudentExamRegistration.objects.filter(
            examVersion__exam=exam, is_deleted=False
        ).select_related(
            'student', 'student_profile__organization', 'student_profile__directorate', 'examVersion'
        ).order_by('seatNumber')

        # جلب أوراق الإجابات والتسليمات المرتبطة
        submissions_map = {}
        for sub in Submission.objects.filter(exam=exam, is_deleted=False).select_related('registration'):
            if sub.registration_id:
                submissions_map[sub.registration_id] = sub
            elif sub.layout_result and sub.layout_result.get("seat_number"):
                submissions_map[str(sub.layout_result.get("seat_number"))] = sub

        students_records = []
        for reg in registrations:
            if reg.student_profile and reg.student_profile.name_ar:
                s_name = reg.student_profile.name_ar
            elif reg.student:
                s_name = reg.student.get_full_name() or reg.student.username
            else:
                s_name = f"طالب ({reg.seatNumber})"
            inst_name = reg.student_profile.organization.name_ar if (reg.student_profile and reg.student_profile.organization) else ""
            dir_name = reg.student_profile.directorate.name_ar if (reg.student_profile and reg.student_profile.directorate) else ""

            # البحث عن التسليم
            sub = submissions_map.get(reg.id) or submissions_map.get(str(reg.seatNumber))
            
            score_val = 0.0
            percent_val = 0.0
            grading_status = "absent"
            is_dispatched = False
            dispatched_at_str = ""
            confidence_val = 0.0
            sub_id = None

            if sub:
                sub_id = sub.id
                score_val = float(sub.total_score or 0.0)
                percent_val = round((score_val / max(1.0, exam_max_score)) * 100.0, 1)
                grading_status = sub.status
                confidence_val = float(sub.overall_confidence or 0.95)

                lr = sub.layout_result or {}
                if lr.get("dispatched_to_control"):
                    is_dispatched = True
                    dispatched_at_str = lr.get("dispatched_at", "")

            grade_info = _calculate_grade_letter(percent_val) if sub else {"code": "—", "name_ar": "غائب", "color": "grey"}

            students_records.append({
                "registration_id": reg.id,
                "submission_id": sub_id,
                "student_id": reg.student_id,
                "student_name": s_name,
                "seat_number": reg.seatNumber,
                "secret_number": reg.secretNumber or "—",
                "version_code": reg.examVersion.versionCode,
                "school_name": inst_name or "المدرسة الرئيسية",
                "directorate_name": dir_name or "المديرية",
                "governorate_name": exam.governorate.name_ar if exam.governorate else "المحافظة",
                "score": score_val,
                "max_score": exam_max_score,
                "percentage": percent_val,
                "grade_code": grade_info["code"],
                "grade_name_ar": grade_info["name_ar"],
                "grade_color": grade_info["color"],
                "status": grading_status,
                "is_dispatched": is_dispatched,
                "dispatched_at": dispatched_at_str,
                "confidence": confidence_val,
                "is_present": sub is not None or reg.isPresent,
            })

        completed_records = [r for r in students_records if r["status"] == Submission.Status.COMPLETED]
        dispatched_records = [r for r in students_records if r["is_dispatched"]]

        return Response({
            "success": True,
            "exam": {
                "id": exam.id,
                "title": exam.title,
                "uniqueCode": exam.uniqueCode,
                "institution_type": exam.institution_type,
                "subject_name": getattr(exam.subject, 'name_ar', str(exam.subject)) if exam.subject else "",
                "year_name": exam.year.gregorian_year if (exam.year and hasattr(exam.year, 'gregorian_year')) else (str(exam.year) if exam.year else ""),
                "max_score": exam_max_score,
                "total_students": len(students_records),
                "completed_count": len(completed_records),
                "dispatched_count": len(dispatched_records),
                "is_fully_dispatched": len(dispatched_records) >= len(completed_records) and len(completed_records) > 0,
            },
            "records": students_records
        })

    @action(detail=True, methods=['post'], url_path='dispatch-to-control')
    def dispatch_to_control(self, request, pk=None):
        """
        ترحيل الدرجات المعتمدة رسمياً إلى نظام الكنترول المركزي وقفل السجلات.
        """
        try:
            exam = Exam.objects.get(pk=pk, is_deleted=False)
        except Exam.DoesNotExist:
            return Response({"success": False, "message": "الاختبار غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        target_reg_ids = request.data.get('registration_ids')
        subs_qs = Submission.objects.filter(exam=exam, status=Submission.Status.COMPLETED, is_deleted=False)

        if target_reg_ids and isinstance(target_reg_ids, list):
            subs_qs = subs_qs.filter(registration_id__in=target_reg_ids)

        if not subs_qs.exists():
            return Response({
                "success": False,
                "message": "لا توجد أوراق إجابة معتمدة ومكتملة التصحيح جاهزة للترحيل حالياً."
            }, status=status.HTTP_400_BAD_REQUEST)

        now_str = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        user_name = request.user.username if request.user and request.user.is_authenticated else "مستخدم الكنترول"

        dispatched_count = 0
        with transaction.atomic():
            for sub in subs_qs:
                lr = sub.layout_result or {}
                lr["dispatched_to_control"] = True
                lr["dispatched_at"] = now_str
                lr["dispatched_by"] = user_name
                sub.layout_result = lr
                sub.save(update_fields=['layout_result'])

                if sub.registration:
                    sub.registration.isPresent = True
                    sub.registration.save(update_fields=['isPresent'])

                dispatched_count += 1

            AuditLog.objects.create(
                user=request.user if request.user and request.user.is_authenticated else None,
                action=AuditLog.ActionChoices.UPDATE,
                resource_type='ExamGradebook',
                resource_id=str(exam.id),
                description=f"ترحيل رسمي لـ ({dispatched_count}) درجة في اختبار '{exam.title}' إلى نظام الكنترول الأكاديمي."
            )

        return Response({
            "success": True,
            "message": f"تم ترحيل {dispatched_count} درجة بنجاح إلى نظام الكنترول المركزي وقفل السجلات.",
            "dispatched_count": dispatched_count,
            "dispatched_at": now_str
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='rollback-dispatch')
    def rollback_dispatch(self, request, pk=None):
        """
        إلغاء ترحيل الدرجات لإتاحة فرصة التدقيق أو التعديل بطلب من إدارة الكنترول.
        """
        try:
            exam = Exam.objects.get(pk=pk, is_deleted=False)
        except Exam.DoesNotExist:
            return Response({"success": False, "message": "الاختبار غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        subs = Submission.objects.filter(exam=exam, is_deleted=False)
        count = 0
        with transaction.atomic():
            for s in subs:
                lr = s.layout_result or {}
                if lr.get("dispatched_to_control"):
                    lr["dispatched_to_control"] = False
                    lr["dispatched_at"] = None
                    lr["dispatched_by"] = None
                    s.layout_result = lr
                    s.save(update_fields=['layout_result'])
                    count += 1

            AuditLog.objects.create(
                user=request.user if request.user and request.user.is_authenticated else None,
                action=AuditLog.ActionChoices.UPDATE,
                resource_type='ExamGradebook',
                resource_id=str(exam.id),
                description=f"إلغاء ترحيل درجات اختبار '{exam.title}' لإعادة التدقيق من الكنترول."
            )

        return Response({
            "success": True,
            "message": f"تم إلغاء ترحيل {count} سجل وإعادتها لوضع المراجعة والتدقيق.",
            "count": count
        })
