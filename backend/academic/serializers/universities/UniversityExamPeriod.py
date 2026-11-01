from rest_framework import serializers
from academic.models.universities.UniversityExamPeriod import UniversityExamPeriod
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class UniversityExamPeriodSerializer(DynamicFieldsModelSerializer):
    semester_name = serializers.CharField(source='fk_semester.name_ar', read_only=True)

    class Meta:
        model = UniversityExamPeriod
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

ExamPeriodSerializer = UniversityExamPeriodSerializer

