from rest_framework import serializers
from academic.models.schools.SchoolStage import SchoolStage
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class SchoolStageSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = SchoolStage
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

EducationalStageSerializer = SchoolStageSerializer
