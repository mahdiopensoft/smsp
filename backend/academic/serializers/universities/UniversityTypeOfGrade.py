from rest_framework import serializers
from academic.models.universities.UniversityTypeOfGrade import UniversityTypeOfGrade
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class UniversityTypeOfGradeSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = UniversityTypeOfGrade
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

TypeOfGradeSerializer = UniversityTypeOfGradeSerializer
