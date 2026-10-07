from rest_framework import serializers
from academic.models.universities.UniversityCollegeSettings import UniversityCollegeSettings
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class UniversityCollegeSettingsSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = UniversityCollegeSettings
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

CollegeSettingsSerializer = UniversityCollegeSettingsSerializer
