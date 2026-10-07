from rest_framework import serializers
from academic.models.universities.UniversityCourseTopic import UniversityCourseTopic
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class UniversityCourseTopicSerializer(DynamicFieldsModelSerializer):
    course_code = serializers.CharField(source='course.course_code', read_only=True)
    course_name = serializers.CharField(source='course.name_ar', read_only=True)

    class Meta:
        model = UniversityCourseTopic
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

CourseTopicSerializer = UniversityCourseTopicSerializer
