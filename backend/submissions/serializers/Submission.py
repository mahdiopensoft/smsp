from rest_framework import serializers
from submissions.models.Submission import Submission

class SubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField(read_only=True)
    seat_number = serializers.SerializerMethodField(read_only=True)
    exam_title = serializers.SerializerMethodField(read_only=True)
    exam_version_code = serializers.SerializerMethodField(read_only=True)
    subject_name = serializers.SerializerMethodField(read_only=True)
    institution_type = serializers.SerializerMethodField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def get_student_name(self, obj):
        try:
            if obj.registration and obj.registration.student:
                s = obj.registration.student
                full_name = f"{s.first_name or ''} {s.last_name or ''}".strip()
                return full_name or s.username
        except Exception:
            pass
        return "طالب غير محدد"

    def get_seat_number(self, obj):
        try:
            if obj.registration:
                return obj.registration.seatNumber
        except Exception:
            pass
        return "-"

    def get_exam_title(self, obj):
        try:
            return obj.exam.title
        except Exception:
            return ""

    def get_exam_version_code(self, obj):
        try:
            if obj.exam_version:
                return f"نموذج {obj.exam_version.version_code}"
        except Exception:
            pass
        return ""

    def get_subject_name(self, obj):
        try:
            if obj.exam and obj.exam.subject:
                return getattr(obj.exam.subject, 'name_ar', None) or getattr(obj.exam.subject, 'name_en', None) or str(obj.exam.subject)
        except Exception:
            pass
        return ""

    def get_institution_type(self, obj):
        try:
            if obj.exam:
                return obj.exam.institution_type
        except Exception:
            pass
        return "school"
