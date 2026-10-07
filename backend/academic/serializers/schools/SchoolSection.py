from rest_framework import serializers
from academic.models.schools.SchoolSection import SchoolSection
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class SchoolSectionSerializer(DynamicFieldsModelSerializer):
    organization_name = serializers.CharField(source='organization.name_ar', read_only=True)
    class_track_name = serializers.CharField(source='class_track.full_name', read_only=True)
    year_name = serializers.CharField(source='academic_year.name', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        model = SchoolSection
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
