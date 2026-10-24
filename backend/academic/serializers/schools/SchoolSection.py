from rest_framework import serializers
from academic.models.schools.SchoolSection import SchoolSection
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class SchoolSectionSerializer(DynamicFieldsModelSerializer):
    organization_name = serializers.CharField(source='organization.name_ar', read_only=True)
    class_track_name = serializers.CharField(source='class_track.full_name', read_only=True)
    year_name = serializers.CharField(source='academic_year.name', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    governorate_id = serializers.SerializerMethodField(read_only=True)
    directorate_id = serializers.SerializerMethodField(read_only=True)
    governorate = serializers.SerializerMethodField(read_only=True)
    directorate = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SchoolSection
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def get_directorate_id(self, obj):
        if not obj.organization:
            return None
        if obj.organization.parent_id:
            return obj.organization.parent_id
        try:
            from OpenSoftCoreV41.common.models.Branch import Organization as CoreOrg
            c = CoreOrg.objects.filter(id=obj.organization_id).first()
            if c and c.fk_parent_organization_id:
                return c.fk_parent_organization_id
        except Exception:
            pass
        return None

    def get_governorate_id(self, obj):
        if not obj.organization:
            return None
        if obj.organization.parent and obj.organization.parent.parent_id:
            return obj.organization.parent.parent_id
        try:
            from OpenSoftCoreV41.common.models.Branch import Organization as CoreOrg
            c = CoreOrg.objects.filter(id=obj.organization_id).first()
            if c and c.fk_parent_organization_id:
                p = CoreOrg.objects.filter(id=c.fk_parent_organization_id).first()
                if p and p.fk_parent_organization_id:
                    return p.fk_parent_organization_id
        except Exception:
            pass
        return None

    def get_directorate(self, obj):
        return self.get_directorate_id(obj)

    def get_governorate(self, obj):
        return self.get_governorate_id(obj)

    def create(self, validated_data):
        validated_data.pop('governorate', None)
        validated_data.pop('directorate', None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('governorate', None)
        validated_data.pop('directorate', None)
        return super().update(instance, validated_data)
