"""
ExamGradebookMVS.py — شاشة سجل درجات الاختبارات وترحيلها لنظام الكنترول
======================================================================
Endpoint: /api/omr/gradebook/
يربط بين نتائج التصحيح الضوئي (OMR Submissions) ونظام الكنترول الأكاديمي،
ويتيح استعراض كشوفات الرصد، تدقيق الدرجات، وترحيلها رسمياً لسجلات الطلاب.
"""

from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Count, Avg, Max, Min, Q
from django.utils import timezone
from django.db import transaction
import uuid
import hashlib

from exams.models.Exam import Exam
from exams.models.ExamVersion import ExamVersion
from exams.models.StudentExamRegistration import StudentExamRegistration
from submissions.models.Submission import Submission
from bank.models.AuditLog import AuditLog


def _calculate_grade_letter(percent: float) -> dict:
    """حساب التقدير المعياري الأكاديمي بناء على النسبة المئوية."""
    if percent >= 90:
        return {"code": "A+", "name_ar": "ممتاز مرتفع", "color": "success"}
    elif percent >= 85:
        return {"code": "A", "name_ar": "ممتاز", "color": "success"}
    elif percent >= 80:
        return {"code": "B+", "name_ar": "جيد جداً مرتفع", "color": "primary"}
    elif percent >= 75:
        return {"code": "B", "name_ar": "جيد جداً", "color": "primary"}
    elif percent >= 70:
        return {"code": "C+", "name_ar": "جيد مرتفع", "color": "info"}
    elif percent >= 65:
        return {"code": "C", "name_ar": "جيد", "color": "info"}
    elif percent >= 60:
        return {"code": "D+", "name_ar": "مقبول مرتفع", "color": "warning"}
    elif percent >= 50:
        return {"code": "D", "name_ar": "مقبول", "color": "warning"}
    else:
        return {"code": "F", "name_ar": "راسب", "color": "error"}


