from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.institutes.InstituteUnit import InstituteUnit
from academic.serializers.institutes.InstituteUnit import InstituteUnitSerializer
from django.db.models import Q

class InstituteUnitMVS(AllMVS):
    queryset = InstituteUnit.objects.select_related('subject', 'curriculum', 'semester').all()
    serializer_class = InstituteUnitSerializer
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'subject': ['exact'],
        'curriculum': ['exact'],
        'semester': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        subject_id = self.request.query_params.get('subject') or self.request.query_params.get('subject_id') or self.request.query_params.get('institute_subject')
        if subject_id:
            qs = qs.filter(subject_id=subject_id)

        curriculum_id = self.request.query_params.get('curriculum') or self.request.query_params.get('curriculum_id')
        if curriculum_id:
            qs = qs.filter(curriculum_id=curriculum_id)

        semester_id = self.request.query_params.get('semester') or self.request.query_params.get('semester_id')
        if semester_id:
            qs = qs.filter(semester_id=semester_id)

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(name_ar__icontains=search) |
                Q(name_en__icontains=search)
            )

        return qs.order_by('order', 'id').distinct()
