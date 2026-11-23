from rest_framework import serializers
from exams.models.ExamVersion import ExamVersion

class ExamVersionSerializer(serializers.ModelSerializer):
    difficulty_profile_display = serializers.CharField(source='get_difficulty_profile_display', read_only=True)

    class Meta:
        model = ExamVersion
        fields = [
            'id', 'created_at', 'exam', 'versionCode',
            'model_group_index', 'difficulty_profile', 'difficulty_profile_display',
            'difficulty_distribution', 'key_status', 'answer_key_hash',
            'key_frozen_at', 'key_frozen_by',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('answer_key_snapshot', None)
        return data
