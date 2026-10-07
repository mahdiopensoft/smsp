from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.schools.SchoolTrack import SchoolTrack
from academic.serializers.schools.SchoolTrack import SchoolTrackSerializer
from django.db.models import Q

class SchoolTrackMVS(AllMVS):
    queryset = SchoolTrack.objects.all().distinct()
    serializer_class = SchoolTrackSerializer
    select_serializer_fields = ['id', 'name_ar']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'code': ['exact', 'icontains'],
        'track_classes__level': ['exact'],
        'track_classes__level__stage': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        # Stage filter
        stage_id = self.request.query_params.get('stage') or self.request.query_params.get('stage_id')
        if stage_id:
            qs = qs.filter(track_classes__level__stage_id=stage_id)

        # Level filter
        level_id = self.request.query_params.get('level') or self.request.query_params.get('level_id')
        if level_id:
            qs = qs.filter(track_classes__level_id=level_id)

        # Active filter
        is_active = self.request.query_params.get('is_active')
        if is_active is not None and is_active != '':
            if is_active in [True, 'true', 'True', 1, '1']:
                qs = qs.filter(is_active=True)
            elif is_active in [False, 'false', 'False', 0, '0']:
                qs = qs.filter(is_active=False)

        # Search Query
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(name_ar__icontains=search) |
                Q(name_en__icontains=search) |
                Q(code__icontains=search) |
                Q(note__icontains=search)
            )

        return qs.order_by('name_ar', 'id').distinct()

TrackMVS = SchoolTrackMVS
