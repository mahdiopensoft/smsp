from rest_framework import serializers
from exams.models.Exam import Exam

class ExamSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    name_ar = serializers.SerializerMethodField(read_only=True)
    subject_name = serializers.CharField(source='subject.name_ar', read_only=True, default='عام')
    year_name = serializers.CharField(source='year.name_ar', read_only=True, default='-')
    governorate_name = serializers.SerializerMethodField(read_only=True)
    directorate_name = serializers.SerializerMethodField(read_only=True)
    region_name = serializers.CharField(source='region.name_ar', read_only=True, default=None)
    country_name = serializers.CharField(source='country.name_ar', read_only=True, default=None)
    stage_name = serializers.SerializerMethodField(read_only=True)
    class_track_name = serializers.SerializerMethodField(read_only=True)
    schedule_date = serializers.CharField(source='examSchedule.date', read_only=True, default=None)
    schedule_duration = serializers.IntegerField(source='examSchedule.duration', read_only=True, default=None)
    schedule_name = serializers.CharField(source='examSchedule.name', read_only=True, default=None)
    target_scope_level_display = serializers.CharField(source='get_target_scope_level_display', read_only=True)
    models_mode_display = serializers.CharField(source='get_models_mode_display', read_only=True)
    institution_type_display = serializers.CharField(source='get_institution_type_display', read_only=True)
    targeted_scopes_summary = serializers.SerializerMethodField(read_only=True)
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

    def get_governorate_name(self, obj):
        if obj.governorate:
            return getattr(obj.governorate, 'name_ar', None) or getattr(obj.governorate, 'name', None) or str(obj.governorate)
        if hasattr(obj, 'target_scopes'):
            gov_names = []
            for ts in obj.target_scopes.filter(is_deleted=False):
                if ts.governorate:
                    name = getattr(ts.governorate, 'name_ar', None) or str(ts.governorate)
                    if name and name not in gov_names:
                        gov_names.append(name)
            if gov_names:
                return "، ".join(gov_names)
        return "جميع المحافظات" if getattr(obj, 'target_scope_level', 'all') == 'all' else None

    def get_directorate_name(self, obj):
        if obj.directorate:
            return getattr(obj.directorate, 'name_ar', None) or getattr(obj.directorate, 'name', None) or str(obj.directorate)
        if hasattr(obj, 'target_scopes'):
            dir_names = []
            for ts in obj.target_scopes.filter(is_deleted=False):
                if ts.directorate:
                    name = getattr(ts.directorate, 'name_ar', None) or str(ts.directorate)
                    if name and name not in dir_names:
                        dir_names.append(name)
            if dir_names:
                return "، ".join(dir_names)
        return "كافة المديريات" if getattr(obj, 'target_scope_level', 'all') in ['all', 'governorate'] else None

    def get_stage_name(self, obj):
        if obj.class_track and hasattr(obj.class_track, 'level') and obj.class_track.level:
            stage = getattr(obj.class_track.level, 'stage', None)
            if stage:
                return getattr(stage, 'name_ar', None) or getattr(stage, 'name', None) or str(stage)
        return None

    def get_class_track_name(self, obj):
        if obj.class_track:
            return getattr(obj.class_track, 'full_name', None) or str(obj.class_track)
        return None

    def get_targeted_scopes_summary(self, obj):
        level = getattr(obj, 'target_scope_level', 'all')
        if level == 'all':
            return {
                "level": "all",
                "level_display": "شامل لكافة المدارس والمديريات",
                "is_all": True,
                "targets": []
            }
        targets = []
        if hasattr(obj, 'target_scopes'):
            for ts in obj.target_scopes.filter(is_deleted=False):
                target_name = None
                if ts.scope_level == 'country' and ts.country:
                    target_name = getattr(ts.country, 'name_ar', str(ts.country))
                elif ts.scope_level == 'governorate' and ts.governorate:
                    target_name = getattr(ts.governorate, 'name_ar', str(ts.governorate))
                elif ts.scope_level == 'directorate' and ts.directorate:
                    target_name = getattr(ts.directorate, 'name_ar', str(ts.directorate))
                elif ts.scope_level == 'region' and ts.region:
                    target_name = getattr(ts.region, 'name_ar', str(ts.region))
                elif ts.scope_level == 'school' and ts.organization:
                    target_name = getattr(ts.organization, 'name_ar', str(ts.organization))
                targets.append({
                    "id": ts.id,
                    "scope_level": ts.scope_level,
                    "scope_level_display": ts.get_scope_level_display(),
                    "name": target_name or '—'
                })
        return {
            "level": level,
            "level_display": obj.get_target_scope_level_display(),
            "is_all": False,
            "targets": targets
        }
