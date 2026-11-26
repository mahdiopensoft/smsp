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
    LIST_ACTIONS = (
        'list', 'filter_paginate', 'filter_by_field_paginate',
        'filter', 'filter_by_fields', 'second_list', 'all', 'select',
    )

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    fields_4_search = ['content', 'description']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]

    def get_serializer_class(self):
        if getattr(self, 'action', None) in self.LIST_ACTIONS:
            return QuestionListSerializer
        return QuestionSerializer

    def get_serializer(self, *args, **kwargs):
        # AllMVS's CustomListRetrieveMixin hardcodes self.serializer_class and
        # ignores get_serializer_class(); bypass it for lightweight list payloads.
        if getattr(self, 'action', None) in self.LIST_ACTIONS:
            kwargs.setdefault('context', self.get_serializer_context(None))
            return QuestionListSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    def _with_optimized_relations(self, qs):
        """Attach only the relations required by the current action."""
        action_name = getattr(self, 'action', None)
        if action_name in self.LIST_ACTIONS:
            return qs.select_related(
                'school_lesson__school_subject',
                'school_lesson__unit__school_subject',
                'school_lesson__unit__class_subject__school_subject',
                'school_lesson__unit__class_subject__subject',
                'institute_lesson__subject',
                'institute_lesson__unit__subject',
                'lesson__subject',
                'lesson__unit__semester_subject__fk_subject',
                'lesson__unit__semester_subject__course',
                'createdBy',
                'reviewer',
                'metrics',
            )
        return qs.select_related(
            'lesson',
            'lesson__subject',
            'lesson__unit',
            'lesson__unit__semester',
            'lesson__unit__semester_subject__fk_subject',
            'lesson__unit__semester_subject__course',
            'lesson__unit__semester_subject__fk_specialization__fk_college',
            'lesson__unit__semester_subject__fk_specialization__fk_section',
            'lesson__unit__semester_subject__semester',
            'school_lesson',
            'school_lesson__school_subject',
            'school_lesson__unit',
            'school_lesson__unit__school_subject',
            'school_lesson__unit__class_subject__subject',
            'school_lesson__unit__class_subject__school_subject',
            'school_lesson__unit__class_subject__class_track',
            'school_lesson__unit__class_subject__class_track__level',
            'school_lesson__unit__class_subject__class_track__level__stage',
            'institute_lesson',
            'institute_lesson__subject',
            'institute_lesson__unit',
            'institute_lesson__unit__subject__field',
            'institute_lesson__unit__curriculum__specialization',
            'createdBy',
            'reviewer',
            'metrics',
        ).prefetch_related('options', 'distractor_analyses')

    def perform_create(self, serializer):
        user = self.request.user if (self.request and self.request.user and self.request.user.is_authenticated) else None
        question = serializer.save(createdBy=user)
        QuestionMetrics.objects.get_or_create(question=question)
        AuditLog.objects.create(
            user=user,
            action=AuditLog.ActionChoices.CREATE,
            resource_type='Question',
            resource_id=str(question.id),
            description=f"إنشاء سؤال جديد #{question.id} ({question.questionType})"
        )

    def perform_update(self, serializer):
        user = self.request.user if (self.request and self.request.user and self.request.user.is_authenticated) else None
        if serializer.validated_data.get('status') == Question.StatusChoices.APPROVED:
            serializer.validated_data['reviewer'] = user
            serializer.validated_data['approved_at'] = timezone.now()
        question = serializer.save()
        metrics, _ = QuestionMetrics.objects.get_or_create(question=question)
        metrics.edit_count += 1
        metrics.save(update_fields=['edit_count'])
        AuditLog.objects.create(
            user=user,
            action=AuditLog.ActionChoices.UPDATE,
            resource_type='Question',
            resource_id=str(question.id),
            description=f"تعديل بيانات السؤال #{question.id}"
        )
    filterset_fields = {
        'status': ['exact', 'in'],
        'difficulty': ['exact', 'in'],
        'questionType': ['exact', 'in'],
        'bloomLevel': ['exact', 'in'],
        'institution_type': ['exact', 'in'],
        'lesson': ['exact'],
        'lesson__subject': ['exact'],
        'lesson__unit': ['exact'],
        'lesson__unit__semester': ['exact'],
        'lesson__unit__semester_subject': ['exact'],
        'lesson__unit__semester_subject__fk_subject': ['exact'],
        'lesson__unit__semester_subject__course': ['exact'],
        'lesson__unit__semester_subject__fk_specialization': ['exact'],
        'lesson__unit__semester_subject__fk_specialization__fk_college': ['exact'],
        'lesson__unit__semester_subject__fk_specialization__fk_section': ['exact'],
    }

    def _apply_school_filters(self, qs, stage, class_track):
        """Filter school questions by stage/class_track via pre-resolved lesson IDs (avoids reverse-FK DISTINCT joins)."""
        if not stage and not class_track:
            return qs

        from academic.models.schools.SchoolClassSubject import SchoolClassSubject
        from academic.models.schools.SchoolLesson import SchoolLesson
        from academic.models.universities.UniversityLesson import UniversityLesson

        scs_qs = SchoolClassSubject.objects.filter(is_deleted=False)
        if stage:
            scs_qs = scs_qs.filter(class_track__level__stage_id=stage)
        if class_track:
            scs_qs = scs_qs.filter(class_track_id=class_track)

        scs_rows = list(scs_qs.values_list('id', 'school_subject_id'))
        if not scs_rows:
            return qs.none()

        cs_ids = [row[0] for row in scs_rows]
        school_subj_ids = list({row[1] for row in scs_rows if row[1]})

        sl_query = Q(unit__class_subject_id__in=cs_ids)
        ul_query = Q(unit__class_subject_id__in=cs_ids)
        if school_subj_ids:
            sl_query |= Q(unit__school_subject_id__in=school_subj_ids) | Q(school_subject_id__in=school_subj_ids)
            ul_query |= Q(unit__school_subject_id__in=school_subj_ids)

        sl_ids = list(SchoolLesson.objects.filter(sl_query).values_list('id', flat=True))
        ul_ids = list(UniversityLesson.objects.filter(ul_query).values_list('id', flat=True))
        if not sl_ids and not ul_ids:
            return qs.none()

        match_q = Q()
        if sl_ids:
            match_q |= Q(school_lesson_id__in=sl_ids)
        if ul_ids:
            match_q |= Q(lesson_id__in=ul_ids)
        return qs.filter(match_q)

    def _apply_institute_filters(self, qs, params):
        """Filter institute questions via pre-resolved InstituteLesson IDs (avoids reverse-FK DISTINCT joins)."""
        inst_field = params.get('field') or params.get('institute_field')
        inst_edu_system = params.get('institute_education_system') or params.get('education_system')
        inst_specialization = params.get('institute_specialization')
        inst_subject = params.get('institute_subject')

        if not any([inst_field, inst_edu_system, inst_specialization, inst_subject]):
            return qs

        from academic.models.institutes.InstituteLesson import InstituteLesson
        from academic.models.institutes.InstituteCurriculumSubject import InstituteCurriculumSubject

        qs = qs.filter(institution_type='institute')
        il_qs = InstituteLesson.objects.all()

        if inst_field:
            il_qs = il_qs.filter(
                Q(unit__subject__field_id=inst_field) |
                Q(subject__field_id=inst_field) |
                Q(unit__curriculum__specialization__field_id=inst_field)
            )

        if inst_edu_system or inst_specialization:
            ics_qs = InstituteCurriculumSubject.objects.filter(is_deleted=False)
            if inst_edu_system:
                ics_qs = ics_qs.filter(curriculum__specialization__education_system_id=inst_edu_system)
            if inst_specialization:
                ics_qs = ics_qs.filter(curriculum__specialization_id=inst_specialization)
            matching_subj_ids = list(ics_qs.values_list('subject_id', flat=True).distinct())

            spec_q = Q()
            if inst_edu_system:
                spec_q &= Q(unit__curriculum__specialization__education_system_id=inst_edu_system)
            if inst_specialization:
                spec_q &= Q(unit__curriculum__specialization_id=inst_specialization)
            if matching_subj_ids:
                spec_q = spec_q | Q(unit__subject_id__in=matching_subj_ids) | Q(subject_id__in=matching_subj_ids)
            elif not (inst_edu_system or inst_specialization):
                return qs.none()
            il_qs = il_qs.filter(spec_q)

        if inst_subject:
            il_qs = il_qs.filter(Q(unit__subject_id=inst_subject) | Q(subject_id=inst_subject))

        il_ids = list(il_qs.values_list('id', flat=True))
        if inst_subject and not any([inst_field, inst_edu_system, inst_specialization]):
            match_q = Q(lesson__subject_id=inst_subject)
            if il_ids:
                match_q |= Q(institute_lesson_id__in=il_ids)
            return qs.filter(match_q)
        return qs.filter(institute_lesson_id__in=il_ids) if il_ids else qs.none()

    def get_queryset(self):
        qs = self._with_optimized_relations(super().get_queryset())
        params = self.request.query_params

        # 1. Institution Type Filter
        inst_type = params.get('institution_type')
        if inst_type and inst_type != 'all':
            qs = qs.filter(institution_type=inst_type)

        # Standard attribute filters (also used directly by QuestionBankView GET queries)
        for param_key in ('status', 'difficulty', 'questionType', 'bloomLevel'):
            val = params.get(param_key)
            if val not in (None, ''):
                qs = qs.filter(**{param_key: val})

        # 2. University Filters
        college = params.get('college') or params.get('fk_college')
        if college:
            qs = qs.filter(lesson__unit__semester_subject__fk_specialization__fk_college_id=college)

        department = params.get('department') or params.get('fk_department') or params.get('section')
        if department:
            qs = qs.filter(lesson__unit__semester_subject__fk_specialization__fk_section_id=department)

        specialization = params.get('specialization') or params.get('fk_specialization')
        if specialization:
            qs = qs.filter(lesson__unit__semester_subject__fk_specialization_id=specialization)

        semester_subject = params.get('semester_subject') or params.get('fk_semester_subject')
        if semester_subject:
            qs = qs.filter(lesson__unit__semester_subject_id=semester_subject)

        # 3. School Filters
        qs = self._apply_school_filters(qs, params.get('stage'), params.get('class_track'))

        # 4. Institute Filters
        qs = self._apply_institute_filters(qs, params)

        # 5. Subject & Unit Filters (strictly Many-to-One forward FKs -> no row multiplication or DISTINCT)
        subject = params.get('subject') or params.get('school_subject')
        if subject:
            school_subject_q = (
                Q(school_lesson__unit__class_subject__school_subject_id=subject) |
                Q(school_lesson__unit__class_subject__subject_id=subject) |
                Q(school_lesson__unit__school_subject_id=subject) |
                Q(school_lesson__school_subject_id=subject) |
                Q(lesson__unit__school_subject_id=subject) |
                Q(lesson__unit__class_subject__school_subject_id=subject) |
                Q(lesson__unit__class_subject__subject_id=subject) |
                Q(lesson__subject_id=subject)
            )
            univ_subject_q = (
                Q(lesson__unit__semester_subject__fk_subject_id=subject) |
                Q(lesson__subject_id=subject) |
                Q(lesson__unit__semester_subject__course_id=subject)
            )
            inst_subject_q = (
                Q(institute_lesson__unit__subject_id=subject) |
                Q(institute_lesson__subject_id=subject) |
                Q(lesson__subject_id=subject)
            )
            if inst_type == 'school':
                qs = qs.filter(school_subject_q)
            elif inst_type == 'university':
                qs = qs.filter(univ_subject_q)
            elif inst_type == 'institute':
                qs = qs.filter(inst_subject_q)
            else:
                qs = qs.filter(school_subject_q | univ_subject_q | inst_subject_q)

        unit = params.get('unit')
        if unit:
            if inst_type == 'school':
                qs = qs.filter(Q(school_lesson__unit_id=unit) | Q(lesson__unit_id=unit))
            elif inst_type == 'institute':
                qs = qs.filter(Q(institute_lesson__unit_id=unit) | Q(lesson__unit_id=unit))
            elif inst_type == 'university':
                qs = qs.filter(lesson__unit_id=unit)
            else:
                qs = qs.filter(
                    Q(school_lesson__unit_id=unit) |
                    Q(institute_lesson__unit_id=unit) |
                    Q(lesson__unit_id=unit)
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

        lesson = question.school_lesson or question.institute_lesson or question.lesson
        if lesson and getattr(lesson, 'unit', None):
            unit = lesson.unit
            data['fk_unit'] = unit.id
            class_sub = getattr(unit, 'class_subject', None)
            sem_sub = getattr(unit, 'semester_subject', None)
            if class_sub:
                data['fk_subject'] = class_sub.school_subject_id or class_sub.subject_id
            elif getattr(unit, 'school_subject_id', None):
                data['fk_subject'] = unit.school_subject_id
            elif sem_sub:
                data['fk_subject'] = sem_sub.fk_subject_id
            elif getattr(lesson, 'school_subject_id', None):
                data['fk_subject'] = lesson.school_subject_id
            elif getattr(lesson, 'subject_id', None):
                data['fk_subject'] = lesson.subject_id
            else:
                data['fk_subject'] = None
        else:
            data['fk_unit'] = None
            data['fk_subject'] = (
                getattr(lesson, 'school_subject_id', None) or getattr(lesson, 'subject_id', None)
            ) if lesson else None
            
        return Response(data)

    @action(detail=True, methods=['get'])
    def audit_trail(self, request, pk=None):
        """Retrieve audit history and activity logs for this specific question."""
        question = self.get_object()
        serializer = self.get_serializer(question)
        return Response({
            "success": True,
            "data": serializer.data.get('audit_trail', [])
        })

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
                institution_type=original.institution_type,
                lesson=original.lesson,
                school_lesson=original.school_lesson,
                institute_lesson=original.institute_lesson,
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
                    isTrue=opt.isTrue,
                    order_index=opt.order_index
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
                institution_type=original.institution_type,
                lesson=original.lesson,
                school_lesson=original.school_lesson,
                institute_lesson=original.institute_lesson,
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
                    isTrue=opt.isTrue,
                    order_index=opt.order_index
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
