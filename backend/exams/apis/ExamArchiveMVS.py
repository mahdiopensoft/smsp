from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q

from exams.models.Exam import Exam
from exams.models.ExamVersion import ExamVersion
from exams.models.StudentExamRegistration import StudentExamRegistration
from exams.serializers.Exam import ExamSerializer

class ExamArchiveMVS(AllMVS):
    """
    Dedicated ModelViewSet for Archived Exams View.
    Endpoint: /api/exams/exam-archive/
    Used by: ExamArchiveView.vue
    """
    queryset = Exam.objects.select_related(
        'subject', 
        'year', 
        'examSchedule',
        'examGenerationSetting'
    ).prefetch_related(
        'versions__question_orders'
    ).annotate(
        annotated_students_count=Count('versions__registered_students', filter=Q(versions__registered_students__is_deleted=False), distinct=True),
        annotated_versions_count=Count('versions', filter=Q(versions__is_deleted=False), distinct=True)
    ).distinct().order_by('-created_at')
    
    serializer_class = ExamSerializer
    filterset_fields = {
        'subject': ['exact'],
        'year': ['exact'],
        'institution_type': ['exact'],
        'examSchedule': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        inst_type = self.request.query_params.get('institution_type')
        if inst_type and inst_type != 'all':
            qs = qs.filter(institution_type=inst_type)

        subject_id = self.request.query_params.get('subject') or self.request.query_params.get('subject_id') or self.request.query_params.get('institute_subject')
        if subject_id:
            qs = qs.filter(
                Q(subject_id=subject_id) |
                Q(versions__question_orders__question__lesson__unit__class_subject__subject_id=subject_id) |
                Q(versions__question_orders__question__lesson__unit__semester_subject__fk_subject_id=subject_id) |
                Q(versions__question_orders__question__lesson__subject_id=subject_id)
            )

        # University Filters
        college_id = self.request.query_params.get('college') or self.request.query_params.get('fk_college')
        if college_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__semester_subject__fk_specialization__fk_college_id=college_id) |
                Q(subject__semester_subjects__fk_specialization__fk_college_id=college_id)
            )

        dept_id = self.request.query_params.get('department') or self.request.query_params.get('fk_department') or self.request.query_params.get('section')
        if dept_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__semester_subject__fk_specialization__fk_section_id=dept_id) |
                Q(subject__semester_subjects__fk_specialization__fk_section_id=dept_id)
            )

        spec_id = self.request.query_params.get('specialization') or self.request.query_params.get('fk_specialization')
        if spec_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__semester_subject__fk_specialization_id=spec_id) |
                Q(subject__semester_subjects__fk_specialization_id=spec_id)
            )

        sem_sub_id = self.request.query_params.get('semester_subject') or self.request.query_params.get('fk_semester_subject')
        if sem_sub_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__semester_subject_id=sem_sub_id) |
                Q(subject__semester_subjects__id=sem_sub_id)
            )

        # School Filters
        stage_id = self.request.query_params.get('stage') or self.request.query_params.get('stage_id')
        if stage_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__class_subject__class_track__level__stage_id=stage_id) |
                Q(subject__class_subjects__class_track__level__stage_id=stage_id)
            )

        class_track_id = self.request.query_params.get('class_track') or self.request.query_params.get('class_track_id')
        if class_track_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__class_subject__class_track_id=class_track_id) |
                Q(subject__class_subjects__class_track_id=class_track_id)
            )

        year_id = self.request.query_params.get('year') or self.request.query_params.get('year_id')
        if year_id:
            qs = qs.filter(year_id=year_id)

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(uniqueCode__icontains=search) |
                Q(subject__name_ar__icontains=search)
            )

        return qs.order_by('-created_at').distinct()

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Returns statistics for Exam Archive cards."""
        total_exams = Exam.objects.filter(is_deleted=False).count()
        total_models = ExamVersion.objects.filter(is_deleted=False).count()
        total_students = StudentExamRegistration.objects.filter(is_deleted=False).count()

        return Response({
            "totalExams": total_exams,
            "totalModels": total_models,
            "registeredStudents": total_students,
        })

    @action(detail=True, methods=['get'])
    def dashboard(self, request, pk=None):
        """
        Returns full detailed dashboard payload for a specific archived exam.
        """
        try:
            exam = Exam.objects.select_related('subject', 'year').get(pk=pk, is_deleted=False)
        except Exam.DoesNotExist:
            return Response({"success": False, "message": "الاختبار غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        versions = ExamVersion.objects.filter(exam=exam, is_deleted=False).order_by('versionCode')
        versions_list = [{"id": v.id, "versionCode": v.versionCode} for v in versions]

        first_v = versions.first()
        questions_count = first_v.question_orders.filter(is_deleted=False).count() if first_v else 0
        students_count = StudentExamRegistration.objects.filter(examVersion__exam=exam, is_deleted=False).count()

        return Response({
            "id": exam.id,
            "title": exam.title,
            "uniqueCode": exam.uniqueCode,
            "subjectName": exam.subject.name_ar if exam.subject else 'عام',
            "yearName": str(exam.year) if exam.year else '-',
            "createdAt": exam.created_at.strftime('%Y-%m-%d') if exam.created_at else '',
            "versionsCount": len(versions_list),
            "versionsList": versions_list,
            "questionsCount": questions_count,
            "studentsCount": students_count,
        })
