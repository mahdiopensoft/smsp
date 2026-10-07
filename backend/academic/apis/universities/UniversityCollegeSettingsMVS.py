from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.universities.UniversityCollegeSettings import UniversityCollegeSettings
from academic.serializers.universities.UniversityCollegeSettings import UniversityCollegeSettingsSerializer

class UniversityCollegeSettingsMVS(AllMVS):
    queryset = UniversityCollegeSettings.objects.all()
    serializer_class = UniversityCollegeSettingsSerializer
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'fk_college': ['exact'],
    }

CollegeSettingsMVS = UniversityCollegeSettingsMVS
