from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.schools.SchoolSubject import SchoolSubject
from academic.serializers.schools.SchoolSubject import SchoolSubjectSerializer
from django.db.models import Q

class SchoolSubjectMVS(AllMVS):
    queryset = SchoolSubject.objects.all()
    serializer_class = SchoolSubjectSerializer
    select_serializer_fields = ['id', 'name_ar', 'name_en', 'subject_code']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'is_ministerial': ['exact'],
        'is_detailed': ['exact'],
        'subject_code': ['exact', 'icontains'],
        'class_subjects__class_track__level': ['exact'],
        'class_subjects__class_track__track': ['exact'],
        'class_subjects__class_track__level__stage': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        stage_id = self.request.query_params.get('stage') or self.request.query_params.get('stage_id')
        if stage_id:
            qs = qs.filter(class_subjects__class_track__level__stage_id=stage_id)

        level_id = self.request.query_params.get('level') or self.request.query_params.get('level_id')
        if level_id:
            qs = qs.filter(class_subjects__class_track__level_id=level_id)

        track_id = self.request.query_params.get('track') or self.request.query_params.get('track_id')
        if track_id:
            qs = qs.filter(class_subjects__class_track__track_id=track_id)

        class_track_id = self.request.query_params.get('class_track') or self.request.query_params.get('class_track_id')
        if class_track_id:
            qs = qs.filter(class_subjects__class_track_id=class_track_id)

        is_ministerial = self.request.query_params.get('is_ministerial')
        if is_ministerial is not None and is_ministerial != '':
            if is_ministerial in [True, 'true', 'True', 1, '1']:
                qs = qs.filter(is_ministerial=True)
            elif is_ministerial in [False, 'false', 'False', 0, '0']:
                qs = qs.filter(is_ministerial=False)

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
                Q(subject_code__icontains=search)
            )

        return qs.order_by('subject_order', 'id').distinct()
