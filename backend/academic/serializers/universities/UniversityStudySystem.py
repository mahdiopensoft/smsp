from rest_framework import serializers
from academic.models.universities.UniversityStudySystem import UniversityStudySystem
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class UniversityStudySystemSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = UniversityStudySystem
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

StudeySystemSerializer = UniversityStudySystemSerializer
StudySystemSerializer = UniversityStudySystemSerializer
