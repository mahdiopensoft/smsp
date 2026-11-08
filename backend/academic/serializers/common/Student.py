from rest_framework import serializers
from academic.models.common.Student import Student

class StudentSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name_ar', read_only=True)
    nationality_name = serializers.CharField(source='nationality.name_ar', read_only=True)
    registration_year_name = serializers.SerializerMethodField(read_only=True)
    governorate_id = serializers.SerializerMethodField(read_only=True)
    governorate_name = serializers.SerializerMethodField(read_only=True)
    directorate_name = serializers.CharField(source='directorate.name_ar', read_only=True)
    organization_name = serializers.CharField(source='organization.name_ar', read_only=True)
    institution_type = serializers.CharField(read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    academic_info = serializers.SerializerMethodField(read_only=True)

    # تفاصيل المدارس
    stage_id = serializers.SerializerMethodField(read_only=True)
    stage_name = serializers.SerializerMethodField(read_only=True)
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

    def get_stage_id(self, obj):
        if obj.class_track and getattr(obj.class_track, 'level', None) and getattr(obj.class_track.level, 'stage_id', None):
            return obj.class_track.level.stage_id
        return None

    def get_stage_name(self, obj):
        if obj.class_track and getattr(obj.class_track, 'level', None) and getattr(obj.class_track.level, 'stage', None):
            return obj.class_track.level.stage.name_ar
        return None

    def get_governorate_id(self, obj):
        if obj.directorate and getattr(obj.directorate, 'fk_governorate_id', None):
            return obj.directorate.fk_governorate_id
        if obj.organization and obj.organization.name_ar:
            from OpenSoftCoreV41.common.models.Branch import Organization as CoreOrg
            c_org = CoreOrg.objects.filter(name_ar=obj.organization.name_ar, is_deleted=False).first()
            if c_org and getattr(c_org, 'fk_governorate_id', None):
                return c_org.fk_governorate_id
        return None

    def get_governorate_name(self, obj):
        if obj.directorate and getattr(obj.directorate, 'fk_governorate', None):
            return obj.directorate.fk_governorate.name_ar
        gov_id = self.get_governorate_id(obj)
        if gov_id:
            from OpenSoftCoreV41.common.models.Governorate import Governorate
            g = Governorate.objects.filter(id=gov_id).first()
            if g:
                return g.name_ar
        return None

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # استنتاج المديرية إذا كانت غير مسجلة ولكن المؤسسة محددة
        if not ret.get('directorate') and instance.organization and instance.organization.name_ar:
            from OpenSoftCoreV41.common.models.Branch import Organization as CoreOrg
            c_org = CoreOrg.objects.filter(name_ar=instance.organization.name_ar, is_deleted=False).first()
            if c_org and c_org.fk_directorate_id:
                ret['directorate'] = c_org.fk_directorate_id
                if not ret.get('directorate_name') and c_org.fk_directorate:
                    ret['directorate_name'] = c_org.fk_directorate.name_ar
        return ret

    def get_registration_year_name(self, obj):
        if obj.registration_date:
            return str(obj.registration_date)
        return None

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

