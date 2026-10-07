from rest_framework import serializers
from omr.models.OMRSheetResult import OMRSheetResult

class OMRSheetResultSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    seat_number = serializers.SerializerMethodField()
    exam_title = serializers.SerializerMethodField()
    institution_type = serializers.SerializerMethodField()

    class Meta:
        model = OMRSheetResult
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def get_student_name(self, obj):
        if obj.submission and obj.submission.registration:
            reg = obj.submission.registration
            if reg.student_profile and reg.student_profile.name_ar:
                return reg.student_profile.name_ar
            if reg.student:
                full = f"{reg.student.first_name} {reg.student.last_name}".strip()
                return full or reg.student.username
        return ""

    def get_seat_number(self, obj):
        if obj.submission and obj.submission.registration:
            return obj.submission.registration.seatNumber
        return ""

    def get_exam_title(self, obj):
        if obj.submission and obj.submission.exam:
            return obj.submission.exam.title
        return ""

    def get_institution_type(self, obj):
        if obj.submission and obj.submission.exam:
            return obj.submission.exam.institution_type
        return "school"