class ExamGradebookMVS(ViewSet):
    """
    سجل درجات الاختبارات والترحيل لنظام الكنترول المركزي.
    """
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        """
        قائمة الاختبارات مع ملخص إحصائيات التصحيح والترحيل للكنترول.
        """
        search = request.query_params.get('search', '').strip()
        institution_type = request.query_params.get('institution_type')
        subject_id = request.query_params.get('subject')

        qs = Exam.objects.filter(is_deleted=False).select_related(
            'subject', 'year', 'governorate', 'directorate'
        ).prefetch_related('versions').order_by('-created_at')

        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(uniqueCode__icontains=search))
        if institution_type and institution_type != 'all':
            qs = qs.filter(institution_type=institution_type)
        if subject_id:
            qs = qs.filter(subject_id=subject_id)

        # School Filters
        stage_id = request.query_params.get('stage')
        if stage_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__class_subject__class_track__level__stage_id=stage_id) |
                Q(subject__class_subjects__class_track__level__stage_id=stage_id)
            )

        class_track_id = request.query_params.get('class_track')
        if class_track_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__class_subject__class_track_id=class_track_id) |
                Q(subject__class_subjects__class_track_id=class_track_id) |
                Q(class_track_id=class_track_id)
            )

        # University Filters
        college_id = request.query_params.get('college')
        if college_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__semester_subject__fk_specialization__fk_college_id=college_id) |
                Q(subject__semester_subjects__fk_specialization__fk_college_id=college_id)
            )

        dept_id = request.query_params.get('department')
        if dept_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__semester_subject__fk_specialization__fk_section_id=dept_id) |
                Q(subject__semester_subjects__fk_specialization__fk_section_id=dept_id)
            )

        spec_id = request.query_params.get('specialization')
        if spec_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__semester_subject__fk_specialization_id=spec_id) |
                Q(subject__semester_subjects__fk_specialization_id=spec_id)
            )

        sem_sub_id = request.query_params.get('semester_subject')
        if sem_sub_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__semester_subject_id=sem_sub_id) |
                Q(subject__semester_subjects__id=sem_sub_id)
            )

        # Institute Filters
        inst_field_id = request.query_params.get('institute_field')
        if inst_field_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__institute_subject__field_id=inst_field_id) |
                Q(subject__institute_subjects__field_id=inst_field_id)
            )

        inst_system_id = request.query_params.get('institute_education_system')
        if inst_system_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__institute_subject__specialization__education_system_id=inst_system_id) |
                Q(subject__institute_subjects__specialization__education_system_id=inst_system_id)
            )

        inst_spec_id = request.query_params.get('institute_specialization')
        if inst_spec_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__institute_subject__specialization_id=inst_spec_id) |
                Q(subject__institute_subjects__specialization_id=inst_spec_id)
            )

        inst_sub_id = request.query_params.get('institute_subject')
        if inst_sub_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__institute_subject_id=inst_sub_id) |
                Q(subject__institute_subjects__id=inst_sub_id)
            )

        exams = list(qs[:100])
        exam_ids = [e.id for e in exams]

        # 1. تجميع عدد الطلاب المسجلين والمدارس لكل اختبار بدفعة واحدة
        reg_counts = dict(
            StudentExamRegistration.objects.filter(
                examVersion__exam_id__in=exam_ids, is_deleted=False
            ).values('examVersion__exam_id')
            .annotate(cnt=Count('id'))
            .values_list('examVersion__exam_id', 'cnt')
        )

        schools_counts = dict(
            StudentExamRegistration.objects.filter(
                examVersion__exam_id__in=exam_ids, is_deleted=False, student_profile__organization__isnull=False
            ).values('examVersion__exam_id')
            .annotate(cnt=Count('student_profile__organization_id', distinct=True))
            .values_list('examVersion__exam_id', 'cnt')
        )

        # 2. تجميع إحصائيات التسليمات لكل اختبار بدفعة واحدة (استعلام واحد)
        sub_counts = {}
        completed_counts = {}
        needs_review_counts = {}
        dispatched_counts = {}
        for row in (
            Submission.objects.filter(exam_id__in=exam_ids, is_deleted=False)
            .values('exam_id', 'status')
            .annotate(cnt=Count('id'))
        ):
            eid, st, cnt = row['exam_id'], row['status'], row['cnt']
            sub_counts[eid] = sub_counts.get(eid, 0) + cnt
            if st == Submission.Status.COMPLETED:
                completed_counts[eid] = cnt
            elif st == Submission.Status.NEEDS_REVIEW:
                needs_review_counts[eid] = cnt

        # 3. تجميع متوسطات ودرجات التسليمات المكتملة (استعلام واحد)
        score_aggregates = {}
        for row in (
            Submission.objects.filter(exam_id__in=exam_ids, status=Submission.Status.COMPLETED, is_deleted=False)
            .values('exam_id')
            .annotate(
                avg_score=Avg('total_score'),
                max_score=Max('total_score'),
                min_score=Min('total_score'),
            )
        ):
            score_aggregates[row['exam_id']] = row

        exams_list = []
        for exam in exams:
            total_registered = reg_counts.get(exam.id, 0)
            total_submissions = sub_counts.get(exam.id, 0)
            completed_subs = completed_counts.get(exam.id, 0)
            needs_review_subs = needs_review_counts.get(exam.id, 0)
            schools_cnt = schools_counts.get(exam.id, 0)
            exam_max_score = float(getattr(exam, 'total_score', 100) or 100)

            aggr = score_aggregates.get(exam.id, {})
            avg_val = float(aggr.get('avg_score') or 0.0)
            highest_sc = float(aggr.get('max_score') or 0.0)
            lowest_sc = float(aggr.get('min_score') or 0.0)

            completion_rate = round((completed_subs / max(1, total_registered)) * 100, 1) if total_registered > 0 else 0.0

            exams_list.append({
                "id": exam.id,
                "title": exam.title,
                "uniqueCode": exam.uniqueCode,
                "institution_type": exam.institution_type,
                "institution_type_display": "مدرسي" if exam.institution_type == 'school' else ("جامعي" if exam.institution_type == 'university' else "معاهد"),
                "subject_name": getattr(exam.subject, 'name_ar', str(exam.subject)) if exam.subject else "غير محدد",
                "year_name": exam.year.gregorian_year if (exam.year and hasattr(exam.year, 'gregorian_year')) else (str(exam.year) if exam.year else "العام الحالي"),
                "governorate_name": getattr(exam.governorate, 'name_ar', str(exam.governorate)) if exam.governorate else "",
                "directorate_name": getattr(exam.directorate, 'name_ar', str(exam.directorate)) if exam.directorate else "",
                "schools_count": schools_cnt,
                "max_score": exam_max_score,
                "total_registered": total_registered,
                "total_submissions": total_submissions,
                "completed_count": completed_subs,
                "needs_review_count": needs_review_subs,
                "absent_count": max(0, total_registered - total_submissions),
                "completion_rate": completion_rate,
                "dispatched_count": 0,
                "dispatch_status": "dispatched" if (completed_subs > 0 and completed_subs == total_submissions) else ("partial" if completed_subs > 0 else "none"),
                "average_score": round(avg_val, 2),
                "highest_score": highest_sc,
                "lowest_score": lowest_sc,
                "pass_rate": 0.0 if completed_subs == 0 else round((avg_val / exam_max_score) * 100, 1),
                "created_at": exam.created_at.strftime("%Y-%m-%d %H:%M") if exam.created_at else "",
            })

        return Response({
            "success": True,
            "count": len(exams_list),
            "results": exams_list
        })

    @action(detail=False, methods=['get'], url_path='by-school')
    def by_school(self, request):
        """
        تجميع إحصائيات الرصد والكنترول حسب المدرسة / المركز الامتحاني.
        """
        search = request.query_params.get('search', '').strip()
        governorate_id = request.query_params.get('governorate')
        directorate_id = request.query_params.get('directorate')
        institution_type = request.query_params.get('institution_type')

        regs_qs = StudentExamRegistration.objects.filter(
            is_deleted=False, 
            student_profile__organization__isnull=False
        )
        if search:
            regs_qs = regs_qs.filter(
                Q(student_profile__organization__name_ar__icontains=search) |
                Q(student_profile__organization__name_en__icontains=search)
            )
        if governorate_id:
            regs_qs = regs_qs.filter(student_profile__directorate__fk_governorate_id=governorate_id)
        if directorate_id:
            regs_qs = regs_qs.filter(student_profile__directorate_id=directorate_id)
        if institution_type and institution_type != 'all':
            regs_qs = regs_qs.filter(student_profile__organization__institution_type=institution_type)

        schools_agg = regs_qs.values(
            'student_profile__organization_id',
            'student_profile__organization__name_ar',
            'student_profile__organization__institution_type',
            'student_profile__directorate__name_ar',
            'student_profile__directorate__fk_governorate__name_ar'
        ).annotate(
            total_students=Count('id', distinct=True),
            exams_count=Count('examVersion__exam_id', distinct=True)
        ).order_by('-total_students')

        org_ids = [s['student_profile__organization_id'] for s in schools_agg]
        subs_completed = dict(
            Submission.objects.filter(
                is_deleted=False, 
                status=Submission.Status.COMPLETED,
                registration__student_profile__organization_id__in=org_ids
            ).values('registration__student_profile__organization_id')
            .annotate(cnt=Count('id'))
            .values_list('registration__student_profile__organization_id', 'cnt')
        )
        subs_scores = dict(
            Submission.objects.filter(
                is_deleted=False, 
                status=Submission.Status.COMPLETED,
                registration__student_profile__organization_id__in=org_ids
            ).values('registration__student_profile__organization_id')
            .annotate(avg=Avg('total_score'))
            .values_list('registration__student_profile__organization_id', 'avg')
        )

        results = []
        for s in schools_agg:
            org_id = s['student_profile__organization_id']
            tot = s['total_students']
            comp = subs_completed.get(org_id, 0)
            avg_sc = subs_scores.get(org_id, 0.0) or 0.0
            results.append({
                "id": org_id,
                "name": s['student_profile__organization__name_ar'] or "مدرسة غير محددة",
                "institution_type": s['student_profile__organization__institution_type'] or "school",
                "directorate_name": s['student_profile__directorate__name_ar'] or "—",
                "governorate_name": s['student_profile__directorate__fk_governorate__name_ar'] or "—",
                "total_students": tot,
                "exams_count": s['exams_count'],
                "completed_count": comp,
                "absent_count": max(0, tot - comp),
                "completion_rate": round((comp / max(1, tot)) * 100, 1) if tot > 0 else 0.0,
                "average_score": round(float(avg_sc), 1),
            })

        return Response({
            "success": True,
            "count": len(results),
            "results": results
        })

    @action(detail=False, methods=['get'], url_path='by-directorate')
    def by_directorate(self, request):
        """
        تجميع إحصائيات الرصد والكنترول حسب المديرية / المنطقة الجغرافية.
        """
        search = request.query_params.get('search', '').strip()
        governorate_id = request.query_params.get('governorate')

        regs_qs = StudentExamRegistration.objects.filter(
            is_deleted=False, 
            student_profile__directorate__isnull=False
        )
        if search:
            regs_qs = regs_qs.filter(student_profile__directorate__name_ar__icontains=search)
        if governorate_id:
            regs_qs = regs_qs.filter(student_profile__directorate__fk_governorate_id=governorate_id)

        dirs_agg = regs_qs.values(
            'student_profile__directorate_id',
            'student_profile__directorate__name_ar',
            'student_profile__directorate__fk_governorate__name_ar'
        ).annotate(
            total_students=Count('id', distinct=True),
            schools_count=Count('student_profile__organization_id', distinct=True),
            exams_count=Count('examVersion__exam_id', distinct=True)
        ).order_by('-total_students')

        dir_ids = [d['student_profile__directorate_id'] for d in dirs_agg]
        subs_completed = dict(
            Submission.objects.filter(
                is_deleted=False, 
                status=Submission.Status.COMPLETED,
                registration__student_profile__directorate_id__in=dir_ids
            ).values('registration__student_profile__directorate_id')
            .annotate(cnt=Count('id'))
            .values_list('registration__student_profile__directorate_id', 'cnt')
        )

        results = []
        for d in dirs_agg:
            did = d['student_profile__directorate_id']
            tot = d['total_students']
            comp = subs_completed.get(did, 0)
            results.append({
                "id": did,
                "name": d['student_profile__directorate__name_ar'] or "مديرية غير محددة",
                "governorate_name": d['student_profile__directorate__fk_governorate__name_ar'] or "—",
                "schools_count": d['schools_count'],
                "exams_count": d['exams_count'],
                "total_students": tot,
                "completed_count": comp,
                "absent_count": max(0, tot - comp),
                "completion_rate": round((comp / max(1, tot)) * 100, 1) if tot > 0 else 0.0,
            })

        return Response({
            "success": True,
            "count": len(results),
            "results": results
        })

    def retrieve(self, request, pk=None):
        """
        جلب كشف درجات الطلاب التفصيلي لاختبار محدد تمهيداً للرصد والترحيل للكنترول،
        مع دعم البجنشن من الباك إند (Server-Side Pagination) والبحث والتصفية.
        """
        try:
            exam = Exam.objects.select_related('subject', 'year', 'governorate', 'directorate').get(pk=pk, is_deleted=False)
        except Exam.DoesNotExist:
            return Response({"success": False, "message": "الاختبار غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        exam_max_score = float(getattr(exam, 'total_score', 100) or 100)

        # 1. جلب أوراق الإجابات والتسليمات المرتبطة للاختبار لبناء خريطة التسليمات وحساب الإحصائيات العامة
        submissions_qs = Submission.objects.filter(exam=exam, is_deleted=False)
        submissions_map = {}
        completed_reg_ids = set()
        completed_seat_numbers = set()
        needs_review_reg_ids = set()
        needs_review_seat_numbers = set()
        all_sub_reg_ids = set()
        all_sub_seat_numbers = set()
        dispatched_reg_ids = set()
        dispatched_seat_numbers = set()

        completed_subs_count = 0
        sum_completed_score = 0.0
        pass_subs_count = 0
        needs_review_count = 0
        dispatched_count = 0

        for sub in submissions_qs:
            reg_id = sub.registration_id
            seat_num = str(sub.layout_result.get("seat_number", "")).strip() if sub.layout_result else ""
            if reg_id:
                submissions_map[reg_id] = sub
                all_sub_reg_ids.add(reg_id)
            if seat_num:
                submissions_map[seat_num] = sub
                all_sub_seat_numbers.add(seat_num)

            lr = sub.layout_result or {}
            is_disp = lr.get("dispatched_to_control") is True or lr.get("dispatched_to_control") == "true"
            if is_disp:
                dispatched_count += 1
                if reg_id:
                    dispatched_reg_ids.add(reg_id)
                if seat_num:
                    dispatched_seat_numbers.add(seat_num)

            if sub.status == Submission.Status.COMPLETED:
                completed_subs_count += 1
                score_val = float(sub.total_score or 0.0)
                sum_completed_score += score_val
                if score_val >= (exam_max_score * 0.5):
                    pass_subs_count += 1
                if reg_id:
                    completed_reg_ids.add(reg_id)
                if seat_num:
                    completed_seat_numbers.add(seat_num)
            elif sub.status == Submission.Status.NEEDS_REVIEW:
                needs_review_count += 1
                if reg_id:
                    needs_review_reg_ids.add(reg_id)
                if seat_num:
                    needs_review_seat_numbers.add(seat_num)

        # 2. الاستعلام الأساسي لتسجيلات الطلاب
        base_registrations = StudentExamRegistration.objects.filter(
            examVersion__exam=exam, is_deleted=False
        )
        total_registered_count = base_registrations.count()

        # قراءة رقم الصفحة لتجنب تكرار استعلامات الفلاتر الثقيلة عند التنقل بين الصفحات
        try:
            req_page = int(request.query_params.get('page', 1) or 1)
        except (ValueError, TypeError):
            req_page = 1

        schools_list = []
        directorates_list = []
        governorates_list = []
        versions_list = []

        # استخراج خيارات التصفية فقط عند أول تحميل (الصفحة 1) لضمان سرعة فائقة في التنقل بين الصفحات
        if req_page == 1:
            schools_list = list(
                base_registrations
                .order_by()
                .values_list('student_profile__organization__name_ar', flat=True)
                .exclude(student_profile__organization__name_ar__isnull=True)
                .exclude(student_profile__organization__name_ar__exact='')
                .distinct()
            )

            directorates_list = list(
                base_registrations
                .order_by()
                .values_list('student_profile__directorate__name_ar', flat=True)
                .exclude(student_profile__directorate__name_ar__isnull=True)
                .exclude(student_profile__directorate__name_ar__exact='')
                .distinct()
            )
            if exam.directorate and exam.directorate.name_ar and exam.directorate.name_ar not in directorates_list:
                directorates_list.append(exam.directorate.name_ar)

            governorates_list = list(
                base_registrations
                .order_by()
                .values_list('student_profile__directorate__fk_governorate__name_ar', flat=True)
                .exclude(student_profile__directorate__fk_governorate__name_ar__isnull=True)
                .exclude(student_profile__directorate__fk_governorate__name_ar__exact='')
                .distinct()
            )
            if exam.governorate and exam.governorate.name_ar and exam.governorate.name_ar not in governorates_list:
                governorates_list.append(exam.governorate.name_ar)

            versions_list = list(
                exam.versions.filter(is_deleted=False).values_list('versionCode', flat=True).distinct()
            )

        # إحصائيات عامة للاختبار
        absent_count = max(0, total_registered_count - len(all_sub_reg_ids | all_sub_seat_numbers))
        avg_score = round(sum_completed_score / max(1, completed_subs_count), 2) if completed_subs_count > 0 else 0.0
        pass_rate = round((pass_subs_count / max(1, completed_subs_count)) * 100.0, 1) if completed_subs_count > 0 else 0.0
        is_fully_dispatched = dispatched_count >= completed_subs_count and completed_subs_count > 0

        exam_stats = {
            "total_students": total_registered_count,
            "completed_count": completed_subs_count,
            "needs_review_count": needs_review_count,
            "absent_count": absent_count,
            "average_score": avg_score,
            "pass_rate": pass_rate,
            "dispatched_count": dispatched_count,
            "is_fully_dispatched": is_fully_dispatched,
        }

        # 3. تطبيق الفلاتر على تسجيلات الطلاب
        registrations = base_registrations.select_related(
            'student',
            'student_profile',
            'student_profile__organization',
            'student_profile__directorate',
            'student_profile__directorate__fk_governorate',
            'examVersion'
        )

        # 3.1 فلتر المحافظة (يدعم المعرف الرقمي واسم المحافظة بالعربية والإنجليزية)
        governorate = request.query_params.get('governorate') or request.query_params.get('governorate_name')
        if governorate and governorate != 'all' and str(governorate).strip() != '':
            gov_str = str(governorate).strip()
            gov_q = (
                Q(student_profile__directorate__fk_governorate__name_ar=gov_str) |
                Q(student_profile__directorate__fk_governorate__name_en=gov_str) |
                Q(student__student_profile__directorate__fk_governorate__name_ar=gov_str) |
                Q(student__student_profile__directorate__fk_governorate__name_en=gov_str) |
                Q(examVersion__exam__governorate__name_ar=gov_str) |
                Q(examVersion__exam__governorate__name_en=gov_str)
            )
            if gov_str.isdigit():
                gov_id = int(gov_str)
                gov_q |= (
                    Q(student_profile__directorate__fk_governorate_id=gov_id) |
                    Q(student__student_profile__directorate__fk_governorate_id=gov_id) |
                    Q(examVersion__exam__governorate_id=gov_id)
                )
            registrations = registrations.filter(gov_q)

        # 3.2 فلتر المديرية (يدعم المعرف الرقمي واسم المديرية بالعربية والإنجليزية)
        directorate = request.query_params.get('directorate') or request.query_params.get('directorate_name')
        if directorate and directorate != 'all' and str(directorate).strip() != '':
            dir_str = str(directorate).strip()
            dir_q = (
                Q(student_profile__directorate__name_ar=dir_str) |
                Q(student_profile__directorate__name_en=dir_str) |
                Q(student__student_profile__directorate__name_ar=dir_str) |
                Q(student__student_profile__directorate__name_en=dir_str) |
                Q(examVersion__exam__directorate__name_ar=dir_str) |
                Q(examVersion__exam__directorate__name_en=dir_str)
            )
            if dir_str.isdigit():
                dir_id = int(dir_str)
                dir_q |= (
                    Q(student_profile__directorate_id=dir_id) |
                    Q(student__student_profile__directorate_id=dir_id) |
                    Q(examVersion__exam__directorate_id=dir_id)
                )
            registrations = registrations.filter(dir_q)

        # 3.3 فلتر المدرسة / المؤسسة (يدعم المعرف الرقمي والاسم)
        school = request.query_params.get('school') or request.query_params.get('school_name') or request.query_params.get('organization')
        if school and school != 'all' and str(school).strip() != '':
            sch_str = str(school).strip()
            sch_q = (
                Q(student_profile__organization__name_ar=sch_str) |
                Q(student_profile__organization__name_en=sch_str) |
                Q(student__student_profile__organization__name_ar=sch_str) |
                Q(student__student_profile__organization__name_en=sch_str)
            )
            if sch_str.isdigit():
                sch_id = int(sch_str)
                sch_q |= (
                    Q(student_profile__organization_id=sch_id) |
                    Q(student__student_profile__organization_id=sch_id)
                )
            registrations = registrations.filter(sch_q)

        # 3.4 فلتر النموذج
        version = request.query_params.get('version') or request.query_params.get('model_code') or request.query_params.get('version_code')
        if version and version != 'all':
            registrations = registrations.filter(examVersion__versionCode=version)

        # 3.5 فلتر التقدير الأكاديمي (A+, A, B+, B, C+, C, D+, D, F)
        filter_grade = request.query_params.get('grade') or request.query_params.get('grade_code')
        if filter_grade and filter_grade != 'all':
            grade_reg_ids = set()
            grade_seat_numbers = set()
            for sub in submissions_qs:
                if sub.status == Submission.Status.COMPLETED:
                    pct = round((float(sub.total_score or 0) / max(1.0, exam_max_score)) * 100.0, 1)
                    if _calculate_grade_letter(pct)["code"] == filter_grade:
                        if sub.registration_id: grade_reg_ids.add(sub.registration_id)
                        s_num = str(sub.layout_result.get("seat_number", "")).strip() if sub.layout_result else ""
                        if s_num: grade_seat_numbers.add(s_num)
            registrations = registrations.filter(
                Q(id__in=grade_reg_ids) | Q(seatNumber__in=grade_seat_numbers)
            )

        # 3.6 فلتر حالة النتيجة (ناجح / راسب)
        result_status = request.query_params.get('result_status')
        if result_status and result_status != 'all':
            res_reg_ids = set()
            res_seat_numbers = set()
            pass_threshold = exam_max_score * 0.5
            for sub in submissions_qs:
                if sub.status == Submission.Status.COMPLETED:
                    sc = float(sub.total_score or 0.0)
                    is_pass = (sc >= pass_threshold)
                    if (result_status == 'passed' and is_pass) or (result_status == 'failed' and not is_pass):
                        if sub.registration_id: res_reg_ids.add(sub.registration_id)
                        s_num = str(sub.layout_result.get("seat_number", "")).strip() if sub.layout_result else ""
                        if s_num: res_seat_numbers.add(s_num)
            registrations = registrations.filter(
                Q(id__in=res_reg_ids) | Q(seatNumber__in=res_seat_numbers)
            )

        # 3.7 فلتر البحث السريع
        search = request.query_params.get('search', '').strip()
        if search:
            registrations = registrations.filter(
                Q(seatNumber__icontains=search) |
                Q(secretNumber__icontains=search) |
                Q(student_profile__name_ar__icontains=search) |
                Q(student_profile__name_en__icontains=search) |
                Q(student_profile__academic_number__icontains=search) |
                Q(student_profile__organization__name_ar__icontains=search) |
                Q(student_profile__directorate__name_ar__icontains=search) |
                Q(student_profile__directorate__fk_governorate__name_ar__icontains=search)
            )

        # 3.8 فلتر الحالة (completed, needs_review, absent)
        filter_status = request.query_params.get('status')
        if filter_status and filter_status != 'all':
            if filter_status == 'completed':
                registrations = registrations.filter(
                    Q(id__in=completed_reg_ids) | Q(seatNumber__in=completed_seat_numbers)
                )
            elif filter_status == 'needs_review':
                registrations = registrations.filter(
                    Q(id__in=needs_review_reg_ids) | Q(seatNumber__in=needs_review_seat_numbers)
                )
            elif filter_status == 'absent':
                registrations = registrations.exclude(
                    id__in=all_sub_reg_ids
                ).exclude(
                    seatNumber__in=all_sub_seat_numbers
                )

        # 3.9 فلتر حالة الترحيل للكنترول
        filter_dispatch = request.query_params.get('dispatch') or request.query_params.get('filterDispatch')
        if filter_dispatch and filter_dispatch != 'all':
            if filter_dispatch == 'dispatched':
                registrations = registrations.filter(
                    Q(id__in=dispatched_reg_ids) | Q(seatNumber__in=dispatched_seat_numbers)
                )
            elif filter_dispatch == 'not_dispatched':
                registrations = registrations.exclude(
                    id__in=dispatched_reg_ids
                ).exclude(
                    seatNumber__in=dispatched_seat_numbers
                )

        # الترتيب
        registrations = registrations.order_by('examVersion__versionCode', 'seatNumber')
        filtered_count = registrations.count()

        # 4. التقسيم (Pagination)
        is_fetch_all = request.query_params.get('all') == 'true' or request.query_params.get('page_size') == 'all'
        try:
            page_num = int(request.query_params.get('page', 1) or 1)
        except (ValueError, TypeError):
            page_num = 1

        try:
            page_size = int(request.query_params.get('page_size', request.query_params.get('perPage', 10)) or 10)
        except (ValueError, TypeError):
            page_size = 10

        if is_fetch_all:
            paged_regs = registrations[:5000]
            page_size = filtered_count
            num_pages = 1
            page_num = 1
        else:
            page_size = max(1, min(page_size, 100))
            page_num = max(1, page_num)
            start = (page_num - 1) * page_size
            end = start + page_size
            paged_regs = registrations[start:end]
            num_pages = max(1, (filtered_count // page_size) + (1 if filtered_count % page_size else 0))

        # 5. بناء السجلات للصفحة المطلوبة
        students_records = []
        exam_gov_name = exam.governorate.name_ar if exam.governorate else ""
        for reg in paged_regs:
            profile = reg.student_profile
            if profile and profile.name_ar:
                s_name = profile.name_ar
            elif reg.student:
                st = reg.student
                s_name = getattr(st, 'get_full_name', lambda: '')() or f"{st.first_name or ''} {st.last_name or ''}".strip() or st.username
            else:
                s_name = f"طالب ({reg.seatNumber})"

            inst_name = profile.organization.name_ar if (profile and profile.organization) else ""
            dir_name = profile.directorate.name_ar if (profile and profile.directorate) else (exam.directorate.name_ar if exam.directorate else "")
            gov_name = (profile.directorate.fk_governorate.name_ar if (profile and profile.directorate and profile.directorate.fk_governorate) else exam_gov_name) or "المحافظة"

            sub = submissions_map.get(reg.id) or submissions_map.get(str(reg.seatNumber))
            score_val = 0.0
            percent_val = 0.0
            grading_status = "absent"
            is_dispatched = False
            dispatched_at_str = ""
            confidence_val = 0.0
            sub_id = None

            if sub:
                sub_id = sub.id
                score_val = float(sub.total_score or 0.0)
                percent_val = round((score_val / max(1.0, exam_max_score)) * 100.0, 1)
                grading_status = sub.status
                confidence_val = float(sub.overall_confidence or 0.95)

                lr = sub.layout_result or {}
                if lr.get("dispatched_to_control") is True or lr.get("dispatched_to_control") == "true":
                    is_dispatched = True
                    dispatched_at_str = lr.get("dispatched_at", "")

            grade_info = _calculate_grade_letter(percent_val) if sub else {"code": "—", "name_ar": "غائب", "color": "grey"}

            students_records.append({
                "id": reg.id,
                "registration_id": reg.id,
                "submission_id": sub_id,
                "student_id": reg.student_id,
                "student_name": s_name,
                "seat_number": reg.seatNumber,
                "secret_number": reg.secretNumber or "—",
                "version_code": reg.examVersion.versionCode if reg.examVersion else "A",
                "school_name": inst_name or "المدرسة الرئيسية",
                "directorate_name": dir_name or "المديرية",
                "governorate_name": gov_name,
                "score": score_val,
                "max_score": exam_max_score,
                "percentage": percent_val,
                "grade_code": grade_info["code"],
                "grade_name_ar": grade_info["name_ar"],
                "grade_color": grade_info["color"],
                "status": grading_status,
                "is_dispatched": is_dispatched,
                "dispatched_at": dispatched_at_str,
                "confidence": confidence_val,
                "is_present": sub is not None or reg.isPresent,
            })

        return Response({
            "success": True,
            "exam": {
                "id": exam.id,
                "title": exam.title,
                "uniqueCode": exam.uniqueCode,
                "institution_type": exam.institution_type,
                "subject_name": getattr(exam.subject, 'name_ar', str(exam.subject)) if exam.subject else "",
                "year_name": exam.year.gregorian_year if (exam.year and hasattr(exam.year, 'gregorian_year')) else (str(exam.year) if exam.year else ""),
                "max_score": exam_max_score,
                "total_students": total_registered_count,
                "completed_count": completed_subs_count,
                "dispatched_count": dispatched_count,
                "is_fully_dispatched": is_fully_dispatched,
            },
            "stats": exam_stats,
            "results": students_records,
            "records": students_records,
            "count": filtered_count,
            "schools": schools_list,
            "directorates": directorates_list,
            "governorates": governorates_list,
            "versions": versions_list,
            "filter_options": {
                "schools": schools_list,
                "directorates": directorates_list,
                "governorates": governorates_list,
                "versions": versions_list,
                "grades": [
                    {"value": "A+", "title": "ممتاز مرتفع (A+)"},
                    {"value": "A", "title": "ممتاز (A)"},
                    {"value": "B+", "title": "جيد جداً مرتفع (B+)"},
                    {"value": "B", "title": "جيد جداً (B)"},
                    {"value": "C+", "title": "جيد مرتفع (C+)"},
                    {"value": "C", "title": "جيد (C)"},
                    {"value": "D+", "title": "مقبول مرتفع (D+)"},
                    {"value": "D", "title": "مقبول (D)"},
                    {"value": "F", "title": "راسب (F)"},
                ],
                "result_statuses": [
                    {"value": "passed", "title": "ناجح (50% فأكثر)"},
                    {"value": "failed", "title": "راسب (أقل من 50%)"},
                ],
            },
            "pagination": {
                "count": filtered_count,
                "num_pages": num_pages,
                "current_page": page_num,
                "page_size": page_size,
                "per_page": page_size,
                "total": filtered_count,
            }
        })

    @action(detail=True, methods=['post'], url_path='dispatch-to-control')
    def dispatch_to_control(self, request, pk=None):
        """
        ترحيل الدرجات المعتمدة رسمياً إلى نظام الكنترول المركزي وقفل السجلات.
        """
        try:
            exam = Exam.objects.get(pk=pk, is_deleted=False)
        except Exam.DoesNotExist:
            return Response({"success": False, "message": "الاختبار غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        target_reg_ids = request.data.get('registration_ids') or request.data.get('selected_ids') or request.data.get('ids')
        subs_qs = Submission.objects.filter(exam=exam, status=Submission.Status.COMPLETED, is_deleted=False)

        if target_reg_ids and isinstance(target_reg_ids, list) and len(target_reg_ids) > 0:
            target_seat_numbers = list(StudentExamRegistration.objects.filter(id__in=target_reg_ids).values_list('seatNumber', flat=True))
            subs_qs = subs_qs.filter(
                Q(registration_id__in=target_reg_ids) |
                Q(layout_result__seat_number__in=[str(s) for s in target_seat_numbers])
            )

        if not subs_qs.exists():
            return Response({
                "success": False,
                "message": "لا توجد أوراق إجابة معتمدة ومكتملة التصحيح جاهزة للترحيل حالياً."
            }, status=status.HTTP_400_BAD_REQUEST)

        now_str = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        user_name = request.user.username if request.user and request.user.is_authenticated else "مستخدم الكنترول"
        receipt_code = f"CTL-{str(exam.id)[:8].upper()}-{uuid.uuid4().hex[:8].upper()}"

        dispatched_count = 0
        with transaction.atomic():
            for sub in subs_qs:
                lr = sub.layout_result or {}
                lr["dispatched_to_control"] = True
                lr["dispatched_at"] = now_str
                lr["dispatched_by"] = user_name
                lr["control_receipt_code"] = receipt_code
                lr["tamper_seal"] = hashlib.sha256(f"{sub.id}:{sub.total_score}:{sub.mcq_score}:{now_str}".encode()).hexdigest()[:16]
                sub.layout_result = lr

                if not sub.registration_id and lr.get("seat_number"):
                    matching_reg = StudentExamRegistration.objects.filter(
                        examVersion__exam=exam, seatNumber=lr.get("seat_number"), is_deleted=False
                    ).first()
                    if matching_reg:
                        sub.registration = matching_reg

                sub.save(update_fields=['layout_result', 'registration'] if sub.registration_id else ['layout_result'])

                if sub.registration:
                    sub.registration.isPresent = True
                    sub.registration.save(update_fields=['isPresent'])

                dispatched_count += 1

            AuditLog.objects.create(
                user=request.user if request.user and request.user.is_authenticated else None,
                action=AuditLog.ActionChoices.UPDATE,
                resource_type='ExamGradebook',
                resource_id=str(exam.id),
                description=f"ترحيل رسمي لـ ({dispatched_count}) درجة في اختبار '{exam.title}' إلى نظام الكنترول الأكاديمي (إيصال: {receipt_code})."
            )

        return Response({
            "success": True,
            "message": f"تم ترحيل {dispatched_count} درجة بنجاح إلى نظام الكنترول المركزي وقفل السجلات (رقم الإيصال: {receipt_code}).",
            "dispatched_count": dispatched_count,
            "dispatched_at": now_str,
            "control_receipt_code": receipt_code,
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='rollback-dispatch')
    def rollback_dispatch(self, request, pk=None):
        """
        إلغاء ترحيل الدرجات لإتاحة فرصة التدقيق أو التعديل بطلب من إدارة الكنترول.
        """
        try:
            exam = Exam.objects.get(pk=pk, is_deleted=False)
        except Exam.DoesNotExist:
            return Response({"success": False, "message": "الاختبار غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        subs = Submission.objects.filter(exam=exam, is_deleted=False)
        count = 0
        with transaction.atomic():
            for s in subs:
                lr = s.layout_result or {}
                if lr.get("dispatched_to_control"):
                    lr["dispatched_to_control"] = False
                    lr["dispatched_at"] = None
                    lr["dispatched_by"] = None
                    s.layout_result = lr
                    s.save(update_fields=['layout_result'])
                    count += 1

            AuditLog.objects.create(
                user=request.user if request.user and request.user.is_authenticated else None,
                action=AuditLog.ActionChoices.UPDATE,
                resource_type='ExamGradebook',
                resource_id=str(exam.id),
                description=f"إلغاء ترحيل درجات اختبار '{exam.title}' لإعادة التدقيق من الكنترول."
            )

        return Response({
            "success": True,
            "message": f"تم إلغاء ترحيل {count} سجل وإعادتها لوضع المراجعة والتدقيق.",
            "count": count
        })

    @action(detail=True, methods=['get'], url_path='export-control-sheet')
    def export_control_sheet(self, request, pk=None):
        """
        تصدير كشف درجات الكنترول المعتمد بصيغة CSV المتوافقة مع برامج الكنترول المركزي (UTF-8 BOM).
        """
        import io
        import csv
        from django.http import HttpResponse

        try:
            exam = Exam.objects.select_related('subject', 'year', 'governorate', 'directorate').get(pk=pk, is_deleted=False)
        except Exam.DoesNotExist:
            return Response({"success": False, "message": "الاختبار غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        # جلب جميع بيانات الطلاب والتسليمات للاختبار
        roster_response = self.retrieve(request, pk=pk)
        records = roster_response.data.get('records', []) if hasattr(roster_response, 'data') else []

        output = io.StringIO()
        output.write('\ufeff')  # UTF-8 BOM for Microsoft Excel Arabic support
        writer = csv.writer(output)

        # ترويسة الكشف الرسمي
        writer.writerow(["وزارة التربية والتعليم / وزارة التعليم العالي والبحث العلمي"])
        writer.writerow(["الإدارة العامة للامتحانات وشؤون الكنترول المركزي"])
        writer.writerow([f"كشف رصد ودرجات اختبار: {exam.title} - الرمز: {exam.uniqueCode}"])
        writer.writerow([f"المادة: {getattr(exam.subject, 'name_ar', str(exam.subject))} | العام الدراسي: {exam.year or ''}"])
        writer.writerow([])

        # عناوين الأعمدة
        writer.writerow([
            "م",
            "رقم الجلوس",
            "الرقم السري",
            "اسم الطالب الرباعي",
            "المدرسة / الكلية",
            "المديرية",
            "المحافظة",
            "النموذج",
            "الدرجة المحرزة",
            "الدرجة العظمى",
            "النسبة المئوية %",
            "التقدير",
            "حالة الحضور والتصحيح",
            "حالة الترحيل للكنترول"
        ])

        for idx, r in enumerate(records):
            writer.writerow([
                idx + 1,
                r.get('seat_number', ''),
                r.get('secret_number') or '—',
                r.get('student_name', ''),
                r.get('school_name', ''),
                r.get('directorate_name', ''),
                r.get('governorate_name', ''),
                r.get('version_code', 'A'),
                'غائب' if r.get('status') == 'absent' else r.get('score', 0),
                r.get('max_score', 100),
                0 if r.get('status') == 'absent' else r.get('percentage', 0),
                f"{r.get('grade_code', '')} ({r.get('grade_name_ar', '')})",
                r.get('status_display', r.get('status', '')),
                "مرحل رسمياً" if r.get('is_dispatched') else "قيد المراجعة"
            ])

        response = HttpResponse(output.getvalue(), content_type='text/csv; charset=utf-8-sig')
        filename = f"Control_Sheet_{exam.uniqueCode}.csv"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    @action(detail=True, methods=['get'], url_path='psychometrics')
    def psychometrics(self, request, pk=None):
        """
        تقرير التحليل السيكومتري وتحليل الفقرات (Item Analysis & Reliability):
        - معامل الصعوبة (Difficulty Index P)
        - معامل التمييز (Discrimination Index D)
        - معامل ثبات الاختبار (Cronbach's Alpha)
        - توزيع المشتتات والخيارات (Distractor Analysis)
        """
        import numpy as np
        from omr.models.OMRSheetResult import OMRSheetResult
        from omr.models.OMRQuestionResult import OMRQuestionResult

        try:
            exam = Exam.objects.get(pk=pk, is_deleted=False)
        except Exam.DoesNotExist:
            return Response({"success": False, "message": "الاختبار غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        subs = list(Submission.objects.filter(
            exam=exam,
            status=Submission.Status.COMPLETED,
            is_deleted=False
        ).select_related('omr_detail').order_by('-total_score'))

        n_students = len(subs)
        if n_students < 2:
            return Response({
                "success": True,
                "message": "عدد الأوراق المكتملة غير كافٍ لإجراء تحليل سيكومتري (يتطلب على الأقل ورقتين)",
                "sample_size": n_students,
                "items": [],
                "cronbach_alpha": None,
                "exam_title": exam.title
            })

        # تقسيم الطلاب إلى فئة عليا وفئة دنيا (أعلى 27% وأدنى 27%)
        k_split = max(1, int(round(n_students * 0.27)))
        upper_subs = subs[:k_split]
        lower_subs = subs[-k_split:]

        upper_sheet_ids = [s.omr_detail.id for s in upper_subs if hasattr(s, 'omr_detail') and s.omr_detail]
        lower_sheet_ids = [s.omr_detail.id for s in lower_subs if hasattr(s, 'omr_detail') and s.omr_detail]
        all_sheet_ids = [s.omr_detail.id for s in subs if hasattr(s, 'omr_detail') and s.omr_detail]

        # جلب كافة الأسئلة وإجاباتها
        all_q_results = OMRQuestionResult.objects.filter(
            sheet_result_id__in=all_sheet_ids
        ).values('sheet_result_id', 'question_number', 'marked_choice', 'correct_choice', 'is_correct')

        # تجميع الإحصائيات حسب رقم السؤال
        questions_stats = {}
        for r in all_q_results:
            q_num = r['question_number']
            if q_num not in questions_stats:
                questions_stats[q_num] = {
                    "question_number": q_num,
                    "correct_choice": r['correct_choice'],
                    "total_correct": 0,
                    "upper_correct": 0,
                    "lower_correct": 0,
                    "distractors": {"A": 0, "B": 0, "C": 0, "D": 0, "empty": 0},
                    "total_responses": 0
                }

            stat = questions_stats[q_num]
            stat["total_responses"] += 1
            choice = r['marked_choice']
            if choice in stat["distractors"]:
                stat["distractors"][choice] += 1
            elif not choice:
                stat["distractors"]["empty"] += 1

            if r['is_correct']:
                stat["total_correct"] += 1
                if r['sheet_result_id'] in upper_sheet_ids:
                    stat["upper_correct"] += 1
                elif r['sheet_result_id'] in lower_sheet_ids:
                    stat["lower_correct"] += 1

        items_analysis = []
        p_values = []

        for q_num in sorted(questions_stats.keys()):
            stat = questions_stats[q_num]
            p_val = round(stat["total_correct"] / float(max(1, stat["total_responses"])), 3)
            p_values.append(p_val)

            # Discrimination Index D = (Upper_correct - Lower_correct) / k_split
            d_val = round((stat["upper_correct"] - stat["lower_correct"]) / float(k_split), 3)

            # تصنيف جودة السؤال
            if 0.30 <= p_val <= 0.70 and d_val >= 0.35:
                quality_badge = "ممتاز"
                quality_color = "success"
                status_note = "سؤال معياري متوازن وقوة تمييز ممتازة"
            elif 0.20 <= p_val <= 0.85 and d_val >= 0.20:
                quality_badge = "جيد ومقبول"
                quality_color = "primary"
                status_note = "سؤال مقبول ومناسب لبنك الأسئلة"
            elif p_val > 0.85:
                quality_badge = "سهل جداً"
                quality_color = "warning"
                status_note = "معظم الطلاب أجابوا صواباً - قدرة التمييز منخفضة"
            elif p_val < 0.20:
                quality_badge = "صعب جداً"
                quality_color = "error"
                status_note = "نسبة نجاح متدنية جداً - يوصى بمراجعة الصياغة"
            elif d_val < 0.15:
                quality_badge = "تمييز ضعيف"
                quality_color = "error"
                status_note = "السؤال لا يميز بين المتفوقين والضعاف"
            else:
                quality_badge = "يحتاج مراجعة"
                quality_color = "warning"
                status_note = "يوصى بمراجعة السؤال أو المشتتات"

            # كشف المشتتات غير الفعالة (خيارات لم يخترها أحد)
            zero_distractors = [c for c, cnt in stat["distractors"].items() if c not in [stat["correct_choice"], "empty"] and cnt == 0]

            items_analysis.append({
                "question_number": q_num,
                "correct_choice": stat["correct_choice"],
                "difficulty_index": p_val,
                "discrimination_index": d_val,
                "quality_badge": quality_badge,
                "quality_color": quality_color,
                "status_note": status_note,
                "zero_distractors": zero_distractors,
                "choices_distribution": stat["distractors"]
            })

        # حساب معامل كرونباخ ألفا (Cronbach's Alpha) لقياس ثبات واتساق الاختبار
        scores_arr = [float(s.total_score or 0) for s in subs]
        variance_total = float(np.var(scores_arr, ddof=1)) if len(scores_arr) > 1 else 0.0

        num_items = len(p_values)
        cronbach_alpha = None
        if num_items > 1 and variance_total > 0:
            sum_item_variances = sum(p * (1.0 - p) for p in p_values)
            alpha_calc = (num_items / (num_items - 1.0)) * (1.0 - (sum_item_variances / variance_total))
            cronbach_alpha = round(max(0.0, min(1.0, alpha_calc)), 3)

        return Response({
            "success": True,
            "sample_size": n_students,
            "k_split": k_split,
            "cronbach_alpha": cronbach_alpha,
            "cronbach_quality": "موثوقية عالية جداً" if (cronbach_alpha and cronbach_alpha >= 0.8) else ("موثوقية مقبولة" if (cronbach_alpha and cronbach_alpha >= 0.7) else "موثوقية منخفضة"),
            "items_count": len(items_analysis),
            "items": items_analysis
        })
