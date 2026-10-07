from rest_framework import serializers
from academic.models.schools.SchoolLevel import SchoolLevel
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class SchoolLevelSerializer(DynamicFieldsModelSerializer):
    stage_name = serializers.CharField(source='stage.name_ar', read_only=True)
    specialization_name = serializers.CharField(source='specialization.name_ar', read_only=True)

    class Meta:
        model = SchoolLevel
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

LevelSerializer = SchoolLevelSerializer
