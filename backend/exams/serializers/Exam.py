from rest_framework import serializers
from exams.models.Exam import Exam

class ExamSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    name_ar = serializers.SerializerMethodField(read_only=True)
    subject_name = serializers.CharField(source='subject.name_ar', read_only=True, default='عام')
    year_name = serializers.CharField(source='year.name_ar', read_only=True, default='-')
    governorate_name = serializers.CharField(source='governorate.name_ar', read_only=True, default=None)
    directorate_name = serializers.CharField(source='directorate.name_ar', read_only=True, default=None)
    versions_count = serializers.SerializerMethodField(read_only=True)
    questions_count = serializers.SerializerMethodField(read_only=True)
    students_count = serializers.SerializerMethodField(read_only=True)
    versions_list = serializers.SerializerMethodField(read_only=True)
    target_scopes_data = serializers.SerializerMethodField(read_only=True)
    model_region_assignments_data = serializers.SerializerMethodField(read_only=True)
    active_distribution = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Exam
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def get_target_scopes_data(self, obj):
        from exams.serializers.ExamTargetScope import ExamTargetScopeSerializer
        if hasattr(obj, 'target_scopes'):
            return ExamTargetScopeSerializer(obj.target_scopes.filter(is_deleted=False), many=True).data
        return []

    def get_model_region_assignments_data(self, obj):
        from exams.serializers.ExamModelRegionAssignment import ExamModelRegionAssignmentSerializer
        if hasattr(obj, 'model_region_assignments'):
            return ExamModelRegionAssignmentSerializer(obj.model_region_assignments.filter(is_deleted=False), many=True).data
        return []

    def get_name(self, obj):
        return str(obj)

    def get_name_ar(self, obj):
        return str(obj)

    def get_versions_count(self, obj):
        if hasattr(obj, 'annotated_versions_count'):
            return obj.annotated_versions_count
        if hasattr(obj, 'prefetched_versions_count'):
            return obj.prefetched_versions_count
        return obj.versions.filter(is_deleted=False).count()

    def get_questions_count(self, obj):
        if hasattr(obj, 'annotated_questions_count'):
            return obj.annotated_questions_count
        first_version = obj.versions.filter(is_deleted=False).first()
        if first_version:
            return first_version.question_orders.filter(is_deleted=False).count()
        return 0

    def get_students_count(self, obj):
        if hasattr(obj, 'annotated_students_count'):
            return obj.annotated_students_count
        from exams.models.StudentExamRegistration import StudentExamRegistration
        return StudentExamRegistration.objects.filter(examVersion__exam=obj, is_deleted=False).count()

    def get_versions_list(self, obj):
        return [
            {"id": v.id, "versionCode": v.versionCode}
            for v in obj.versions.filter(is_deleted=False).order_by('versionCode')
        ]

    def get_active_distribution(self, obj):
        active_statuses = ['scheduled', 'dispatched', 'accessible', 'in_progress']
        dist = obj.distributions.filter(is_deleted=False, status__in=active_statuses).order_by('-created_at').first()
        if dist:
            return {
                "id": dist.id,
                "title": dist.title,
                "status": dist.status,
                "status_display": dist.get_status_display(),
                "created_at": dist.created_at.isoformat() if dist.created_at else None
            }
        return None
