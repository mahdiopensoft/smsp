from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from rest_framework.response import Response
from django.db.models import Q
from exams.models.StudentExamRegistration import StudentExamRegistration
from exams.serializers.StudentExamRegistration import StudentExamRegistrationSerializer


class StudentRegistrationsReportMVS(AllMVS):
    """
    تقرير تسجيلات الطلاب في الاختبارات
    Endpoint: /api/exams/student-registrations-report/
    Used by: StudentRegistrationsReportView.vue
    """
    queryset = StudentExamRegistration.objects.filter(is_deleted=False).select_related(
        'student', 'student_profile',
        'examVersion', 'examVersion__exam', 'examVersion__exam__subject',
    ).order_by('-created_at')
    serializer_class = StudentExamRegistrationSerializer

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()

        exam_id = request.query_params.get('exam')
        version_id = request.query_params.get('version')
        is_present = request.query_params.get('is_present')
        is_printed = request.query_params.get('is_printed')
        search = request.query_params.get('search')

        if exam_id:
            qs = qs.filter(examVersion__exam_id=exam_id)
        if version_id:
            qs = qs.filter(examVersion_id=version_id)
        if is_present is not None and is_present != '':
            qs = qs.filter(isPresent=(is_present in ['true', 'True', '1', True]))
        if is_printed is not None and is_printed != '':
            qs = qs.filter(is_printed=(is_printed in ['true', 'True', '1', True]))
        if search:
            qs = qs.filter(
                Q(seatNumber__icontains=search) |
                Q(secretNumber__icontains=search) |
                Q(student__first_name__icontains=search) |
                Q(student__last_name__icontains=search) |
                Q(student_profile__name_ar__icontains=search) |
                Q(student_profile__academic_number__icontains=search)
            )

        results = []
        for reg in qs[:300]:
            student_name = ''
            academic_number = ''
            if reg.student_profile:
                student_name = reg.student_profile.name_ar or reg.student_profile.name_en or ''
                academic_number = getattr(reg.student_profile, 'academic_number', '') or ''
            elif reg.student:
                student_name = f"{reg.student.first_name or ''} {reg.student.last_name or ''}".strip() or reg.student.username or ''

            exam_title = ''
            version_code = ''
            subject_name = ''
            if reg.examVersion:
                version_code = reg.examVersion.versionCode or ''
                if reg.examVersion.exam:
                    exam_title = reg.examVersion.exam.title or ''
                    if reg.examVersion.exam.subject:
                        subject_name = reg.examVersion.exam.subject.name_ar or ''

            results.append({
                'id': reg.id,
                'studentName': student_name,
                'academicNumber': academic_number,
                'seatNumber': reg.seatNumber or '',
                'secretNumber': reg.secretNumber or '',
                'examTitle': exam_title,
                'versionCode': version_code,
                'subject': subject_name,
                'isPresent': reg.isPresent,
                'isPrinted': reg.is_printed,
                'printedAt': reg.printed_at.strftime('%Y-%m-%d %H:%M') if reg.printed_at else '',
            })

        return Response({'results': results, 'count': len(results)})

