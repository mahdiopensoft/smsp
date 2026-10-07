from rest_framework import serializers
from academic.models.universities.UniversityCourse import UniversityCourse
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class UniversityCourseSerializer(DynamicFieldsModelSerializer):
    college_name = serializers.CharField(source='college.name_ar', read_only=True)
    department_name = serializers.CharField(source='department.name_ar', read_only=True)
    prerequisite_name = serializers.CharField(source='prerequisite_course.name_ar', read_only=True)
    full_title = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UniversityCourse
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def get_full_title(self, obj):
        return f"{obj.course_code} - {obj.name_ar}" if obj.course_code else obj.name_ar
