from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.schools.SchoolLesson import SchoolLesson
from academic.serializers.schools.SchoolLesson import SchoolLessonSerializer
from django.db.models import Q

class SchoolLessonMVS(AllMVS):
    queryset = SchoolLesson.objects.select_related(
        'unit',
        'school_subject',
        'unit__semester',
        'unit__school_subject',
        'unit__class_subject__school_subject',
        'unit__class_subject__class_track__level__stage'
    ).all()
    serializer_class = SchoolLessonSerializer
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'unit': ['exact'],
        'school_subject': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        stage_id = self.request.query_params.get('stage') or self.request.query_params.get('stage_id')
        if stage_id:
            qs = qs.filter(unit__class_subject__class_track__level__stage_id=stage_id)

        class_track_id = self.request.query_params.get('class_track') or self.request.query_params.get('class_track_id')
        if class_track_id:
            qs = qs.filter(unit__class_subject__class_track_id=class_track_id)

        semester_id = self.request.query_params.get('semester') or self.request.query_params.get('semester_id')
        if semester_id:
            qs = qs.filter(unit__semester_id=semester_id)

        unit_id = self.request.query_params.get('unit') or self.request.query_params.get('unit_id')
        if unit_id:
            qs = qs.filter(unit_id=unit_id)

        subject_id = self.request.query_params.get('school_subject') or self.request.query_params.get('subject') or self.request.query_params.get('subject_id')
        if subject_id:
            qs = qs.filter(
                Q(school_subject_id=subject_id) |
                Q(unit__school_subject_id=subject_id) |
                Q(unit__class_subject__school_subject_id=subject_id)
            )

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(name_ar__icontains=search) |
                Q(name_en__icontains=search)
            )

        return qs.order_by('order', 'id').distinct()
