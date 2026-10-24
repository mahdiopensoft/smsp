from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from academic.models.schools.SchoolTrack import SchoolTrack
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class SchoolTrackSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = SchoolTrack
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
            qs_ar = SchoolTrack.objects.filter(
                name_ar__iexact=name_ar_clean,
                is_deleted=False
            )
            if instance_id:
                qs_ar = qs_ar.exclude(id=instance_id)
            if qs_ar.exists():
                raise serializers.ValidationError({
                    "name_ar": _("اسم المسار باللغة العربية مسجل مسبقاً، يرجى إدخال اسم فريد.")
                })

        # 2. التحقق من تفرد الاسم باللغة الإنجليزية (name_en)
        name_en = attrs.get('name_en')
        if name_en is None and self.instance:
            name_en = self.instance.name_en
        if name_en is not None and str(name_en).strip():
            name_en_clean = str(name_en).strip()
            qs_en = SchoolTrack.objects.filter(
                name_en__iexact=name_en_clean,
                is_deleted=False
            )
            if instance_id:
                qs_en = qs_en.exclude(id=instance_id)
            if qs_en.exists():
                raise serializers.ValidationError({
                    "name_en": _("اسم المسار باللغة الإنجليزية مسجل مسبقاً، يرجى إدخال اسم فريد.")
                })

        # 3. التحقق من تفرد الكود (code)
        code = attrs.get('code')
        if code is None and self.instance:
            code = self.instance.code
        if code is not None and str(code).strip():
            code_clean = str(code).strip()
            qs_code = SchoolTrack.objects.filter(
                code__iexact=code_clean,
                is_deleted=False
            )
            if instance_id:
                qs_code = qs_code.exclude(id=instance_id)
            if qs_code.exists():
                raise serializers.ValidationError({
                    "code": _("كود المسار مسجل لمسار آخر مسبقاً، يرجى اختيار كود فريد.")
                })

        return attrs

TrackSerializer = SchoolTrackSerializer

