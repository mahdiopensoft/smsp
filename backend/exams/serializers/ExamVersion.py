from rest_framework import serializers
from exams.models.ExamVersion import ExamVersion

class ExamVersionSerializer(serializers.ModelSerializer):
    difficulty_profile_display = serializers.CharField(source='get_difficulty_profile_display', read_only=True)

    class Meta:
        model = ExamVersion
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
