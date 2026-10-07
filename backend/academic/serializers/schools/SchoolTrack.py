from rest_framework import serializers
from academic.models.schools.SchoolTrack import SchoolTrack
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class SchoolTrackSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = SchoolTrack
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

TrackSerializer = SchoolTrackSerializer
