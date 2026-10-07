from rest_framework import serializers
from academic.models.universities.UniversityCourseCLO import UniversityCourseCLO
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class UniversityCourseCLOSerializer(DynamicFieldsModelSerializer):
    course_code = serializers.CharField(source='course.course_code', read_only=True)
    course_name = serializers.CharField(source='course.name_ar', read_only=True)
    topic_name = serializers.CharField(source='topic.name_ar', read_only=True)

    class Meta:
        model = UniversityCourseCLO
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

CourseCLOSerializer = UniversityCourseCLOSerializer
