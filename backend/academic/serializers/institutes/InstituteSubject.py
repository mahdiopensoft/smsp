from rest_framework import serializers
from academic.models.institutes.InstituteSubject import InstituteSubject
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class InstituteSubjectSerializer(DynamicFieldsModelSerializer):
    field_name = serializers.CharField(source='field.name_ar', read_only=True)
    subject_type_display = serializers.CharField(source='get_subject_type_display', read_only=True)
    subject_entity_display = serializers.CharField(source='get_subject_entity_display', read_only=True)
    academic_category_display = serializers.CharField(source='get_academic_category_display', read_only=True)

    class Meta:
        model = InstituteSubject
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
