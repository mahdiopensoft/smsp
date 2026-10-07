from rest_framework import serializers
from academic.models.common.Subject import Subject
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class SubjectSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
