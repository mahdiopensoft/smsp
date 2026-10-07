from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.common.ExamPeriod import ExamPeriod
from academic.serializers.common.ExamPeriod import ExamPeriodSerializer
from django.db.models import Q

class ExamPeriodMVS(AllMVS):
    queryset = ExamPeriod.objects.select_related('fk_semester').all()
    serializer_class = ExamPeriodSerializer
    select_serializer_fields = ['id', 'name_ar']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'order': ['exact'],
        'fk_semester': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()
        
        semester_id = self.request.query_params.get('semester') or self.request.query_params.get('fk_semester')
        if semester_id:
            qs = qs.filter(fk_semester_id=semester_id)
                
        # Active filter
        is_active = self.request.query_params.get('is_active')
        if is_active is not None and is_active != '':
            if is_active in [True, 'true', 'True', 1, '1']:
                qs = qs.filter(is_active=True)
            elif is_active in [False, 'false', 'False', 0, '0']:
                qs = qs.filter(is_active=False)

        # Search Query
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(name_ar__icontains=search) |
                Q(name_en__icontains=search)
            )

        return qs.order_by('order', 'id')
