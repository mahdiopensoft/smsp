from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from academic.models.schools.SchoolLevel import SchoolLevel
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class SchoolLevelSerializer(DynamicFieldsModelSerializer):
    stage_name = serializers.CharField(source='stage.name_ar', read_only=True)
    specialization_name = serializers.CharField(source='specialization.name_ar', read_only=True)

    class Meta:
        model = SchoolLevel
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def validate(self, attrs):
        instance_id = self.instance.id if self.instance else None

        # 1. التحقق من تفرد الاسم باللغة العربية (name_ar)
        name_ar = attrs.get('name_ar')
        if name_ar is None and self.instance:
            name_ar = self.instance.name_ar
        if name_ar is not None and str(name_ar).strip():
            name_ar_clean = str(name_ar).strip()
            qs_ar = SchoolLevel.objects.filter(
                name_ar__iexact=name_ar_clean,
                is_deleted=False
            )
            if instance_id:
                qs_ar = qs_ar.exclude(id=instance_id)
            if qs_ar.exists():
                raise serializers.ValidationError({
                    "name_ar": _("اسم الصف الدراسي باللغة العربية مسجل مسبقاً، يرجى إدخال اسم فريد.")
                })

        # 2. التحقق من تفرد الاسم باللغة الإنجليزية (name_en)
        name_en = attrs.get('name_en')
        if name_en is None and self.instance:
            name_en = self.instance.name_en
        if name_en is not None and str(name_en).strip():
            name_en_clean = str(name_en).strip()
            qs_en = SchoolLevel.objects.filter(
                name_en__iexact=name_en_clean,
                is_deleted=False
            )
            if instance_id:
                qs_en = qs_en.exclude(id=instance_id)
            if qs_en.exists():
                raise serializers.ValidationError({
                    "name_en": _("اسم الصف الدراسي باللغة الإنجليزية مسجل مسبقاً، يرجى إدخال اسم فريد.")
                })

        # 3. التحقق من تفرد الترتيب (order)
        order = attrs.get('order')
        if order is None and self.instance:
            order = self.instance.order
        if order is not None:
            qs_order = SchoolLevel.objects.filter(
                order=order,
                is_deleted=False
            )
            if instance_id:
                qs_order = qs_order.exclude(id=instance_id)
            if qs_order.exists():
                raise serializers.ValidationError({
                    "order": _("رقم الترتيب مسجل لصف دراسي آخر مسبقاً، يرجى اختيار رقم ترتيب فريد.")
                })

        return attrs

LevelSerializer = SchoolLevelSerializer

