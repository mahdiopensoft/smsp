from rest_framework import serializers
from exams.models.CurriculumExclusion import CurriculumExclusion
from academic.models.schools.SchoolUnit import SchoolUnit
from academic.models.schools.SchoolLesson import SchoolLesson

class CurriculumExclusionSerializer(serializers.ModelSerializer):
    academic_year_name = serializers.SerializerMethodField()
    institution_type_display = serializers.CharField(source='get_institution_type_display', read_only=True)
    exclusion_type_display = serializers.CharField(source='get_exclusion_type_display', read_only=True)
    
    # Hierarchy names
    stage_name = serializers.SerializerMethodField()
    class_track_name = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()
    college_name = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()
    specialization_name = serializers.SerializerMethodField()
    semester_subject_name = serializers.SerializerMethodField()
    institute_field_name = serializers.SerializerMethodField()
    institute_specialization_name = serializers.SerializerMethodField()
    institute_subject_name = serializers.SerializerMethodField()
    
    # Target names
    unit_name = serializers.SerializerMethodField()
    lesson_name = serializers.SerializerMethodField()

    class Meta:
        model = CurriculumExclusion
        fields = '__all__'

    def get_academic_year_name(self, obj):
        if obj.academic_year:
            return str(obj.academic_year)
        return ""

    def get_stage_name(self, obj):
        return getattr(obj.stage, 'name_ar', '') if obj.stage else ""

    def get_class_track_name(self, obj):
        if obj.class_track:
            return getattr(obj.class_track, 'full_name', '') or getattr(obj.class_track, 'name_ar', '') or str(obj.class_track)
        return ""

    def get_subject_name(self, obj):
        if obj.subject:
            return getattr(obj.subject, 'name_ar', '')
        if obj.class_subject:
            if hasattr(obj.class_subject, 'school_subject') and obj.class_subject.school_subject:
                return obj.class_subject.school_subject.name_ar
            return getattr(obj.class_subject, 'name_ar', '')
        return ""

    def get_college_name(self, obj):
        return getattr(obj.college, 'name_ar', '') if obj.college else ""

    def get_department_name(self, obj):
        return getattr(obj.department, 'name_ar', '') if obj.department else ""

    def get_specialization_name(self, obj):
        return getattr(obj.specialization, 'name_ar', '') if obj.specialization else ""

    def get_semester_subject_name(self, obj):
        if obj.semester_subject:
            return getattr(obj.semester_subject, 'name_ar', '') or str(obj.semester_subject)
        return ""

    def get_institute_field_name(self, obj):
        return getattr(obj.institute_field, 'name_ar', '') if obj.institute_field else ""

    def get_institute_specialization_name(self, obj):
        return getattr(obj.institute_specialization, 'name_ar', '') if obj.institute_specialization else ""

    def get_institute_subject_name(self, obj):
        if hasattr(obj, 'institute_subject') and obj.institute_subject:
            return getattr(obj.institute_subject, 'name_ar', '') or str(obj.institute_subject)
        if hasattr(obj, 'institute_curriculum') and obj.institute_curriculum:
            return getattr(obj.institute_curriculum, 'name_ar', '') or str(obj.institute_curriculum)
        return ""

    def get_unit_name(self, obj):
        if obj.unit_id:
            if obj.unit:
                return getattr(obj.unit, 'name_ar', '') or getattr(obj.unit, 'name_en', '') or f"الوحدة #{obj.unit_id}"
            su = SchoolUnit.objects.filter(id=obj.unit_id).first()
            if su:
                return su.name_ar or su.name_en or f"الوحدة #{obj.unit_id}"
        return ""

    def get_lesson_name(self, obj):
        if obj.lesson_id:
            if obj.lesson:
                return getattr(obj.lesson, 'name_ar', '') or getattr(obj.lesson, 'name_en', '') or f"الدرس #{obj.lesson_id}"
            sl = SchoolLesson.objects.filter(id=obj.lesson_id).first()
            if sl:
                return sl.name_ar or sl.name_en or f"الدرس #{obj.lesson_id}"
        return ""
