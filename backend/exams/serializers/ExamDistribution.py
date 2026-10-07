from rest_framework import serializers
from exams.models.ExamDistribution import ExamDistribution
from exams.models.ExamSchoolDispatchStatus import ExamSchoolDispatchStatus

class ExamSchoolDispatchStatusSerializer(serializers.ModelSerializer):
    school_name_ar = serializers.CharField(source='school.name_ar', read_only=True)
    school_name_en = serializers.CharField(source='school.name_en', read_only=True)
    school_branch_no = serializers.CharField(source='school.branch_no', read_only=True)
    governorate_name = serializers.SerializerMethodField(read_only=True)
    directorate_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ExamSchoolDispatchStatus
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def get_governorate_name(self, obj):
        if obj.school and obj.school.fk_governorate:
            return obj.school.fk_governorate.name_ar
        return '-'

    def get_directorate_name(self, obj):
        if obj.school and obj.school.fk_directorate:
            return obj.school.fk_directorate.name_ar
        return '-'


class ExamDistributionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    name_ar = serializers.SerializerMethodField(read_only=True)
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    exam_unique_code = serializers.CharField(source='exam.uniqueCode', read_only=True)
    subject_name = serializers.SerializerMethodField(read_only=True)
    year_name = serializers.SerializerMethodField(read_only=True)
    
    targeted_schools_count = serializers.SerializerMethodField(read_only=True)
    received_schools_count = serializers.SerializerMethodField(read_only=True)
    accessible_schools_count = serializers.SerializerMethodField(read_only=True)
    
    school_statuses = ExamSchoolDispatchStatusSerializer(many=True, read_only=True)

    class Meta:
        model = ExamDistribution
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def get_name(self, obj):
        return obj.title

    def get_name_ar(self, obj):
        return obj.title

    def get_subject_name(self, obj):
        if obj.exam and obj.exam.subject:
            return getattr(obj.exam.subject, 'name_ar', str(obj.exam.subject))
        return 'عام'

    def get_year_name(self, obj):
        if obj.exam and obj.exam.year:
            return getattr(obj.exam.year, 'name_ar', str(obj.exam.year))
        return '-'

    def get_targeted_schools_count(self, obj):
        return obj.organizations.filter(is_deleted=False).count()

    def get_received_schools_count(self, obj):
        return obj.school_statuses.filter(is_received=True, is_deleted=False).count()

    def get_accessible_schools_count(self, obj):
        return obj.school_statuses.filter(is_accessible=True, is_deleted=False).count()
