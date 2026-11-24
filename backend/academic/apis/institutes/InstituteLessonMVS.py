from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.institutes.InstituteLesson import InstituteLesson
from academic.serializers.institutes.InstituteLesson import InstituteLessonSerializer
from django.db.models import Q

class InstituteLessonMVS(AllMVS):
    queryset = InstituteLesson.objects.select_related('unit', 'subject', 'unit__subject', 'unit__curriculum').all()
    serializer_class = InstituteLessonSerializer
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'unit': ['exact'],
        'subject': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        unit_id = self.request.query_params.get('unit') or self.request.query_params.get('unit_id')
        if unit_id:
            qs = qs.filter(unit_id=unit_id)

        subject_id = self.request.query_params.get('subject') or self.request.query_params.get('subject_id') or self.request.query_params.get('institute_subject')
        if subject_id:
            qs = qs.filter(Q(subject_id=subject_id) | Q(unit__subject_id=subject_id))

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(name_ar__icontains=search) |
                Q(name_en__icontains=search)
            )

        return qs.order_by('order', 'id').distinct()
