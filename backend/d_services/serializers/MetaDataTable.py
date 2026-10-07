from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from d_services.models.MetaDataTable import MetaDataTable
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class MetaDataTableSerializer(DynamicFieldsModelSerializer):
    name_table__display = serializers.ReadOnlyField(source='name_table')
    external_id = serializers.SerializerMethodField()
    class Meta:
        model = MetaDataTable
        fields = '__all__'
        read_only_fields = ['id']

    def get_external_id(self, obj):
        value = obj.external_id
        if value and '-' in value:
            ex = value.split('-')[-1]
            try: 
                return int(ex)
            except ValueError:
                return None
        return value