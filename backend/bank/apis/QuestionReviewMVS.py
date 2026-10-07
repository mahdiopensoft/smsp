from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from bank.models.Question import Question
from bank.models.QuestionMetrics import QuestionMetrics
from bank.models.ReviewChecklist import ReviewChecklist
from bank.models.AuditLog import AuditLog
from bank.serializers.Question import QuestionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils import timezone

from django.db.models import Q

class QuestionReviewMVS(AllMVS):
    """
    Dedicated ModelViewSet for Question Review Queue.
    Endpoint: /api/bank/question-review/
    Used by: ReviewQueueView.vue
    """
    queryset = Question.objects.select_related(
        'lesson__unit__class_subject__subject',
        'lesson__unit__class_subject__class_track__level__stage',
        'lesson__unit__class_subject__class_track__track',
        'lesson__unit__semester_subject__fk_subject',
        'lesson__unit__semester_subject__fk_specialization__fk_college',
        'lesson__unit__semester_subject__fk_specialization__fk_section',
        'lesson__unit__semester_subject__semester',
        'createdBy',
        'reviewer'
    ).prefetch_related('options', 'review_checklists')
    serializer_class = QuestionSerializer
    filterset_fields = {
        'status': ['exact', 'in'],
        'difficulty': ['exact', 'in'],
        'questionType': ['exact', 'in'],
        'bloomLevel': ['exact', 'in'],
        'institution_type': ['exact', 'in'],
        'lesson': ['exact'],
        'lesson__unit': ['exact'],
        'lesson__unit__class_subject__subject': ['exact'],
        'lesson__unit__class_subject__class_track': ['exact'],
        'lesson__unit__class_subject__class_track__level': ['exact'],
        'lesson__unit__class_subject__class_track__track': ['exact'],
        'lesson__unit__class_subject__class_track__level__stage': ['exact'],
        'lesson__unit__semester_subject': ['exact'],
        'lesson__unit__semester_subject__fk_subject': ['exact'],
        'lesson__unit__semester_subject__fk_specialization': ['exact'],
        'lesson__unit__semester_subject__fk_specialization__fk_college': ['exact'],
        'lesson__unit__semester_subject__fk_specialization__fk_section': ['exact'],
        'lesson__subject': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        # 1. Institution Type Filter
        inst_type = params.get('institution_type')
        if inst_type and inst_type != 'all':
            qs = qs.filter(institution_type=inst_type)

        # 2. University Filters
        college = params.get('college') or params.get('fk_college')
        if college:
            qs = qs.filter(
                Q(lesson__unit__semester_subject__fk_specialization__fk_college_id=college)
            )

        department = params.get('department') or params.get('fk_department') or params.get('section')
        if department:
            qs = qs.filter(
                Q(lesson__unit__semester_subject__fk_specialization__fk_section_id=department)
            )

        specialization = params.get('specialization') or params.get('fk_specialization')
        if specialization:
            qs = qs.filter(
                Q(lesson__unit__semester_subject__fk_specialization_id=specialization)
            )

        semester_subject = params.get('semester_subject') or params.get('fk_semester_subject')
        if semester_subject:
            qs = qs.filter(lesson__unit__semester_subject_id=semester_subject)

        # 3. School Filters
        stage = params.get('stage')
        if stage:
            qs = qs.filter(lesson__unit__class_subject__class_track__level__stage_id=stage)

        class_track = params.get('class_track')
        if class_track:
            qs = qs.filter(lesson__unit__class_subject__class_track_id=class_track)

        # 4. Institute Filters
        inst_field = params.get('field') or params.get('institute_field')
        if inst_field:
            qs = qs.filter(institution_type='institute')

        # 5. Unified Subject & Unit Filters
        subject = params.get('subject') or params.get('institute_subject')
        if subject:
            qs = qs.filter(
                Q(lesson__unit__class_subject__subject_id=subject) |
                Q(lesson__unit__semester_subject__fk_subject_id=subject) |
                Q(lesson__subject_id=subject)
            )

        unit = params.get('unit') or params.get('lesson__unit')
        if unit:
            qs = qs.filter(lesson__unit_id=unit)

        # 5. Search Filter
        search = params.get('search')
        if search:
            qs = qs.filter(
                Q(content__icontains=search) |
                Q(description__icontains=search)
            )

        return qs

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Returns statistics for the review queue cards."""
        queryset = self.get_queryset()
        return Response({
            "total": queryset.count(),
            "drafts": queryset.filter(status=Question.StatusChoices.DRAFT).count(),
            "pending": queryset.filter(status=Question.StatusChoices.PENDING).count(),
            "dept_head_review": queryset.filter(status=Question.StatusChoices.DEPT_HEAD_REVIEW).count(),
            "approved": queryset.filter(status=Question.StatusChoices.APPROVED).count(),
            "rejected": queryset.filter(status=Question.StatusChoices.REJECTED).count(),
        })

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a specific question with optional checklist logging."""
        question = self.get_object()
        checklist_data = request.data.get('checklist')
        
        with transaction.atomic():
            question.status = Question.StatusChoices.APPROVED
            question.approved_at = timezone.now()
            if request.user and request.user.is_authenticated:
                question.reviewer = request.user
            question.rejectionReason = None
            question.save(update_fields=['status', 'approved_at', 'reviewer', 'rejectionReason'])
            
            # Save checklist if provided
            if checklist_data and isinstance(checklist_data, dict):
                ReviewChecklist.objects.create(
                    question=question,
                    linguistic_check=checklist_data.get('linguistic_check', True),
                    scientific_check=checklist_data.get('scientific_check', True),
                    image_check=checklist_data.get('image_check', True),
                    answer_check=checklist_data.get('answer_check', True),
                    curriculum_check=checklist_data.get('curriculum_check', True),
                    learning_outcome_check=checklist_data.get('learning_outcome_check', True),
                    bloom_check=checklist_data.get('bloom_check', True),
                    notes=checklist_data.get('notes', ''),
                    decision='Approved',
                    reviewer=request.user if request.user.is_authenticated else None
                )

            # Audit log
            AuditLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                action=AuditLog.ActionChoices.APPROVE,
                resource_type='Question',
                resource_id=str(question.id),
                description=f"اعتماد السؤال #{question.id}"
            )

        return Response({
            "success": True, 
            "message": "تم اعتماد السؤال بنجاح", 
            "data": self.get_serializer(question).data
        })

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a specific question with a mandatory reason."""
        question = self.get_object()
        reason = request.data.get('reason') or request.data.get('rejectionReason') or ''
        
        if not reason:
            return Response({"error": "سبب الرفض إجباري لتوضيح المشكلة للمؤلف"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            question.status = Question.StatusChoices.REJECTED
            question.rejectionReason = reason
            if request.user and request.user.is_authenticated:
                question.reviewer = request.user
            question.save(update_fields=['status', 'rejectionReason', 'reviewer'])
            
            # Update metrics rejection count
            metrics, _ = QuestionMetrics.objects.get_or_create(question=question)
            metrics.rejection_count += 1
            metrics.save(update_fields=['rejection_count'])

            # Audit log
            AuditLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                action=AuditLog.ActionChoices.REJECT,
                resource_type='Question',
                resource_id=str(question.id),
                description=f"رفض السؤال #{question.id} بالسبب: {reason}"
            )

        return Response({
            "success": True, 
            "message": "تم تسجيل قرار الرفض وإعادة السؤال للمؤلف", 
            "data": self.get_serializer(question).data
        })

    @action(detail=True, methods=['post'])
    def escalate_dept_head(self, request, pk=None):
        """Escalate review to Department Head (Universities workflow)."""
        question = self.get_object()
        question.status = Question.StatusChoices.DEPT_HEAD_REVIEW
        question.save(update_fields=['status'])
        
        AuditLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action=AuditLog.ActionChoices.UPDATE,
            resource_type='Question',
            resource_id=str(question.id),
            description=f"إحالة السؤال #{question.id} لمراجعة رئيس القسم"
        )
        return Response({"success": True, "message": "تم تحويل السؤال لمراجعة رئيس القسم"})

    @action(detail=False, methods=['post'], url_path='bulk-approve')
    def bulk_approve(self, request):
        """Bulk approve multiple questions atomically."""
        question_ids = request.data.get('ids') or request.data.get('question_ids', [])
        if not question_ids:
            return Response({"success": False, "message": "يجب تحديد أسئلة للاعتماد"}, status=status.HTTP_400_BAD_REQUEST)
        
        reviewer = request.user if request.user and request.user.is_authenticated else None
        with transaction.atomic():
            updated = Question.objects.filter(id__in=question_ids).update(
                status=Question.StatusChoices.APPROVED,
                approved_at=timezone.now(),
                reviewer=reviewer,
                rejectionReason=None
            )
            AuditLog.objects.create(
                user=reviewer,
                action=AuditLog.ActionChoices.APPROVE,
                resource_type='Question',
                resource_id=f"{updated} questions",
                description=f"اعتماد جماعي لـ {updated} سؤالاً"
            )
        return Response({"success": True, "count": updated, "message": f"تم اعتماد {updated} أسئلة بنجاح"})

    @action(detail=False, methods=['post'], url_path='bulk-reject')
    def bulk_reject(self, request):
        """Bulk reject multiple questions atomically."""
        question_ids = request.data.get('ids') or request.data.get('question_ids', [])
        reason = request.data.get('reason') or request.data.get('rejectionReason') or ''
        if not question_ids:
            return Response({"success": False, "message": "يجب تحديد أسئلة للرفض"}, status=status.HTTP_400_BAD_REQUEST)
        
        reviewer = request.user if request.user and request.user.is_authenticated else None
        with transaction.atomic():
            updated = Question.objects.filter(id__in=question_ids).update(
                status=Question.StatusChoices.REJECTED,
                reviewer=reviewer,
                rejectionReason=reason
            )
            AuditLog.objects.create(
                user=reviewer,
                action=AuditLog.ActionChoices.REJECT,
                resource_type='Question',
                resource_id=f"{updated} questions",
                description=f"رفض جماعي لـ {updated} أسئلة بالسبب: {reason}"
            )
        return Response({"success": True, "count": updated, "message": f"تم رفض {updated} أسئلة"})
