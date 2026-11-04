from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from academic.models.universities.UniversityUnit import UniversityUnit
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class UniversityUnitSerializer(DynamicFieldsModelSerializer):
    semester_name = serializers.CharField(source='semester.name_ar', read_only=True)
    semester_subject_name = serializers.CharField(source='semester_subject.__str__', read_only=True)
    subject_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UniversityUnit
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def get_subject_name(self, obj):
        try:
            if obj.semester_subject:
                if getattr(obj.semester_subject, 'fk_subject', None):
                    return obj.semester_subject.fk_subject.name_ar
                if getattr(obj.semester_subject, 'course', None):
                    return obj.semester_subject.course.name_ar
            return None
        except Exception:
            return None

    def validate(self, attrs):
        semester_subject = attrs.get('semester_subject')
        if semester_subject is None and self.instance:
            semester_subject = self.instance.semester_subject

        semester = attrs.get('semester')
        if semester is None and self.instance:
            semester = self.instance.semester
        semester_id = semester.id if hasattr(semester, 'id') else semester

        name_ar = attrs.get('name_ar')
        if name_ar is None and self.instance:
            name_ar = self.instance.name_ar
        name_ar = (name_ar or '').strip()

        order = attrs.get('order')
        if order is None and self.instance:
            order = self.instance.order

        instance_id = self.instance.id if self.instance else None

        if semester_subject:
            # 1. Uniqueness check for order
            if order is not None:
                qs_order = UniversityUnit.objects.filter(
                    semester_subject=semester_subject,
                    semester_id=semester_id,
                    order=order,
                    is_deleted=False
                )
                if instance_id:
                    qs_order = qs_order.exclude(id=instance_id)
                if qs_order.exists():
                    raise serializers.ValidationError({
                        'order': f'ترتيب الوحدة رقم ({order}) مستخدم بالفعل لهذا المقرر والفصل الدراسي.'
                    })

            # 2. Uniqueness check for name_ar
            if name_ar:
                qs_name = UniversityUnit.objects.filter(
                    semester_subject=semester_subject,
                    semester_id=semester_id,
                    name_ar__iexact=name_ar,
                    is_deleted=False
                )
                if instance_id:
                    qs_name = qs_name.exclude(id=instance_id)
                if qs_name.exists():
                    raise serializers.ValidationError({
                        'name_ar': f'الوحدة الدراسية بهذا الاسم ({name_ar}) موجودة مسبقاً لهذا المقرر والفصل الدراسي.'
                    })

            # 3. Uniqueness check for name_en (if provided)
            name_en = attrs.get('name_en')
            if name_en is None and self.instance:
                name_en = self.instance.name_en
            name_en = (name_en or '').strip()
            if name_en:
                qs_en = UniversityUnit.objects.filter(
                    semester_subject=semester_subject,
                    semester_id=semester_id,
                    name_en__iexact=name_en,
                    is_deleted=False
                )
                if instance_id:
                    qs_en = qs_en.exclude(id=instance_id)
                if qs_en.exists():
                    raise serializers.ValidationError({
                        'name_en': f'اسم الوحدة بالإنجليزية ({name_en}) موجود مسبقاً لهذا المقرر والفصل الدراسي.'
                    })

        return super().validate(attrs)

UnitSerializer = UniversityUnitSerializer

