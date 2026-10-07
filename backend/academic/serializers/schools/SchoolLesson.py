from rest_framework import serializers
from academic.models.schools.SchoolLesson import SchoolLesson
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class SchoolLessonSerializer(DynamicFieldsModelSerializer):
    unit_name = serializers.CharField(source='unit.name_ar', read_only=True)
    subject_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SchoolLesson
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def get_subject_name(self, obj):
        if obj.school_subject:
            return obj.school_subject.name_ar
        if obj.unit:
            if obj.unit.school_subject:
                return obj.unit.school_subject.name_ar
            if obj.unit.class_subject and getattr(obj.unit.class_subject, 'school_subject', None):
                return obj.unit.class_subject.school_subject.name_ar
        return None
