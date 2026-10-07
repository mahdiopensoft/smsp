from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.schools.SchoolClassTrack import SchoolClassTrack
from academic.serializers.schools.SchoolClassTrack import SchoolClassTrackSerializer
from django.db.models import Q

class SchoolClassTrackMVS(AllMVS):
    queryset = SchoolClassTrack.objects.select_related('level', 'track', 'level__stage').all()
    serializer_class = SchoolClassTrackSerializer
    select_serializer_fields = ['id', 'full_name', 'name_ar']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_default': ['exact'],
        'track': ['exact'],
        'level__stage': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        # Stage filter
        stage_id = self.request.query_params.get('stage') or self.request.query_params.get('stage_id')
        if stage_id:
            qs = qs.filter(level__stage_id=stage_id)

        # Track filter
        track_id = self.request.query_params.get('track') or self.request.query_params.get('track_id')
        if track_id:
            qs = qs.filter(track_id=track_id)

        # Default track filter
        is_default = self.request.query_params.get('is_default')
        if is_default is not None and is_default != '':
            if is_default in [True, 'true', 'True', 1, '1']:
                qs = qs.filter(is_default=True)
            elif is_default in [False, 'false', 'False', 0, '0']:
                qs = qs.filter(is_default=False)

        # Search Query
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(level__name_ar__icontains=search) |
                Q(track__name_ar__icontains=search) |
                Q(note__icontains=search)
            )

        return qs.order_by('level__order', 'id')

ClassTrackMVS = SchoolClassTrackMVS
