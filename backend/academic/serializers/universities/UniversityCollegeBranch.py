from rest_framework import serializers
from academic.models.universities.UniversityCollegeBranch import UniversityCollegeBranch
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class UniversityCollegeBranchSerializer(DynamicFieldsModelSerializer):
    college_name = serializers.CharField(source='fk_college.name_ar', read_only=True)
    branch_name = serializers.CharField(source='fk_branch.name_ar', read_only=True)

    class Meta:
        model = UniversityCollegeBranch
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

CollegeBranchSerializer = UniversityCollegeBranchSerializer
