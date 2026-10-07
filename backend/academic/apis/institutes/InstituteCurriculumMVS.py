from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.institutes.InstituteCurriculum import InstituteCurriculum
from academic.serializers.institutes.InstituteCurriculum import InstituteCurriculumSerializer

class InstituteCurriculumMVS(AllMVS):
    queryset = InstituteCurriculum.objects.select_related('specialization', 'academic_year').all()
    serializer_class = InstituteCurriculumSerializer
    select_serializer_fields = ['id', 'name_ar', 'version_code', 'specialization_id', 'academic_year_id']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'specialization': ['exact'],
        'academic_year': ['exact'],
        'is_approved': ['exact'],
        'is_current': ['exact'],
        'version_code': ['exact'],
        'name_ar': ['icontains'],
    }
    search_fields = ['name_ar', 'name_en', 'version_code']
