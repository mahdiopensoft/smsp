from rest_framework import serializers
from academic.models.universities.UniversitySpecialization import UniversitySpecialization
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class UniversitySpecializationSerializer(DynamicFieldsModelSerializer):
    college_name = serializers.CharField(source='fk_college.name_ar', read_only=True)
    department_name = serializers.CharField(source='fk_section.name_ar', read_only=True)
    educational_level_name = serializers.CharField(source='fk_educational_levels.name_ar', read_only=True)

    class Meta:
        model = UniversitySpecialization
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

SpecializationSerializer = UniversitySpecializationSerializer
