from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.institutes.InstituteField import InstituteField
from academic.serializers.institutes.InstituteField import InstituteFieldSerializer

class InstituteFieldMVS(AllMVS):
    queryset = InstituteField.objects.all()
    serializer_class = InstituteFieldSerializer
    select_serializer_fields = ['id', 'name_ar', 'field_code']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'field_code': ['exact', 'icontains'],
        'name_ar': ['icontains'],
    }
    search_fields = ['name_ar', 'name_en', 'field_code']
