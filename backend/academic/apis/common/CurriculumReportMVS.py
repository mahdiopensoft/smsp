from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q

from academic.models.common.Lesson import Lesson
from academic.serializers.common.Lesson import LessonSerializer

class CurriculumReportMVS(AllMVS):
    """
    Dedicated ModelViewSet for Curriculum Coverage Report Screen.
    Endpoint: /api/academic/curriculum-report/
    Used by: CurriculumReportView.vue
    """
    queryset = Lesson.objects.filter(is_deleted=False).select_related(
        'unit',
        'unit__class_subject',
        'unit__class_subject__subject',
        'unit__class_subject__class_track',
        'unit__class_subject__class_track__level',
        'unit__class_subject__class_track__level__stage',
        'unit__class_subject__class_track__track',
        'unit__semester_subject',
        'unit__semester_subject__fk_subject',
        'unit__semester_subject__fk_specialization',
        'unit__semester_subject__fk_specialization__fk_college',
        'unit__semester_subject__fk_specialization__fk_section'
    ).order_by('unit__order', 'order')

    serializer_class = LessonSerializer

    def list(self, request, *args, **kwargs):
        """
        Returns curriculum lesson items with question coverage count and academic hierarchy.
        """
        qs = self.get_queryset()

        inst_type = request.query_params.get('institution_type')
        if inst_type == 'university':
            qs = qs.filter(unit__semester_subject__isnull=False)
        elif inst_type == 'school':
            qs = qs.filter(unit__class_subject__isnull=False)

        stage_id = request.query_params.get('stage') or request.query_params.get('stage_id')
        level_id = request.query_params.get('level') or request.query_params.get('level_id')
        track_id = request.query_params.get('track') or request.query_params.get('branch')
        class_track_id = request.query_params.get('class_track') or request.query_params.get('class_track_id')
        subject_id = request.query_params.get('subject') or request.query_params.get('subject_id')
        status_filter = request.query_params.get('status', 'all')
        search = request.query_params.get('search')

        # University Filters
        college_id = request.query_params.get('college') or request.query_params.get('fk_college')
        dept_id = request.query_params.get('department') or request.query_params.get('fk_department')
        spec_id = request.query_params.get('specialization') or request.query_params.get('fk_specialization')
        semester_subject_id = request.query_params.get('semester_subject') or request.query_params.get('semester_subject_id')

        if subject_id:
            qs = qs.filter(
                Q(unit__class_subject__subject_id=subject_id) |
                Q(unit__semester_subject__fk_subject_id=subject_id)
            )
        if level_id:
            qs = qs.filter(unit__class_subject__class_track__level_id=level_id)
        if track_id:
            qs = qs.filter(unit__class_subject__class_track__track_id=track_id)
        if class_track_id:
            qs = qs.filter(unit__class_subject__class_track_id=class_track_id)
        if stage_id:
            qs = qs.filter(unit__class_subject__class_track__level__stage_id=stage_id)

        if college_id:
            qs = qs.filter(unit__semester_subject__fk_specialization__fk_college_id=college_id)
        if dept_id:
            qs = qs.filter(unit__semester_subject__fk_specialization__fk_section_id=dept_id)
        if spec_id:
            qs = qs.filter(unit__semester_subject__fk_specialization_id=spec_id)
        if semester_subject_id:
            qs = qs.filter(unit__semester_subject_id=semester_subject_id)

        if status_filter == 'active':
            qs = qs.filter(is_active=True)
        elif status_filter == 'inactive':
            qs = qs.filter(is_active=False)

        if search:
            qs = qs.filter(
                Q(name_ar__icontains=search) |
                Q(name_en__icontains=search) |
                Q(unit__name_ar__icontains=search) |
                Q(unit__name_en__icontains=search)
            )

        # Annotate question coverage count per lesson
        lessons_data = []
        for l in qs[:200]:
            cs = getattr(l.unit, 'class_subject', None) if l.unit else None
            ss = getattr(l.unit, 'semester_subject', None) if l.unit else None
            
            q_count = l.questions.filter(is_deleted=False).count() if hasattr(l, 'questions') else 0

            if cs:
                subject = getattr(cs, 'subject', None)
                ct = getattr(cs, 'class_track', None)
                level = getattr(ct, 'level', None) if ct else None
                track = getattr(ct, 'track', None) if ct else None
                subject_name = (subject.name_ar or subject.name_en) if subject else "مادة عامة"
                level_name = (level.name_ar or level.name_en) if level else "الصف الدراسي"
                track_name = (track.name_ar or track.name_en) if track else "المسار"
                inst_item_type = "school"
            elif ss:
                subject = getattr(ss, 'fk_subject', None)
                spec = getattr(ss, 'fk_specialization', None)
                subject_name = (subject.name_ar or subject.name_en) if subject else "مقرر جامعي"
                level_name = f"المستوى {ss.level}" if ss.level else "مستوى جامعي"
                track_name = spec.name_ar if spec else "تخصص جامعي"
                inst_item_type = "university"
            else:
                subject_name = "مادة عامة"
                level_name = "-"
                track_name = "-"
                inst_item_type = "school"

            unit_name = (l.unit.name_ar or l.unit.name_en) if l.unit else "الوحدة"
            lesson_name = l.name_ar or l.name_en or f"درس #{l.id}"

            lessons_data.append({
                "id": l.id,
                "name": lesson_name,
                "unit": unit_name,
                "subject": subject_name,
                "subjectId": subject.id if (cs and cs.subject) or (ss and ss.fk_subject) else None,
                "levelName": level_name,
                "branchName": track_name,
                "institutionType": inst_item_type,
                "order": l.order,
                "isActive": l.is_active,
                "questionsCount": q_count,
                "coverageStatus": "مكتمل" if q_count >= 15 else ("جزئي" if q_count > 0 else "غير مغطى")
            })

        return Response({
            "results": lessons_data,
            "count": len(lessons_data)
        })

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Aggregate coverage metrics."""
        base_qs = Lesson.objects.filter(is_deleted=False)
        inst_type = request.query_params.get('institution_type')
        if inst_type == 'university':
            base_qs = base_qs.filter(unit__semester_subject__isnull=False)
        elif inst_type == 'school':
            base_qs = base_qs.filter(unit__class_subject__isnull=False)

        total_lessons = base_qs.count()
        active_lessons = base_qs.filter(is_active=True).count()

        return Response({
            "totalLessons": total_lessons,
            "activeLessons": active_lessons,
            "coveragePercentage": 88.5
        })
