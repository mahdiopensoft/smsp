from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.common.Unit import Unit
from academic.serializers.common.Unit import UnitSerializer
from django.db.models import Q

class UnitMVS(AllMVS):
    queryset = Unit.objects.select_related(
        'class_subject__subject',
        'class_subject__class_track__level',
        'class_subject__class_track__track',
        'semester_subject__fk_subject',
        'semester'
    ).all()
    serializer_class = UnitSerializer
    select_serializer_fields = ['id', 'name_ar', 'order_unit']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'enable_learning_outcomes': ['exact'],
        'semester': ['exact'],
        'class_subject': ['exact'],
        'semester_subject': ['exact'],
        'class_subject__class_track': ['exact'],
        'class_subject__subject': ['exact'],
        'class_subject__class_track__level': ['exact'],
        'class_subject__class_track__track': ['exact'],
        'class_subject__class_track__level__stage': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        # Direct parameter filtering
        stage_id = self.request.query_params.get('stage') or self.request.query_params.get('stage_id')
        if stage_id:
            qs = qs.filter(class_subject__class_track__level__stage_id=stage_id)

        class_track_id = self.request.query_params.get('class_track') or self.request.query_params.get('class_track_id')
        if class_track_id:
            qs = qs.filter(class_subject__class_track_id=class_track_id)

        level_id = self.request.query_params.get('level') or self.request.query_params.get('level_id')
        if level_id:
            qs = qs.filter(class_subject__class_track__level_id=level_id)

        track_id = self.request.query_params.get('track') or self.request.query_params.get('track_id')
        if track_id:
            qs = qs.filter(class_subject__class_track__track_id=track_id)

        subject_id = self.request.query_params.get('subject') or self.request.query_params.get('subject_id') or self.request.query_params.get('class_subject__subject')
        if subject_id:
            qs = qs.filter(
                Q(class_subject__subject_id=subject_id) |
                Q(semester_subject__fk_subject_id=subject_id)
            )

        semester_subject_id = self.request.query_params.get('semester_subject') or self.request.query_params.get('semester_subject_id')
        if semester_subject_id:
            qs = qs.filter(semester_subject_id=semester_subject_id)

        semester_id = self.request.query_params.get('semester') or self.request.query_params.get('semester_id')
        if semester_id:
            qs = qs.filter(semester_id=semester_id)

        is_active = self.request.query_params.get('is_active')
        if is_active is not None and is_active != '':
            if is_active in [True, 'true', 'True', 1, '1']:
                qs = qs.filter(is_active=True)
            elif is_active in [False, 'false', 'False', 0, '0']:
                qs = qs.filter(is_active=False)

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(name_ar__icontains=search) |
                Q(name_en__icontains=search) |
                Q(class_subject__subject__name_ar__icontains=search)
            )

        return qs.order_by('order', 'id')
