from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.universities.UniversitySpecialization import UniversitySpecialization
from academic.serializers.universities.UniversitySpecialization import UniversitySpecializationSerializer
from django.db.models import Q

class UniversitySpecializationMVS(AllMVS):
    queryset = UniversitySpecialization.objects.select_related('fk_college', 'fk_section', 'fk_educational_levels').all()
    serializer_class = UniversitySpecializationSerializer
    select_serializer_fields = ['id', 'name_ar']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'fk_college': ['exact'],
        'fk_section': ['exact'],
        'fk_educational_levels': ['exact'],
        'is_active': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()
        
        college_id = self.request.query_params.get('college') or self.request.query_params.get('fk_college')
        if college_id:
            qs = qs.filter(fk_college_id=college_id)
            
        section_id = self.request.query_params.get('section') or self.request.query_params.get('department') or self.request.query_params.get('fk_section')
        if section_id:
            qs = qs.filter(fk_section_id=section_id)

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(name_ar__icontains=search) |
                Q(name_en__icontains=search) |
                Q(specialization_code__icontains=search)
            )

        return qs.order_by('id')

SpecializationMVS = UniversitySpecializationMVS
