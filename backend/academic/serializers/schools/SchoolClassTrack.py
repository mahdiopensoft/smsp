from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from academic.models.schools.SchoolClassTrack import SchoolClassTrack
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class SchoolClassTrackSerializer(DynamicFieldsModelSerializer):
    level_name = serializers.CharField(source='level.name_ar', read_only=True)
    track_name = serializers.CharField(source='track.name_ar', read_only=True)
    full_name = serializers.CharField(read_only=True)
    name_ar = serializers.CharField(source='full_name', read_only=True)

    class Meta:
        model = SchoolClassTrack
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def validate(self, attrs):
        level = attrs.get('level', getattr(self.instance, 'level', None))
        track = attrs.get('track', getattr(self.instance, 'track', None))

        if level and track:
            instance_id = self.instance.id if self.instance else None
            level_id = level.id if hasattr(level, 'id') else level
            track_id = track.id if hasattr(track, 'id') else track

            qs = SchoolClassTrack.objects.filter(
                level_id=level_id,
                track_id=track_id,
                is_deleted=False
            )
            if instance_id:
                qs = qs.exclude(id=instance_id)

            if qs.exists():
                raise serializers.ValidationError({
                    "track": _("مسار الصف هذا مسجل مسبقاً (تم ربط هذا الصف الدراسي بهذا المسار التعليمي بالفعل، يرجى اختيار مسار آخر أو صف آخر).")
                })

        return attrs

ClassTrackSerializer = SchoolClassTrackSerializer

