from rest_framework import serializers
from exams.models.TableOfSpecifications import TableOfSpecifications

class TableOfSpecificationsSerializer(serializers.ModelSerializer):
    subject_name = serializers.SerializerMethodField()
    level_name = serializers.SerializerMethodField()

    class Meta:
        model = TableOfSpecifications
        fields = '__all__'

    def get_subject_name(self, obj):
        if obj.subject:
            return getattr(obj.subject, 'name_ar', None) or getattr(obj.subject, 'name_en', None) or str(obj.subject_id)
        return ""

    def get_level_name(self, obj):
        if obj.level:
            return getattr(obj.level, 'name_ar', None) or getattr(obj.level, 'name_en', None) or str(obj.level_id)
        return ""
