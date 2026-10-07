from rest_framework import serializers
from academic.models.universities.UniversityGradeDistribution import UniversityGradeDistribution
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class UniversityGradeDistributionSerializer(DynamicFieldsModelSerializer):
    grading_system_name = serializers.CharField(source='fk_grading_system.name_ar', read_only=True)
    type_of_grade_name = serializers.CharField(source='fk_type_of_grade.name_ar', read_only=True)

    class Meta:
        model = UniversityGradeDistribution
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

GradeDistributionSerializer = UniversityGradeDistributionSerializer
