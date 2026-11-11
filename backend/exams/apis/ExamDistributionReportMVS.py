from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from rest_framework.response import Response
from django.db.models import Q
from exams.models.ExamDistribution import ExamDistribution
from exams.serializers.ExamDistribution import ExamDistributionSerializer


class ExamDistributionReportMVS(AllMVS):
    """
    تقرير توزيع وإرسال الاختبارات
    Endpoint: /api/exams/exam-distribution-report/
    Used by: ExamDistributionReportView.vue
    """
    queryset = ExamDistribution.objects.filter(is_deleted=False).select_related(
        'exam', 'exam__subject', 'exam__class_track',
    ).order_by('-created_at')
    serializer_class = ExamDistributionSerializer

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()

        exam_id = request.query_params.get('exam')
        status_filter = request.query_params.get('status')
        delivery_mode = request.query_params.get('delivery_mode')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        if exam_id:
            qs = qs.filter(exam_id=exam_id)
        if status_filter:
            qs = qs.filter(status=status_filter)
        if delivery_mode:
            qs = qs.filter(delivery_mode=delivery_mode)
        if date_from:
            qs = qs.filter(dispatch_at__date__gte=date_from)
        if date_to:
            qs = qs.filter(dispatch_at__date__lte=date_to)

        results = []
        for d in qs[:200]:
            exam_title = d.exam.title if d.exam else ''
            subject_name = (d.exam.subject.name_ar or d.exam.subject.name_en) if d.exam and d.exam.subject else ''
            results.append({
                'id': d.id,
                'examTitle': exam_title,
                'subject': subject_name,
                'title': d.title or '',
                'targetLevel': d.target_level or '',
                'deliveryMode': d.delivery_mode or '',
                'status': d.status or '',
                'dispatchAt': d.dispatch_at.strftime('%Y-%m-%d %H:%M') if d.dispatch_at else '',
                'accessibleFrom': d.accessible_from.strftime('%Y-%m-%d %H:%M') if d.accessible_from else '',
                'examStartAt': d.exam_start_at.strftime('%Y-%m-%d %H:%M') if d.exam_start_at else '',
                'examEndAt': d.exam_end_at.strftime('%Y-%m-%d %H:%M') if d.exam_end_at else '',
            })

        return Response({'results': results, 'count': len(results)})

