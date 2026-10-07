from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.institutes.InstituteShortCourse import InstituteShortCourse
from academic.serializers.institutes.InstituteShortCourse import InstituteShortCourseSerializer

class InstituteShortCourseMVS(AllMVS):
    queryset = InstituteShortCourse.objects.select_related('field', 'organization').all()
    serializer_class = InstituteShortCourseSerializer
    select_serializer_fields = ['id', 'name_ar', 'course_code', 'field_id', 'total_hours']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'field': ['exact'],
        'organization': ['exact'],
        'course_code': ['exact'],
        'name_ar': ['icontains'],
    }
    search_fields = ['name_ar', 'name_en', 'course_code']
