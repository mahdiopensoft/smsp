from rest_framework import serializers
from academic.models.common.Student import Student

class StudentSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name_ar', read_only=True)
    governorate_id = serializers.IntegerField(source='directorate.fk_governorate_id', read_only=True)
    governorate_name = serializers.CharField(source='directorate.fk_governorate.name_ar', read_only=True)
    directorate_name = serializers.CharField(source='directorate.name_ar', read_only=True)
    organization_name = serializers.CharField(source='organization.name_ar', read_only=True)
    institution_type = serializers.CharField(read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    academic_info = serializers.SerializerMethodField(read_only=True)

    # تفاصيل المدارس
    class_track_name = serializers.CharField(source='class_track.full_name', read_only=True)

    # تفاصيل الجامعات
    university_college_name = serializers.CharField(source='university_college.name_ar', read_only=True)
    university_department_name = serializers.CharField(source='university_department.name_ar', read_only=True)
    university_specialization_name = serializers.CharField(source='university_specialization.name_ar', read_only=True)
    university_level_name = serializers.CharField(source='university_level.name_ar', read_only=True)

    # تفاصيل المعاهد
    institute_field_name = serializers.CharField(source='institute_field.name_ar', read_only=True)
    institute_education_system_name = serializers.CharField(source='institute_education_system.name_ar', read_only=True)
    institute_specialization_name = serializers.CharField(source='institute_specialization.name_ar', read_only=True)
    institute_level_name = serializers.CharField(source='institute_level.name_ar', read_only=True)

    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def get_academic_info(self, obj):
        inst_type = getattr(obj, 'institution_type', 'school')
        if inst_type == "university":
            parts = [
                obj.university_college.name_ar if obj.university_college else "",
                obj.university_specialization.name_ar if obj.university_specialization else "",
                obj.university_level.name_ar if obj.university_level else ""
            ]
            return " - ".join([p for p in parts if p]) or "تعليم جامعي"
        elif inst_type == "institute":
            parts = [
                obj.institute_field.name_ar if obj.institute_field else "",
                obj.institute_specialization.name_ar if obj.institute_specialization else "",
                obj.institute_level.name_ar if obj.institute_level else ""
            ]
            return " - ".join([p for p in parts if p]) or "تعليم وتدريب مهني"
        else:
            if obj.class_track:
                return obj.class_track.full_name
            return "تعليم مدرسي"

