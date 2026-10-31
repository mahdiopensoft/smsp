from rest_framework import serializers
from omr.models.OMRSheetResult import OMRSheetResult
from omr.serializers.OMRQuestionResult import OMRQuestionResultSerializer

class OMRSheetResultSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    seat_number = serializers.SerializerMethodField()
    exam_title = serializers.SerializerMethodField()
    institution_type = serializers.SerializerMethodField()
    version_code = serializers.SerializerMethodField()
    school_name = serializers.SerializerMethodField()
    directorate_name = serializers.SerializerMethodField()
    governorate_name = serializers.SerializerMethodField()
    sheet_image = serializers.SerializerMethodField()
    original_image = serializers.SerializerMethodField()
    aligned_image = serializers.SerializerMethodField()
    questions = OMRQuestionResultSerializer(many=True, read_only=True)

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
        if obj.submission and obj.submission.layout_result:
            return obj.submission.layout_result.get("student_name", "")
        return ""

    def get_seat_number(self, obj):
        if obj.submission and obj.submission.registration:
            return obj.submission.registration.seatNumber
        if obj.submission and obj.submission.layout_result:
            return obj.submission.layout_result.get("seat_number", "")
        return ""

    def get_exam_title(self, obj):
        if obj.submission and obj.submission.exam:
            return obj.submission.exam.title
        return ""

    def get_institution_type(self, obj):
        if obj.submission and obj.submission.exam:
            return obj.submission.exam.institution_type
        return "school"

    def get_version_code(self, obj):
        if obj.submission and obj.submission.exam_version:
            return obj.submission.exam_version.versionCode
        if obj.submission and obj.submission.layout_result:
            return obj.submission.layout_result.get('version_code', 'A')
        return 'A'

    def get_school_name(self, obj):
        if obj.submission and obj.submission.registration and obj.submission.registration.student_profile:
            sp = obj.submission.registration.student_profile
            if sp.organization:
                return sp.organization.name_ar
        return ""

    def get_directorate_name(self, obj):
        if obj.submission and obj.submission.registration and obj.submission.registration.student_profile:
            sp = obj.submission.registration.student_profile
            if sp.directorate:
                return sp.directorate.name_ar
        return ""

    def get_governorate_name(self, obj):
        if obj.submission and obj.submission.registration and obj.submission.registration.student_profile:
            sp = obj.submission.registration.student_profile
            if sp.directorate and sp.directorate.fk_governorate:
                return sp.directorate.fk_governorate.name_ar
        return ""

    def get_sheet_image(self, obj):
        if obj.submission:
            if obj.submission.aligned_image:
                try:
                    return obj.submission.aligned_image.url
                except Exception:
                    pass
            if obj.submission.original_image:
                try:
                    return obj.submission.original_image.url
                except Exception:
                    return None
        return None

    def get_original_image(self, obj):
        if obj.submission and obj.submission.original_image:
            try:
                return obj.submission.original_image.url
            except Exception:
                return None
        return None

    def get_aligned_image(self, obj):
        if obj.submission and obj.submission.aligned_image:
            try:
                return obj.submission.aligned_image.url
            except Exception:
                return None
        return None

