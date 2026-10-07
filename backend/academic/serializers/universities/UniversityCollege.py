from rest_framework import serializers
from academic.models.universities.UniversityCollege import UniversityCollege
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class UniversityCollegeSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = UniversityCollege
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

CollegeSerializer = UniversityCollegeSerializer
