from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.universities.UniversityGradeDistribution import UniversityGradeDistribution
from academic.serializers.universities.UniversityGradeDistribution import UniversityGradeDistributionSerializer

class UniversityGradeDistributionMVS(AllMVS):
    queryset = UniversityGradeDistribution.objects.select_related('fk_grading_system', 'fk_type_of_grade').all()
    serializer_class = UniversityGradeDistributionSerializer
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'fk_grading_system': ['exact'],
        'fk_type_of_grade': ['exact'],
    }

GradeDistributionMVS = UniversityGradeDistributionMVS
