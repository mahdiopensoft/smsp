from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
import re

from bank.models.Question import Question
from exams.models.Exam import Exam
from academic.models.common.Subject import Subject

class DashboardMVS(ViewSet):
    """
    Dedicated ViewSet for Main Dashboard Metrics & Aggregations.
    Endpoint: /api/bank/dashboard/
    Used by: DashBoard.vue
    """

    def list(self, request):
        """Default GET /api/bank/dashboard/ returns the full dashboard summary."""
        return self._get_summary(request)

    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        """GET /api/bank/dashboard/summary/"""
        return self._get_summary(request)

    def _get_summary(self, request):
        period = request.query_params.get('period', 'month')
        base_qs = Question.objects.filter(is_deleted=False)
        
        # 1. Overall stats
        total_questions = base_qs.count()
        approved_questions = base_qs.filter(status="معتمد").count()
        pending_questions = base_qs.filter(status="قيد المراجعة").count()
        generated_exams = Exam.objects.filter(is_deleted=False).count()

        # 2. Time-filtered questions for Subject distribution
        period_qs = base_qs
        now = timezone.now()
        if period == 'week':
            period_qs = base_qs.filter(created_at__gte=now - timedelta(days=7))
        elif period == 'month':
            period_qs = base_qs.filter(created_at__gte=now - timedelta(days=30))
        elif period == 'year':
            period_qs = base_qs.filter(created_at__gte=now - timedelta(days=365))

        # Questions by Subject
        subject_counts = (
            period_qs.filter(lesson__unit__class_subject__subject__isnull=False)
            .values(
                'lesson__unit__class_subject__subject__id',
                'lesson__unit__class_subject__subject__name_ar'
            )
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        
        questions_by_subject = []
        for sc in subject_counts:
            questions_by_subject.append({
                "id": sc['lesson__unit__class_subject__subject__id'],
                "name": sc['lesson__unit__class_subject__subject__name_ar'] or 'مادة',
                "count": sc['count']
            })

        if not questions_by_subject:
            all_subjects = Subject.objects.filter(is_deleted=False)[:8]
            for s in all_subjects:
                cnt = base_qs.filter(lesson__unit__class_subject__subject=s).count()
                questions_by_subject.append({
                    "id": s.id,
                    "name": s.name_ar or s.name_en or f"مادة {s.id}",
                    "count": cnt
                })

        # 3. Question Types Distribution (with percentages)
        type_counts = base_qs.values('questionType').annotate(count=Count('id'))
        type_labels_map = {
            'Single Choice': 'اختيار من متعدد',
            'Multiple Choice': 'اختيارات متعددة',
            'True/False': 'صح وخطأ',
            'Essay': 'مقالي',
            'Fill in the Blanks': 'إكمال الفراغ',
            'Matching': 'مطابقة',
            'Ordering': 'ترتيب',
        }
        question_types = []
        for tc in type_counts:
            raw_t = tc['questionType']
            cnt = tc['count']
            pct = round((cnt / total_questions * 100), 1) if total_questions > 0 else 0
            question_types.append({
                "type": raw_t,
                "name": type_labels_map.get(raw_t, raw_t or 'غير محدد'),
                "count": cnt,
                "percentage": pct
            })

        # 4. Difficulty Distribution (3 Standard Levels: Easy=Success, Medium=Warning, Hard=Error)
        diff_counts_map = {item['difficulty']: item['count'] for item in base_qs.values('difficulty').annotate(count=Count('id'))}
        diff_config = [
            {"key": 1, "name": "سهل", "color": "success"},
            {"key": 2, "name": "متوسط", "color": "warning"},
            {"key": 3, "name": "صعب", "color": "error"},
        ]
        difficulty_distribution = []
        for cfg in diff_config:
            cnt = diff_counts_map.get(cfg["key"], 0)
            pct = round((cnt / total_questions * 100), 1) if total_questions > 0 else 0
            difficulty_distribution.append({
                "key": cfg["key"],
                "name": cfg["name"],
                "color": cfg["color"],
                "count": cnt,
                "percentage": pct,
            })

        # 5. Bloom Taxonomy Distribution (Standard Levels with Colors and Percentages)
        bloom_counts_map = {item['bloomLevel']: item['count'] for item in base_qs.values('bloomLevel').annotate(count=Count('id'))}
        bloom_config = [
            {"name": "تذكر", "color": "#6366f1"},
            {"name": "فهم", "color": "#3b82f6"},
            {"name": "تطبيق", "color": "#10b981"},
            {"name": "تحليل", "color": "#f59e0b"},
            {"name": "تقييم", "color": "#8b5cf6"},
            {"name": "ابتكار", "color": "#ec4899"},
        ]
        bloom_distribution = []
        for b_cfg in bloom_config:
            cnt = bloom_counts_map.get(b_cfg["name"], 0)
            pct = round((cnt / total_questions * 100), 1) if total_questions > 0 else 0
            bloom_distribution.append({
                "name": b_cfg["name"],
                "color": b_cfg["color"],
                "count": cnt,
                "percentage": pct,
            })

        # 6. Recent Questions
        recent_qs = base_qs.select_related(
            'lesson__unit__class_subject__subject'
        ).order_by('-created_at')[:5]
        recent_questions = []
        diff_labels_map = {1: 'سهل', 2: 'متوسط', 3: 'صعب'}
        for q in recent_qs:
            clean_content = re.sub('<[^<]+?>', '', q.content) if q.content else ''
            subject_name = 'عام'
            lesson_name = 'عام'
            try:
                subject_name = q.lesson.unit.class_subject.subject.name_ar
                lesson_name = q.lesson.name_ar
            except Exception:
                pass
            recent_questions.append({
                "id": q.id,
                "title": clean_content[:60] + ('...' if len(clean_content) > 60 else ''),
                "subject": subject_name or 'عام',
                "lesson": lesson_name or 'عام',
                "type": type_labels_map.get(q.questionType, q.questionType or 'سؤال'),
                "difficulty": diff_labels_map.get(q.difficulty, 'متوسط'),
                "status": q.status or 'مسودة',
                "created_at": q.created_at.strftime('%Y-%m-%d %H:%M') if q.created_at else ''
            })

        # 7. Top Contributors
        contributors = (
            base_qs.filter(createdBy__isnull=False)
            .values('createdBy__id', 'createdBy__first_name', 'createdBy__last_name', 'createdBy__username')
            .annotate(questions_count=Count('id'))
            .order_by('-questions_count')[:4]
        )
        top_contributors = []
        avatar_colors = ['indigo-darken-1', 'emerald-darken-1', 'amber-darken-1', 'purple-darken-1']
        for i, c in enumerate(contributors):
            name = f"{c['createdBy__first_name'] or ''} {c['createdBy__last_name'] or ''}".strip() or c['createdBy__username'] or f"مستخدم #{c['createdBy__id']}"
            initials = ''.join([w[0] for w in name.split()[:2]]) if name else 'م'
            top_contributors.append({
                "id": c['createdBy__id'],
                "name": name,
                "initials": initials,
                "role": 'مُعد أسئلة',
                "questions_count": c['questions_count'],
                "questionsCount": c['questions_count'],
                "avatar_color": avatar_colors[i % len(avatar_colors)],
                "avatarColor": avatar_colors[i % len(avatar_colors)]
            })

        return Response({
            "stats": {
                "total_questions": total_questions,
                "approved_questions": approved_questions,
                "pending_questions": pending_questions,
                "generated_exams": generated_exams,
            },
            "questions_by_subject": questions_by_subject,
            "question_types": question_types,
            "difficulty_distribution": difficulty_distribution,
            "bloom_distribution": bloom_distribution,
            "recent_questions": recent_questions,
            "top_contributors": top_contributors,
        })
