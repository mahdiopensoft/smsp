from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.universities.UniversityCourseTopic import UniversityCourseTopic
from academic.serializers.universities.UniversityCourseTopic import UniversityCourseTopicSerializer
from django.db.models import Q

class UniversityCourseTopicMVS(AllMVS):
    queryset = UniversityCourseTopic.objects.select_related('course', 'semester_subject').all()
    serializer_class = UniversityCourseTopicSerializer
    select_serializer_fields = ['id', 'name_ar', 'order', 'week_number']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'course': ['exact'],
        'semester_subject': ['exact'],
        'week_number': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        course_id = self.request.query_params.get('course') or self.request.query_params.get('course_id')
        if course_id:
            qs = qs.filter(course_id=course_id)

        semester_subject_id = self.request.query_params.get('semester_subject') or self.request.query_params.get('semester_subject_id')
        if semester_subject_id:
            qs = qs.filter(semester_subject_id=semester_subject_id)

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(name_ar__icontains=search) |
                Q(name_en__icontains=search) |
                Q(description__icontains=search)
            )

        return qs.order_by('week_number', 'order', 'id')

CourseTopicMVS = UniversityCourseTopicMVS
