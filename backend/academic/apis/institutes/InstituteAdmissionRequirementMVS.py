from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.institutes.InstituteAdmissionRequirement import InstituteAdmissionRequirement
from academic.serializers.institutes.InstituteAdmissionRequirement import InstituteAdmissionRequirementSerializer

class InstituteAdmissionRequirementMVS(AllMVS):
    queryset = InstituteAdmissionRequirement.objects.select_related('education_system', 'specialization').all()
    serializer_class = InstituteAdmissionRequirementSerializer
    select_serializer_fields = ['id', 'title', 'education_system_id', 'specialization_id', 'required_qualification']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'education_system': ['exact'],
        'specialization': ['exact'],
        'title': ['icontains'],
        'required_qualification': ['icontains'],
    }
    search_fields = ['title', 'required_qualification', 'accepted_tracks']
