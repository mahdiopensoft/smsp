from rest_framework import serializers
from exams.models.ExamModelRegionAssignment import ExamModelRegionAssignment

class ExamModelRegionAssignmentSerializer(serializers.ModelSerializer):
    difficulty_profile_display = serializers.CharField(source='get_difficulty_profile_display', read_only=True)
    target_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ExamModelRegionAssignment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def get_target_name(self, obj):
        target = obj.governorate or obj.directorate or obj.region or obj.organization
        if target:
            return getattr(target, 'name_ar', None) or getattr(target, 'name', None) or str(target)
        return '—'
