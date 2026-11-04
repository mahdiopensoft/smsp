from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.universities.UniversityLesson import UniversityLesson
from academic.serializers.universities.UniversityLesson import UniversityLessonSerializer
from django.db.models import Q

class UniversityLessonMVS(AllMVS):
    queryset = UniversityLesson.objects.select_related(
        'subject',
        'unit__semester_subject__fk_subject',
        'unit__semester'
    )
    serializer_class = UniversityLessonSerializer
    select_serializer_fields = ['id', 'name_ar', 'order']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'unit': ['exact'],
        'unit__semester': ['exact'],
        'unit__semester_subject': ['exact'],
        'subject': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        subject_id = self.request.query_params.get('subject') or self.request.query_params.get('subject_id')
        if subject_id:
            qs = qs.filter(
                Q(subject_id=subject_id) |
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
                Q(name_ar__icontains=search) |
                Q(name_en__icontains=search) |
                Q(unit__name_ar__icontains=search)
            )

        return qs.order_by('order', 'id')

LessonMVS = UniversityLessonMVS

