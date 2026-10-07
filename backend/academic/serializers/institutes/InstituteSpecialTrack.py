from rest_framework import serializers
from academic.models.institutes.InstituteSpecialTrack import InstituteSpecialTrack
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class InstituteSpecialTrackSerializer(DynamicFieldsModelSerializer):
    field_name = serializers.CharField(source='field.name_ar', read_only=True)
    education_system_name = serializers.CharField(source='education_system.name_ar', read_only=True)

    class Meta:
        model = InstituteSpecialTrack
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
