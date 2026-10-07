from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.common.AcademicYear import AcademicYear
from academic.serializers.common.AcademicYear import AcademicYearSerializer

class AcademicYearMVS(AllMVS):
    queryset = AcademicYear.objects.all().order_by('-id')
    serializer_class = AcademicYearSerializer
    select_serializer_fields = ['id', 'name', 'name_ar']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'is_current': ['exact'],
        'hijri_year': ['exact', 'icontains'],
        'gregorian_year': ['exact', 'icontains'],
    }
