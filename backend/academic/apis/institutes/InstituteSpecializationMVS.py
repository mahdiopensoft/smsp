from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.institutes.InstituteSpecialization import InstituteSpecialization
from academic.serializers.institutes.InstituteSpecialization import InstituteSpecializationSerializer

class InstituteSpecializationMVS(AllMVS):
    queryset = InstituteSpecialization.objects.select_related('field', 'education_system', 'organization').all()
    serializer_class = InstituteSpecializationSerializer
    select_serializer_fields = ['id', 'name_ar', 'specialization_code', 'field_id', 'education_system_id']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'field': ['exact'],
        'education_system': ['exact'],
        'organization': ['exact'],
        'specialization_code': ['exact'],
        'name_ar': ['icontains'],
    }
    search_fields = ['name_ar', 'name_en', 'specialization_code']
