from rest_framework import serializers
from academic.models.institutes.InstituteEducationSystem import InstituteEducationSystem
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class InstituteEducationSystemSerializer(DynamicFieldsModelSerializer):
    system_type_display = serializers.CharField(source='get_system_type_display', read_only=True)
    study_nature_display = serializers.CharField(source='get_study_nature_display', read_only=True)
    grading_calculation_method_display = serializers.CharField(source='get_grading_calculation_method_display', read_only=True)

    class Meta:
        model = InstituteEducationSystem
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
