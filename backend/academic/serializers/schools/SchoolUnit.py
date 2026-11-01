from rest_framework import serializers
from academic.models.schools.SchoolUnit import SchoolUnit
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class SchoolUnitSerializer(DynamicFieldsModelSerializer):
    semester_name = serializers.CharField(source='semester.name_ar', read_only=True)
    class_subject_name = serializers.CharField(source='class_subject.__str__', read_only=True)
    subject_name = serializers.SerializerMethodField(read_only=True)
    class_track = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = SchoolUnit
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def get_subject_name(self, obj):
        if obj.school_subject:
            return obj.school_subject.name_ar
        if obj.class_subject:
            if getattr(obj.class_subject, 'school_subject', None):
                return obj.class_subject.school_subject.name_ar
            if getattr(obj.class_subject, 'subject', None):
                return obj.class_subject.subject.name_ar
        return None

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.class_subject and instance.class_subject.class_track_id:
            ret['class_track'] = instance.class_subject.class_track_id
        return ret

    def validate(self, attrs):
        class_track_id = attrs.get('class_track')
        if class_track_id is None and self.instance and self.instance.class_subject:
            class_track_id = self.instance.class_subject.class_track_id

        school_subject = attrs.get('school_subject')
        if school_subject is None and self.instance:
            school_subject = self.instance.school_subject

        semester = attrs.get('semester')
        if semester is None and self.instance:
            semester = self.instance.semester
        semester_id = semester.id if hasattr(semester, 'id') else semester

        class_subject = attrs.get('class_subject')
        if not class_subject and self.instance:
            class_subject = self.instance.class_subject

        if not class_subject and class_track_id and school_subject:
            from academic.models.schools.SchoolClassSubject import SchoolClassSubject
            subj_id = school_subject.id if hasattr(school_subject, 'id') else school_subject
            class_subject = SchoolClassSubject.objects.filter(
                class_track_id=class_track_id,
                school_subject_id=subj_id
            ).first()
            if not class_subject:
                class_subject = SchoolClassSubject.objects.filter(
                    class_track_id=class_track_id,
                    subject_id=subj_id
                ).first()

        name_ar = attrs.get('name_ar')
        if name_ar is None and self.instance:
            name_ar = self.instance.name_ar
        name_ar = (name_ar or '').strip()

        order = attrs.get('order')
        if order is None and self.instance:
            order = self.instance.order

        instance_id = self.instance.id if self.instance else None

        if class_subject:
            # 1. Uniqueness check for order
            if order is not None:
                qs_order = SchoolUnit.objects.filter(
                    class_subject=class_subject,
                    semester_id=semester_id,
                    order=order,
                    is_deleted=False
                )
                if instance_id:
                    qs_order = qs_order.exclude(id=instance_id)
                if qs_order.exists():
                    raise serializers.ValidationError({
                        'order': f'ترتيب الوحدة رقم ({order}) مستخدم بالفعل لهذا الصف والمسار والمادة والفصل الدراسي.'
                    })

            # 2. Uniqueness check for name_ar
            if name_ar:
                qs_name = SchoolUnit.objects.filter(
                    class_subject=class_subject,
                    semester_id=semester_id,
                    name_ar=name_ar,
                    is_deleted=False
                )
                if instance_id:
                    qs_name = qs_name.exclude(id=instance_id)
                if qs_name.exists():
                    raise serializers.ValidationError({
                        'name_ar': 'الوحدة الدراسية بهذا الاسم موجودة مسبقاً لهذا الصف والمسار والمادة والفصل الدراسي.'
                    })

            # 3. Uniqueness check for name_en (if provided)
            name_en = attrs.get('name_en')
            if name_en is None and self.instance:
                name_en = self.instance.name_en
            name_en = (name_en or '').strip()
            if name_en:
                qs_en = SchoolUnit.objects.filter(
                    class_subject=class_subject,
                    semester_id=semester_id,
                    name_en=name_en,
                    is_deleted=False
                )
                if instance_id:
                    qs_en = qs_en.exclude(id=instance_id)
                if qs_en.exists():
                    raise serializers.ValidationError({
                        'name_en': 'اسم الوحدة باللغة الإنجليزية موجود مسبقاً لهذا الصف والمسار والمادة والفصل الدراسي.'
                    })

        return super().validate(attrs)

    def create(self, validated_data):
        class_track_id = validated_data.pop('class_track', None)
        school_subject = validated_data.get('school_subject')
        if class_track_id and school_subject and not validated_data.get('class_subject'):
            from academic.models.schools.SchoolClassSubject import SchoolClassSubject
            subj_id = school_subject.id if hasattr(school_subject, 'id') else school_subject
            cs = SchoolClassSubject.objects.filter(
                class_track_id=class_track_id,
                school_subject_id=subj_id
            ).first()
            if not cs:
                cs = SchoolClassSubject.objects.filter(
                    class_track_id=class_track_id,
                    subject_id=subj_id
                ).first()
            if cs:
                validated_data['class_subject'] = cs
        return super().create(validated_data)

    def update(self, instance, validated_data):
        class_track_id = validated_data.pop('class_track', None)
        school_subject = validated_data.get('school_subject', instance.school_subject)
        if class_track_id and school_subject:
            from academic.models.schools.SchoolClassSubject import SchoolClassSubject
            subj_id = school_subject.id if hasattr(school_subject, 'id') else school_subject
            cs = SchoolClassSubject.objects.filter(
                class_track_id=class_track_id,
                school_subject_id=subj_id
            ).first()
            if not cs:
                cs = SchoolClassSubject.objects.filter(
                    class_track_id=class_track_id,
                    subject_id=subj_id
                ).first()
            if cs:
                validated_data['class_subject'] = cs
        return super().update(instance, validated_data)
