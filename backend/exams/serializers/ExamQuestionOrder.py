from rest_framework import serializers
from exams.models.ExamQuestionOrder import ExamQuestionOrder

class ExamQuestionOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamQuestionOrder
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
