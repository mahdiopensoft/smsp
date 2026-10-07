from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from academic.models.common.LearningOutcome import LearningOutcome
from academic.models.common.Subject import Subject
from academic.models.universities.UniversitySemesterSubject import UniversitySemesterSubject as SemesterSubject
from academic.models.common.Unit import Unit
from bank.models.Question import Question

class AlignmentMatrixReportMVS(AllMVS):
    """
    Dedicated ModelViewSet for Course Learning Outcomes (CLO) Alignment Matrix Report.
    Endpoint: /api/academic/alignment-matrix-report/
    Used by: AlignmentMatrixReportView.vue
    Required for: ABET / NCAAA Academic Quality & Accreditation Audits.
    Supports both University (SemesterSubject/Specialization) and School (Subject/ClassTrack).
    """
    queryset = LearningOutcome.objects.select_related('unit').all()

    @action(detail=False, methods=['get'])
    def matrix(self, request):
        """
        Calculates CLO alignment matrix for a specific subject, semester subject, or unit.
        Query Params:
            institution_type: str ('school', 'university', 'all')
            college: int (optional)
            department: int (optional)
            specialization: int (optional)
            semester_subject: int (optional)
            subject_id: int (optional)
            stage: int (optional)
            level: int (optional)
            class_track: int (optional)
            unit_id: int (optional)
            search: str (optional)
        """
        institution_type = request.query_params.get('institution_type')
        college_id = request.query_params.get('college')
        department_id = request.query_params.get('department')
        specialization_id = request.query_params.get('specialization')
        semester_subject_id = request.query_params.get('semester_subject') or request.query_params.get('semester_subject_id')

        subject_id = request.query_params.get('subject_id') or request.query_params.get('subject')
        unit_id = request.query_params.get('unit_id') or request.query_params.get('unit')
        stage_id = request.query_params.get('stage')
        level_id = request.query_params.get('level')
        class_track_id = request.query_params.get('class_track') or request.query_params.get('class_track_id')
        search = request.query_params.get('search')

        # If no subject specified, pick first subject / semester_subject based on institution_type
        if not subject_id and not semester_subject_id and not stage_id and not level_id and not college_id:
            if institution_type == 'university':
                first_sem = SemesterSubject.objects.filter(is_deleted=False).select_related('course', 'fk_subject', 'fk_specialization').first()
                if first_sem:
                    semester_subject_id = first_sem.id
            else:
                first_subject = Subject.objects.filter(is_active=True).first()
                if first_subject:
                    subject_id = first_subject.id

        # Determine subject / course display name
        subject_name = "مادة / مقرر عام"
        if semester_subject_id:
            try:
                ss = SemesterSubject.objects.select_related('course', 'fk_subject', 'fk_specialization').get(id=semester_subject_id)
                course_title = ss.course.name_ar if ss.course else (ss.fk_subject.name_ar if ss.fk_subject else f"مقرر #{ss.id}")
                subject_name = course_title
                if ss.fk_specialization:
                    subject_name += f" ({ss.fk_specialization.name_ar or ss.fk_specialization.name_en})"
            except SemesterSubject.DoesNotExist:
                subject_name = f"مقرر #{semester_subject_id}"
        elif subject_id:
            try:
                subj = Subject.objects.get(id=subject_id)
                subject_name = getattr(subj, 'name_ar', None) or getattr(subj, 'name_en', None) or str(subj)
            except Subject.DoesNotExist:
                # Check if it was a semester subject ID
                try:
                    ss = SemesterSubject.objects.select_related('course', 'fk_subject', 'fk_specialization').get(id=subject_id)
                    course_title = ss.course.name_ar if ss.course else (ss.fk_subject.name_ar if ss.fk_subject else f"مقرر #{ss.id}")
                    subject_name = course_title
                    if ss.fk_specialization:
                        subject_name += f" ({ss.fk_specialization.name_ar or ss.fk_specialization.name_en})"
                except SemesterSubject.DoesNotExist:
                    subject_name = f"مادة #{subject_id}"

        # Filter learning outcomes
        los_qs = LearningOutcome.objects.all().select_related(
            'unit__semester_subject__fk_subject',
            'unit__semester_subject__course',
            'unit__semester_subject__fk_specialization__fk_college',
            'unit__class_subject__subject',
            'unit__class_subject__class_track__level__stage',
            'subject'
        )

        # Institution type filter
        if institution_type == 'university':
            los_qs = los_qs.filter(unit__semester_subject__isnull=False)
        elif institution_type == 'school':
            los_qs = los_qs.filter(unit__class_subject__isnull=False)

        # University filters
        if semester_subject_id:
            los_qs = los_qs.filter(unit__semester_subject_id=semester_subject_id)
        if specialization_id:
            los_qs = los_qs.filter(unit__semester_subject__fk_specialization_id=specialization_id)
        if department_id:
            los_qs = los_qs.filter(unit__semester_subject__fk_specialization__fk_section_id=department_id)
        if college_id:
            los_qs = los_qs.filter(unit__semester_subject__fk_specialization__fk_college_id=college_id)

        # School filters
        if subject_id and not semester_subject_id:
            los_qs = los_qs.filter(
                Q(unit__class_subject__subject_id=subject_id) |
                Q(subject_id=subject_id) |
                Q(unit__semester_subject__fk_subject_id=subject_id) |
                Q(unit__semester_subject_id=subject_id)
            )

        if stage_id:
            los_qs = los_qs.filter(unit__class_subject__class_track__level__stage_id=stage_id)

        if level_id:
            los_qs = los_qs.filter(unit__class_subject__class_track__level_id=level_id)

        if class_track_id:
            los_qs = los_qs.filter(unit__class_subject__class_track_id=class_track_id)

        if unit_id:
            los_qs = los_qs.filter(unit_id=unit_id)

        if search:
            los_qs = los_qs.filter(
                Q(code__icontains=search) |
                Q(description__icontains=search)
            )

        clo_data = []
        total_questions = 0
        uncovered_clos = 0

        for lo in los_qs[:150]:
            # Questions attached to this LO
            questions = Question.objects.filter(
                learningOutcome=lo,
                status=Question.StatusChoices.APPROVED
            )
            q_count = questions.count()
            total_questions += q_count

            if q_count == 0:
                uncovered_clos += 1
                coverage_status = 'فجوة - لا توجد أسئلة'
                coverage_color = 'error'
            elif q_count < 3:
                coverage_status = 'تغطية منخفضة'
                coverage_color = 'warning'
            else:
                coverage_status = 'تغطية كافية'
                coverage_color = 'success'

            # Bloom taxonomy breakdown
            bloom_counts = {
                'remember': questions.filter(bloomLevel='تذكر').count(),
                'understand': questions.filter(bloomLevel='فهم').count(),
                'apply': questions.filter(bloomLevel='تطبيق').count(),
                'analyze': questions.filter(bloomLevel='تحليل').count(),
                'evaluate': questions.filter(bloomLevel='تقييم').count(),
                'create': questions.filter(bloomLevel='ابتكار').count(),
            }

            # Difficulty breakdown
            difficulty_counts = {
                'easy': questions.filter(difficulty=1).count(),
                'medium': questions.filter(difficulty=2).count(),
                'hard': questions.filter(difficulty=3).count(),
            }

            is_univ = bool(hasattr(lo, 'unit') and lo.unit and getattr(lo.unit, 'semester_subject_id', None))

            clo_data.append({
                'id': lo.id,
                'code': getattr(lo, 'code', None) or f"CLO-{lo.id}",
                'name_ar': getattr(lo, 'description', None) or getattr(lo, 'name_ar', '') or str(lo),
                'unit_id': lo.unit_id if hasattr(lo, 'unit_id') else None,
                'unit_name': getattr(lo.unit, 'name_ar', '') if hasattr(lo, 'unit') and lo.unit else '',
                'institutionType': 'university' if is_univ else 'school',
                'questions_count': q_count,
                'coverage_status': coverage_status,
                'coverage_color': coverage_color,
                'bloom_breakdown': bloom_counts,
                'difficulty_breakdown': difficulty_counts,
            })

        total_clos = len(clo_data)
        coverage_rate = round(((total_clos - uncovered_clos) / total_clos * 100), 1) if total_clos > 0 else 0

        return Response({
            "subject_id": semester_subject_id or subject_id,
            "subject_name": subject_name,
            "total_clos": total_clos,
            "uncovered_clos": uncovered_clos,
            "coverage_rate_percentage": coverage_rate,
            "total_approved_questions": total_questions,
            "clos": clo_data
        })
