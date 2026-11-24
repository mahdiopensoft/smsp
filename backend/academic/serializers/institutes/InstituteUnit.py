from rest_framework import serializers
from academic.models.institutes.InstituteUnit import InstituteUnit
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class InstituteUnitSerializer(DynamicFieldsModelSerializer):
    subject_name = serializers.CharField(source='subject.name_ar', read_only=True)
    curriculum_name = serializers.CharField(source='curriculum.name_ar', read_only=True)
    semester_name = serializers.CharField(source='semester.name_ar', read_only=True)

    class Meta:
        model = InstituteUnit
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
