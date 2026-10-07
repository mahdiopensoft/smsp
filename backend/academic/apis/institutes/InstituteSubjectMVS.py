from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.institutes.InstituteSubject import InstituteSubject
from academic.serializers.institutes.InstituteSubject import InstituteSubjectSerializer

class InstituteSubjectMVS(AllMVS):
    queryset = InstituteSubject.objects.select_related('field').all()
    serializer_class = InstituteSubjectSerializer
    select_serializer_fields = ['id', 'name_ar', 'subject_code', 'subject_type', 'subject_entity', 'academic_category']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'field': ['exact'],
        'subject_type': ['exact'],
        'subject_entity': ['exact'],
        'academic_category': ['exact'],
        'subject_code': ['exact'],
        'name_ar': ['icontains'],
    }
    search_fields = ['name_ar', 'name_en', 'subject_code']
