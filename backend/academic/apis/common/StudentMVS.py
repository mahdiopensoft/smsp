from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.common.Student import Student
from academic.serializers.common.Student import StudentSerializer
from django.db.models import Q

class StudentMVS(AllMVS):
    queryset = Student.objects.select_related(
        'country', 'directorate', 'directorate__fk_governorate', 'organization', 'user',
        'class_track', 'class_track__level', 'class_track__track',
        'university_college', 'university_department', 'university_specialization', 'university_level',
        'institute_field', 'institute_education_system', 'institute_specialization', 'institute_level'
    ).all()
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
        'class_track': ['exact'],
        'university_college': ['exact'],
        'university_department': ['exact'],
        'university_specialization': ['exact'],
        'university_level': ['exact'],
        'institute_field': ['exact'],
        'institute_education_system': ['exact'],
        'institute_specialization': ['exact'],
        'institute_level': ['exact'],
        'academic_number': ['exact', 'icontains'],
        'phone_number': ['exact', 'icontains'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        # Institution Type filter
        inst_type = self.request.query_params.get('institution_type')
        if inst_type and inst_type != 'all':
            if inst_type == 'university':
                qs = qs.filter(Q(organization__institution_type='university') | Q(university_college__isnull=False) | Q(university_specialization__isnull=False))
            elif inst_type == 'institute':
                qs = qs.filter(Q(organization__institution_type='institute') | Q(institute_field__isnull=False) | Q(institute_specialization__isnull=False))
            elif inst_type == 'school':
                qs = qs.filter(Q(organization__institution_type='school') | Q(class_track__isnull=False))
            else:
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

        # ── School Filters ──
        class_track_id = self.request.query_params.get('class_track') or self.request.query_params.get('class_track_id')
        if class_track_id:
            qs = qs.filter(class_track_id=class_track_id)

        stage_id = self.request.query_params.get('stage') or self.request.query_params.get('stage_id')
        if stage_id:
            qs = qs.filter(class_track__level__stage_id=stage_id)

        # ── University Filters ──
        college_id = self.request.query_params.get('college') or self.request.query_params.get('university_college')
        if college_id:
            qs = qs.filter(university_college_id=college_id)

        dept_id = self.request.query_params.get('department') or self.request.query_params.get('university_department')
        if dept_id:
            qs = qs.filter(university_department_id=dept_id)

        spec_id = self.request.query_params.get('specialization') or self.request.query_params.get('university_specialization')
        if spec_id:
            qs = qs.filter(university_specialization_id=spec_id)

        univ_level_id = self.request.query_params.get('educational_level') or self.request.query_params.get('university_level')
        if univ_level_id:
            qs = qs.filter(university_level_id=univ_level_id)

        # ── Institute Filters ──
        field_id = self.request.query_params.get('institute_field') or self.request.query_params.get('field')
        if field_id:
            qs = qs.filter(institute_field_id=field_id)

        edu_sys_id = self.request.query_params.get('institute_education_system') or self.request.query_params.get('education_system')
        if edu_sys_id:
            qs = qs.filter(institute_education_system_id=edu_sys_id)

        inst_spec_id = self.request.query_params.get('institute_specialization')
        if inst_spec_id:
            qs = qs.filter(institute_specialization_id=inst_spec_id)

        inst_level_id = self.request.query_params.get('institute_level')
        if inst_level_id:
            qs = qs.filter(institute_level_id=inst_level_id)

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
                Q(organization__name_ar__icontains=search) |
                Q(university_specialization__name_ar__icontains=search) |
                Q(institute_specialization__name_ar__icontains=search)
            )

        return qs.order_by('-academic_number')
