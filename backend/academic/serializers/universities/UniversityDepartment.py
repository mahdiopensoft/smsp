from rest_framework import serializers
from academic.models.universities.UniversityDepartment import UniversityDepartment
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class UniversityDepartmentSerializer(DynamicFieldsModelSerializer):
    college_name = serializers.CharField(source='fk_college.name_ar', read_only=True)

    class Meta:
        model = UniversityDepartment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

DepartmentSerializer = UniversityDepartmentSerializer
