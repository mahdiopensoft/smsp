from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.universities.UniversityCollegeBranch import UniversityCollegeBranch
from academic.serializers.universities.UniversityCollegeBranch import UniversityCollegeBranchSerializer

class UniversityCollegeBranchMVS(AllMVS):
    queryset = UniversityCollegeBranch.objects.select_related('fk_branch', 'fk_college').all()
    serializer_class = UniversityCollegeBranchSerializer
    select_serializer_fields = ['id', 'fk_college__name_ar']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'fk_branch': ['exact'],
        'fk_college': ['exact'],
    }

CollegeBranchMVS = UniversityCollegeBranchMVS
