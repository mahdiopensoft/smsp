from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.universities.UniversitySpecializationBranch import UniversitySpecializationBranch
from academic.serializers.universities.UniversitySpecializationBranch import UniversitySpecializationBranchSerializer

class UniversitySpecializationBranchMVS(AllMVS):
    queryset = UniversitySpecializationBranch.objects.select_related('fk_branch', 'fk_specialization').all()
    serializer_class = UniversitySpecializationBranchSerializer
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'fk_branch': ['exact'],
        'fk_specialization': ['exact'],
    }

SpecializationBranchMVS = UniversitySpecializationBranchMVS
