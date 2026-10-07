from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.institutes.InstituteSpecialTrack import InstituteSpecialTrack
from academic.serializers.institutes.InstituteSpecialTrack import InstituteSpecialTrackSerializer

class InstituteSpecialTrackMVS(AllMVS):
    queryset = InstituteSpecialTrack.objects.select_related('field', 'education_system').all()
    serializer_class = InstituteSpecialTrackSerializer
    select_serializer_fields = ['id', 'name_ar', 'track_code', 'field_id', 'education_system_id', 'target_profession']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'field': ['exact'],
        'education_system': ['exact'],
        'track_code': ['exact'],
        'target_profession': ['icontains'],
        'name_ar': ['icontains'],
    }
    search_fields = ['name_ar', 'name_en', 'track_code', 'target_profession']
