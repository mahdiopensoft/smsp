from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.universities.UniversityStudySystem import UniversityStudySystem
from academic.serializers.universities.UniversityStudySystem import UniversityStudySystemSerializer

class UniversityStudySystemMVS(AllMVS):
    queryset = UniversityStudySystem.objects.all()
    serializer_class = UniversityStudySystemSerializer
    select_serializer_fields = ['id', 'name_ar']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
    }

StudeySystemMVS = UniversityStudySystemMVS
StudySystemMVS = UniversityStudySystemMVS
