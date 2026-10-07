from rest_framework import serializers
from academic.models.schools.SchoolClassSubject import SchoolClassSubject
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class SchoolClassSubjectSerializer(DynamicFieldsModelSerializer):
    class_track_name = serializers.CharField(source='class_track.full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name_ar', read_only=True)
    name_ar = serializers.SerializerMethodField()

    def get_name_ar(self, obj):
        track_str = obj.class_track.full_name if obj.class_track else ''
        subj_str = obj.school_subject.name_ar if getattr(obj, 'school_subject', None) else (obj.subject.name_ar if obj.subject else '')
        return f"{track_str} - {subj_str}" if track_str and subj_str else (subj_str or track_str)

    class Meta:
        model = SchoolClassSubject
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

ClassSubjectSerializer = SchoolClassSubjectSerializer
