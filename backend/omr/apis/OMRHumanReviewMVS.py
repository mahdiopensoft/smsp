from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.db.models import Q

from omr.models.OMRSheetResult import OMRSheetResult
from omr.models.OMRQuestionResult import OMRQuestionResult
from omr.serializers.OMRSheetResult import OMRSheetResultSerializer

class OMRHumanReviewMVS(AllMVS):
    """
    Dedicated ModelViewSet for OMR Human Review Screen.
    Endpoint: /api/omr/human-review/
    Used by: OMRHumanReviewView.vue
    """
    queryset = OMRSheetResult.objects.filter(is_deleted=False).select_related(
        'submission__exam__subject',
        'submission__registration__student',
        'submission__registration__student_profile'
    ).prefetch_related('questions')
    serializer_class = OMRSheetResultSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        inst_type = self.request.query_params.get('institution_type')
        if inst_type and inst_type != 'all':
            qs = qs.filter(submission__exam__institution_type=inst_type)

        # School Filters
        stage_id = self.request.query_params.get('stage') or self.request.query_params.get('stage_id')
        if stage_id:
            qs = qs.filter(
                Q(submission__exam__versions__question_orders__question__lesson__unit__class_subject__class_track__level__stage_id=stage_id) |
                Q(submission__exam__subject__class_subjects__class_track__level__stage_id=stage_id)
            )

        class_track_id = self.request.query_params.get('class_track') or self.request.query_params.get('class_track_id')
        if class_track_id:
            qs = qs.filter(
                Q(submission__exam__versions__question_orders__question__lesson__unit__class_subject__class_track_id=class_track_id) |
                Q(submission__exam__subject__class_subjects__class_track_id=class_track_id)
            )

        level_id = self.request.query_params.get('level') or self.request.query_params.get('level_id')
        if level_id:
            qs = qs.filter(
                Q(submission__exam__versions__question_orders__question__lesson__unit__class_subject__class_track__level_id=level_id) |
                Q(submission__exam__subject__class_subjects__class_track__level_id=level_id)
            )

        track_id = self.request.query_params.get('track') or self.request.query_params.get('track_id')
        if track_id:
            qs = qs.filter(
                Q(submission__exam__versions__question_orders__question__lesson__unit__class_subject__class_track__track_id=track_id) |
                Q(submission__exam__subject__class_subjects__class_track__track_id=track_id)
            )

        # University Filters
        college_id = self.request.query_params.get('college') or self.request.query_params.get('fk_college')
        if college_id:
            qs = qs.filter(
                Q(submission__exam__versions__question_orders__question__lesson__unit__semester_subject__fk_specialization__fk_college_id=college_id) |
                Q(submission__exam__subject__semester_subjects__fk_specialization__fk_college_id=college_id)
            )

        dept_id = self.request.query_params.get('department') or self.request.query_params.get('fk_department') or self.request.query_params.get('section')
        if dept_id:
            qs = qs.filter(
                Q(submission__exam__versions__question_orders__question__lesson__unit__semester_subject__fk_specialization__fk_section_id=dept_id) |
                Q(submission__exam__subject__semester_subjects__fk_specialization__fk_section_id=dept_id)
            )

        spec_id = self.request.query_params.get('specialization') or self.request.query_params.get('fk_specialization')
        if spec_id:
            qs = qs.filter(
                Q(submission__exam__versions__question_orders__question__lesson__unit__semester_subject__fk_specialization_id=spec_id) |
                Q(submission__exam__subject__semester_subjects__fk_specialization_id=spec_id)
            )

        sem_sub_id = self.request.query_params.get('semester_subject') or self.request.query_params.get('fk_semester_subject')
        if sem_sub_id:
            qs = qs.filter(
                Q(submission__exam__versions__question_orders__question__lesson__unit__semester_subject_id=sem_sub_id) |
                Q(submission__exam__subject__semester_subjects__id=sem_sub_id)
            )

        subject_id = self.request.query_params.get('subject') or self.request.query_params.get('subject_id')
        if subject_id:
            qs = qs.filter(
                Q(submission__exam__subject_id=subject_id) |
                Q(submission__exam__versions__question_orders__question__lesson__unit__class_subject__subject_id=subject_id) |
                Q(submission__exam__versions__question_orders__question__lesson__unit__semester_subject__fk_subject_id=subject_id)
            )

        exam_id = self.request.query_params.get('exam') or self.request.query_params.get('exam_id')
        if exam_id:
            qs = qs.filter(submission__exam_id=exam_id)

        review_status = self.request.query_params.get('status')
        if review_status:
            if review_status == 'pending':
                qs = qs.filter(Q(status='needs_review') | Q(confidence__lt=0.85) | Q(ambiguous_count__gt=0))
            elif review_status == 'verified':
                qs = qs.filter(status='verified')

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(submission__registration__seatNumber__icontains=search) |
                Q(submission__registration__student__first_name__icontains=search) |
                Q(submission__registration__student__last_name__icontains=search) |
                Q(submission__registration__student_profile__name_ar__icontains=search) |
                Q(submission__exam__title__icontains=search) |
                Q(id__icontains=search)
            )

        return qs.order_by('confidence', '-created_at').distinct()

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistics of sheets requiring human review."""
        base_qs = self.get_queryset()
        pending_review = base_qs.filter(confidence__lt=0.85).count()
        ambiguous_total = base_qs.filter(ambiguous_count__gt=0).count()
        completed = base_qs.filter(confidence__gte=0.85).count()

        return Response({
            "pendingReview": pending_review,
            "ambiguousSheets": ambiguous_total,
            "verifiedSheets": completed,
            "totalSheets": base_qs.count()
        })

    @action(detail=True, methods=['post'], url_path='approve-review')
    def approve_review(self, request, pk=None):
        """Mark sheet review as completed after human audit."""
        sheet = self.get_object()
        sheet.status = 'verified'
        sheet.confidence = max(sheet.confidence, 0.95)
        sheet.save(update_fields=['status', 'confidence'])

        return Response({
            "success": True,
            "message": "تم اعتماد مراجعة ورقة الإجابة بنجاح",
            "data": self.get_serializer(sheet).data
        })

    @action(detail=True, methods=['post'], url_path='override-question')
    def override_question(self, request, pk=None):
        """Manual human override of a specific question's detected bubble."""
        sheet = self.get_object()
        q_num = request.data.get('question_number')
        choice = request.data.get('marked_choice')

        if q_num is None or choice is None:
            return Response({"success": False, "message": "يجب تحديد رقم السؤال والخيار المعدل"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            q_res = OMRQuestionResult.objects.get(sheet_result=sheet, question_number=q_num)
            q_res.marked_choice = choice
            q_res.is_correct = (choice == q_res.correct_choice) if q_res.correct_choice else False
            q_res.bubble_state = OMRQuestionResult.BubbleState.FILLED
            q_res.final_confidence = 1.0
            q_res.save()

            # Recalculate sheet statistics
            with transaction.atomic():
                all_q = sheet.questions.all()
                sheet.correct_answers = sum(1 for q in all_q if q.is_correct)
                sheet.wrong_answers = sum(1 for q in all_q if q.is_correct is False and q.marked_choice)
                sheet.unanswered = sum(1 for q in all_q if not q.marked_choice)
                sheet.ambiguous_count = sum(1 for q in all_q if q.bubble_state == OMRQuestionResult.BubbleState.AMBIGUOUS)
                sheet.save()

            return Response({
                "success": True,
                "message": f"تم تعديل إجابة السؤال {q_num} بنجاح",
                "data": self.get_serializer(sheet).data
            })
        except OMRQuestionResult.DoesNotExist:
            return Response({"success": False, "message": "السؤال غير موجود"}, status=status.HTTP_404_NOT_FOUND)
