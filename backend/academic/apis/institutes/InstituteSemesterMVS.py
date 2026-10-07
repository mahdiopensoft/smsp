from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.institutes.InstituteSemester import InstituteSemester
from academic.serializers.institutes.InstituteSemester import InstituteSemesterSerializer

class InstituteSemesterMVS(AllMVS):
    queryset = InstituteSemester.objects.all()
    serializer_class = InstituteSemesterSerializer
    select_serializer_fields = ['id', 'name_ar', 'order', 'semester_nature']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'order': ['exact'],
        'semester_nature': ['exact'],
        'is_current': ['exact'],
        'name_ar': ['icontains'],
    }
    search_fields = ['name_ar', 'name_en']
