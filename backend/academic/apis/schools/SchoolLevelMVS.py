from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.schools.SchoolLevel import SchoolLevel
from academic.serializers.schools.SchoolLevel import SchoolLevelSerializer
from django.db.models import Q

class SchoolLevelMVS(AllMVS):
    queryset = SchoolLevel.objects.select_related('stage').all().distinct()
    serializer_class = SchoolLevelSerializer
    select_serializer_fields = ['id', 'name_ar']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'stage': ['exact'],
        'order': ['exact'],
        'class_tracks__track': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        # Stage filter
        stage_id = self.request.query_params.get('stage') or self.request.query_params.get('stage_id')
        if stage_id:
            qs = qs.filter(stage_id=stage_id)

        # Track filter
        track_id = self.request.query_params.get('track') or self.request.query_params.get('track_id')
        if track_id:
            qs = qs.filter(class_tracks__track_id=track_id)

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
                Q(stage__name_ar__icontains=search)
            )

        return qs.order_by('order', 'id').distinct()

LevelMVS = SchoolLevelMVS
