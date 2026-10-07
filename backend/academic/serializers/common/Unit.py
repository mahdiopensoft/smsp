from rest_framework import serializers
from academic.models.common.Unit import Unit
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class UnitSerializer(DynamicFieldsModelSerializer):
    semester_name = serializers.CharField(source='semester.name_ar', read_only=True)
    class_subject_name = serializers.CharField(source='class_subject.__str__', read_only=True)
    class_track_name = serializers.CharField(source='class_subject.class_track.full_name', read_only=True)
    subject_name = serializers.SerializerMethodField(read_only=True)
    level_name = serializers.SerializerMethodField(read_only=True)
    track_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Unit
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def get_subject_name(self, obj):
        try:
            return obj.class_subject.subject.name_ar
        except Exception:
            return None

    def get_level_name(self, obj):
        try:
            return obj.class_subject.class_track.level.name_ar
        except Exception:
            return None

    def get_track_name(self, obj):
        try:
            return obj.class_subject.class_track.track.name_ar
        except Exception:
            return None
