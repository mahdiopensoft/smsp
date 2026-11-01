from rest_framework import serializers
from academic.models.universities.UniversityLesson import UniversityLesson
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class UniversityLessonSerializer(DynamicFieldsModelSerializer):
    unit_name = serializers.CharField(source='unit.name_ar', read_only=True)
    subject_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UniversityLesson
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def get_subject_name(self, obj):
        try:
            if obj.subject:
                return obj.subject.name_ar
            if obj.unit and obj.unit.semester_subject and obj.unit.semester_subject.fk_subject:
                return obj.unit.semester_subject.fk_subject.name_ar
        except Exception:
            return None

LessonSerializer = UniversityLessonSerializer

