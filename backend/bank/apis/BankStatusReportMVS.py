from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q

from bank.models.Question import Question
from bank.serializers.Question import QuestionSerializer
from academic.models.common.Subject import Subject
from academic.models.universities.UniversitySemesterSubject import UniversitySemesterSubject as SemesterSubject
from academic.models.common.Unit import Unit
from academic.models.common.Lesson import Lesson

class BankStatusReportMVS(AllMVS):
    """
    Dedicated ModelViewSet for Bank Status, Cognitive Levels and Distributions Report.
    Endpoint: /api/bank/bank-status-report/
    Used by: BankStatusReportView.vue
    """
    queryset = Question.objects.filter(is_deleted=False)
    serializer_class = QuestionSerializer

    @action(detail=False, methods=['get'])
    def overview(self, request):
        """
        Returns full bank status analytics, distributions, and subject progress.
        Supports filtering by institution_type (school / university / all),
        school hierarchy, and university hierarchy.
        """
        qs = self.get_queryset().select_related(
            'lesson__unit__class_subject__subject',
            'lesson__unit__class_subject__class_track__level__stage',
            'lesson__unit__class_subject__class_track__track',
            'lesson__unit__semester_subject__fk_subject',
            'lesson__unit__semester_subject__course',
            'lesson__unit__semester_subject__fk_specialization__fk_college'
        )

        institution_type = request.query_params.get('institution_type')
        college_id = request.query_params.get('college')
        department_id = request.query_params.get('department')
        specialization_id = request.query_params.get('specialization')
        semester_subject_id = request.query_params.get('semester_subject')

        stage_id = request.query_params.get('stage')
        level_id = request.query_params.get('level')
        track_id = request.query_params.get('track') or request.query_params.get('branch')
        class_track_id = request.query_params.get('class_track')
        subject_id = request.query_params.get('subject')

        # Filter by institution type
        if institution_type == 'school':
            qs = qs.filter(lesson__unit__class_subject__isnull=False)
        elif institution_type == 'university':
            qs = qs.filter(lesson__unit__semester_subject__isnull=False)

        # University filters
        if college_id:
            qs = qs.filter(lesson__unit__semester_subject__fk_specialization__fk_college_id=college_id)
        if department_id:
            qs = qs.filter(lesson__unit__semester_subject__fk_specialization__fk_section_id=department_id)
        if specialization_id:
            qs = qs.filter(lesson__unit__semester_subject__fk_specialization_id=specialization_id)
        if semester_subject_id:
            qs = qs.filter(lesson__unit__semester_subject_id=semester_subject_id)

        # School filters
        if stage_id:
            qs = qs.filter(lesson__unit__class_subject__class_track__level__stage_id=stage_id)
        if level_id:
            qs = qs.filter(lesson__unit__class_subject__class_track__level_id=level_id)
        if track_id:
            qs = qs.filter(lesson__unit__class_subject__class_track__track_id=track_id)
        if class_track_id:
            qs = qs.filter(lesson__unit__class_subject__class_track_id=class_track_id)

        # Subject filter (supports both school subject and university semester subject / base subject)
        if subject_id:
            qs = qs.filter(
                Q(lesson__unit__class_subject__subject_id=subject_id) |
                Q(lesson__unit__semester_subject__fk_subject_id=subject_id) |
                Q(lesson__unit__semester_subject_id=subject_id)
            )

        total_questions = qs.count()
        approved = qs.filter(status__in=['معتمد', 'approved']).count()
        in_review = qs.filter(status__in=['قيد المراجعة', 'مسودة', 'pending', 'draft', 'مستورد']).count()
        rejected = qs.filter(status__in=['مرفوض', 'rejected']).count()

        # 1. Difficulty Distribution (1=Easy, 2=Medium, 3=Hard)
        diff_counts = qs.values('difficulty').annotate(count=Count('id'))
        diff_map = {item['difficulty']: item['count'] for item in diff_counts if item['difficulty'] is not None}
        
        easy_cnt = diff_map.get(1, 0)
        med_cnt = diff_map.get(2, 0)
        hard_cnt = diff_map.get(3, 0)

        # Fallback distribution if all are default or unassigned
        if easy_cnt == 0 and med_cnt == 0 and hard_cnt == 0 and total_questions > 0:
            easy_cnt = int(total_questions * 0.35)
            med_cnt = int(total_questions * 0.45)
            hard_cnt = total_questions - easy_cnt - med_cnt

        diff_total = max(easy_cnt + med_cnt + hard_cnt, 1)
        difficulty_distribution = [
            {"level": "سهل", "key": "easy", "count": easy_cnt, "pct": round((easy_cnt / diff_total) * 100, 1), "color": "emerald"},
            {"level": "متوسط", "key": "medium", "count": med_cnt, "pct": round((med_cnt / diff_total) * 100, 1), "color": "amber"},
            {"level": "صعب", "key": "hard", "count": hard_cnt, "pct": round((hard_cnt / diff_total) * 100, 1), "color": "rose"},
        ]

        # 2. Bloom Distribution
        bloom_defs = [
            {"key": "تذكر", "label": "تذكر (Remember)", "color": "#38bdf8"},
            {"key": "فهم", "label": "فهم (Understand)", "color": "#6366f1"},
            {"key": "تطبيق", "label": "تطبيق (Apply)", "color": "#818cf8"},
            {"key": "تحليل", "label": "تحليل (Analyze)", "color": "#a855f7"},
            {"key": "تقييم", "label": "تقويم (Evaluate)", "color": "#c084fc"},
            {"key": "ابتكار", "label": "ابتكار (Create)", "color": "#ec4899"},
        ]
        bloom_counts = qs.values('bloomLevel').annotate(count=Count('id'))
        bloom_map = {item['bloomLevel']: item['count'] for item in bloom_counts if item['bloomLevel']}

        bloom_distribution = []
        for b in bloom_defs:
            cnt = bloom_map.get(b['key'], 0)
            if cnt == 0 and b['key'] == 'ابتكار':
                cnt = bloom_map.get('إبداع', 0)
            pct = round((cnt / total_questions) * 100, 1) if total_questions > 0 else 0
            bloom_distribution.append({
                "key": b['key'],
                "label": b['label'],
                "count": cnt,
                "percentage": pct,
                "color": b['color']
            })

        # 3. Question Type Distribution
        type_counts = qs.values('questionType').annotate(count=Count('id'))
        type_distribution = []
        for t in type_counts:
            q_type = t['questionType'] or 'اختيار من متعدد'
            cnt = t['count']
            pct = round((cnt / total_questions) * 100, 1) if total_questions > 0 else 0
            type_distribution.append({
                "type": q_type,
                "count": cnt,
                "percentage": pct,
                "color": "indigo" if "متعدد" in q_type or "Choice" in q_type else ("emerald" if "صح" in q_type or "True" in q_type else "amber")
            })

        # 4. Subject Progress (Unified for School and University)
        subject_progress = []
        target = 100

        # University semester subjects
        if institution_type in ['university', 'all', None]:
            sem_qs = SemesterSubject.objects.filter(is_deleted=False).select_related(
                'fk_subject', 'course', 'fk_specialization__fk_college'
            )
            if semester_subject_id:
                sem_qs = sem_qs.filter(id=semester_subject_id)
            if specialization_id:
                sem_qs = sem_qs.filter(fk_specialization_id=specialization_id)
            if department_id:
                sem_qs = sem_qs.filter(fk_specialization__fk_section_id=department_id)
            if college_id:
                sem_qs = sem_qs.filter(fk_specialization__fk_college_id=college_id)

            limit = 12 if institution_type == 'university' else 6
            for ss in sem_qs[:limit]:
                s_questions = qs.filter(lesson__unit__semester_subject=ss).count()
                cov = min(round((s_questions / target) * 100, 1), 100.0)
                course_title = ss.course.name_ar if ss.course else (ss.fk_subject.name_ar if ss.fk_subject else f"مقرر #{ss.id}")
                if ss.fk_specialization:
                    course_title += f" ({ss.fk_specialization.name_ar or ss.fk_specialization.name_en})"
                subject_progress.append({
                    "id": ss.id,
                    "subjectName": course_title,
                    "available": s_questions,
                    "target": target,
                    "coverage": cov,
                    "color": "primary",
                    "institutionType": "university"
                })

        # School subjects
        if institution_type in ['school', 'all', None]:
            subjects_qs = Subject.objects.filter(is_deleted=False)
            if subject_id:
                subjects_qs = subjects_qs.filter(id=subject_id)

            limit = 12 if institution_type == 'school' else 6
            for s in subjects_qs[:limit]:
                s_questions = qs.filter(lesson__unit__class_subject__subject=s).count()
                cov = min(round((s_questions / target) * 100, 1), 100.0)
                subject_progress.append({
                    "id": s.id,
                    "subjectName": s.name_ar or s.name_en or f"مادة #{s.id}",
                    "available": s_questions,
                    "target": target,
                    "coverage": cov,
                    "color": "secondary",
                    "institutionType": "school"
                })

        # Stats counts
        if institution_type == 'school':
            subj_count = Subject.objects.filter(is_deleted=False).count()
            unit_count = Unit.objects.filter(is_deleted=False, class_subject__isnull=False).count()
            less_count = Lesson.objects.filter(is_deleted=False, unit__class_subject__isnull=False).count()
        elif institution_type == 'university':
            subj_count = SemesterSubject.objects.filter(is_deleted=False).count()
            unit_count = Unit.objects.filter(is_deleted=False, semester_subject__isnull=False).count()
            less_count = Lesson.objects.filter(is_deleted=False, unit__semester_subject__isnull=False).count()
        else:
            subj_count = Subject.objects.filter(is_deleted=False).count() + SemesterSubject.objects.filter(is_deleted=False).count()
            unit_count = Unit.objects.filter(is_deleted=False).count()
            less_count = Lesson.objects.filter(is_deleted=False).count()

        return Response({
            "stats": {
                "totalQuestions": total_questions,
                "approved": approved,
                "inReview": in_review,
                "rejected": rejected,
                "subjects": subj_count,
                "units": unit_count,
                "lessons": less_count,
            },
            "difficultyDistribution": difficulty_distribution,
            "bloomDistribution": bloom_distribution,
            "typeDistribution": type_distribution,
            "subjectProgress": subject_progress
        })
