from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.institutes.InstituteBatch import InstituteBatch
from academic.serializers.institutes.InstituteBatch import InstituteBatchSerializer

class InstituteBatchMVS(AllMVS):
    queryset = InstituteBatch.objects.select_related('specialization', 'curriculum', 'academic_year').all()
    serializer_class = InstituteBatchSerializer
    select_serializer_fields = ['id', 'name_ar', 'batch_number', 'specialization_id', 'curriculum_id', 'academic_year_id']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'specialization': ['exact'],
        'curriculum': ['exact'],
        'academic_year': ['exact'],
        'is_graduated': ['exact'],
        'batch_number': ['exact'],
        'name_ar': ['icontains'],
    }
    search_fields = ['name_ar', 'name_en']
