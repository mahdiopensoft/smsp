from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from rest_framework.response import Response
from django.db.models import Q
from exams.models.CurriculumExclusion import CurriculumExclusion
from exams.serializers.CurriculumExclusion import CurriculumExclusionSerializer


class CurriculumExclusionsReportMVS(AllMVS):
    """
    تقرير المحذوفات من المنهج
    Endpoint: /api/exams/curriculum-exclusions-report/
    Used by: CurriculumExclusionsReportView.vue
    """
    queryset = CurriculumExclusion.objects.filter(is_deleted=False).select_related(
        'stage', 'class_track', 'subject', 'unit', 'lesson', 'academic_year',
    ).order_by('-created_at')
    serializer_class = CurriculumExclusionSerializer

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()

        inst_type = request.query_params.get('institution_type')
        if inst_type and inst_type != 'all':
            qs = qs.filter(institution_type=inst_type)

        academic_year_id = request.query_params.get('academic_year')
        stage_id = request.query_params.get('stage')
        subject_id = request.query_params.get('subject')
        exclusion_type = request.query_params.get('exclusion_type')
        is_active = request.query_params.get('is_active')

        if academic_year_id:
            qs = qs.filter(academic_year_id=academic_year_id)
        if stage_id:
            qs = qs.filter(stage_id=stage_id)
        if subject_id:
            qs = qs.filter(subject_id=subject_id)
        if exclusion_type:
            qs = qs.filter(exclusion_type=exclusion_type)
        if is_active is not None and is_active != '':
            qs = qs.filter(is_active=(is_active in ['true', 'True', '1', True]))

        results = []
        for ex in qs[:300]:
            year_name = ''
            if ex.academic_year:
                year_name = getattr(ex.academic_year, 'name', '') or getattr(ex.academic_year, 'name_ar', '') or str(ex.academic_year)
            stage_name = (ex.stage.name_ar or ex.stage.name_en) if ex.stage else ''
            subject_name = (ex.subject.name_ar or ex.subject.name_en) if ex.subject else ''
            unit_name = (ex.unit.name_ar or ex.unit.name_en) if ex.unit else ''
            lesson_name = (ex.lesson.name_ar or ex.lesson.name_en) if ex.lesson else ''

            results.append({
                'id': ex.id,
                'academicYear': year_name,
                'institutionType': ex.institution_type or '',
                'stage': stage_name,
                'subject': subject_name,
                'exclusionType': ex.exclusion_type or '',
                'unit': unit_name,
                'lesson': lesson_name,
                'reason': ex.reason or '',
                'isActive': ex.is_active,
                'createdAt': ex.created_at.strftime('%Y-%m-%d') if ex.created_at else '',
            })

        return Response({'results': results, 'count': len(results)})

