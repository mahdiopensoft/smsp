from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.institutes.InstituteLevel import InstituteLevel
from academic.serializers.institutes.InstituteLevel import InstituteLevelSerializer

class InstituteLevelMVS(AllMVS):
    queryset = InstituteLevel.objects.all()
    serializer_class = InstituteLevelSerializer
    select_serializer_fields = ['id', 'name_ar', 'order']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'order': ['exact'],
        'name_ar': ['icontains'],
    }
    search_fields = ['name_ar', 'name_en']
