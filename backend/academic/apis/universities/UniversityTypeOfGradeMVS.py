from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.universities.UniversityTypeOfGrade import UniversityTypeOfGrade
from academic.serializers.universities.UniversityTypeOfGrade import UniversityTypeOfGradeSerializer
from django.db.models import Q

class UniversityTypeOfGradeMVS(AllMVS):
    queryset = UniversityTypeOfGrade.objects.all()
    serializer_class = UniversityTypeOfGradeSerializer
    select_serializer_fields = ['id', 'name_ar']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'fk_branch': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        branch_id = self.request.query_params.get('branch') or self.request.query_params.get('fk_branch')
        if branch_id:
            qs = qs.filter(fk_branch_id=branch_id)

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(name_ar__icontains=search) |
                Q(name_en__icontains=search)
            )

        return qs.order_by('id')

TypeOfGradeMVS = UniversityTypeOfGradeMVS
