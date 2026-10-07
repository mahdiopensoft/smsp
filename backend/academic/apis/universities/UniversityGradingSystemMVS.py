from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.universities.UniversityGradingSystem import UniversityGradingSystem
from academic.serializers.universities.UniversityGradingSystem import UniversityGradingSystemSerializer

class UniversityGradingSystemMVS(AllMVS):
    queryset = UniversityGradingSystem.objects.all()
    serializer_class = UniversityGradingSystemSerializer
    select_serializer_fields = ['id', 'name_ar']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'grade_system_type': ['exact'],
    }

GradingSystemMVS = UniversityGradingSystemMVS
