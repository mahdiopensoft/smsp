from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.universities.UniversityUnit import UniversityUnit
from academic.serializers.universities.UniversityUnit import UniversityUnitSerializer
from django.db.models import Q

class UniversityUnitMVS(AllMVS):
    queryset = UniversityUnit.objects.select_related(
        'semester_subject__fk_subject',
        'semester'
    ).all()
    serializer_class = UniversityUnitSerializer
    select_serializer_fields = ['id', 'name_ar', 'order']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'semester': ['exact'],
        'semester_subject': ['exact'],
        'semester_subject__fk_specialization': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        semester_subject_id = self.request.query_params.get('semester_subject') or self.request.query_params.get('semester_subject_id')
        if semester_subject_id:
            qs = qs.filter(semester_subject_id=semester_subject_id)

        semester_id = self.request.query_params.get('semester') or self.request.query_params.get('semester_id')
        if semester_id:
            qs = qs.filter(semester_id=semester_id)

        specialization_id = self.request.query_params.get('specialization') or self.request.query_params.get('specialization_id')
        if specialization_id:
            qs = qs.filter(semester_subject__fk_specialization_id=specialization_id)

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
                Q(semester_subject__fk_subject__name_ar__icontains=search)
            )

        return qs.order_by('order', 'id')

UnitMVS = UniversityUnitMVS

