from rest_framework import serializers
from academic.models.schools.SchoolExamPeriod import SchoolExamPeriod
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class SchoolExamPeriodSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = SchoolExamPeriod
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
