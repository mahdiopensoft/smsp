from rest_framework import serializers
from django.db import transaction
from bank.models.Question import Question
from bank.models.Answer import Answer
from bank.serializers.Base64ImageField import Base64ImageField

class AnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Answer
        fields = ['id', 'question', 'text', 'image', 'latex', 'isTrue']
        extra_kwargs = {
            'question': {'required': False}
        }

class QuestionListSerializer(serializers.ModelSerializer):
    """
    Lightweight, high-performance serializer for Question Bank Table / List.
    - Eliminates redundant relational trees
    - Excludes sensitive answer options (isTrue) from the list endpoint
    - Reduces JSON payload by >90%
    """
    subject_name = serializers.SerializerMethodField(read_only=True)
    unit_name = serializers.SerializerMethodField(read_only=True)
    lesson_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Question
        fields = [
            'id',
            'content',
            'questionType',
            'difficulty',
            'bloomLevel',
            'defaultMark',
            'expected_time_minutes',
            'status',
            'version_number',
            'institution_type',
            'subject_name',
            'unit_name',
            'lesson_name',
            'created_at',
        ]

    def get_subject_name(self, obj):
        try:
            if obj.lesson and obj.lesson.unit:
                if obj.lesson.unit.class_subject and obj.lesson.unit.class_subject.subject:
                    return obj.lesson.unit.class_subject.subject.name_ar
                elif obj.lesson.unit.semester_subject and obj.lesson.unit.semester_subject.fk_subject:
                    return obj.lesson.unit.semester_subject.fk_subject.name_ar
            if obj.lesson and getattr(obj.lesson, 'subject', None):
                return obj.lesson.subject.name_ar
        except Exception:
            pass
        return None

    def get_unit_name(self, obj):
        try:
            return obj.lesson.unit.name_ar if (obj.lesson and obj.lesson.unit) else None
        except Exception:
            return None

    def get_lesson_name(self, obj):
        try:
            return obj.lesson.name_ar if obj.lesson else None
        except Exception:
            return None

class QuestionSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)
    options = AnswerSerializer(many=True, required=False)
    
    # Read-only relational fields for fast rendering
    subject_name = serializers.SerializerMethodField(read_only=True)
    subject_id = serializers.SerializerMethodField(read_only=True)
    unit_name = serializers.SerializerMethodField(read_only=True)
    unit_id = serializers.SerializerMethodField(read_only=True)
    lesson_name = serializers.SerializerMethodField(read_only=True)
    author_name = serializers.SerializerMethodField(read_only=True)
    reviewer_name = serializers.SerializerMethodField(read_only=True)
    learning_outcome_name = serializers.SerializerMethodField(read_only=True)

    # School Hierarchy
    stage_name = serializers.SerializerMethodField(read_only=True)
    stage_id = serializers.SerializerMethodField(read_only=True)
    class_track_name = serializers.SerializerMethodField(read_only=True)
    class_track_id = serializers.SerializerMethodField(read_only=True)

    # University Hierarchy
    college_name = serializers.SerializerMethodField(read_only=True)
    college_id = serializers.SerializerMethodField(read_only=True)
    department_name = serializers.SerializerMethodField(read_only=True)
    department_id = serializers.SerializerMethodField(read_only=True)
    specialization_name = serializers.SerializerMethodField(read_only=True)
    specialization_id = serializers.SerializerMethodField(read_only=True)
    semester_subject_name = serializers.SerializerMethodField(read_only=True)
    semester_subject_id = serializers.SerializerMethodField(read_only=True)

    # Institute Hierarchy
    institute_field_name = serializers.SerializerMethodField(read_only=True)
    institute_field_id = serializers.SerializerMethodField(read_only=True)
    institute_specialization_name = serializers.SerializerMethodField(read_only=True)
    institute_specialization_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def create(self, validated_data):
        options_data = validated_data.pop('options', None)
        if options_data is None:
            options_data = self.initial_data.get('options', [])
        
        with transaction.atomic():
            question = Question.objects.create(**validated_data)
            
            answers_to_create = []
            for opt in options_data:
                if isinstance(opt, dict):
                    text = opt.get('text', '')
                    is_true = opt.get('isTrue', False)
                else:
                    text = getattr(opt, 'text', '')
                    is_true = getattr(opt, 'isTrue', False)
                answers_to_create.append(Answer(
                    question=question,
                    text=text,
                    isTrue=is_true
                ))
                
            if answers_to_create:
                Answer.objects.bulk_create(answers_to_create)
                
            return question

    def update(self, instance, validated_data):
        options_data = validated_data.pop('options', None)
        if options_data is None:
            options_data = self.initial_data.get('options', None)
        
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            
            if options_data is not None:
                # Replace options with updated set
                instance.options.all().delete()
                answers_to_create = []
                for opt in options_data:
                    if isinstance(opt, dict):
                        text = opt.get('text', '')
                        is_true = opt.get('isTrue', False)
                    else:
                        text = getattr(opt, 'text', '')
                        is_true = getattr(opt, 'isTrue', False)
                    answers_to_create.append(Answer(
                        question=instance,
                        text=text,
                        isTrue=is_true
                    ))
                if answers_to_create:
                    Answer.objects.bulk_create(answers_to_create)
                    
            return instance


    def get_subject_name(self, obj):
        try:
            if obj.lesson and obj.lesson.unit:
                if obj.lesson.unit.class_subject and obj.lesson.unit.class_subject.subject:
                    return obj.lesson.unit.class_subject.subject.name_ar
                elif obj.lesson.unit.semester_subject and obj.lesson.unit.semester_subject.fk_subject:
                    return obj.lesson.unit.semester_subject.fk_subject.name_ar
        except Exception:
            pass
        return None

    def get_subject_id(self, obj):
        try:
            if obj.lesson and obj.lesson.unit:
                if obj.lesson.unit.class_subject:
                    return obj.lesson.unit.class_subject.subject_id
                elif obj.lesson.unit.semester_subject:
                    return obj.lesson.unit.semester_subject.fk_subject_id
        except Exception:
            pass
        return None

    def get_unit_name(self, obj):
        try:
            return obj.lesson.unit.name_ar
        except Exception:
            return None

    def get_unit_id(self, obj):
        try:
            return obj.lesson.unit_id
        except Exception:
            return None

    def get_lesson_name(self, obj):
        try:
            return obj.lesson.name_ar
        except Exception:
            return None

    def get_author_name(self, obj):
        if obj.createdBy:
            name = f"{obj.createdBy.first_name or ''} {obj.createdBy.last_name or ''}".strip()
            return name or obj.createdBy.username
        return None

    def get_reviewer_name(self, obj):
        if obj.reviewer:
            name = f"{obj.reviewer.first_name or ''} {obj.reviewer.last_name or ''}".strip()
            return name or obj.reviewer.username
        return None

    def get_learning_outcome_name(self, obj):
        try:
            return obj.learningOutcome.name_ar
        except Exception:
            return None

    def get_stage_name(self, obj):
        try:
            return obj.lesson.unit.class_subject.class_track.level.stage.name_ar
        except Exception:
            return None

    def get_stage_id(self, obj):
        try:
            return obj.lesson.unit.class_subject.class_track.level.stage_id
        except Exception:
            return None

    def get_class_track_name(self, obj):
        try:
            return obj.lesson.unit.class_subject.class_track.full_name
        except Exception:
            return None

    def get_class_track_id(self, obj):
        try:
            return obj.lesson.unit.class_subject.class_track_id
        except Exception:
            return None

    def get_college_name(self, obj):
        try:
            return obj.lesson.unit.semester_subject.fk_specialization.fk_college.name_ar
        except Exception:
            return None

    def get_college_id(self, obj):
        try:
            return obj.lesson.unit.semester_subject.fk_specialization.fk_college_id
        except Exception:
            return None

    def get_department_name(self, obj):
        try:
            return obj.lesson.unit.semester_subject.fk_specialization.fk_section.name_ar
        except Exception:
            return None

    def get_department_id(self, obj):
        try:
            return obj.lesson.unit.semester_subject.fk_specialization.fk_section_id
        except Exception:
            return None

    def get_specialization_name(self, obj):
        try:
            return obj.lesson.unit.semester_subject.fk_specialization.name_ar
        except Exception:
            return None

    def get_specialization_id(self, obj):
        try:
            return obj.lesson.unit.semester_subject.fk_specialization_id
        except Exception:
            return None

    def get_semester_subject_name(self, obj):
        try:
            return obj.lesson.unit.semester_subject.fk_subject.name_ar
        except Exception:
            return None

    def get_semester_subject_id(self, obj):
        try:
            return obj.lesson.unit.semester_subject_id
        except Exception:
            return None

    def get_institute_field_name(self, obj):
        try:
            if obj.institution_type == 'institute' and obj.lesson and obj.lesson.subject:
                from academic.models.institutes.InstituteSubject import InstituteSubject
                inst_sub = InstituteSubject.objects.filter(name_ar=obj.lesson.subject.name_ar).first()
                if inst_sub and inst_sub.field:
                    return inst_sub.field.name_ar
        except Exception:
            pass
        return None

    def get_institute_field_id(self, obj):
        try:
            if obj.institution_type == 'institute' and obj.lesson and obj.lesson.subject:
                from academic.models.institutes.InstituteSubject import InstituteSubject
                inst_sub = InstituteSubject.objects.filter(name_ar=obj.lesson.subject.name_ar).first()
                if inst_sub and inst_sub.field:
                    return inst_sub.field_id
        except Exception:
            pass
        return None

    def get_institute_specialization_name(self, obj):
        return None

    def get_institute_specialization_id(self, obj):
        return None
