from rest_framework import serializers
from academic.models.institutes.InstituteSemester import InstituteSemester
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class InstituteSemesterSerializer(DynamicFieldsModelSerializer):
    semester_nature_display = serializers.CharField(source='get_semester_nature_display', read_only=True)

    class Meta:
        model = InstituteSemester
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
