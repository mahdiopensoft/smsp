from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from rest_framework.response import Response
from django.db.models import Q
from bank.models.Question import Question
from bank.serializers.Question import QuestionSerializer


class RejectedQuestionsReportMVS(AllMVS):
    """
    تقرير الأسئلة المرفوضة
    Endpoint: /api/bank/rejected-questions-report/
    Used by: RejectedQuestionsReportView.vue
    """
    queryset = Question.objects.filter(is_deleted=False, status__in=['مرفوض', 'rejected']).select_related(
        'createdBy', 'reviewer', 'lesson',
        'lesson__unit', 'lesson__unit__semester_subject',
        'lesson__unit__semester_subject__fk_subject',
        'lesson__subject',
    ).order_by('-created_at')
    serializer_class = QuestionSerializer

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()

        inst_type = request.query_params.get('institution_type')
        if inst_type and inst_type != 'all':
            qs = qs.filter(institution_type=inst_type)

        subject_id = request.query_params.get('subject')
        college_id = request.query_params.get('college')
        dept_id = request.query_params.get('department')
        spec_id = request.query_params.get('specialization')
        semester_subject_id = request.query_params.get('semester_subject')
        author_id = request.query_params.get('author')
        reviewer_id = request.query_params.get('reviewer')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        if subject_id:
            qs = qs.filter(
                Q(lesson__subject_id=subject_id) |
                Q(lesson__unit__semester_subject__fk_subject_id=subject_id)
            )
        if college_id:
            qs = qs.filter(lesson__unit__semester_subject__fk_specialization__fk_college_id=college_id)
        if dept_id:
            qs = qs.filter(lesson__unit__semester_subject__fk_specialization__fk_section_id=dept_id)
        if spec_id:
            qs = qs.filter(lesson__unit__semester_subject__fk_specialization_id=spec_id)
        if semester_subject_id:
            qs = qs.filter(lesson__unit__semester_subject_id=semester_subject_id)
        if author_id:
            qs = qs.filter(createdBy_id=author_id)
        if reviewer_id:
            qs = qs.filter(reviewer_id=reviewer_id)
        if date_from:
            qs = qs.filter(created_at__date__gte=date_from)
        if date_to:
            qs = qs.filter(created_at__date__lte=date_to)

        results = []
        for q in qs[:300]:
            lesson = q.lesson
            unit_name = subject_name = lesson_name = ''
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

            results.append({
                'id': q.id,
                'contentPreview': (q.content or '')[:120],
                'subject': subject_name,
                'unit': unit_name,
                'lesson': lesson_name,
                'author': author_name,
                'reviewer': reviewer_name,
                'rejectionReason': getattr(q, 'rejectionReason', '') or getattr(q, 'notes', '') or '',
                'createdAt': q.created_at.strftime('%Y-%m-%d') if q.created_at else '',
                'rejectedAt': q.created_at.strftime('%Y-%m-%d') if q.created_at else '',
            })

        return Response({'results': results, 'count': len(results)})
