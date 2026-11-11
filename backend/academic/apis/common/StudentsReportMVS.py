from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from rest_framework.response import Response
from django.db.models import Q
from academic.models.common.Student import Student
from academic.serializers.common.Student import StudentSerializer


class StudentsReportMVS(AllMVS):
    """
    تقرير الطلاب
    Endpoint: /api/academic/students-report/
    Used by: StudentsReportView.vue
    """
    queryset = Student.objects.filter(is_deleted=False).select_related(
        'organization', 'directorate', 'directorate__fk_governorate',
        'class_track', 'class_track__level', 'class_track__level__stage',
        'university_college',
    ).order_by('name_ar')
    serializer_class = StudentSerializer

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()

        inst_type = request.query_params.get('institution_type')
        governorate_id = request.query_params.get('governorate')
        directorate_id = request.query_params.get('directorate')
        organization_id = request.query_params.get('organization') or request.query_params.get('school')
        college_id = request.query_params.get('college')
        stage_id = request.query_params.get('stage')
        search = request.query_params.get('search')

        if inst_type == 'university':
            qs = qs.filter(university_college__isnull=False)
        elif inst_type == 'school':
            qs = qs.filter(class_track__isnull=False)

        if governorate_id:
            qs = qs.filter(directorate__fk_governorate_id=governorate_id)
        if directorate_id:
            qs = qs.filter(directorate_id=directorate_id)
        if organization_id:
            qs = qs.filter(organization_id=organization_id)
        if college_id:
            qs = qs.filter(university_college_id=college_id)
        if stage_id:
            qs = qs.filter(class_track__level__stage_id=stage_id)
        if search:
            qs = qs.filter(
                Q(name_ar__icontains=search) |
                Q(name_en__icontains=search) |
                Q(academic_number__icontains=search)
            )

        results = []
        for s in qs[:300]:
            gov_name = ''
            dir_name = ''
            if s.directorate:
                dir_name = s.directorate.name_ar or s.directorate.name_en or ''
                if s.directorate.fk_governorate:
                    gov_name = s.directorate.fk_governorate.name_ar or s.directorate.fk_governorate.name_en or ''

            org_name = ''
            if s.organization:
                org_name = s.organization.name_ar or s.organization.name_en or ''
            elif s.university_college:
                org_name = s.university_college.name_ar or s.university_college.name_en or ''

            stage_or_level = ''
            if s.class_track and s.class_track.level:
                stage_or_level = s.class_track.level.name_ar or s.class_track.level.name_en or ''
            elif s.university_college:
                stage_or_level = 'جامعي'

            results.append({
                'id': s.id,
                'name': s.name_ar or s.name_en or '',
                'academicNumber': s.academic_number or '',
                'gender': 'ذكر' if s.gender == 1 else 'أنثى',
                'institution': org_name,
                'levelStage': stage_or_level,
                'governorate': gov_name,
                'directorate': dir_name,
                'createdAt': s.created_at.strftime('%Y-%m-%d') if s.created_at else '',
            })

        return Response({'results': results, 'count': len(results)})
