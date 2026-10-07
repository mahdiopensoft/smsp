from rest_framework import serializers
from academic.models.institutes.InstituteAdmissionRequirement import InstituteAdmissionRequirement
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class InstituteAdmissionRequirementSerializer(DynamicFieldsModelSerializer):
    education_system_name = serializers.CharField(source='education_system.name_ar', read_only=True)
    specialization_name = serializers.CharField(source='specialization.name_ar', read_only=True)

    class Meta:
        model = InstituteAdmissionRequirement
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
