from rest_framework import serializers
from academic.models.institutes.InstituteField import InstituteField
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class InstituteFieldSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = InstituteField
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
