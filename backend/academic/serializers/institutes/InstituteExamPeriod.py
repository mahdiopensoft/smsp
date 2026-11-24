from rest_framework import serializers
from academic.models.institutes.InstituteExamPeriod import InstituteExamPeriod
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class InstituteExamPeriodSerializer(DynamicFieldsModelSerializer):
    semester_name = serializers.CharField(source='fk_semester.name_ar', read_only=True)

    class Meta:
        model = InstituteExamPeriod
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
