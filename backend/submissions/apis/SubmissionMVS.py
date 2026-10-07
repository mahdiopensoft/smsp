from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from submissions.models.Submission import Submission
from submissions.serializers.Submission import SubmissionSerializer
from bank.models.AuditLog import AuditLog
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.db.models import Q, Count, Avg

class SubmissionMVS(AllMVS):
    """
    Dedicated ModelViewSet for OMR Submissions & Processed Answer Sheets.
    Endpoint: /api/submissions/submissions/
    Used by: OMRSubmissionsView.vue
    """
    queryset = Submission.objects.select_related(
        'batch',
        'exam__subject',
        'exam_version',
        'registration__student',
        'registration__student_profile'
    ).all().distinct()
    serializer_class = SubmissionSerializer
    filterset_fields = {
        'status': ['exact'],
        'batch': ['exact'],
        'exam': ['exact'],
        'exam_version': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        inst_type = self.request.query_params.get('institution_type')
        if inst_type and inst_type != 'all':
            qs = qs.filter(exam__institution_type=inst_type)

        exam_id = self.request.query_params.get('exam') or self.request.query_params.get('exam_id')
        if exam_id:
            qs = qs.filter(exam_id=exam_id)

        version_id = self.request.query_params.get('exam_version') or self.request.query_params.get('examVersion')
        if version_id:
            qs = qs.filter(exam_version_id=version_id)

        subject_id = self.request.query_params.get('subject') or self.request.query_params.get('subject_id')
        if subject_id:
            qs = qs.filter(
                Q(exam__subject_id=subject_id) |
                Q(exam__versions__question_orders__question__lesson__unit__class_subject__subject_id=subject_id) |
                Q(exam__versions__question_orders__question__lesson__unit__semester_subject__fk_subject_id=subject_id)
            )

        # School Filters
        stage_id = self.request.query_params.get('stage') or self.request.query_params.get('stage_id')
        if stage_id:
            qs = qs.filter(
                Q(exam__versions__question_orders__question__lesson__unit__class_subject__class_track__level__stage_id=stage_id) |
                Q(exam__subject__class_subjects__class_track__level__stage_id=stage_id)
            )

        class_track_id = self.request.query_params.get('class_track') or self.request.query_params.get('class_track_id')
        if class_track_id:
            qs = qs.filter(
                Q(exam__versions__question_orders__question__lesson__unit__class_subject__class_track_id=class_track_id) |
                Q(exam__subject__class_subjects__class_track_id=class_track_id)
            )

        level_id = self.request.query_params.get('level') or self.request.query_params.get('level_id')
        if level_id:
            qs = qs.filter(
                Q(exam__versions__question_orders__question__lesson__unit__class_subject__class_track__level_id=level_id) |
                Q(exam__subject__class_subjects__class_track__level_id=level_id)
            )

        track_id = self.request.query_params.get('track') or self.request.query_params.get('track_id') or self.request.query_params.get('branch')
        if track_id:
            qs = qs.filter(
                Q(exam__versions__question_orders__question__lesson__unit__class_subject__class_track__track_id=track_id) |
                Q(exam__subject__class_subjects__class_track__track_id=track_id)
            )

        # University Filters
        college_id = self.request.query_params.get('college') or self.request.query_params.get('fk_college')
        if college_id:
            qs = qs.filter(
                Q(exam__versions__question_orders__question__lesson__unit__semester_subject__fk_specialization__fk_college_id=college_id) |
                Q(exam__subject__semester_subjects__fk_specialization__fk_college_id=college_id)
            )

        dept_id = self.request.query_params.get('department') or self.request.query_params.get('fk_department') or self.request.query_params.get('section')
        if dept_id:
            qs = qs.filter(
                Q(exam__versions__question_orders__question__lesson__unit__semester_subject__fk_specialization__fk_section_id=dept_id) |
                Q(exam__subject__semester_subjects__fk_specialization__fk_section_id=dept_id)
            )

        spec_id = self.request.query_params.get('specialization') or self.request.query_params.get('fk_specialization')
        if spec_id:
            qs = qs.filter(
                Q(exam__versions__question_orders__question__lesson__unit__semester_subject__fk_specialization_id=spec_id) |
                Q(exam__subject__semester_subjects__fk_specialization_id=spec_id)
            )

        sem_sub_id = self.request.query_params.get('semester_subject') or self.request.query_params.get('fk_semester_subject')
        if sem_sub_id:
            qs = qs.filter(
                Q(exam__versions__question_orders__question__lesson__unit__semester_subject_id=sem_sub_id) |
                Q(exam__subject__semester_subjects__id=sem_sub_id)
            )

        submission_status = self.request.query_params.get('status')
        if submission_status:
            qs = qs.filter(status=submission_status)

        batch_id = self.request.query_params.get('batch') or self.request.query_params.get('batch_id')
        if batch_id:
            qs = qs.filter(batch_id=batch_id)

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(registration__seatNumber__icontains=search) |
                Q(registration__student__first_name__icontains=search) |
                Q(registration__student__last_name__icontains=search) |
                Q(registration__student__username__icontains=search) |
                Q(registration__student_profile__name_ar__icontains=search) |
                Q(registration__student_profile__academic_number__icontains=search) |
                Q(exam__title__icontains=search) |
                Q(exam__uniqueCode__icontains=search)
            )

        return qs.order_by('-id').distinct()

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Calculates aggregate OMR processing statistics directly in database."""
        qs = self.get_queryset()
        aggregates = qs.aggregate(
            total=Count('id'),
            completed=Count('id', filter=Q(status=Submission.Status.COMPLETED)),
            needs_review=Count('id', filter=Q(status=Submission.Status.NEEDS_REVIEW)),
            failed=Count('id', filter=Q(status=Submission.Status.FAILED)),
            pending=Count('id', filter=Q(status__in=[Submission.Status.PENDING, Submission.Status.ALIGNING, Submission.Status.OMR_PROCESSING])),
            avg_score=Avg('total_score', filter=Q(status=Submission.Status.COMPLETED))
        )
        return Response({
            "total": aggregates['total'] or 0,
            "completed": aggregates['completed'] or 0,
            "needs_review": aggregates['needs_review'] or 0,
            "failed": aggregates['failed'] or 0,
            "pending": aggregates['pending'] or 0,
            "average_score": round(float(aggregates['avg_score'] or 0), 2)
        })

    @action(detail=True, methods=['post'])
    def reprocess(self, request, pk=None):
        """Trigger reprocessing of an individual submission through the OMR pipeline."""
        submission = self.get_object()
        submission.status = Submission.Status.PENDING
        submission.error_message = ""
        submission.save(update_fields=['status', 'error_message'])

        AuditLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action=AuditLog.ActionChoices.UPDATE,
            resource_type='Submission',
            resource_id=str(submission.id),
            description=f"طلب إعادة معالجة ورقة الإجابة #{submission.id}"
        )

        return Response({
            "success": True,
            "id": submission.id,
            "status": submission.status,
            "message": "تمت جدولة إعادة معالجة الورقة بنجاح"
        })

    @action(detail=True, methods=['post'])
    def update_review(self, request, pk=None):
        """
        Human reviewer manual override for MCQ / Essay score.
        Body:
            mcq_score: float (optional)
            essay_score: float (optional)
            total_score: float (optional)
            status: str (default 'completed')
        """
        submission = self.get_object()
        mcq_score = request.data.get('mcq_score')
        essay_score = request.data.get('essay_score')
        new_status = request.data.get('status', Submission.Status.COMPLETED)

        with transaction.atomic():
            if mcq_score is not None:
                submission.mcq_score = mcq_score
            if essay_score is not None:
                submission.essay_score = essay_score

            # Auto calculate total if not explicitly given
            calc_mcq = float(submission.mcq_score or 0)
            calc_essay = float(submission.essay_score or 0)
            submission.total_score = request.data.get('total_score', calc_mcq + calc_essay)
            submission.status = new_status
            submission.save()

            AuditLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                action=AuditLog.ActionChoices.UPDATE,
                resource_type='Submission',
                resource_id=str(submission.id),
                description=f"مراجعة واعتماد يدوي لدرجة الورقة #{submission.id}: المجموع ({submission.total_score})"
            )

        return Response({
            "success": True,
            "id": submission.id,
            "status": submission.status,
            "total_score": submission.total_score,
            "message": "تم حفظ نتائج المراجعة البشرية بنجاح"
        })
