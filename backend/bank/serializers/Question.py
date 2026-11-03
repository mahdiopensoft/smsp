from rest_framework import serializers
from django.db import transaction
from bank.models.Question import Question
from bank.models.Answer import Answer
from bank.serializers.Base64ImageField import Base64ImageField

class AnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Answer
        fields = ['id', 'question', 'text', 'image', 'latex', 'isTrue', 'order_index']
        extra_kwargs = {
            'question': {'required': False}
        }

class QuestionListSerializer(serializers.ModelSerializer):
    """
    Lightweight, high-performance serializer for Question Bank Table / List.
    - Eliminates redundant relational trees
    - Excludes sensitive answer options (isTrue) from the list endpoint
    - Reduces JSON payload by >90%
    - Provides audit & tracking fields (creator, last modifier, edit count, timestamps)
    """
    subject_name = serializers.SerializerMethodField(read_only=True)
    unit_name = serializers.SerializerMethodField(read_only=True)
    lesson_name = serializers.SerializerMethodField(read_only=True)
    author_name = serializers.SerializerMethodField(read_only=True)
    created_by_username = serializers.SerializerMethodField(read_only=True)
    last_modified_by = serializers.SerializerMethodField(read_only=True)
    last_modified_at = serializers.SerializerMethodField(read_only=True)
    last_action = serializers.SerializerMethodField(read_only=True)
    reviewer_name = serializers.SerializerMethodField(read_only=True)
    edit_count = serializers.SerializerMethodField(read_only=True)
    is_imported = serializers.SerializerMethodField(read_only=True)
    import_source = serializers.SerializerMethodField(read_only=True)

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
            'import_session',
            'is_imported',
            'import_source',
            'subject_name',
            'unit_name',
            'lesson_name',
            'author_name',
            'created_by_username',
            'last_modified_by',
            'last_modified_at',
            'last_action',
            'reviewer_name',
            'edit_count',
            'created_at',
            'approved_at',
        ]

    def _preload_audit_logs(self, instances):
        unfetched = [i for i in instances if not hasattr(i, '_cached_last_update_log')]
        if not unfetched:
            return
        from bank.models.AuditLog import AuditLog
        ids = [str(i.id) for i in unfetched]
        logs = AuditLog.objects.filter(
            resource_type='Question',
            resource_id__in=ids,
            action__in=['تعديل', 'اعتماد', 'رفض', 'إصدار جديد', 'أرشفة', 'استعادة']
        ).select_related('user').order_by('resource_id', '-created_at')

        log_map = {}
        for l in logs:
            if l.resource_id not in log_map:
                log_map[l.resource_id] = l
        for i in unfetched:
            i._cached_last_update_log = log_map.get(str(i.id), None)

    def _get_last_log(self, obj):
        if not hasattr(obj, '_cached_last_update_log'):
            parent = getattr(self, 'parent', None)
            if parent and hasattr(parent, 'instance') and isinstance(parent.instance, (list, tuple)):
                self._preload_audit_logs(parent.instance)
            else:
                from bank.models.AuditLog import AuditLog
                obj._cached_last_update_log = AuditLog.objects.filter(
                    resource_type='Question',
                    resource_id=str(obj.id),
                    action__in=['تعديل', 'اعتماد', 'رفض', 'إصدار جديد', 'أرشفة', 'استعادة']
                ).select_related('user').order_by('-created_at').first()
        return getattr(obj, '_cached_last_update_log', None)

    def get_author_name(self, obj):
        if obj.createdBy:
            name = f"{obj.createdBy.first_name or ''} {obj.createdBy.last_name or ''}".strip()
            return name or obj.createdBy.username
        return None

    def get_created_by_username(self, obj):
        return obj.createdBy.username if obj.createdBy else None

    def get_reviewer_name(self, obj):
        if obj.reviewer:
            name = f"{obj.reviewer.first_name or ''} {obj.reviewer.last_name or ''}".strip()
            return name or obj.reviewer.username
        return None

    def get_last_modified_by(self, obj):
        log = self._get_last_log(obj)
        if log and log.user:
            name = f"{log.user.first_name or ''} {log.user.last_name or ''}".strip()
            return name or log.user.username
        return None

    def get_last_modified_at(self, obj):
        log = self._get_last_log(obj)
        if log:
            return log.created_at
        return None

    def get_last_action(self, obj):
        log = self._get_last_log(obj)
        if log:
            return log.action
        return None

    def get_edit_count(self, obj):
        try:
            if hasattr(obj, 'metrics') and obj.metrics:
                return obj.metrics.edit_count or 0
        except Exception:
            pass
        return 0

    def get_subject_name(self, obj):
        try:
            if obj.lesson:
                if getattr(obj.lesson, 'subject', None):
                    return obj.lesson.subject.name_ar
                unit = getattr(obj.lesson, 'unit', None)
                if unit:
                    if hasattr(unit, 'class_subject') and unit.class_subject and getattr(unit.class_subject, 'subject', None):
                        return unit.class_subject.subject.name_ar
                    ss = getattr(unit, 'semester_subject', None)
                    if ss:
                        if getattr(ss, 'fk_subject', None):
                            return ss.fk_subject.name_ar
                        elif getattr(ss, 'course', None):
                            return ss.course.name_ar
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

    def get_is_imported(self, obj):
        return bool(getattr(obj, 'import_session_id', None) or getattr(obj, 'status', None) == 'مستورد')

    def get_import_source(self, obj):
        if getattr(obj, 'import_session_id', None) or getattr(obj, 'status', None) == 'مستورد':
            return 'إكسل'
        return 'يدوي'

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
    created_by_username = serializers.SerializerMethodField(read_only=True)
    reviewer_name = serializers.SerializerMethodField(read_only=True)
    last_modified_by = serializers.SerializerMethodField(read_only=True)
    last_modified_at = serializers.SerializerMethodField(read_only=True)
    last_action = serializers.SerializerMethodField(read_only=True)
    edit_count = serializers.SerializerMethodField(read_only=True)
    is_imported = serializers.SerializerMethodField(read_only=True)
    import_source = serializers.SerializerMethodField(read_only=True)
    audit_trail = serializers.SerializerMethodField(read_only=True)

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
            used_orders = set()
            for idx, opt in enumerate(options_data):
                if isinstance(opt, dict):
                    text = opt.get('text', '')
                    image = opt.get('image', None)
                    latex = opt.get('latex', None)
                    is_true = opt.get('isTrue', False)
                    order_idx = opt.get('order_index')
                    if order_idx is None:
                        order_idx = opt.get('order')
                else:
                    text = getattr(opt, 'text', '')
                    image = getattr(opt, 'image', None)
                    latex = getattr(opt, 'latex', None)
                    is_true = getattr(opt, 'isTrue', False)
                    order_idx = getattr(opt, 'order_index', getattr(opt, 'order', None))

                try:
                    order_val = int(order_idx) if order_idx is not None else idx
                except (ValueError, TypeError):
                    order_val = idx

                if order_val < 0:
                    order_val = idx
                while order_val in used_orders:
                    order_val += 1
                used_orders.add(order_val)

                answers_to_create.append(Answer(
                    question=question,
                    text=text,
                    image=image,
                    latex=latex,
                    isTrue=is_true,
                    order_index=order_val
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
                used_orders = set()
                for idx, opt in enumerate(options_data):
                    if isinstance(opt, dict):
                        text = opt.get('text', '')
                        image = opt.get('image', None)
                        latex = opt.get('latex', None)
                        is_true = opt.get('isTrue', False)
                        order_idx = opt.get('order_index')
                        if order_idx is None:
                            order_idx = opt.get('order')
                    else:
                        text = getattr(opt, 'text', '')
                        image = getattr(opt, 'image', None)
                        latex = getattr(opt, 'latex', None)
                        is_true = getattr(opt, 'isTrue', False)
                        order_idx = getattr(opt, 'order_index', getattr(opt, 'order', None))

                    try:
                        order_val = int(order_idx) if order_idx is not None else idx
                    except (ValueError, TypeError):
                        order_val = idx

                    if order_val < 0:
                        order_val = idx
                    while order_val in used_orders:
                        order_val += 1
                    used_orders.add(order_val)

                    answers_to_create.append(Answer(
                        question=instance,
                        text=text,
                        image=image,
                        latex=latex,
                        isTrue=is_true,
                        order_index=order_val
                    ))
                if answers_to_create:
                    Answer.objects.bulk_create(answers_to_create)
                    
            return instance


    def get_subject_name(self, obj):
        try:
            if obj.lesson:
                if getattr(obj.lesson, 'subject', None):
                    return obj.lesson.subject.name_ar
                unit = getattr(obj.lesson, 'unit', None)
                if unit:
                    if hasattr(unit, 'class_subject') and unit.class_subject and getattr(unit.class_subject, 'subject', None):
                        return unit.class_subject.subject.name_ar
                    ss = getattr(unit, 'semester_subject', None)
                    if ss:
                        if getattr(ss, 'fk_subject', None):
                            return ss.fk_subject.name_ar
                        elif getattr(ss, 'course', None):
                            return ss.course.name_ar
        except Exception:
            pass
        return None

    def get_subject_id(self, obj):
        try:
            if obj.lesson:
                if getattr(obj.lesson, 'subject_id', None):
                    return obj.lesson.subject_id
                unit = getattr(obj.lesson, 'unit', None)
                if unit:
                    if hasattr(unit, 'class_subject') and unit.class_subject:
                        return getattr(unit.class_subject, 'subject_id', None)
                    ss = getattr(unit, 'semester_subject', None)
                    if ss:
                        if getattr(ss, 'fk_subject_id', None):
                            return ss.fk_subject_id
                        elif getattr(ss, 'course_id', None):
                            return ss.course_id
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

    def _get_last_log(self, obj):
        if not hasattr(obj, '_cached_last_update_log'):
            from bank.models.AuditLog import AuditLog
            obj._cached_last_update_log = AuditLog.objects.filter(
                resource_type='Question',
                resource_id=str(obj.id),
                action__in=['تعديل', 'اعتماد', 'رفض', 'إصدار جديد', 'أرشفة', 'استعادة']
            ).select_related('user').order_by('-created_at').first()
        return obj._cached_last_update_log

    def get_author_name(self, obj):
        if obj.createdBy:
            name = f"{obj.createdBy.first_name or ''} {obj.createdBy.last_name or ''}".strip()
            return name or obj.createdBy.username
        return None

    def get_created_by_username(self, obj):
        return obj.createdBy.username if obj.createdBy else None

    def get_reviewer_name(self, obj):
        if obj.reviewer:
            name = f"{obj.reviewer.first_name or ''} {obj.reviewer.last_name or ''}".strip()
            return name or obj.reviewer.username
        return None

    def get_last_modified_by(self, obj):
        log = self._get_last_log(obj)
        if log and log.user:
            name = f"{log.user.first_name or ''} {log.user.last_name or ''}".strip()
            return name or log.user.username
        return None

    def get_last_modified_at(self, obj):
        log = self._get_last_log(obj)
        if log:
            return log.created_at
        return None

    def get_last_action(self, obj):
        log = self._get_last_log(obj)
        if log:
            return log.action
        return None

    def get_edit_count(self, obj):
        try:
            if hasattr(obj, 'metrics') and obj.metrics:
                return obj.metrics.edit_count or 0
        except Exception:
            pass
        return 0

    def get_audit_trail(self, obj):
        from bank.models.AuditLog import AuditLog
        logs = AuditLog.objects.filter(
            resource_type='Question',
            resource_id=str(obj.id)
        ).select_related('user').order_by('-created_at')[:30]

        trail = []
        for l in logs:
            user_full = ""
            if l.user:
                user_full = f"{l.user.first_name or ''} {l.user.last_name or ''}".strip() or l.user.username
            trail.append({
                'id': l.id,
                'action': l.action,
                'user_name': user_full or 'النظام',
                'username': l.user.username if l.user else 'system',
                'description': l.description,
                'created_at': l.created_at.strftime('%Y-%m-%d %H:%M:%S') if l.created_at else None,
                'ip_address': l.ip_address,
            })

        has_create = any(t['action'] in ['إنشاء', 'استيراد جماعي'] for t in trail)
        if not has_create and (obj.createdBy or obj.created_at):
            creator_full = ""
            if obj.createdBy:
                creator_full = f"{obj.createdBy.first_name or ''} {obj.createdBy.last_name or ''}".strip() or obj.createdBy.username
            is_imp = bool(getattr(obj, 'import_session_id', None) or obj.status == 'مستورد')
            action_name = 'استيراد جماعي' if is_imp else 'إنشاء'
            action_desc = f"تم استيراد السؤال #{obj.id} من ملف إكسل ({obj.questionType})" if is_imp else f"إنشاء السؤال #{obj.id} ({obj.questionType})"
            trail.append({
                'id': 'initial',
                'action': action_name,
                'user_name': creator_full or 'مستخدم النظام',
                'username': obj.createdBy.username if obj.createdBy else 'system',
                'description': action_desc,
                'created_at': obj.created_at.strftime('%Y-%m-%d %H:%M:%S') if obj.created_at else None,
                'ip_address': None,
            })
        return trail

    def get_is_imported(self, obj):
        return bool(getattr(obj, 'import_session_id', None) or getattr(obj, 'status', None) == 'مستورد')

    def get_import_source(self, obj):
        if getattr(obj, 'import_session_id', None) or getattr(obj, 'status', None) == 'مستورد':
            return 'إكسل'
        return 'يدوي'

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
