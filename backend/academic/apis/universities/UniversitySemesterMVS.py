from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.universities.UniversitySemester import UniversitySemester
from academic.serializers.universities.UniversitySemester import UniversitySemesterSerializer
from django.db.models import Q

class UniversitySemesterMVS(AllMVS):
    queryset = UniversitySemester.objects.all()
    serializer_class = UniversitySemesterSerializer
    select_serializer_fields = ['id', 'name_ar']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'is_current': ['exact'],
        'order': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        is_active = self.request.query_params.get('is_active')
        if is_active is not None and is_active != '':
            if is_active in [True, 'true', 'True', 1, '1']:
                qs = qs.filter(is_active=True)
            elif is_active in [False, 'false', 'False', 0, '0']:
                qs = qs.filter(is_active=False)

        is_current = self.request.query_params.get('is_current')
        if is_current is not None and is_current != '':
            if is_current in [True, 'true', 'True', 1, '1']:
                qs = qs.filter(is_current=True)
            elif is_current in [False, 'false', 'False', 0, '0']:
                qs = qs.filter(is_current=False)

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(name_ar__icontains=search) |
                Q(name_en__icontains=search)
            )

        return qs.order_by('order', 'id')

SemesterMVS = UniversitySemesterMVS
