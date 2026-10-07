from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from django.contrib.auth import get_user_model

from bank.models.Question import Question
from bank.serializers.Question import QuestionSerializer

User = get_user_model()

class AuthorsReportMVS(AllMVS):
    """
    Dedicated ModelViewSet for Question Authors Performance Report.
    Endpoint: /api/bank/authors-report/
    Used by: AuthorsReportView.vue
    """
    queryset = Question.objects.filter(is_deleted=False)
    serializer_class = QuestionSerializer

    def list(self, request, *args, **kwargs):
        """
        Aggregates question statistics per author (createdBy / User) in real-time SQL.
        """
        qs = self.get_queryset().select_related(
            'createdBy',
            'lesson',
            'lesson__unit',
            'lesson__unit__class_subject__subject',
            'lesson__unit__class_subject__class_track__level',
            'lesson__unit__class_subject__class_track__track'
        )

        inst_type = request.query_params.get('institution_type')
        if inst_type and inst_type != 'all':
            qs = qs.filter(institution_type=inst_type)

        stage_id = request.query_params.get('stage') or request.query_params.get('stage_id')
        level_id = request.query_params.get('level') or request.query_params.get('level_id')
        track_id = request.query_params.get('track') or request.query_params.get('branch')
        class_track_id = request.query_params.get('class_track') or request.query_params.get('class_track_id')
        subject_id = request.query_params.get('subject') or request.query_params.get('subject_id')
        search = request.query_params.get('search')

        # University Filters
        college_id = request.query_params.get('college') or request.query_params.get('fk_college')
        dept_id = request.query_params.get('department') or request.query_params.get('fk_department')
        spec_id = request.query_params.get('specialization') or request.query_params.get('fk_specialization')
        semester_subject_id = request.query_params.get('semester_subject') or request.query_params.get('semester_subject_id')

        if subject_id:
            qs = qs.filter(
                Q(lesson__unit__class_subject__subject_id=subject_id) |
                Q(lesson__unit__semester_subject__fk_subject_id=subject_id)
            )
        if level_id:
            qs = qs.filter(lesson__unit__class_subject__class_track__level_id=level_id)
        if track_id:
            qs = qs.filter(lesson__unit__class_subject__class_track__track_id=track_id)
        if class_track_id:
            qs = qs.filter(lesson__unit__class_subject__class_track_id=class_track_id)
        if stage_id:
            qs = qs.filter(lesson__unit__class_subject__class_track__level__stage_id=stage_id)

        if college_id:
            qs = qs.filter(lesson__unit__semester_subject__fk_specialization__fk_college_id=college_id)
        if dept_id:
            qs = qs.filter(lesson__unit__semester_subject__fk_specialization__fk_section_id=dept_id)
        if spec_id:
            qs = qs.filter(lesson__unit__semester_subject__fk_specialization_id=spec_id)
        if semester_subject_id:
            qs = qs.filter(lesson__unit__semester_subject_id=semester_subject_id)

        if search:
            qs = qs.filter(
                Q(createdBy__first_name__icontains=search) |
                Q(createdBy__last_name__icontains=search) |
                Q(createdBy__username__icontains=search) |
                Q(createdBy__email__icontains=search)
            )

        author_stats = qs.values(
            'createdBy__id',
            'createdBy__first_name',
            'createdBy__last_name',
            'createdBy__username',
            'createdBy__email'
        ).annotate(
            total=Count('id'),
            approved=Count('id', filter=Q(status='معتمد') | Q(status='approved')),
            pending=Count('id', filter=Q(status='قيد المراجعة') | Q(status='مسودة') | Q(status='draft') | Q(status='pending')),
            rejected=Count('id', filter=Q(status='مرفوض') | Q(status='rejected'))
        ).order_by('-total')

        results = []
        for idx, item in enumerate(author_stats[:50]):
            user_id = item['createdBy__id']
            if not user_id:
                continue

            full_name = f"{item['createdBy__first_name'] or ''} {item['createdBy__last_name'] or ''}".strip()
            if not full_name:
                full_name = item['createdBy__username'] or f"مؤلف #{user_id}"

            total = item['total'] or 0
            approved = item['approved'] or 0
            rate = round((approved / total * 100), 1) if total > 0 else 0

            # Sample subject/level authored
            first_q = qs.filter(createdBy_id=user_id).first()
            subject_name = "مادة عامة"
            level_name = "الصف الدراسي"
            track_name = "المسار"

            if first_q and first_q.lesson and first_q.lesson.unit:
                unit = first_q.lesson.unit
                cs = getattr(unit, 'class_subject', None)
                ss = getattr(unit, 'semester_subject', None)
                if cs:
                    if hasattr(cs, 'subject') and cs.subject:
                        subject_name = cs.subject.name_ar or cs.subject.name_en or subject_name
                    if hasattr(cs, 'class_track') and cs.class_track:
                        ct = cs.class_track
                        if hasattr(ct, 'level') and ct.level:
                            level_name = ct.level.name_ar or ct.level.name_en or level_name
                        if hasattr(ct, 'track') and ct.track:
                            track_name = ct.track.name_ar or ct.track.name_en or track_name
                elif ss:
                    if hasattr(ss, 'fk_subject') and ss.fk_subject:
                        subject_name = ss.fk_subject.name_ar or ss.fk_subject.name_en or subject_name
                    if hasattr(ss, 'fk_specialization') and ss.fk_specialization:
                        track_name = ss.fk_specialization.name_ar or track_name
                    level_name = f"المستوى {ss.level}" if ss.level else "مستوى جامعي"

            results.append({
                "id": user_id,
                "rank": idx + 1,
                "name": full_name,
                "email": item['createdBy__email'] or '',
                "subjectName": subject_name,
                "levelName": level_name,
                "branchName": track_name,
                "institutionType": getattr(first_q, 'institution_type', 'school') if first_q else 'school',
                "total": total,
                "approved": approved,
                "pending": item['pending'] or 0,
                "rejected": item['rejected'] or 0,
                "approvalRate": rate,
                "lastActivity": "مؤخراً"
            })

        return Response({
            "results": results,
            "count": len(results)
        })

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Returns author leaderboard metrics."""
        base_qs = Question.objects.filter(is_deleted=False)
        inst_type = request.query_params.get('institution_type')
        if inst_type and inst_type != 'all':
            base_qs = base_qs.filter(institution_type=inst_type)

        total_questions = base_qs.count()
        active_authors = base_qs.values('createdBy').distinct().count()
        approved_total = base_qs.filter(status__in=['معتمد', 'approved']).count()

        avg_rate = round((approved_total / total_questions) * 100, 1) if total_questions > 0 else 0

        return Response({
            "activeAuthors": active_authors,
            "totalAuthoredQuestions": total_questions,
            "averageApprovalRate": avg_rate
        })
