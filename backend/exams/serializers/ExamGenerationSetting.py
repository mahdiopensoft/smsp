from rest_framework import serializers
from exams.models.ExamGenerationSetting import ExamGenerationSetting

class ExamGenerationSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamGenerationSetting
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
