from rest_framework import serializers
from exams.models.ExamTemplate import ExamTemplate

class ExamTemplateSerializer(serializers.ModelSerializer):
    institution_type_display = serializers.CharField(source='get_institution_type_display', read_only=True)
    name = serializers.CharField()

    class Meta:
        model = ExamTemplate
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
