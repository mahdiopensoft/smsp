from rest_framework import serializers
from academic.models.schools.SchoolUnit import SchoolUnit
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class SchoolUnitSerializer(DynamicFieldsModelSerializer):
    semester_name = serializers.CharField(source='semester.name_ar', read_only=True)
    class_subject_name = serializers.CharField(source='class_subject.__str__', read_only=True)
    subject_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SchoolUnit
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def get_subject_name(self, obj):
        if obj.school_subject:
            return obj.school_subject.name_ar
        if obj.class_subject:
            if getattr(obj.class_subject, 'school_subject', None):
                return obj.class_subject.school_subject.name_ar
            if getattr(obj.class_subject, 'subject', None):
                return obj.class_subject.subject.name_ar
        return None
