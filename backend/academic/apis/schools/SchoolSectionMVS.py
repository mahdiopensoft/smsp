from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.schools.SchoolSection import SchoolSection
from academic.serializers.schools.SchoolSection import SchoolSectionSerializer
from django.db.models import Q

class SchoolSectionMVS(AllMVS):
    queryset = SchoolSection.objects.select_related('organization', 'class_track', 'academic_year').all()
    serializer_class = SchoolSectionSerializer
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'organization': ['exact'],
        'class_track': ['exact'],
        'academic_year': ['exact'],
        'gender': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        org_id = self.request.query_params.get('organization') or self.request.query_params.get('organization_id')
        if org_id:
            qs = qs.filter(organization_id=org_id)

        class_track_id = self.request.query_params.get('class_track') or self.request.query_params.get('class_track_id')
        if class_track_id:
            qs = qs.filter(class_track_id=class_track_id)

        level_id = self.request.query_params.get('level') or self.request.query_params.get('level_id')
        if level_id:
            qs = qs.filter(class_track__level_id=level_id)

        year_id = self.request.query_params.get('year') or self.request.query_params.get('academic_year')
        if year_id:
            qs = qs.filter(academic_year_id=year_id)

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(name_ar__icontains=search) |
                Q(name_en__icontains=search) |
                Q(section_code__icontains=search)
            )

        return qs.order_by('class_track', 'name_ar', 'id').distinct()
