from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from rest_framework.response import Response
from django.db.models import Q
from omr.models.OMRQuestionResult import OMRQuestionResult
from omr.serializers.OMRQuestionResult import OMRQuestionResultSerializer


class OMRReviewQuestionsReportMVS(AllMVS):
    """
    تقرير الأسئلة التي تحتاج مراجعة (OMR)
    Endpoint: /api/omr/omr-review-questions-report/
    Used by: OMRReviewQuestionsReportView.vue
    """
    queryset = OMRQuestionResult.objects.filter(
        is_deleted=False
    ).filter(
        Q(needs_review=True) | Q(is_manually_overridden=True) | Q(bubble_state__in=['ambiguous', 'multiple', 'empty'])
    ).select_related(
        'sheet_result',
        'sheet_result__submission',
        'sheet_result__submission__exam',
        'sheet_result__submission__exam_version',
        'sheet_result__submission__registration',
        'sheet_result__submission__registration__student_profile',
    ).order_by('-review_priority')
    serializer_class = OMRQuestionResultSerializer

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()

        exam_id = request.query_params.get('exam')
        version_id = request.query_params.get('version')
        review_priority = request.query_params.get('review_priority')
        is_manually_overridden = request.query_params.get('is_manually_overridden')
        bubble_state = request.query_params.get('bubble_state')

        if exam_id:
            qs = qs.filter(sheet_result__submission__exam_id=exam_id)
        if version_id:
            qs = qs.filter(sheet_result__submission__exam_version_id=version_id)
        if review_priority:
            qs = qs.filter(review_priority=review_priority)
        if is_manually_overridden is not None and is_manually_overridden != '':
            qs = qs.filter(is_manually_overridden=(is_manually_overridden in ['true', 'True', '1', True]))
        if bubble_state:
            qs = qs.filter(bubble_state=bubble_state)

        results = []
        for r in qs[:300]:
            student_name = ''
            exam_title = ''
            if r.sheet_result and r.sheet_result.submission:
                sub = r.sheet_result.submission
                if sub.exam:
                    exam_title = sub.exam.title or ''
                if sub.registration and sub.registration.student_profile:
                    student_name = sub.registration.student_profile.name_ar or sub.registration.student_profile.name_en or ''

            results.append({
                'id': r.id,
                'studentName': student_name,
                'examTitle': exam_title,
                'questionNumber': r.question_number or 0,
                'markedChoice': r.marked_choice or '',
                'correctChoice': r.correct_choice or '',
                'isCorrect': r.is_correct,
                'bubbleState': r.bubble_state or '',
                'needsReview': r.needs_review,
                'reviewPriority': r.review_priority or 'NONE',
                'isManuallyOverridden': r.is_manually_overridden,
            })

        return Response({'results': results, 'count': len(results)})

