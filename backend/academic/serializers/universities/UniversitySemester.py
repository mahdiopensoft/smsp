from rest_framework import serializers
from academic.models.universities.UniversitySemester import UniversitySemester
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class UniversitySemesterSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = UniversitySemester
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

SemesterSerializer = UniversitySemesterSerializer
