from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.universities.UniversityDepartment import UniversityDepartment
from academic.serializers.universities.UniversityDepartment import UniversityDepartmentSerializer
from django.db.models import Q

class UniversityDepartmentMVS(AllMVS):
    queryset = UniversityDepartment.objects.select_related('fk_college').all()
    serializer_class = UniversityDepartmentSerializer
    select_serializer_fields = ['id', 'name_ar']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'fk_college': ['exact'],
        'is_active': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()
        
        college_id = self.request.query_params.get('college') or self.request.query_params.get('fk_college')
        if college_id:
            qs = qs.filter(fk_college_id=college_id)

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(name_ar__icontains=search) |
                Q(name_en__icontains=search) |
                Q(section_code__icontains=search)
            )

        return qs.order_by('id')

DepartmentMVS = UniversityDepartmentMVS
