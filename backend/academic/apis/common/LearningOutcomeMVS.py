from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.common.LearningOutcome import LearningOutcome
from academic.serializers.common.LearningOutcome import LearningOutcomeSerializer
from django.db.models import Q

class LearningOutcomeMVS(AllMVS):
    queryset = LearningOutcome.objects.select_related(
        'subject',
        'unit__class_subject__subject',
        'unit__class_subject__class_track__level',
        'unit__class_subject__class_track__track',
        'unit__semester_subject__fk_subject',
        'unit__semester'
    )
    serializer_class = LearningOutcomeSerializer
    select_serializer_fields = ['id', 'name_ar', 'code']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'unit': ['exact'],
        'unit__semester': ['exact'],
        'unit__class_subject': ['exact'],
        'unit__class_subject__class_track': ['exact'],
        'unit__class_subject__subject': ['exact'],
        'unit__class_subject__class_track__level': ['exact'],
        'unit__class_subject__class_track__track': ['exact'],
        'unit__class_subject__class_track__level__stage': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        # Direct parameter filtering
        stage_id = self.request.query_params.get('stage') or self.request.query_params.get('stage_id')
        if stage_id:
            qs = qs.filter(unit__class_subject__class_track__level__stage_id=stage_id)

        class_track_id = self.request.query_params.get('class_track') or self.request.query_params.get('class_track_id')
        if class_track_id:
            qs = qs.filter(unit__class_subject__class_track_id=class_track_id)

        level_id = self.request.query_params.get('level') or self.request.query_params.get('level_id')
        if level_id:
            qs = qs.filter(unit__class_subject__class_track__level_id=level_id)

        track_id = self.request.query_params.get('track') or self.request.query_params.get('track_id')
        if track_id:
            qs = qs.filter(unit__class_subject__class_track__track_id=track_id)

        subject_id = self.request.query_params.get('subject') or self.request.query_params.get('subject_id')
        if subject_id:
            qs = qs.filter(
                Q(subject_id=subject_id) |
                Q(unit__class_subject__subject_id=subject_id) |
                Q(unit__semester_subject__fk_subject_id=subject_id)
            )

        semester_id = self.request.query_params.get('semester') or self.request.query_params.get('semester_id')
        if semester_id:
            qs = qs.filter(unit__semester_id=semester_id)

        unit_id = self.request.query_params.get('unit') or self.request.query_params.get('unit_id')
        if unit_id:
            qs = qs.filter(unit_id=unit_id)

        is_active = self.request.query_params.get('is_active')
        if is_active is not None and is_active != '':
            if is_active in [True, 'true', 'True', 1, '1']:
                qs = qs.filter(is_active=True)
            elif is_active in [False, 'false', 'False', 0, '0']:
                qs = qs.filter(is_active=False)

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(code__icontains=search) |
                Q(description__icontains=search) |
                Q(unit__name_ar__icontains=search) |
                Q(unit__class_subject__subject__name_ar__icontains=search)
            )

        return qs.order_by('order', 'id')
