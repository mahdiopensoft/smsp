from rest_framework import serializers
from academic.models.schools.SchoolLesson import SchoolLesson
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class SchoolLessonSerializer(DynamicFieldsModelSerializer):
    unit_name = serializers.CharField(source='unit.name_ar', read_only=True)
    subject_name = serializers.SerializerMethodField(read_only=True)
    subject = serializers.SerializerMethodField(read_only=True)
    stage = serializers.SerializerMethodField(read_only=True)
    class_track = serializers.SerializerMethodField(read_only=True)
    semester = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SchoolLesson
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def to_internal_value(self, data):
        data = data.copy() if hasattr(data, 'copy') else dict(data)
        if 'subject' in data and not data.get('school_subject'):
            data['school_subject'] = data.get('subject')
        return super().to_internal_value(data)

    def get_subject_name(self, obj):
        if obj.school_subject:
            return obj.school_subject.name_ar
        if obj.unit:
            if obj.unit.school_subject:
                return obj.unit.school_subject.name_ar
            if obj.unit.class_subject and getattr(obj.unit.class_subject, 'school_subject', None):
                return obj.unit.class_subject.school_subject.name_ar
        return None

    def get_subject(self, obj):
        if obj.school_subject_id:
            return obj.school_subject_id
        if obj.unit:
            if obj.unit.school_subject_id:
                return obj.unit.school_subject_id
            if obj.unit.class_subject and getattr(obj.unit.class_subject, 'school_subject_id', None):
                return obj.unit.class_subject.school_subject_id
        return None

    def get_semester(self, obj):
        if obj.unit and obj.unit.semester_id:
            return obj.unit.semester_id
        return None

    def get_class_track(self, obj):
        if obj.unit and obj.unit.class_subject and getattr(obj.unit.class_subject, 'class_track_id', None):
            return obj.unit.class_subject.class_track_id
        return None

    def get_stage(self, obj):
        if (
            obj.unit and 
            obj.unit.class_subject and 
            getattr(obj.unit.class_subject, 'class_track', None) and 
            getattr(obj.unit.class_subject.class_track, 'level', None) and 
            getattr(obj.unit.class_subject.class_track.level, 'stage_id', None)
        ):
            return obj.unit.class_subject.class_track.level.stage_id
        return None
