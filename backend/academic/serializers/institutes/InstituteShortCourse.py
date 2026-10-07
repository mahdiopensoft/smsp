from rest_framework import serializers
from academic.models.institutes.InstituteShortCourse import InstituteShortCourse
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class InstituteShortCourseSerializer(DynamicFieldsModelSerializer):
    field_name = serializers.CharField(source='field.name_ar', read_only=True)
    organization_name = serializers.CharField(source='organization.name_ar', read_only=True)

    class Meta:
        model = InstituteShortCourse
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
