from rest_framework import serializers
from academic.models.common.Student import Student

class StudentSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name_ar', read_only=True)
    directorate_name = serializers.CharField(source='directorate.name_ar', read_only=True)
    organization_name = serializers.CharField(source='organization.name_ar', read_only=True)
    class_track_name = serializers.CharField(source='class_track.full_name', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
