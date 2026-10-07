from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.institutes.InstituteCurriculumSubject import InstituteCurriculumSubject
from academic.serializers.institutes.InstituteCurriculumSubject import InstituteCurriculumSubjectSerializer

class InstituteCurriculumSubjectMVS(AllMVS):
    queryset = InstituteCurriculumSubject.objects.select_related(
        'curriculum', 'subject', 'level', 'semester'
    ).all()
    serializer_class = InstituteCurriculumSubjectSerializer
    select_serializer_fields = ['id', 'curriculum_id', 'subject_id', 'level_id', 'semester_id', 'is_ministerial_exam']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'curriculum': ['exact'],
        'subject': ['exact'],
        'level': ['exact'],
        'semester': ['exact'],
        'is_ministerial_exam': ['exact'],
        'exam_entity': ['exact'],
        'added_to_total': ['exact'],
    }
    search_fields = ['subject__name_ar', 'curriculum__name_ar']
