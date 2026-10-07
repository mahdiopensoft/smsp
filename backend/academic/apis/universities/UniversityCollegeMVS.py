from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.universities.UniversityCollege import UniversityCollege
from academic.serializers.universities.UniversityCollege import UniversityCollegeSerializer
from django.db.models import Q

class UniversityCollegeMVS(AllMVS):
    queryset = UniversityCollege.objects.all()
    serializer_class = UniversityCollegeSerializer
    select_serializer_fields = ['id', 'name_ar']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()
            
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
                Q(name_en__icontains=search)
            )

        return qs.order_by('college_no', 'id')

CollegeMVS = UniversityCollegeMVS
