from rest_framework import serializers
from academic.models.schools.SchoolLearningOutcome import SchoolLearningOutcome
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class SchoolLearningOutcomeSerializer(DynamicFieldsModelSerializer):
    unit_name = serializers.CharField(source='unit.name_ar', read_only=True)
    lesson_name = serializers.CharField(source='lesson.name_ar', read_only=True)
    subject_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SchoolLearningOutcome
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def get_subject_name(self, obj):
        if obj.school_subject:
            return obj.school_subject.name_ar
        if obj.unit and obj.unit.school_subject:
            return obj.unit.school_subject.name_ar
        return None
