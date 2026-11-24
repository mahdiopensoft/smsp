from rest_framework import serializers
from academic.models.institutes.InstituteLesson import InstituteLesson
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class InstituteLessonSerializer(DynamicFieldsModelSerializer):
    unit_name = serializers.CharField(source='unit.name_ar', read_only=True)
    subject_name = serializers.CharField(source='subject.name_ar', read_only=True)

    class Meta:
        model = InstituteLesson
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
