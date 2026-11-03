from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from bank.models.Question import Question
from bank.models.QuestionMetrics import QuestionMetrics
from bank.models.AuditLog import AuditLog
from bank.models.AdvancedQuestionStructures import MatchingPair, OrderingItem, BlankAnswer, CaseStudySubQuestion
from bank.serializers.Question import QuestionSerializer
from bank.serializers.Answer import AnswerSerializer
from bank.utils.similarity_checker import check_question_similarity
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

class QuestionNewMVS(AllMVS):
    """
    Dedicated ModelViewSet for Question Creation & Single Question Editing.
    Endpoint: /api/bank/question-new/
    Used by: QuestionNewView.vue
    """
    queryset = Question.objects.select_related(
        'lesson',
        'lesson__subject',
        'lesson__unit',
        'lesson__unit__semester_subject__fk_subject',
        'lesson__unit__semester_subject__course',
        'lesson__unit__semester_subject__fk_specialization__fk_college',
        'lesson__unit__semester_subject__fk_specialization__fk_section',
        'lesson__unit__semester_subject__semester',
        'createdBy',
        'reviewer'
    ).prefetch_related('options', 'matching_pairs', 'ordering_items', 'blank_answers', 'case_study_sub_questions')
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        question = serializer.save(createdBy=user)
        # Create blank metrics
        QuestionMetrics.objects.get_or_create(question=question)
        
        # Log audit
        AuditLog.objects.create(
            user=user,
            action=AuditLog.ActionChoices.CREATE,
            resource_type='Question',
            resource_id=str(question.id),
            description=f"إنشاء سؤال جديد #{question.id} ({question.questionType})"
        )

    def perform_update(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        question = serializer.save()
        
        # Increment edit count on metrics
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

    @action(detail=False, methods=['post'])
    def check_similarity(self, request):
        """API to check text similarity for duplicate detection."""
        content = request.data.get('content', '')
        lesson_id = request.data.get('lesson_id')
        exclude_id = request.data.get('exclude_id')
        threshold = float(request.data.get('threshold', 0.80))
        
        result = check_question_similarity(
            content_text=content,
            lesson_id=lesson_id,
            threshold=threshold,
            exclude_question_id=exclude_id
        )
        return Response(result)

    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        question = self.get_object()
        
        # 1. Format clean answers array
        answers = []
        for opt in question.options.all():
            answers.append({
                'id': opt.id,
                'text': opt.text,
                'isTrue': opt.isTrue,
                'latex': opt.latex,
            })
        
        # 2. Build exact needed fields payload
        data = {
            'id': question.id,
            'content': question.content,
            'difficulty': question.difficulty,
            'bloomLevel': question.bloomLevel,
            'defaultMark': question.defaultMark,
            'expected_time_minutes': question.expected_time_minutes,
            'image': question.image.url if getattr(question, 'image', None) and hasattr(question.image, 'url') else (question.image if isinstance(question.image, str) else None),
            'questionType': question.questionType,
            'status': question.status,
            'institution_type': question.institution_type or 'school',
            'answers': answers,
            'matching_pairs': [
                {'id': mp.id, 'left_text': mp.left_text, 'right_text': mp.right_text, 'order': mp.order}
                for mp in question.matching_pairs.all()
            ],
            'ordering_items': [
                {'id': oi.id, 'text': oi.text, 'correct_position': oi.correct_position}
                for oi in question.ordering_items.all()
            ],
            'blank_answers': [
                {'id': ba.id, 'blank_index': ba.blank_index, 'accepted_answers': ba.accepted_answers, 'is_case_sensitive': ba.is_case_sensitive}
                for ba in question.blank_answers.all()
            ],
            # Academic Hierarchy IDs
            'college_id': None,
            'department_id': None,
            'specialization_id': None,
            'semester_subject_id': None,
            'semester_id': None,
            'stage_id': None,
            'class_track_id': None,
            'subject_id': None,
            'unit_id': None,
            'lesson': None,
        }

        lesson = getattr(question, 'lesson', None)
        target_inst = getattr(question, 'institution_type', None) or 'school'
        data['institution_type'] = target_inst

        if lesson:
            data['lesson'] = lesson.id
            sub_id = getattr(lesson, 'subject_id', None) or getattr(lesson, 'school_subject_id', None)
            if sub_id:
                data['subject_id'] = sub_id
                data['fk_subject'] = sub_id

            unit = getattr(lesson, 'unit', None)
            if unit:
                data['fk_unit'] = unit.id
                data['unit_id'] = unit.id
                
                # Check unit semester
                if getattr(unit, 'semester_id', None):
                    data['semester_id'] = unit.semester_id

                # Check school-specific relations
                class_sub = getattr(unit, 'class_subject', None)
                school_sub = getattr(unit, 'school_subject', None)
                if class_sub:
                    data['fk_subject'] = class_sub.subject_id
                    data['subject_id'] = class_sub.subject_id
                    if getattr(class_sub, 'semester_id', None):
                        data['semester_id'] = class_sub.semester_id
                    if getattr(class_sub, 'class_track', None):
                        data['class_track_id'] = class_sub.class_track_id
                        if getattr(class_sub.class_track, 'level', None):
                            data['stage_id'] = class_sub.class_track.level.stage_id
                elif school_sub:
                    data['fk_subject'] = school_sub.id
                    data['subject_id'] = school_sub.id

                # Check university-specific relations
                sem_sub = getattr(unit, 'semester_subject', None)
                if sem_sub:
                    data['fk_subject'] = sem_sub.fk_subject_id
                    data['subject_id'] = sem_sub.fk_subject_id
                    data['semester_subject_id'] = sem_sub.id
                    if getattr(sem_sub, 'semester_id', None):
                        data['semester_id'] = sem_sub.semester_id
                    if getattr(sem_sub, 'fk_specialization', None):
                        spec = sem_sub.fk_specialization
                        data['specialization_id'] = spec.id
                        data['department_id'] = getattr(spec, 'fk_section_id', None)
                        data['college_id'] = getattr(spec, 'fk_college_id', None)

        # Fallback 1: If university fields are missing, try resolving from subject
        if target_inst == 'university' or (not data.get('stage_id') and not data.get('class_track_id') and not data.get('college_id') and not data.get('semester_subject_id') and target_inst != 'school'):
            if not data.get('semester_subject_id'):
                sub_id = data.get('subject_id') or getattr(lesson, 'subject_id', None)
                if sub_id:
                    from academic.models.universities.UniversitySemesterSubject import UniversitySemesterSubject as SemesterSubject
                    sem_sub = SemesterSubject.objects.filter(fk_subject_id=sub_id).select_related(
                        'fk_specialization__fk_college', 'fk_specialization__fk_section'
                    ).first()
                    if sem_sub:
                        data['semester_subject_id'] = sem_sub.id
                        data['subject_id'] = sem_sub.fk_subject_id
                        data['fk_subject'] = sem_sub.fk_subject_id
                        if getattr(sem_sub, 'semester_id', None) and not data.get('semester_id'):
                            data['semester_id'] = sem_sub.semester_id
                        if sem_sub.fk_specialization:
                            data['specialization_id'] = sem_sub.fk_specialization_id
                            data['department_id'] = sem_sub.fk_specialization.fk_section_id
                            data['college_id'] = sem_sub.fk_specialization.fk_college_id
                        data['institution_type'] = 'university'

        # Fallback 2: If school fields are missing, try resolving from subject
        if target_inst == 'school' or (not data.get('college_id') and not data.get('semester_subject_id')):
            if not data.get('class_track_id'):
                sub_id = data.get('subject_id') or getattr(lesson, 'subject_id', None)
                if sub_id:
                    from academic.models.schools.SchoolClassSubject import SchoolClassSubject
                    cs = SchoolClassSubject.objects.filter(subject_id=sub_id).select_related(
                        'class_track__level__stage'
                    ).first()
                    if cs:
                        data['subject_id'] = cs.subject_id
                        data['fk_subject'] = cs.subject_id
                        if getattr(cs, 'semester_id', None) and not data.get('semester_id'):
                            data['semester_id'] = cs.semester_id
                        if cs.class_track:
                            data['class_track_id'] = cs.class_track_id
                            if cs.class_track.level:
                                data['stage_id'] = cs.class_track.level.stage_id
                        if not target_inst or target_inst == 'school':
                            data['institution_type'] = 'school'

        # Final check on institution_type
        if getattr(question, 'institution_type', None) == 'institute' or target_inst == 'institute':
            data['institution_type'] = 'institute'
        elif target_inst == 'school':
            data['institution_type'] = 'school'
        elif target_inst == 'university':
            data['institution_type'] = 'university'
        elif data.get('semester_subject_id') or data.get('college_id'):
            data['institution_type'] = 'university'
        elif data.get('stage_id') or data.get('class_track_id'):
            data['institution_type'] = 'school'
        else:
            data['institution_type'] = getattr(question, 'institution_type', 'school') or 'school'

        return Response(data)
