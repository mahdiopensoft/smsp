from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.universities.UniversitySubject import UniversitySubject
from academic.serializers.universities.UniversitySubject import UniversitySubjectSerializer
from django.db.models import Q

class UniversitySubjectMVS(AllMVS):
    queryset = UniversitySubject.objects.all().distinct()
    serializer_class = UniversitySubjectSerializer
    select_serializer_fields = ['id', 'name_ar', 'name_en']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'is_ministerial': ['exact'],
        'subject_code': ['exact', 'icontains'],
        'semester_subjects__fk_specialization': ['exact'],
        'semester_subjects__fk_specialization__fk_college': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        specialization_id = self.request.query_params.get('specialization') or self.request.query_params.get('specialization_id')
        if specialization_id:
            qs = qs.filter(semester_subjects__fk_specialization_id=specialization_id)

        college_id = self.request.query_params.get('college') or self.request.query_params.get('college_id')
        if college_id:
            qs = qs.filter(semester_subjects__fk_specialization__fk_college_id=college_id)

        department_id = self.request.query_params.get('department') or self.request.query_params.get('department_id')
        if department_id:
            qs = qs.filter(semester_subjects__fk_specialization__fk_section_id=department_id)

        semester_subject_id = self.request.query_params.get('semester_subject') or self.request.query_params.get('semester_subject_id')
        if semester_subject_id:
            qs = qs.filter(semester_subjects__id=semester_subject_id)

        is_ministerial = self.request.query_params.get('is_ministerial')
        if is_ministerial is not None and is_ministerial != '':
            if is_ministerial in [True, 'true', 'True', 1, '1']:
                qs = qs.filter(is_ministerial=True)
            elif is_ministerial in [False, 'false', 'False', 0, '0']:
                qs = qs.filter(is_ministerial=False)

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
                Q(subject_code__icontains=search)
            )

        return qs.order_by('subject_order', 'id').distinct()

SubjectMVS = UniversitySubjectMVS

