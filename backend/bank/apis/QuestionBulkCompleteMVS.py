from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from bank.models.Question import Question
from bank.models.AuditLog import AuditLog
from bank.serializers.Question import QuestionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.db.models import Count, Q

class QuestionBulkCompleteMVS(AllMVS):
    """
    Dedicated ModelViewSet for Two-Phase Bulk Import Data Completion Screen.
    Endpoint: /api/bank/bulk-complete/
    Used by: QuestionBulkCompleteView.vue

    Backend Responsibilities:
    1. Filter and query all questions in 'مستورد' (IMPORTED) status.
    2. Server-side calculations of data completeness metrics (Total, Missing Lesson, Ready to Activate).
    3. Atomically assign academic attributes (Lesson, Unit, Bloom, Difficulty) across batches of questions.
    4. Guard business validation: Enforce that NO imported question can be activated to 'مسودة' without a Lesson.
    5. Log all batch operations in AuditLog.
    """
    queryset = Question.objects.filter(
        status=Question.StatusChoices.IMPORTED
    ).select_related(
        'lesson__unit__class_subject__subject',
        'lesson__unit__semester_subject__fk_subject',
        'import_session',
        'createdBy'
    ).prefetch_related('options')
    serializer_class = QuestionSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        
        # Filter by Institution Type
        inst_type = self.request.query_params.get('institution_type')
        if inst_type and inst_type != 'all':
            qs = qs.filter(institution_type=inst_type)

        # Filter by Import Session
        session_id = self.request.query_params.get('import_session')
        if session_id:
            qs = qs.filter(import_session_id=session_id)

        # Filter by School Hierarchy
        stage_id = self.request.query_params.get('stage') or self.request.query_params.get('stage_id')
        if stage_id:
            qs = qs.filter(lesson__unit__class_subject__class_track__level__stage_id=stage_id)

        level_id = self.request.query_params.get('level') or self.request.query_params.get('level_id')
        if level_id:
            qs = qs.filter(lesson__unit__class_subject__class_track__level_id=level_id)

        track_id = self.request.query_params.get('track') or self.request.query_params.get('track_id')
        if track_id:
            qs = qs.filter(lesson__unit__class_subject__class_track__track_id=track_id)

        # Filter by University Hierarchy
        college_id = self.request.query_params.get('college') or self.request.query_params.get('college_id')
        if college_id:
            qs = qs.filter(lesson__unit__semester_subject__fk_specialization__fk_college_id=college_id)

        department_id = self.request.query_params.get('department') or self.request.query_params.get('department_id')
        if department_id:
            qs = qs.filter(lesson__unit__semester_subject__fk_specialization__fk_section_id=department_id)

        specialization_id = self.request.query_params.get('specialization') or self.request.query_params.get('specialization_id')
        if specialization_id:
            qs = qs.filter(lesson__unit__semester_subject__fk_specialization_id=specialization_id)

        semester_subject_id = self.request.query_params.get('semester_subject') or self.request.query_params.get('semester_subject_id')
        if semester_subject_id:
            qs = qs.filter(lesson__unit__semester_subject_id=semester_subject_id)

        # Filter by Institute Hierarchy
        field_id = self.request.query_params.get('field') or self.request.query_params.get('institute_field')
        if field_id:
            qs = qs.filter(institution_type='institute')

        # Filter by Subject (School, University, or Institute)
        subject_id = self.request.query_params.get('subject') or self.request.query_params.get('subject_id') or self.request.query_params.get('institute_subject')
        if subject_id:
            qs = qs.filter(
                Q(lesson__unit__class_subject__subject_id=subject_id) |
                Q(lesson__unit__semester_subject__fk_subject_id=subject_id) |
                Q(lesson__subject_id=subject_id)
            )

        # Filter by Unit & Lesson
        unit_id = self.request.query_params.get('unit') or self.request.query_params.get('unit_id')
        if unit_id:
            qs = qs.filter(lesson__unit_id=unit_id)

        lesson_id = self.request.query_params.get('lesson') or self.request.query_params.get('lesson_id')
        if lesson_id:
            qs = qs.filter(lesson_id=lesson_id)

        # Filter by Difficulty
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            qs = qs.filter(difficulty=difficulty)

        # Filter by Bloom Level
        bloom_level = self.request.query_params.get('bloom_level') or self.request.query_params.get('bloomLevel')
        if bloom_level:
            qs = qs.filter(bloomLevel=bloom_level)

        # Filter by Readiness Status
        readiness = self.request.query_params.get('readiness')
        if readiness == 'ready':
            qs = qs.filter(lesson__isnull=False)
        elif readiness == 'missing':
            qs = qs.filter(lesson__isnull=True)

        # Search Query
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(content__icontains=search) |
                Q(description__icontains=search) |
                Q(id__icontains=search)
            )

        return qs.order_by('-id')

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Aggregate metrics calculated directly in the database.
        Returns:
            - total_imported: Total count of imported questions.
            - missing_lessons: Count of questions missing lesson assignment.
            - ready_to_activate: Count of questions ready for draft activation.
            - bloom_breakdown: Breakdown of bloom levels.
            - difficulty_breakdown: Breakdown of difficulty levels.
        """
        base_qs = self.get_queryset()

        aggregates = base_qs.aggregate(
            total=Count('id'),
            missing_lessons=Count('id', filter=Q(lesson__isnull=True)),
            ready_to_activate=Count('id', filter=Q(lesson__isnull=False))
        )

        return Response({
            "total_imported": aggregates['total'] or 0,
            "missing_lessons": aggregates['missing_lessons'] or 0,
            "ready_to_activate": aggregates['ready_to_activate'] or 0,
        })

    @action(detail=False, methods=['get'])
    def imported_list(self, request):
        """Fetch imported questions with pagination and metadata."""
        qs = self.get_queryset()
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def bulk_assign(self, request):
        """
        Batch assign attributes to multiple questions at once.
        Body:
            question_ids: list[int]
            lesson_id: int (optional)
            bloom_level: str (optional)
            difficulty: int (optional)
            learning_outcome_id: int (optional)
        """
        question_ids = request.data.get('question_ids', [])
        if not question_ids or not isinstance(question_ids, list):
            return Response({"error": "يرجى تحديد قائمة الأسئلة المراد تعديلها"}, status=status.HTTP_400_BAD_REQUEST)

        updates = {}
        if 'institution_type' in request.data and request.data['institution_type']:
            updates['institution_type'] = request.data['institution_type']
        if 'lesson_id' in request.data and request.data['lesson_id']:
            updates['lesson_id'] = request.data['lesson_id']
        if 'bloom_level' in request.data and request.data['bloom_level']:
            updates['bloomLevel'] = request.data['bloom_level']
        if 'difficulty' in request.data and request.data['difficulty']:
            updates['difficulty'] = request.data['difficulty']
        if 'learning_outcome_id' in request.data and request.data['learning_outcome_id']:
            updates['learningOutcome_id'] = request.data['learning_outcome_id']

        if not updates:
            return Response({"error": "لم يتم تحديد أي خاصية لتطبيقها على الأسئلة"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            target_qs = Question.objects.filter(id__in=question_ids, status=Question.StatusChoices.IMPORTED)
            count = target_qs.update(**updates)
            
            AuditLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                action=AuditLog.ActionChoices.UPDATE,
                resource_type='Question',
                resource_id=f"{len(question_ids)} questions",
                description=f"تعيين جماعي لخصائص ({count}) سؤالاً مستورداً"
            )

        return Response({
            "success": True,
            "message": f"تم تحديث بيانات {count} سؤال بنجاح",
            "updated_count": count
        })

    @action(detail=False, methods=['post'])
    def bulk_activate(self, request):
        """
        Move completed questions from 'مستورد' (IMPORTED) to 'مسودة' (DRAFT).
        Backend Rule: Requires lesson to be set. Questions without lesson are rejected.
        """
        question_ids = request.data.get('question_ids', [])
        target_status = request.data.get('target_status', Question.StatusChoices.DRAFT)
        
        if not question_ids or not isinstance(question_ids, list):
            return Response({"error": "يرجى تحديد الأسئلة المراد نقلها"}, status=status.HTTP_400_BAD_REQUEST)

        # Enforce validation in database query
        valid_qs = Question.objects.filter(
            id__in=question_ids,
            status=Question.StatusChoices.IMPORTED,
            lesson__isnull=False
        )
        valid_count = valid_qs.count()

        if valid_count == 0:
            return Response({
                "error": "لا يمكن ترحيل أي سؤال! يجب تحديد الدرس الأدنى الإجباري لجميع الأسئلة قبل النقل إلى مسودة."
            }, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            valid_qs.update(status=target_status)
            
            AuditLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                action=AuditLog.ActionChoices.UPDATE,
                resource_type='Question',
                resource_id=f"{valid_count} questions",
                description=f"ترحيل {valid_count} سؤالاً مستورداً إلى بنك الأسئلة بحالة ({target_status})"
            )

        skipped_count = len(question_ids) - valid_count
        msg = f"تم ترحيل {valid_count} سؤال بنجاح إلى بنك الأسئلة"
        if skipped_count > 0:
            msg += f" (تم تخطي {skipped_count} سؤال لعدم تحديد الدرس)"

        return Response({
            "success": True,
            "message": msg,
            "activated_count": valid_count,
            "skipped_count": skipped_count
        })
