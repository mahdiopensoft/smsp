from rest_framework import serializers
from academic.models.common.Organization import Organization

class OrganizationSerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source='parent.name_ar', read_only=True)

    class Meta:
        model = Organization
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
