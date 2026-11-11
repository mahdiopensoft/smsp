from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from rest_framework.response import Response
from django.db.models import Q
from omr.models.OMRSheetResult import OMRSheetResult
from omr.serializers.OMRSheetResult import OMRSheetResultSerializer


class OMRResultsReportMVS(AllMVS):
    """
    تقرير نتائج التصحيح الآلي (OMR)
    Endpoint: /api/omr/omr-results-report/
    Used by: OMRResultsReportView.vue
    """
    queryset = OMRSheetResult.objects.filter(is_deleted=False).select_related(
        'submission',
        'submission__exam',
        'submission__exam_version',
        'submission__registration',
        'submission__registration__student_profile',
        'submission__registration__student',
    ).order_by('-created_at')
    serializer_class = OMRSheetResultSerializer

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()

        exam_id = request.query_params.get('exam')
        version_id = request.query_params.get('version')
        status_filter = request.query_params.get('status')
        confidence_min = request.query_params.get('confidence_min')

        if exam_id:
            qs = qs.filter(submission__exam_id=exam_id)
        if version_id:
            qs = qs.filter(submission__exam_version_id=version_id)
        if status_filter:
            qs = qs.filter(status=status_filter)
        if confidence_min:
            try:
                qs = qs.filter(confidence__gte=float(confidence_min))
            except (ValueError, TypeError):
                pass

        results = []
        for r in qs[:300]:
            student_name = ''
            exam_title = ''
            version_code = ''
            if r.submission:
                if r.submission.exam:
                    exam_title = r.submission.exam.title or ''
                if r.submission.exam_version:
                    version_code = r.submission.exam_version.versionCode or ''
                if r.submission.registration:
                    reg = r.submission.registration
                    if reg.student_profile:
                        student_name = reg.student_profile.name_ar or reg.student_profile.name_en or ''
                    elif reg.student:
                        student_name = f"{reg.student.first_name or ''} {reg.student.last_name or ''}".strip() or reg.student.username or ''

            results.append({
                'id': r.id,
                'studentName': student_name,
                'examTitle': exam_title,
                'versionCode': version_code,
                'totalQuestions': r.total_questions or 0,
                'answeredQuestions': r.answered_questions or 0,
                'correctAnswers': r.correct_answers or 0,
                'wrongAnswers': r.wrong_answers or 0,
                'unanswered': r.unanswered or 0,
                'ambiguousCount': r.ambiguous_count or 0,
                'mcqScore': float(r.mcq_score) if r.mcq_score else 0,
                'mcqMaxScore': float(r.mcq_max_score) if r.mcq_max_score else 0,
                'confidence': round(float(r.confidence) * 100, 1) if r.confidence else 0,
                'status': r.status or '',
            })

        return Response({'results': results, 'count': len(results)})

