from rest_framework import serializers
from academic.models.common.LearningOutcome import LearningOutcome
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class LearningOutcomeSerializer(DynamicFieldsModelSerializer):
    unit_name = serializers.CharField(source='unit.name_ar', read_only=True)
    class_track_name = serializers.CharField(source='unit.class_subject.class_track.full_name', read_only=True)
    subject_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = LearningOutcome
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def get_subject_name(self, obj):
        try:
            if obj.subject:
                return obj.subject.name_ar
            if obj.unit and obj.unit.class_subject and obj.unit.class_subject.subject:
                return obj.unit.class_subject.subject.name_ar
            elif obj.unit and obj.unit.semester_subject and obj.unit.semester_subject.fk_subject:
                return obj.unit.semester_subject.fk_subject.name_ar
        except Exception:
            return None
