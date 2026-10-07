from rest_framework import serializers
from academic.models.universities.UniversityGradingSystem import UniversityGradingSystem
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class UniversityGradingSystemSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = UniversityGradingSystem
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

GradingSystemSerializer = UniversityGradingSystemSerializer
