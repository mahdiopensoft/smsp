from rest_framework import serializers
from academic.models.universities.UniversitySpecializationBranch import UniversitySpecializationBranch
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class UniversitySpecializationBranchSerializer(DynamicFieldsModelSerializer):
    specialization_name = serializers.CharField(source='fk_specialization.name_ar', read_only=True)
    branch_name = serializers.CharField(source='fk_branch.name_ar', read_only=True)

    class Meta:
        model = UniversitySpecializationBranch
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

SpecializationBranchSerializer = UniversitySpecializationBranchSerializer
