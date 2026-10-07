from rest_framework import serializers
from exams.models.ExamTargetScope import ExamTargetScope

class ExamTargetScopeSerializer(serializers.ModelSerializer):
    scope_level_display = serializers.CharField(source='get_scope_level_display', read_only=True)
    target_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ExamTargetScope
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def get_target_name(self, obj):
        level_map = {
            'country': obj.country,
            'governorate': obj.governorate,
            'directorate': obj.directorate,
            'region': obj.region,
            'school': obj.organization,
        }
        target = level_map.get(obj.scope_level)
        if target:
            return getattr(target, 'name_ar', None) or getattr(target, 'name', None) or str(target)
        return '—'
