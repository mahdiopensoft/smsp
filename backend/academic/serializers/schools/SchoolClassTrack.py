from rest_framework import serializers
from academic.models.schools.SchoolClassTrack import SchoolClassTrack
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class SchoolClassTrackSerializer(DynamicFieldsModelSerializer):
    level_name = serializers.CharField(source='level.name_ar', read_only=True)
    track_name = serializers.CharField(source='track.name_ar', read_only=True)
    full_name = serializers.CharField(read_only=True)
    name_ar = serializers.CharField(source='full_name', read_only=True)

    class Meta:
        model = SchoolClassTrack
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

ClassTrackSerializer = SchoolClassTrackSerializer
