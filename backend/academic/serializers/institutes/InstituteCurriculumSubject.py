from rest_framework import serializers
from academic.models.institutes.InstituteCurriculumSubject import InstituteCurriculumSubject
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class InstituteCurriculumSubjectSerializer(DynamicFieldsModelSerializer):
    curriculum_name = serializers.CharField(source='curriculum.name_ar', read_only=True)
    subject_name = serializers.CharField(source='subject.name_ar', read_only=True)
    subject_code = serializers.CharField(source='subject.subject_code', read_only=True)
    level_name = serializers.CharField(source='level.name_ar', read_only=True)
    semester_name = serializers.CharField(source='semester.name_ar', read_only=True)
    exam_entity_display = serializers.CharField(source='get_exam_entity_display', read_only=True)
    name_ar = serializers.SerializerMethodField(read_only=True)

    def get_name_ar(self, obj):
        try:
            curr = f"{obj.curriculum.name_ar} - " if obj.curriculum else ""
            subj = obj.subject.name_ar if obj.subject else ""
            lvl = f" ({obj.level.name_ar})" if obj.level else ""
            return f"{curr}{subj}{lvl}"
        except Exception:
            return str(obj)

    class Meta:
        model = InstituteCurriculumSubject
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
