from rest_framework import serializers
from academic.models.institutes.InstituteBatch import InstituteBatch
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class InstituteBatchSerializer(DynamicFieldsModelSerializer):
    specialization_name = serializers.CharField(source='specialization.name_ar', read_only=True)
    curriculum_name = serializers.CharField(source='curriculum.name_ar', read_only=True)
    academic_year_name = serializers.CharField(source='academic_year.__str__', read_only=True)

    class Meta:
        model = InstituteBatch
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
