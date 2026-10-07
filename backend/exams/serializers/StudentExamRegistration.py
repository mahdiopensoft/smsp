from rest_framework import serializers
from exams.models.StudentExamRegistration import StudentExamRegistration

class StudentExamRegistrationSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField(read_only=True)
    exam_title = serializers.SerializerMethodField(read_only=True)
    exam_version_code = serializers.SerializerMethodField(read_only=True)
    subject_name = serializers.SerializerMethodField(read_only=True)
    academic_year_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StudentExamRegistration
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def get_student_name(self, obj):
        if obj.student:
            full_name = f"{obj.student.first_name or ''} {obj.student.last_name or ''}".strip()
            return full_name or obj.student.username
        return ""

    def get_exam_title(self, obj):
        try:
            return obj.examVersion.exam.title
        except Exception:
            return ""

    def get_exam_version_code(self, obj):
        try:
            return f"نموذج {obj.examVersion.version_code}"
        except Exception:
            return ""

    def get_subject_name(self, obj):
        try:
            subject = obj.examVersion.exam.subject
            return getattr(subject, 'name_ar', None) or getattr(subject, 'name_en', None) or str(subject)
        except Exception:
            return ""

    def get_academic_year_name(self, obj):
        try:
            year = obj.examVersion.exam.year
            return getattr(year, 'name_ar', None) or getattr(year, 'name_en', None) or str(year)
        except Exception:
            return ""
