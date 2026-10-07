from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.schools.SchoolClassSubject import SchoolClassSubject
from academic.serializers.schools.SchoolClassSubject import SchoolClassSubjectSerializer
from django.db.models import Q

class SchoolClassSubjectMVS(AllMVS):
    queryset = SchoolClassSubject.objects.select_related(
        'class_track__level', 
        'class_track__track', 
        'class_track__level__stage', 
        'school_subject',
        'subject'
    ).all()
    serializer_class = SchoolClassSubjectSerializer
    select_serializer_fields = ['id', 'subject_name', 'name_ar']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'added_to_total': ['exact'],
        'optional': ['exact'],
        'subject': ['exact'],
        'school_subject': ['exact'],
        'class_track': ['exact'],
        'class_track__level': ['exact'],
        'class_track__track': ['exact'],
        'class_track__level__stage': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        # Hierarchy filters
        stage_id = self.request.query_params.get('stage') or self.request.query_params.get('stage_id')
        if stage_id:
            qs = qs.filter(class_track__level__stage_id=stage_id)

        level_id = self.request.query_params.get('level') or self.request.query_params.get('level_id')
        if level_id:
            qs = qs.filter(class_track__level_id=level_id)

        track_id = self.request.query_params.get('track') or self.request.query_params.get('track_id')
        if track_id:
            qs = qs.filter(class_track__track_id=track_id)

        subject_id = self.request.query_params.get('subject') or self.request.query_params.get('subject_id')
        if subject_id:
            qs = qs.filter(Q(subject_id=subject_id) | Q(school_subject_id=subject_id))

        # Added to total filter
        added_to_total = self.request.query_params.get('added_to_total')
        if added_to_total is not None and added_to_total != '':
            if added_to_total in [True, 'true', 'True', 1, '1']:
                qs = qs.filter(added_to_total=True)
            elif added_to_total in [False, 'false', 'False', 0, '0']:
                qs = qs.filter(added_to_total=False)

        # Optional filter
        optional = self.request.query_params.get('optional')
        if optional is not None and optional != '':
            if optional in [True, 'true', 'True', 1, '1']:
                qs = qs.filter(optional=True)
            elif optional in [False, 'false', 'False', 0, '0']:
                qs = qs.filter(optional=False)

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
                Q(school_subject__name_ar__icontains=search) |
                Q(school_subject__name_en__icontains=search) |
                Q(subject__name_ar__icontains=search) |
                Q(subject__name_en__icontains=search) |
                Q(class_track__level__name_ar__icontains=search) |
                Q(class_track__track__name_ar__icontains=search)
            )

        return qs.order_by('class_track__level__order', 'id')

ClassSubjectMVS = SchoolClassSubjectMVS
