from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from django.db.models import Q
from exams.models.Exam import Exam
from exams.serializers.Exam import ExamSerializer
from utils.report_pagination import paginate_records, paginated_report_response


class ExamsGeneratedReportMVS(AllMVS):
    """
    تقرير الاختبارات المولدة
    Endpoint: /api/exams/exams-generated-report/
    Used by: ExamsGeneratedReportView.vue
    """
    queryset = Exam.objects.filter(is_deleted=False).select_related(
        'subject', 'class_track', 'year', 'governorate', 'directorate', 'approved_by',
    ).prefetch_related('versions', 'versions__question_orders').order_by('-created_at')
    serializer_class = ExamSerializer

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()

        inst_type = request.query_params.get('institution_type')
        if inst_type and inst_type != 'all':
            qs = qs.filter(institution_type=inst_type)

        year_id = request.query_params.get('year')
        subject_id = request.query_params.get('subject')
        class_track_id = request.query_params.get('class_track')
        is_approved = request.query_params.get('is_approved')
        governorate_id = request.query_params.get('governorate')
        directorate_id = request.query_params.get('directorate')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        search = request.query_params.get('search')

        if year_id:
            qs = qs.filter(year_id=year_id)
        if subject_id:
            qs = qs.filter(subject_id=subject_id)
        if class_track_id:
            qs = qs.filter(class_track_id=class_track_id)
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
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(uniqueCode__icontains=search) |
                Q(subject__name_ar__icontains=search)
            )

        paginated_qs, pagination_meta = paginate_records(qs, request, default_size=20)

        results = []
        for exam in paginated_qs:
            versions_count = exam.versions.count() if hasattr(exam, 'versions') else 0
            subject_name = ''
            if exam.subject:
                subject_name = exam.subject.name_ar or exam.subject.name_en or ''
            class_track_name = ''
            if exam.class_track:
                class_track_name = getattr(exam.class_track, 'full_name', '') or getattr(exam.class_track, 'name_ar', '') or str(exam.class_track)
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

        return paginated_report_response(results, pagination_meta)
