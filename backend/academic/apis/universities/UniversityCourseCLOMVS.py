from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.universities.UniversityCourseCLO import UniversityCourseCLO
from academic.serializers.universities.UniversityCourseCLO import UniversityCourseCLOSerializer
from django.db.models import Q

class UniversityCourseCLOMVS(AllMVS):
    queryset = UniversityCourseCLO.objects.select_related('course', 'topic').all()
    serializer_class = UniversityCourseCLOSerializer
    select_serializer_fields = ['id', 'clo_code', 'description']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'course': ['exact'],
        'topic': ['exact'],
        'domain': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        course_id = self.request.query_params.get('course') or self.request.query_params.get('course_id')
        if course_id:
            qs = qs.filter(course_id=course_id)

        topic_id = self.request.query_params.get('topic') or self.request.query_params.get('topic_id')
        if topic_id:
            qs = qs.filter(topic_id=topic_id)

        domain = self.request.query_params.get('domain')
        if domain:
            qs = qs.filter(domain=domain)

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(clo_code__icontains=search) |
                Q(description__icontains=search)
            )

        return qs.order_by('order', 'id')

CourseCLOMVS = UniversityCourseCLOMVS
