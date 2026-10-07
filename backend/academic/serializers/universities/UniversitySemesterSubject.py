from rest_framework import serializers
from academic.models.universities.UniversitySemesterSubject import UniversitySemesterSubject
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class UniversitySemesterSubjectSerializer(DynamicFieldsModelSerializer):
    subject_name = serializers.CharField(source='fk_subject.name_ar', read_only=True)
    subject_code = serializers.CharField(source='fk_subject.subject_code', read_only=True)
    course_name = serializers.CharField(source='course.name_ar', read_only=True)
    course_code = serializers.CharField(source='course.course_code', read_only=True)
    semester_name = serializers.CharField(source='semester.name_ar', read_only=True)
    specialization_name = serializers.CharField(source='fk_specialization.name_ar', read_only=True)
    college_name = serializers.CharField(source='fk_specialization.fk_college.name_ar', read_only=True)
    name_ar = serializers.SerializerMethodField(read_only=True)

    def get_name_ar(self, obj):
        try:
            spec = f"{obj.fk_specialization.name_ar} - " if obj.fk_specialization else ""
            c_name = obj.course.name_ar if obj.course else (obj.fk_subject.name_ar if obj.fk_subject else "")
            return f"{spec}{c_name} (مستوى {obj.level})"
        except Exception:
            return str(obj)

    class Meta:
        model = UniversitySemesterSubject
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

SemesterSubjectSerializer = UniversitySemesterSubjectSerializer
