from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.schools.SchoolLesson import SchoolLesson
from academic.serializers.schools.SchoolLesson import SchoolLessonSerializer
from django.db.models import Q

class SchoolLessonMVS(AllMVS):
    queryset = SchoolLesson.objects.select_related('unit', 'school_subject').all()
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

        unit_id = self.request.query_params.get('unit') or self.request.query_params.get('unit_id')
        if unit_id:
            qs = qs.filter(unit_id=unit_id)

        subject_id = self.request.query_params.get('school_subject') or self.request.query_params.get('subject') or self.request.query_params.get('subject_id')
        if subject_id:
            qs = qs.filter(Q(school_subject_id=subject_id) | Q(unit__school_subject_id=subject_id))

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(name_ar__icontains=search) |
                Q(name_en__icontains=search)
            )

        return qs.order_by('order', 'id').distinct()
