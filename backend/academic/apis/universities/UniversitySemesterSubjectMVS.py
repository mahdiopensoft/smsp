from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.universities.UniversitySemesterSubject import UniversitySemesterSubject
from academic.serializers.universities.UniversitySemesterSubject import UniversitySemesterSubjectSerializer
from django.db.models import Q

class UniversitySemesterSubjectMVS(AllMVS):
    queryset = UniversitySemesterSubject.objects.select_related(
        'fk_specialization',
        'fk_specialization__fk_college',
        'course',
        'fk_subject',
        'semester'
    ).all()
    serializer_class = UniversitySemesterSubjectSerializer
    select_serializer_fields = ['id', 'name_ar']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'fk_specialization': ['exact'],
        'course': ['exact'],
        'fk_subject': ['exact'],
        'semester': ['exact'],
        'level': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()
        
        specialization_id = self.request.query_params.get('specialization') or self.request.query_params.get('fk_specialization')
        if specialization_id:
            qs = qs.filter(fk_specialization_id=specialization_id)
            
        semester_id = self.request.query_params.get('semester')
        if semester_id:
            qs = qs.filter(semester_id=semester_id)

        level = self.request.query_params.get('level')
        if level:
            qs = qs.filter(level=level)
            
        subject_id = self.request.query_params.get('subject') or self.request.query_params.get('fk_subject') or self.request.query_params.get('course')
        if subject_id:
            qs = qs.filter(Q(fk_subject_id=subject_id) | Q(course_id=subject_id))

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(course__name_ar__icontains=search) |
                Q(course__name_en__icontains=search) |
                Q(course__course_code__icontains=search) |
                Q(fk_subject__name_ar__icontains=search) |
                Q(fk_specialization__name_ar__icontains=search)
            )

        return qs.order_by('level', 'id')

SemesterSubjectMVS = UniversitySemesterSubjectMVS
