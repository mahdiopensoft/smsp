from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Count, Q

from exams.models.Exam import Exam
from exams.models.StudentExamRegistration import StudentExamRegistration
from submissions.models.Submission import Submission

class OMRVerificationMVS(ViewSet):
    """
    ViewSet for comparing Printed sheets vs Scanned submissions (Verification).
    Endpoint: /api/omr/verification/
    """
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        """
        List exams with verification statistics.
        """
        search = request.query_params.get('search', '').strip()

        institution_type = request.query_params.get('institution_type')
        subject_id = request.query_params.get('subject')

        qs = Exam.objects.filter(is_deleted=False).order_by('-created_at')
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(uniqueCode__icontains=search))
        if institution_type and institution_type != 'all':
            qs = qs.filter(institution_type=institution_type)
        if subject_id:
            qs = qs.filter(subject_id=subject_id)

        # School Filters
        stage_id = request.query_params.get('stage')
        if stage_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__class_subject__class_track__level__stage_id=stage_id) |
                Q(subject__class_subjects__class_track__level__stage_id=stage_id)
            )

        class_track_id = request.query_params.get('class_track')
        if class_track_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__class_subject__class_track_id=class_track_id) |
                Q(subject__class_subjects__class_track_id=class_track_id) |
                Q(class_track_id=class_track_id)
            )

        # University Filters
        college_id = request.query_params.get('college')
        if college_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__semester_subject__fk_specialization__fk_college_id=college_id) |
                Q(subject__semester_subjects__fk_specialization__fk_college_id=college_id)
            )

        dept_id = request.query_params.get('department')
        if dept_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__semester_subject__fk_specialization__fk_section_id=dept_id) |
                Q(subject__semester_subjects__fk_specialization__fk_section_id=dept_id)
            )

        spec_id = request.query_params.get('specialization')
        if spec_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__semester_subject__fk_specialization_id=spec_id) |
                Q(subject__semester_subjects__fk_specialization_id=spec_id)
            )

        sem_sub_id = request.query_params.get('semester_subject')
        if sem_sub_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__semester_subject_id=sem_sub_id) |
                Q(subject__semester_subjects__id=sem_sub_id)
            )

        # Institute Filters
        inst_field_id = request.query_params.get('institute_field')
        if inst_field_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__institute_subject__field_id=inst_field_id) |
                Q(subject__institute_subjects__field_id=inst_field_id)
            )

        inst_system_id = request.query_params.get('institute_education_system')
        if inst_system_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__institute_subject__specialization__education_system_id=inst_system_id) |
                Q(subject__institute_subjects__specialization__education_system_id=inst_system_id)
            )

        inst_spec_id = request.query_params.get('institute_specialization')
        if inst_spec_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__institute_subject__specialization_id=inst_spec_id) |
                Q(subject__institute_subjects__specialization_id=inst_spec_id)
            )

        inst_sub_id = request.query_params.get('institute_subject')
        if inst_sub_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__institute_subject_id=inst_sub_id) |
                Q(subject__institute_subjects__id=inst_sub_id)
            )

        results = []
        for exam in qs[:50]:
            # Count printed
            total_registered = StudentExamRegistration.objects.filter(examVersion__exam=exam, is_deleted=False).count()
            total_printed = StudentExamRegistration.objects.filter(examVersion__exam=exam, is_deleted=False, is_printed=True).count()
            
            # Count scanned (submissions)
            total_scanned = Submission.objects.filter(exam=exam, is_deleted=False).count()

            # Missing are those printed but not scanned
            # We can find the exact students later, but for the summary, it's approximately:
            missing_approx = total_printed - total_scanned
            if missing_approx < 0: missing_approx = 0

            # Show exams that have registered students, printing, or scanning activity
            if total_registered > 0 or total_printed > 0 or total_scanned > 0:
                verif_status = "مكتمل" if (total_scanned >= total_registered and total_registered > 0) else ("بانتظار المسح" if total_printed > 0 else "بانتظار الطباعة")
                results.append({
                    "id": exam.id,
                    "title": exam.title,
                    "uniqueCode": exam.uniqueCode,
                    "total_registered": total_registered,
                    "total_printed": total_printed,
                    "total_scanned": total_scanned,
                    "missing_count": max(0, total_printed - total_scanned),
                    "status": verif_status,
                    "created_at": exam.created_at.strftime("%Y-%m-%d %H:%M") if exam.created_at else ""
                })

        return Response({
            "success": True,
            "count": len(results),
            "results": results
        })

    def retrieve(self, request, pk=None):
        """
        Retrieve exact missing students for a specific exam.
        pk = exam_id
        """
        try:
            exam = Exam.objects.get(pk=pk, is_deleted=False)
        except Exam.DoesNotExist:
            return Response({"success": False, "message": "الاختبار غير موجود"}, status=404)

        # Get all registrations
        regs = StudentExamRegistration.objects.filter(
            examVersion__exam=exam, 
            is_deleted=False
        ).select_related('student_profile', 'examVersion')

        # Get all submissions for this exam
        subs = Submission.objects.filter(
            exam=exam, 
            is_deleted=False
        ).values_list('registration_id', flat=True)

        scanned_reg_ids = set(subs)

        students_list = []
        for reg in regs:
            has_scanned = reg.id in scanned_reg_ids
            status = "تم المسح" if has_scanned else ("مفقودة" if reg.is_printed else "لم تطبع ولم تمسح")
            if reg.student_profile and reg.student_profile.name_ar:
                s_name = reg.student_profile.name_ar
            elif reg.student:
                st = reg.student
                s_name = getattr(st, 'get_full_name', lambda: '')() or f"{st.first_name or ''} {st.last_name or ''}".strip() or st.username
            else:
                s_name = f"طالب ({reg.seatNumber})"

            students_list.append({
                "id": reg.id,
                "student_name": s_name,
                "seat_number": reg.seatNumber,
                "model_code": reg.examVersion.versionCode,
                "is_printed": reg.is_printed,
                "has_scanned": has_scanned,
                "status": status
            })

        return Response({
            "success": True,
            "exam_id": exam.id,
            "exam_title": exam.title,
            "students": students_list
        })
