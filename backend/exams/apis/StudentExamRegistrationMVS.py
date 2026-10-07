from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from exams.models.StudentExamRegistration import StudentExamRegistration
from exams.serializers.StudentExamRegistration import StudentExamRegistrationSerializer
from bank.models.AuditLog import AuditLog
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.db.models import Q, Count

class StudentExamRegistrationMVS(AllMVS):
    """
    Dedicated ModelViewSet for Student Exam Registrations & Examinee Records.
    Endpoint: /api/exams/student-exam-registrations/
    Used by: StudentsView2.vue
    """
    queryset = StudentExamRegistration.objects.select_related(
        'student',
        'student_profile',
        'examVersion__exam__subject',
        'examVersion__exam__year',
        'examVersion__exam__examGenerationSetting',
        'examVersion__exam__examSchedule'
    ).all().distinct()
    serializer_class = StudentExamRegistrationSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        inst_type = self.request.query_params.get('institution_type')
        if inst_type and inst_type != 'all':
            qs = qs.filter(examVersion__exam__institution_type=inst_type)

        exam_id = self.request.query_params.get('exam') or self.request.query_params.get('exam_id')
        if exam_id:
            qs = qs.filter(examVersion__exam_id=exam_id)

        version_id = self.request.query_params.get('exam_version') or self.request.query_params.get('examVersion')
        if version_id:
            qs = qs.filter(examVersion_id=version_id)

        subject_id = self.request.query_params.get('subject') or self.request.query_params.get('subject_id')
        if subject_id:
            qs = qs.filter(
                Q(examVersion__exam__subject_id=subject_id) |
                Q(examVersion__question_orders__question__lesson__unit__class_subject__subject_id=subject_id) |
                Q(examVersion__question_orders__question__lesson__unit__semester_subject__fk_subject_id=subject_id)
            )

        # School Filters
        stage_id = self.request.query_params.get('stage') or self.request.query_params.get('stage_id')
        if stage_id:
            qs = qs.filter(
                Q(examVersion__question_orders__question__lesson__unit__class_subject__class_track__level__stage_id=stage_id) |
                Q(examVersion__exam__subject__class_subjects__class_track__level__stage_id=stage_id)
            )

        class_track_id = self.request.query_params.get('class_track') or self.request.query_params.get('class_track_id')
        if class_track_id:
            qs = qs.filter(
                Q(examVersion__question_orders__question__lesson__unit__class_subject__class_track_id=class_track_id) |
                Q(examVersion__exam__subject__class_subjects__class_track_id=class_track_id)
            )

        level_id = self.request.query_params.get('level') or self.request.query_params.get('level_id')
        if level_id:
            qs = qs.filter(
                Q(examVersion__question_orders__question__lesson__unit__class_subject__class_track__level_id=level_id) |
                Q(examVersion__exam__subject__class_subjects__class_track__level_id=level_id)
            )

        track_id = self.request.query_params.get('track') or self.request.query_params.get('track_id') or self.request.query_params.get('branch')
        if track_id:
            qs = qs.filter(
                Q(examVersion__question_orders__question__lesson__unit__class_subject__class_track__track_id=track_id) |
                Q(examVersion__exam__subject__class_subjects__class_track__track_id=track_id)
            )

        # University Filters
        college_id = self.request.query_params.get('college') or self.request.query_params.get('fk_college')
        if college_id:
            qs = qs.filter(
                Q(examVersion__question_orders__question__lesson__unit__semester_subject__fk_specialization__fk_college_id=college_id) |
                Q(examVersion__exam__subject__semester_subjects__fk_specialization__fk_college_id=college_id)
            )

        dept_id = self.request.query_params.get('department') or self.request.query_params.get('fk_department') or self.request.query_params.get('section')
        if dept_id:
            qs = qs.filter(
                Q(examVersion__question_orders__question__lesson__unit__semester_subject__fk_specialization__fk_section_id=dept_id) |
                Q(examVersion__exam__subject__semester_subjects__fk_specialization__fk_section_id=dept_id)
            )

        spec_id = self.request.query_params.get('specialization') or self.request.query_params.get('fk_specialization')
        if spec_id:
            qs = qs.filter(
                Q(examVersion__question_orders__question__lesson__unit__semester_subject__fk_specialization_id=spec_id) |
                Q(examVersion__exam__subject__semester_subjects__fk_specialization_id=spec_id)
            )

        sem_sub_id = self.request.query_params.get('semester_subject') or self.request.query_params.get('fk_semester_subject')
        if sem_sub_id:
            qs = qs.filter(
                Q(examVersion__question_orders__question__lesson__unit__semester_subject_id=sem_sub_id) |
                Q(examVersion__exam__subject__semester_subjects__id=sem_sub_id)
            )

        year_id = self.request.query_params.get('year') or self.request.query_params.get('year_id')
        if year_id:
            qs = qs.filter(examVersion__exam__year_id=year_id)

        is_present = self.request.query_params.get('is_present') or self.request.query_params.get('isPresent')
        if is_present is not None and is_present != '':
            if is_present in [True, 'true', 'True', 1, '1']:
                qs = qs.filter(isPresent=True)
            elif is_present in [False, 'false', 'False', 0, '0']:
                qs = qs.filter(isPresent=False)

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(seatNumber__icontains=search) |
                Q(secretNumber__icontains=search) |
                Q(student__first_name__icontains=search) |
                Q(student__last_name__icontains=search) |
                Q(student__username__icontains=search) |
                Q(student_profile__name_ar__icontains=search) |
                Q(student_profile__name_en__icontains=search) |
                Q(student_profile__academic_number__icontains=search) |
                Q(examVersion__exam__title__icontains=search) |
                Q(examVersion__exam__uniqueCode__icontains=search)
            )

        return qs.order_by('-id').distinct()

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Calculates examinee attendance and registration counts."""
        qs = self.get_queryset()
        aggregates = qs.aggregate(
            total=Count('id'),
            present=Count('id', filter=Q(isPresent=True)),
            absent=Count('id', filter=Q(isPresent=False))
        )
        return Response({
            "total_students": aggregates['total'] or 0,
            "present_count": aggregates['present'] or 0,
            "absent_count": aggregates['absent'] or 0
        })

    @action(detail=True, methods=['post'])
    def toggle_attendance(self, request, pk=None):
        """Toggle or update presence status of a student for an exam."""
        registration = self.get_object()
        new_status = request.data.get('is_present', not registration.isPresent)
        registration.isPresent = bool(new_status)
        registration.save(update_fields=['isPresent'])

        return Response({
            "success": True,
            "id": registration.id,
            "isPresent": registration.isPresent,
            "message": f"تم تحديث حالة حضور الطالب إلى: {'حاضر' if registration.isPresent else 'غائب'}"
        })

    @action(detail=False, methods=['post'])
    def bulk_register(self, request):
        """
        Batch register students for a specific exam version.
        Body:
            exam_version_id: int
            students: list of dicts [{'student_id': int, 'seat_number': str}]
        """
        version_id = request.data.get('exam_version_id')
        students_data = request.data.get('students', [])

        if not version_id or not students_data:
            return Response({"error": "يرجى تحديد نموذج الاختبار وبيانات الطلاب"}, status=status.HTTP_400_BAD_REQUEST)

        created_objs = []
        with transaction.atomic():
            for item in students_data:
                student_id = item.get('student_id')
                seat_number = item.get('seat_number', '')
                if student_id and seat_number:
                    obj, _ = StudentExamRegistration.objects.update_or_create(
                        student_id=student_id,
                        examVersion_id=version_id,
                        defaults={'seatNumber': seat_number}
                    )
                    created_objs.append(obj)

            AuditLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                action=AuditLog.ActionChoices.CREATE,
                resource_type='StudentExamRegistration',
                resource_id=f"{len(created_objs)} students",
                description=f"تسجيل جماعي لـ ({len(created_objs)}) طالب في نموذج الاختبار #{version_id}"
            )

        return Response({
            "success": True,
            "registered_count": len(created_objs),
            "message": f"تم تسجيل {len(created_objs)} طالب بنجاح"
        })
