from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.universities.UniversityCourse import UniversityCourse
from academic.serializers.universities.UniversityCourse import UniversityCourseSerializer
from django.db.models import Q

class UniversityCourseMVS(AllMVS):
    queryset = UniversityCourse.objects.select_related('college', 'department', 'prerequisite_course').all()
    serializer_class = UniversityCourseSerializer
    select_serializer_fields = ['id', 'name_ar', 'name_en', 'course_code', 'credit_hours']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'course_type': ['exact'],
        'credit_hours': ['exact', 'gte', 'lte'],
        'course_code': ['exact', 'icontains'],
        'college': ['exact'],
        'department': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        college_id = self.request.query_params.get('college') or self.request.query_params.get('college_id') or self.request.query_params.get('fk_college')
        if college_id:
            qs = qs.filter(college_id=college_id)

        department_id = self.request.query_params.get('department') or self.request.query_params.get('department_id') or self.request.query_params.get('fk_section')
        if department_id:
            qs = qs.filter(department_id=department_id)

        specialization_id = self.request.query_params.get('specialization') or self.request.query_params.get('specialization_id') or self.request.query_params.get('fk_specialization')
        if specialization_id:
            qs = qs.filter(semester_subjects__fk_specialization_id=specialization_id)

        course_type = self.request.query_params.get('course_type')
        if course_type:
            qs = qs.filter(course_type=course_type)

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
                Q(course_code__icontains=search)
            )

        return qs.order_by('course_code', 'id').distinct()
