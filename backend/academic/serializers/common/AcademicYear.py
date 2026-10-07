from rest_framework import serializers
from academic.models.common.AcademicYear import AcademicYear
from django.utils.translation import gettext_lazy as _
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class AcademicYearSerializer(DynamicFieldsModelSerializer):
    name = serializers.SerializerMethodField()
    name_ar = serializers.SerializerMethodField()

    class Meta:
        model = AcademicYear
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def get_name(self, obj):
        return str(obj)

    def get_name_ar(self, obj):
        return str(obj)

    def validate(self, attrs):
        hijri = attrs.get('hijri_year', getattr(self.instance, 'hijri_year', None))
        gregorian = attrs.get('gregorian_year', getattr(self.instance, 'gregorian_year', None))
        
        if hijri and gregorian:
            qs = AcademicYear.objects.filter(
                hijri_year=hijri.strip(), 
                gregorian_year=gregorian.strip(), 
                is_deleted=False
            )
            if self.instance:
                qs = qs.exclude(id=self.instance.id)
                
            if qs.exists():
                raise serializers.ValidationError({
                    "hijri_year": _("العام الدراسي (الهجري والميلادي) مسجل مسبقاً في النظام.")
                })
                
        return attrs
