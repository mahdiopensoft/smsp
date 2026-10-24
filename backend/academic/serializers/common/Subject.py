from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from academic.models.common.Subject import Subject
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class SubjectSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def validate(self, attrs):
        instance_id = self.instance.id if self.instance else None

        # 1. التحقق من تفرد اسم المادة بالعربية (name_ar)
        name_ar = attrs.get('name_ar')
        if name_ar is None and self.instance:
            name_ar = self.instance.name_ar
        if name_ar is not None and str(name_ar).strip():
            name_ar_clean = str(name_ar).strip()
            qs_ar = Subject.objects.filter(
                name_ar__iexact=name_ar_clean,
                is_deleted=False
            )
            if instance_id:
                qs_ar = qs_ar.exclude(id=instance_id)
            if qs_ar.exists():
                raise serializers.ValidationError({
                    "name_ar": _("اسم المادة باللغة العربية مسجل مسبقاً، يرجى إدخال اسم فريد.")
                })

        # 2. التحقق من تفرد اسم المادة بالإنجليزية (name_en)
        name_en = attrs.get('name_en')
        if name_en is None and self.instance:
            name_en = self.instance.name_en
        if name_en is not None and str(name_en).strip():
            name_en_clean = str(name_en).strip()
            qs_en = Subject.objects.filter(
                name_en__iexact=name_en_clean,
                is_deleted=False
            )
            if instance_id:
                qs_en = qs_en.exclude(id=instance_id)
            if qs_en.exists():
                raise serializers.ValidationError({
                    "name_en": _("اسم المادة باللغة الإنجليزية مسجل مسبقاً، يرجى إدخال اسم فريد.")
                })

        # 3. التحقق من تفرد كود المادة (subject_code)
        subject_code = attrs.get('subject_code')
        if subject_code is None and self.instance:
            subject_code = self.instance.subject_code
        if subject_code is not None and str(subject_code).strip():
            code_clean = str(subject_code).strip()
            qs_code = Subject.objects.filter(
                subject_code__iexact=code_clean,
                is_deleted=False
            )
            if instance_id:
                qs_code = qs_code.exclude(id=instance_id)
            if qs_code.exists():
                raise serializers.ValidationError({
                    "subject_code": _("كود المادة مسجل مسبقاً، يرجى اختيار كود فريد.")
                })

        # 4. التحقق من تفرد ترتيب المادة (subject_order)
        subject_order = attrs.get('subject_order')
        if subject_order is None and self.instance:
            subject_order = self.instance.subject_order
        if subject_order is not None:
            qs_order = Subject.objects.filter(
                subject_order=subject_order,
                is_deleted=False
            )
            if instance_id:
                qs_order = qs_order.exclude(id=instance_id)
            if qs_order.exists():
                raise serializers.ValidationError({
                    "subject_order": _("ترتيب المادة مسجل مسبقاً، يرجى اختيار ترتيب آخر.")
                })

        return attrs

