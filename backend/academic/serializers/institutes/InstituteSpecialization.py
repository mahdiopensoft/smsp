from rest_framework import serializers
from academic.models.institutes.InstituteSpecialization import InstituteSpecialization
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class InstituteSpecializationSerializer(DynamicFieldsModelSerializer):
    field_name = serializers.CharField(source='field.name_ar', read_only=True)
    education_system_name = serializers.CharField(source='education_system.name_ar', read_only=True)
    organization_name = serializers.CharField(source='organization.name_ar', read_only=True)

    class Meta:
        model = InstituteSpecialization
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
