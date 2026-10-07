from rest_framework import serializers
from academic.models.universities.UniversityLevel import UniversityLevel
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class UniversityLevelSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = UniversityLevel
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

EducationalLevelsSerializer = UniversityLevelSerializer
