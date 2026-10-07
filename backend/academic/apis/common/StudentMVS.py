from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.common.Student import Student
from academic.serializers.common.Student import StudentSerializer
from django.db.models import Q

class StudentMVS(AllMVS):
    queryset = Student.objects.select_related('country', 'directorate', 'organization', 'user').all()
    serializer_class = StudentSerializer
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'gender': ['exact'],
        'organization': ['exact'],
        'organization__institution_type': ['exact'],
        'country': ['exact'],
        'directorate': ['exact'],
        'academic_number': ['exact', 'icontains'],
        'phone_number': ['exact', 'icontains'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        # Institution Type filter
        inst_type = self.request.query_params.get('institution_type')
        if inst_type and inst_type != 'all':
            qs = qs.filter(organization__institution_type=inst_type)

        # Organization filter
        org_id = self.request.query_params.get('organization') or self.request.query_params.get('organization_id')
        if org_id:
            qs = qs.filter(organization_id=org_id)

        # Gender filter
        gender = self.request.query_params.get('gender')
        if gender:
            qs = qs.filter(gender=gender)

        # Country filter
        country_id = self.request.query_params.get('country') or self.request.query_params.get('country_id')
        if country_id:
            qs = qs.filter(country_id=country_id)

        # Governorate filter
        gov_id = self.request.query_params.get('governorate') or self.request.query_params.get('governorate_id')
        if gov_id:
            qs = qs.filter(directorate__fk_governorate_id=gov_id)

        # Directorate filter
        directorate_id = self.request.query_params.get('directorate') or self.request.query_params.get('directorate_id')
        if directorate_id:
            qs = qs.filter(directorate_id=directorate_id)

        # Active filter
        is_active = self.request.query_params.get('is_active')
        if is_active is not None and is_active != '':
            if is_active in [True, 'true', 'True', 1, '1']:
                qs = qs.filter(is_active=True)
            elif is_active in [False, 'false', 'False', 0, '0']:
                qs = qs.filter(is_active=False)

        # Search Query
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(name_ar__icontains=search) |
                Q(name_en__icontains=search) |
                Q(academic_number__icontains=search) |
                Q(phone_number__icontains=search) |
                Q(organization__name_ar__icontains=search)
            )

        return qs.order_by('-academic_number')
