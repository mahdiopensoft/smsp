from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from django.db.models import Q
from bank.models.Question import Question
from bank.serializers.Question import QuestionSerializer
from utils.report_pagination import paginate_records, paginated_report_response


class QuestionsDetailReportMVS(AllMVS):
    """
    تقرير الأسئلة التفصيلي
    Endpoint: /api/bank/questions-detail-report/
    Used by: QuestionsDetailReportView.vue
    """
    queryset = Question.objects.filter(is_deleted=False).select_related(
        'createdBy', 'reviewer', 'lesson',
        'lesson__unit', 'lesson__unit__semester_subject',
        'lesson__unit__semester_subject__fk_subject',
        'lesson__unit__semester_subject__course',
        'lesson__unit__semester_subject__fk_specialization',
        'lesson__unit__semester_subject__fk_specialization__fk_college',
        'lesson__subject',
    ).order_by('-created_at')
    serializer_class = QuestionSerializer

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()

        inst_type = request.query_params.get('institution_type')
        if inst_type and inst_type != 'all':
            qs = qs.filter(institution_type=inst_type)

        # University Filters
        college_id = request.query_params.get('college') or request.query_params.get('fk_college')
        dept_id = request.query_params.get('department') or request.query_params.get('fk_department')
        spec_id = request.query_params.get('specialization') or request.query_params.get('fk_specialization')
        semester_subject_id = request.query_params.get('semester_subject') or request.query_params.get('fk_semester_subject')

        if college_id:
            qs = qs.filter(lesson__unit__semester_subject__fk_specialization__fk_college_id=college_id)
        if dept_id:
            qs = qs.filter(lesson__unit__semester_subject__fk_specialization__fk_section_id=dept_id)
        if spec_id:
            qs = qs.filter(lesson__unit__semester_subject__fk_specialization_id=spec_id)
        if semester_subject_id:
            qs = qs.filter(lesson__unit__semester_subject_id=semester_subject_id)

        # Institute Filters
        inst_field = request.query_params.get('field') or request.query_params.get('institute_field')
        if inst_field:
            qs = qs.filter(institution_type='institute')

        # School Filters
        stage_id = request.query_params.get('stage')
        class_track_id = request.query_params.get('class_track')

        # General Subject & Unit
        subject_id = request.query_params.get('subject') or request.query_params.get('institute_subject')
        unit_id = request.query_params.get('unit')

        if subject_id:
            qs = qs.filter(
                Q(lesson__unit__semester_subject__fk_subject_id=subject_id) |
                Q(lesson__subject_id=subject_id) |
                Q(lesson__unit__semester_subject__course_id=subject_id)
            )

        if unit_id:
            qs = qs.filter(lesson__unit_id=unit_id)

        question_type = request.query_params.get('question_type')
        difficulty = request.query_params.get('difficulty')
        bloom_level = request.query_params.get('bloom_level')
        status_filter = request.query_params.get('status')
        author_id = request.query_params.get('author')
        reviewer_id = request.query_params.get('reviewer')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        search = request.query_params.get('search')

        if question_type:
            qs = qs.filter(questionType=question_type)
        if difficulty:
            try:
                qs = qs.filter(difficulty=int(difficulty))
            except (ValueError, TypeError):
                pass
        if bloom_level:
            qs = qs.filter(bloomLevel=bloom_level)
        if status_filter:
            qs = qs.filter(status=status_filter)
        if author_id:
            qs = qs.filter(createdBy_id=author_id)
        if reviewer_id:
            qs = qs.filter(reviewer_id=reviewer_id)
        if date_from:
            qs = qs.filter(created_at__date__gte=date_from)
        if date_to:
            qs = qs.filter(created_at__date__lte=date_to)
        if search:
            qs = qs.filter(
                Q(content__icontains=search) |
                Q(description__icontains=search)
            )

        paginated_qs, pagination_meta = paginate_records(qs, request, default_size=20)

        results = []
        for q in paginated_qs:
            lesson = q.lesson
            unit_name = ''
            subject_name = ''
            lesson_name = ''
            if lesson:
                lesson_name = lesson.name_ar or lesson.name_en or f'درس #{lesson.id}'
                if lesson.unit:
                    unit_name = lesson.unit.name_ar or lesson.unit.name_en or ''
                    ss = getattr(lesson.unit, 'semester_subject', None)
                    if ss and ss.fk_subject:
                        subject_name = ss.fk_subject.name_ar or ss.fk_subject.name_en or ''
                if not subject_name and getattr(lesson, 'subject', None):
                    subject_name = lesson.subject.name_ar or lesson.subject.name_en or ''

            author_name = ''
            if q.createdBy:
                author_name = f"{q.createdBy.first_name or ''} {q.createdBy.last_name or ''}".strip() or q.createdBy.username or ''
            reviewer_name = ''
            if q.reviewer:
                reviewer_name = f"{q.reviewer.first_name or ''} {q.reviewer.last_name or ''}".strip() or q.reviewer.username or ''

            content_preview = (q.content or '')[:120]

            results.append({
                'id': q.id,
                'contentPreview': content_preview,
                'questionType': q.questionType or '',
                'difficulty': q.difficulty,
                'difficultyLabel': {1: 'سهل', 2: 'متوسط', 3: 'صعب'}.get(q.difficulty, ''),
                'bloomLevel': q.bloomLevel or '',
                'status': q.status or '',
                'institutionType': q.institution_type or '',
                'subject': subject_name,
                'unit': unit_name,
                'lesson': lesson_name,
                'author': author_name,
                'reviewer': reviewer_name,
                'defaultMark': q.defaultMark,
                'expectedTime': q.expected_time_minutes,
                'createdAt': q.created_at.strftime('%Y-%m-%d') if q.created_at else '',
                'approvedAt': q.approved_at.strftime('%Y-%m-%d') if q.approved_at else '',
            })

        return paginated_report_response(results, pagination_meta)
