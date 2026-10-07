from rest_framework import serializers
from academic.models.institutes.InstituteLevel import InstituteLevel
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class InstituteLevelSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = InstituteLevel
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
