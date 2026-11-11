from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from rest_framework.response import Response
from django.db.models import Count, Q
from exams.models.Exam import Exam
from exams.serializers.Exam import ExamSerializer


class ExamsGeneratedReportMVS(AllMVS):
    """
    تقرير الاختبارات المولدة
    Endpoint: /api/exams/exams-generated-report/
    Used by: ExamsGeneratedReportView.vue
    """
    queryset = Exam.objects.filter(is_deleted=False).select_related(
        'subject', 'class_track', 'governorate', 'directorate',
        'approved_by', 'year',
    ).prefetch_related('versions').order_by('-created_at')
    serializer_class = ExamSerializer

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()

        inst_type = request.query_params.get('institution_type')
        if inst_type and inst_type != 'all':
            qs = qs.filter(institution_type=inst_type)

        year_id = request.query_params.get('year')
        stage_id = request.query_params.get('stage')
        class_track_id = request.query_params.get('class_track')
        subject_id = request.query_params.get('subject')
        is_approved = request.query_params.get('is_approved')
        governorate_id = request.query_params.get('governorate')
        directorate_id = request.query_params.get('directorate')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        if year_id:
            qs = qs.filter(year_id=year_id)
        if stage_id:
            qs = qs.filter(class_track__level__stage_id=stage_id)
        if class_track_id:
            qs = qs.filter(class_track_id=class_track_id)
        if subject_id:
            qs = qs.filter(subject_id=subject_id)
        if is_approved is not None and is_approved != '':
            qs = qs.filter(is_approved=(is_approved in ['true', 'True', '1', True]))
        if governorate_id:
            qs = qs.filter(governorate_id=governorate_id)
        if directorate_id:
            qs = qs.filter(directorate_id=directorate_id)
        if date_from:
            qs = qs.filter(created_at__date__gte=date_from)
        if date_to:
            qs = qs.filter(created_at__date__lte=date_to)

        results = []
        for exam in qs[:200]:
            versions_count = exam.versions.count() if hasattr(exam, 'versions') else 0
            subject_name = ''
            if exam.subject:
                subject_name = exam.subject.name_ar or exam.subject.name_en or ''
            class_track_name = ''
            if exam.class_track:
                class_track_name = exam.class_track.name_ar or exam.class_track.name_en or ''
            year_name = ''
            if exam.year:
                year_name = getattr(exam.year, 'name', '') or getattr(exam.year, 'name_ar', '') or str(exam.year)
            approved_by_name = ''
            if exam.approved_by:
                approved_by_name = f"{exam.approved_by.first_name or ''} {exam.approved_by.last_name or ''}".strip() or exam.approved_by.username or ''

            total_questions = 0
            first_version = exam.versions.first() if hasattr(exam, 'versions') else None
            if first_version:
                total_questions = first_version.question_orders.count() if hasattr(first_version, 'question_orders') else 0

            results.append({
                'id': exam.id,
                'title': exam.title or '',
                'uniqueCode': exam.uniqueCode or '',
                'subject': subject_name,
                'classTrack': class_track_name,
                'year': year_name,
                'versionsCount': versions_count,
                'totalQuestions': total_questions,
                'totalMarks': exam.total_marks or 0,
                'isApproved': exam.is_approved,
                'approvedBy': approved_by_name,
                'approvedAt': exam.approved_at.strftime('%Y-%m-%d') if exam.approved_at else '',
                'institutionType': exam.institution_type or '',
                'createdAt': exam.created_at.strftime('%Y-%m-%d') if exam.created_at else '',
            })

        return Response({'results': results, 'count': len(results)})

