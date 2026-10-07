from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from bank.models.Question import Question
from bank.models.QuestionMetrics import QuestionMetrics
from bank.models.DistractorAnalysis import DistractorAnalysis
from bank.models.QuestionVersion import QuestionVersion
from bank.models.AuditLog import AuditLog
from bank.serializers.Question import QuestionSerializer, QuestionListSerializer
from bank.serializers.Answer import AnswerSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils import timezone
from django.db.models import Q

class QuestionMVS(AllMVS):
    """
    Dedicated ModelViewSet exclusively for Question Bank View.
    Endpoint: /api/bank/questions/
    Used by: QuestionBankView.vue
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
    ).prefetch_related('options', 'metrics', 'distractor_analyses')
    serializer_class = QuestionSerializer
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]

    def get_serializer_class(self):
        if getattr(self, 'action', None) in ['list', 'filter_paginate', 'filter', 'second_list', 'all', 'select']:
            return QuestionListSerializer
        return QuestionSerializer
    filterset_fields = {
        'status': ['exact', 'in'],
        'difficulty': ['exact', 'in'],
        'questionType': ['exact', 'in'],
        'bloomLevel': ['exact', 'in'],
        'institution_type': ['exact', 'in'],
        'lesson': ['exact'],
        'lesson__unit': ['exact'],
        'lesson__unit__semester': ['exact'],
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

        # 5. Subject & Unit Filter
        subject = params.get('subject') or params.get('institute_subject')
        if subject:
            qs = qs.filter(
                Q(lesson__unit__class_subject__subject_id=subject) |
                Q(lesson__unit__semester_subject__fk_subject_id=subject) |
                Q(lesson__subject_id=subject)
            )

        unit = params.get('unit')
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

    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        """Retrieve full question details including options, psychometrics, and academic hierarchy."""
        question = self.get_object()
        serializer = self.get_serializer(question)
        data = serializer.data
        
        answers = question.options.all()
        data['answers'] = AnswerSerializer(answers, many=True).data
        
        # Include psychometrics
        metrics, _ = QuestionMetrics.objects.get_or_create(question=question)
        data['metrics'] = {
            'usage_count': metrics.usage_count,
            'last_used_at': metrics.last_used_at,
            'total_correct_answers': metrics.total_correct_answers,
            'total_respondents': metrics.total_respondents,
            'actual_difficulty': metrics.actual_difficulty,
            'discrimination_index': metrics.discrimination_index,
            'point_biserial': metrics.point_biserial,
            'avg_answer_time': metrics.avg_answer_time,
            'rejection_count': metrics.rejection_count,
            'edit_count': metrics.edit_count,
        }
        
        # Distractor analysis
        distractors = DistractorAnalysis.objects.filter(question=question).select_related('answer')
        data['distractor_analysis'] = [
            {
                'answer_id': d.answer_id,
                'answer_text': d.answer.text if d.answer else '',
                'is_correct': d.answer.isTrue if d.answer else False,
                'selection_count': d.selection_count,
                'selection_rate': d.selection_rate,
                'upper_group_rate': d.upper_group_rate,
                'lower_group_rate': d.lower_group_rate,
            }
            for d in distractors
        ]

        lesson = question.lesson
        if lesson and lesson.unit:
            data['fk_unit'] = lesson.unit_id
            try:
                data['fk_subject'] = lesson.unit.class_subject.subject_id if lesson.unit.class_subject else None
            except AttributeError:
                data['fk_subject'] = None
        else:
            data['fk_unit'] = None
            data['fk_subject'] = None
            
        return Response(data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Returns statistics for Question Bank stat cards."""
        queryset = self.get_queryset()
        return Response({
            "total": queryset.count(),
            "drafts": queryset.filter(status="مسودة").count(),
            "pending": queryset.filter(status="قيد المراجعة").count(),
            "approved": queryset.filter(status="معتمد").count(),
            "rejected": queryset.filter(status="مرفوض").count(),
            "archived": queryset.filter(status="مؤرشف").count(),
            "disabled": queryset.filter(status="معطل").count(),
        })

    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Duplicate a question as a new Draft within the same lesson."""
        original = self.get_object()
        with transaction.atomic():
            new_q = Question.objects.create(
                content=f"{original.content}",
                description=original.description,
                lesson=original.lesson,
                learningOutcome=original.learningOutcome,
                difficulty=original.difficulty,
                bloomLevel=original.bloomLevel,
                questionType=original.questionType,
                isTrue=original.isTrue,
                answerText=original.answerText,
                status=Question.StatusChoices.DRAFT,
                defaultMark=original.defaultMark,
                expected_time_minutes=original.expected_time_minutes,
                image=original.image,
                version_number=1,
                createdBy=request.user if request.user.is_authenticated else None
            )
            
            # Duplicate options
            from bank.models.Answer import Answer
            for opt in original.options.all():
                Answer.objects.create(
                    question=new_q,
                    text=opt.text,
                    image=opt.image,
                    latex=opt.latex,
                    isTrue=opt.isTrue
                )
            
            # Create blank metrics
            QuestionMetrics.objects.create(question=new_q)
            
            # Audit log
            AuditLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                action=AuditLog.ActionChoices.DUPLICATE,
                resource_type='Question',
                resource_id=str(new_q.id),
                description=f"استنساخ السؤال #{original.id} إلى سؤال مسودة جديد #{new_q.id}"
            )
            
        return Response({
            "success": True,
            "message": "تم استنساخ السؤال بنجاح",
            "new_question_id": new_q.id
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """Archive a question."""
        question = self.get_object()
        question.status = Question.StatusChoices.ARCHIVED
        question.save(update_fields=['status'])
        
        AuditLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action=AuditLog.ActionChoices.ARCHIVE,
            resource_type='Question',
            resource_id=str(question.id),
            description=f"أرشفة السؤال #{question.id}"
        )
        return Response({"success": True, "message": "تمت أرشفة السؤال بنجاح"})

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """Restore an archived question back to Draft."""
        question = self.get_object()
        question.status = Question.StatusChoices.DRAFT
        question.save(update_fields=['status'])
        
        AuditLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action=AuditLog.ActionChoices.RESTORE,
            resource_type='Question',
            resource_id=str(question.id),
            description=f"استعادة السؤال #{question.id} إلى مسودة"
        )
        return Response({"success": True, "message": "تمت استعادة السؤال إلى مسودة"})

    @action(detail=True, methods=['post'])
    def create_version(self, request, pk=None):
        """Create a new version (v+1) for an approved question."""
        original = self.get_object()
        reason = request.data.get('reason', '')
        
        with transaction.atomic():
            new_version_num = (original.version_number or 1) + 1
            new_q = Question.objects.create(
                content=original.content,
                description=original.description,
                lesson=original.lesson,
                learningOutcome=original.learningOutcome,
                difficulty=original.difficulty,
                bloomLevel=original.bloomLevel,
                questionType=original.questionType,
                isTrue=original.isTrue,
                answerText=original.answerText,
                status=Question.StatusChoices.DRAFT,
                defaultMark=original.defaultMark,
                expected_time_minutes=original.expected_time_minutes,
                image=original.image,
                version_number=new_version_num,
                parent_version=original,
                createdBy=request.user if request.user.is_authenticated else None
            )
            
            # Duplicate options
            from bank.models.Answer import Answer
            for opt in original.options.all():
                Answer.objects.create(
                    question=new_q,
                    text=opt.text,
                    image=opt.image,
                    latex=opt.latex,
                    isTrue=opt.isTrue
                )
            
            # Copy old metrics to new version as starting point
            old_metrics = getattr(original, 'metrics', None)
            QuestionMetrics.objects.create(
                question=new_q,
                usage_count=old_metrics.usage_count if old_metrics else 0,
                actual_difficulty=old_metrics.actual_difficulty if old_metrics else None,
                discrimination_index=old_metrics.discrimination_index if old_metrics else None,
                point_biserial=old_metrics.point_biserial if old_metrics else None,
                avg_answer_time=old_metrics.avg_answer_time if old_metrics else None,
                total_correct_answers=old_metrics.total_correct_answers if old_metrics else 0,
                total_respondents=old_metrics.total_respondents if old_metrics else 0,
            )
            
            # Record QuestionVersion link
            QuestionVersion.objects.create(
                original_question=original,
                version_question=new_q,
                version_number=new_version_num,
                change_reason=reason,
                createdBy=request.user if request.user.is_authenticated else None
            )
            
            # Audit log
            AuditLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                action=AuditLog.ActionChoices.NEW_VERSION,
                resource_type='Question',
                resource_id=str(new_q.id),
                description=f"إنشاء الإصدار {new_version_num} من السؤال #{original.id}"
            )

        return Response({
            "success": True,
            "message": f"تم إنشاء الإصدار {new_version_num} بنجاح",
            "new_question_id": new_q.id
        }, status=status.HTTP_201_CREATED)
