from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.schools.SchoolUnit import SchoolUnit
from academic.serializers.schools.SchoolUnit import SchoolUnitSerializer
from django.db.models import Q

class SchoolUnitMVS(AllMVS):
    queryset = SchoolUnit.objects.select_related('school_subject', 'class_subject', 'semester').all()
    serializer_class = SchoolUnitSerializer
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'school_subject': ['exact'],
        'class_subject': ['exact'],
        'semester': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        subject_id = self.request.query_params.get('school_subject') or self.request.query_params.get('subject') or self.request.query_params.get('subject_id')
        if subject_id:
            qs = qs.filter(Q(school_subject_id=subject_id) | Q(class_subject__school_subject_id=subject_id))

        class_subject_id = self.request.query_params.get('class_subject') or self.request.query_params.get('class_subject_id')
        if class_subject_id:
            qs = qs.filter(class_subject_id=class_subject_id)

        class_track_id = self.request.query_params.get('class_track') or self.request.query_params.get('class_track_id')
        if class_track_id:
            qs = qs.filter(class_subject__class_track_id=class_track_id)

        semester_id = self.request.query_params.get('semester') or self.request.query_params.get('semester_id')
        if semester_id:
            qs = qs.filter(semester_id=semester_id)

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(name_ar__icontains=search) |
                Q(name_en__icontains=search)
            )

        return qs.order_by('order', 'id').distinct()
