from rest_framework import serializers
from omr.models.OMRQuestionResult import OMRQuestionResult

class OMRQuestionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = OMRQuestionResult
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
