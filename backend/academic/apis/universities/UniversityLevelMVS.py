from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.universities.UniversityLevel import UniversityLevel
from academic.serializers.universities.UniversityLevel import UniversityLevelSerializer

class UniversityLevelMVS(AllMVS):
    queryset = UniversityLevel.objects.all()
    serializer_class = UniversityLevelSerializer
    select_serializer_fields = ['id', 'name_ar']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
    }

EducationalLevelsMVS = UniversityLevelMVS
