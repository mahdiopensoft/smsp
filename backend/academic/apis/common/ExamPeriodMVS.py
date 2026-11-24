from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.universities.UniversityExamPeriod import UniversityExamPeriod
from academic.models.schools.SchoolExamPeriod import SchoolExamPeriod
from academic.models.institutes.InstituteExamPeriod import InstituteExamPeriod

from academic.serializers.universities.UniversityExamPeriod import UniversityExamPeriodSerializer
from academic.serializers.schools.SchoolExamPeriod import SchoolExamPeriodSerializer
from academic.serializers.institutes.InstituteExamPeriod import InstituteExamPeriodSerializer
from academic.apis.universities.UniversityExamPeriodMVS import UniversityExamPeriodMVS
from django.db.models import Q

class CommonExamPeriodMVS(AllMVS):
    """
    موجه الفترات الامتحانية الموحد (Unified Exam Period Router):
    - إذا كان institution_type == 'school' -> يعيد فترات المدارس (SchoolExamPeriod)
    - إذا كان institution_type == 'institute' -> يعيد فترات المعاهد (InstituteExamPeriod)
    - إذا كان institution_type == 'university' (أو افتراضي) -> يعيد فترات الجامعات (UniversityExamPeriod)
    """
    queryset = UniversityExamPeriod.objects.select_related('fk_semester').all()
    serializer_class = UniversityExamPeriodSerializer
    select_serializer_fields = ['id', 'name_ar']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]

    def _get_institution_type(self):
        inst_type = self.request.query_params.get('institution_type') or self.request.query_params.get('institutionType')
        if not inst_type and hasattr(self.request, 'data') and isinstance(self.request.data, dict):
            inst_type = self.request.data.get('institution_type') or self.request.data.get('institutionType')
        return (inst_type or '').strip().lower()

    def get_serializer_class(self):
        inst_type = self._get_institution_type()
        if inst_type == 'school':
            return SchoolExamPeriodSerializer
        elif inst_type == 'institute':
            return InstituteExamPeriodSerializer
        return UniversityExamPeriodSerializer

    def get_queryset(self):
        inst_type = self._get_institution_type()
        is_active = self.request.query_params.get('is_active')
        search = self.request.query_params.get('search')
        semester_id = self.request.query_params.get('semester') or self.request.query_params.get('fk_semester')

        if inst_type == 'school':
            qs = SchoolExamPeriod.objects.all()
        elif inst_type == 'institute':
            qs = InstituteExamPeriod.objects.select_related('fk_semester').all()
            if semester_id:
                qs = qs.filter(fk_semester_id=semester_id)
        else:
            qs = UniversityExamPeriod.objects.select_related('fk_semester').all()
            if semester_id:
                qs = qs.filter(fk_semester_id=semester_id)

        if is_active is not None and is_active != '':
            if is_active in [True, 'true', 'True', 1, '1']:
                qs = qs.filter(is_active=True)
            elif is_active in [False, 'false', 'False', 0, '0']:
                qs = qs.filter(is_active=False)

        if search:
            qs = qs.filter(
                Q(name_ar__icontains=search) |
                Q(name_en__icontains=search)
            )

        return qs.order_by('order', 'id')

ExamPeriodMVS = CommonExamPeriodMVS
__all__ = ['ExamPeriodMVS', 'CommonExamPeriodMVS']
