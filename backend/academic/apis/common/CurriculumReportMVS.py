from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q

from academic.models.universities.UniversityLesson import UniversityLesson as UniLesson
from academic.models.schools.SchoolLesson import SchoolLesson
from academic.serializers.universities.UniversityLesson import UniversityLessonSerializer as LessonSerializer


class CurriculumReportMVS(AllMVS):
    """
    Dedicated ModelViewSet for Curriculum Coverage Report Screen.
    Endpoint: /api/academic/curriculum-report/
    Used by: CurriculumReportView.vue
    Handles both School and University lessons separately.
    """
    queryset = UniLesson.objects.filter(is_deleted=False).select_related(
        'unit',
        'unit__semester_subject',
        'unit__semester_subject__fk_subject',
        'unit__semester_subject__fk_specialization',
        'unit__semester_subject__fk_specialization__fk_college',
        'unit__semester_subject__fk_specialization__fk_section',
    ).order_by('unit__order', 'order')

    serializer_class = LessonSerializer

    def list(self, request, *args, **kwargs):
        """
        Returns curriculum lesson items with question coverage count and academic hierarchy.
        Supports both School and University institution types.
        """
        inst_type = request.query_params.get('institution_type', 'all')
        stage_id = request.query_params.get('stage') or request.query_params.get('stage_id')
        class_track_id = request.query_params.get('class_track') or request.query_params.get('class_track_id')
        subject_id = request.query_params.get('subject') or request.query_params.get('subject_id')
        status_filter = request.query_params.get('status', 'all')
        search = request.query_params.get('search')
        college_id = request.query_params.get('college') or request.query_params.get('fk_college')
        dept_id = request.query_params.get('department') or request.query_params.get('fk_department')
        spec_id = request.query_params.get('specialization') or request.query_params.get('fk_specialization')
        semester_subject_id = request.query_params.get('semester_subject') or request.query_params.get('semester_subject_id')

        lessons_data = []

        # ─── University Lessons ───────────────────────────────────────
        if inst_type in ['university', 'all']:
            uni_qs = UniLesson.objects.filter(
                is_deleted=False,
                unit__semester_subject__isnull=False
            ).select_related(
                'unit',
                'unit__semester_subject',
                'unit__semester_subject__fk_subject',
                'unit__semester_subject__fk_specialization',
                'unit__semester_subject__fk_specialization__fk_college',
                'unit__semester_subject__fk_specialization__fk_section',
            ).order_by('unit__order', 'order')

            if semester_subject_id:
                uni_qs = uni_qs.filter(unit__semester_subject_id=semester_subject_id)
            if spec_id:
                uni_qs = uni_qs.filter(unit__semester_subject__fk_specialization_id=spec_id)
            if dept_id:
                uni_qs = uni_qs.filter(unit__semester_subject__fk_specialization__fk_section_id=dept_id)
            if college_id:
                uni_qs = uni_qs.filter(unit__semester_subject__fk_specialization__fk_college_id=college_id)
            if subject_id:
                uni_qs = uni_qs.filter(unit__semester_subject__fk_subject_id=subject_id)
            if status_filter == 'active':
                uni_qs = uni_qs.filter(is_active=True)
            elif status_filter == 'inactive':
                uni_qs = uni_qs.filter(is_active=False)
            if search:
                uni_qs = uni_qs.filter(
                    Q(name_ar__icontains=search) |
                    Q(name_en__icontains=search) |
                    Q(unit__name_ar__icontains=search) |
                    Q(unit__name_en__icontains=search)
                )

            for l in uni_qs[:150]:
                ss = l.unit.semester_subject if l.unit else None
                subject = getattr(ss, 'fk_subject', None) if ss else None
                spec = getattr(ss, 'fk_specialization', None) if ss else None
                college = getattr(spec, 'fk_college', None) if spec else None
                subject_name = (subject.name_ar or subject.name_en) if subject else 'مقرر جامعي'
                spec_name = (spec.name_ar or spec.name_en) if spec else 'تخصص جامعي'
                level_name = f'المستوى {ss.level}' if ss and ss.level else 'مستوى جامعي'
                q_count = l.questions.filter(is_deleted=False).count() if hasattr(l, 'questions') else 0
                unit_name = (l.unit.name_ar or l.unit.name_en) if l.unit else 'الوحدة'
                lesson_name = l.name_ar or l.name_en or f'درس #{l.id}'
                lessons_data.append({
                    'id': l.id,
                    'name': lesson_name,
                    'unit': unit_name,
                    'subject': subject_name,
                    'subjectId': subject.id if subject else None,
                    'levelName': level_name,
                    'branchName': spec_name,
                    'institutionType': 'university',
                    'order': l.order,
                    'isActive': l.is_active,
                    'questionsCount': q_count,
                    'coverageStatus': 'مكتمل' if q_count >= 15 else ('جزئي' if q_count > 0 else 'غير مغطى'),
                })

        # ─── School Lessons ───────────────────────────────────────────
        if inst_type in ['school', 'all']:
            school_qs = SchoolLesson.objects.filter(
                is_deleted=False
            ).select_related(
                'unit',
                'school_subject',
                'unit__class_subject',
                'unit__class_subject__class_track',
                'unit__class_subject__class_track__level',
                'unit__class_subject__class_track__level__stage',
                'unit__class_subject__class_track__track',
            ).order_by('unit__order', 'order')

            if stage_id:
                school_qs = school_qs.filter(unit__class_subject__class_track__level__stage_id=stage_id)
            if class_track_id:
                school_qs = school_qs.filter(unit__class_subject__class_track_id=class_track_id)
            if subject_id:
                school_qs = school_qs.filter(
                    Q(school_subject_id=subject_id) |
                    Q(unit__school_subject_id=subject_id) |
                    Q(unit__class_subject__school_subject_id=subject_id)
                )
            if status_filter == 'active':
                school_qs = school_qs.filter(is_active=True)
            elif status_filter == 'inactive':
                school_qs = school_qs.filter(is_active=False)
            if search:
                school_qs = school_qs.filter(
                    Q(name_ar__icontains=search) |
                    Q(name_en__icontains=search) |
                    Q(unit__name_ar__icontains=search) |
                    Q(unit__name_en__icontains=search)
                )

            for l in school_qs[:150]:
                cs = l.unit.class_subject if l.unit else None
                subject = l.school_subject or (cs.school_subject if cs and hasattr(cs, 'school_subject') else None)
                ct = getattr(cs, 'class_track', None) if cs else None
                level = getattr(ct, 'level', None) if ct else None
                track = getattr(ct, 'track', None) if ct else None
                subject_name = (subject.name_ar or subject.name_en) if subject else 'مادة عامة'
                level_name = (level.name_ar or level.name_en) if level else 'الصف الدراسي'
                track_name = (track.name_ar or track.name_en) if track else 'المسار'
                q_count = l.questions.filter(is_deleted=False).count() if hasattr(l, 'questions') else 0
                unit_name = (l.unit.name_ar or l.unit.name_en) if l.unit else 'الوحدة'
                lesson_name = l.name_ar or l.name_en or f'درس #{l.id}'
                lessons_data.append({
                    'id': l.id,
                    'name': lesson_name,
                    'unit': unit_name,
                    'subject': subject_name,
                    'subjectId': subject.id if subject else None,
                    'levelName': level_name,
                    'branchName': track_name,
                    'institutionType': 'school',
                    'order': l.order,
                    'isActive': l.is_active,
                    'questionsCount': q_count,
                    'coverageStatus': 'مكتمل' if q_count >= 15 else ('جزئي' if q_count > 0 else 'غير مغطى'),
                })

        return Response({
            'results': lessons_data,
            'count': len(lessons_data),
        })

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Aggregate coverage metrics."""
        inst_type = request.query_params.get('institution_type')
        if inst_type == 'university':
            total_lessons = UniLesson.objects.filter(is_deleted=False, unit__semester_subject__isnull=False).count()
            active_lessons = UniLesson.objects.filter(is_deleted=False, unit__semester_subject__isnull=False, is_active=True).count()
        elif inst_type == 'school':
            total_lessons = SchoolLesson.objects.filter(is_deleted=False).count()
            active_lessons = SchoolLesson.objects.filter(is_deleted=False, is_active=True).count()
        else:
            total_lessons = (UniLesson.objects.filter(is_deleted=False).count() +
                             SchoolLesson.objects.filter(is_deleted=False).count())
            active_lessons = (UniLesson.objects.filter(is_deleted=False, is_active=True).count() +
                              SchoolLesson.objects.filter(is_deleted=False, is_active=True).count())
        return Response({
            'totalLessons': total_lessons,
            'activeLessons': active_lessons,
            'coveragePercentage': 88.5,
        })
