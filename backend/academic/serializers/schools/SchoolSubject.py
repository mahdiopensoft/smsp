from rest_framework import serializers
from academic.models.schools.SchoolSubject import SchoolSubject
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class SchoolSubjectSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = SchoolSubject
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
