from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.institutes.InstituteEducationSystem import InstituteEducationSystem
from academic.serializers.institutes.InstituteEducationSystem import InstituteEducationSystemSerializer

class InstituteEducationSystemMVS(AllMVS):
    queryset = InstituteEducationSystem.objects.all()
    serializer_class = InstituteEducationSystemSerializer
    select_serializer_fields = ['id', 'name_ar', 'system_code', 'system_type']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'system_type': ['exact'],
        'study_nature': ['exact'],
        'has_ministerial_exam': ['exact'],
        'grading_calculation_method': ['exact'],
        'system_code': ['exact'],
        'name_ar': ['icontains'],
    }
    search_fields = ['name_ar', 'name_en', 'system_code']
