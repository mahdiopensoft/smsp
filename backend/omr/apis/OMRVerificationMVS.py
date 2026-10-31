from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, status
from django.db.models import Count, Avg, Max, Min, Q
from django.utils import timezone

from exams.models.Exam import Exam
from exams.models.ExamVersion import ExamVersion
from exams.models.StudentExamRegistration import StudentExamRegistration
from submissions.models.Submission import Submission
from OpenSoftCoreV41.common.models.Branch import Organization as CoreOrg


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


def _detect_cheating_or_violation(sub):
    """التحقق من وجود رصد غش أو مخالفة في ورقة الطالب الممسوحة."""
    if not sub:
        return False, ""
    vr = sub.verification_result or {}
    lr = sub.layout_result or {}
    
    if vr.get('is_cheating') or vr.get('cheating') or vr.get('violation'):
        return True, vr.get('cheating_reason') or vr.get('violation_reason') or "رصد حالة غش أو مخالفة في الورقة"
    if lr.get('is_cheating') or lr.get('cheating'):
        return True, lr.get('cheating_reason') or "رصد تظليل مزدوج شاذ أو مخالفة في ورقة الإجابة"
    if sub.status == 'needs_review' and ('غش' in str(sub.error_message) or 'مخالفة' in str(sub.error_message)):
        return True, sub.error_message
    return False, ""


class OMRVerificationMVS(ViewSet):
    """
    شاشة المطابقة والتحقق من الأوراق المفقودة والرقابة الشاملة.
    Endpoint: /api/omr/verification/
    """
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        """
        قائمة الاختبارات مع ملخص شامل لحالات المطابقة:
        (المسجلين، المطبوع، الممسوح، المفقود، الفاشل، الغياب، الغش، النجاح والرسوب).
        """
        search = request.query_params.get('search', '').strip()
        institution_type = request.query_params.get('institution_type')
        subject_id = request.query_params.get('subject') or request.query_params.get('subject_id')

        qs = Exam.objects.filter(is_deleted=False).select_related(
            'subject', 'year', 'governorate', 'directorate'
        ).prefetch_related('versions').order_by('-created_at')

        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(uniqueCode__icontains=search))
        if institution_type and institution_type != 'all':
            qs = qs.filter(institution_type=institution_type)
        if subject_id and subject_id != 'all':
            if str(subject_id).isdigit():
                qs = qs.filter(subject_id=int(subject_id))
            else:
                qs = qs.filter(Q(subject__name_ar__icontains=subject_id) | Q(subject__name_en__icontains=subject_id))

        office_id = request.query_params.get('office_id') or request.query_params.get('office')
        directorate_id = request.query_params.get('directorate_id') or request.query_params.get('directorate')
        school_id = request.query_params.get('school_id') or request.query_params.get('school')

        # فلترة حسب المدرسة / المركز الامتحاني (تدعم التحديد المفرد أو المتعدد)
        if school_id and school_id != 'all':
            sch_ids = [int(x) for x in str(school_id).split(',') if x.strip().isdigit()]
            sch_names = [x.strip() for x in str(school_id).split(',') if not x.strip().isdigit() and x.strip()]
            q_sch = Q()
            if sch_ids:
                q_sch |= Q(student_profile__organization_id__in=sch_ids)
                core_names = list(CoreOrg.objects.filter(id__in=sch_ids, company_level=50).values_list('name_ar', flat=True))
                if core_names:
                    q_sch |= Q(student_profile__organization__name_ar__in=core_names)
            if sch_names:
                q_sch |= Q(student_profile__organization__name_ar__in=sch_names)

            exam_ids_for_school = StudentExamRegistration.objects.filter(
                is_deleted=False
            ).filter(q_sch).values_list('examVersion__exam_id', flat=True).distinct()
            qs = qs.filter(id__in=exam_ids_for_school)

        # فلترة حسب المديرية (تدعم التحديد المفرد أو المتعدد)
        elif directorate_id and directorate_id != 'all':
            dir_ids = [int(x) for x in str(directorate_id).split(',') if x.strip().isdigit()]
            dir_names = [x.strip() for x in str(directorate_id).split(',') if not x.strip().isdigit() and x.strip()]
            child_school_names = []
            if dir_ids:
                core_dirs = CoreOrg.objects.filter(id__in=dir_ids, company_level=40)
                for cd in core_dirs:
                    clean = cd.name_ar.replace('إدارة التربية والتعليم - مديرية ', '').replace('إدارة التربية والتعليم - ', '').strip()
                    dir_names.extend([cd.name_ar, clean])
                child_schools = CoreOrg.objects.filter(company_level=50, fk_parent_organization__in=dir_ids, is_deleted=False)
                child_school_names = list(child_schools.values_list('name_ar', flat=True))

            dir_exam_ids = StudentExamRegistration.objects.filter(is_deleted=False).filter(
                Q(student_profile__directorate__name_ar__in=dir_names) |
                Q(student_profile__organization__name_ar__in=child_school_names)
            ).values_list('examVersion__exam_id', flat=True).distinct()

            dir_q = Q(id__in=dir_exam_ids)
            if dir_ids:
                dir_q |= Q(directorate_id__in=dir_ids)
            for d_name in dir_names:
                dir_q |= Q(directorate__name_ar__icontains=d_name)
            qs = qs.filter(dir_q)

        # فلترة حسب مكتب التربية والتعليم بالمحافظة (تدعم التحديد المتعدد)
        elif office_id and office_id != 'all':
            off_ids = [int(x) for x in str(office_id).split(',') if x.strip().isdigit()]
            gov_names = [x.strip() for x in str(office_id).split(',') if not x.strip().isdigit() and x.strip()]
            child_school_names = []
            gov_ids = []
            if off_ids:
                core_offs = CoreOrg.objects.filter(id__in=off_ids, company_level=30)
                for co in core_offs:
                    clean_gov = co.name_ar.replace('مكتب التربية والتعليم - ', '').strip()
                    gov_names.extend([co.name_ar, clean_gov])
                    if co.fk_governorate_id:
                        gov_ids.append(co.fk_governorate_id)
                child_dirs = CoreOrg.objects.filter(company_level=40, fk_parent_organization__in=off_ids, is_deleted=False)
                child_schools = CoreOrg.objects.filter(company_level=50, fk_parent_organization__in=child_dirs.values_list('id', flat=True), is_deleted=False)
                child_school_names = list(child_schools.values_list('name_ar', flat=True))

            off_exam_ids = StudentExamRegistration.objects.filter(is_deleted=False).filter(
                Q(student_profile__directorate__fk_governorate__name_ar__in=gov_names) |
                Q(student_profile__organization__name_ar__in=child_school_names)
            ).values_list('examVersion__exam_id', flat=True).distinct()

            off_q = Q(id__in=off_exam_ids)
            if gov_ids:
                off_q |= Q(governorate_id__in=gov_ids)
            for g_name in gov_names:
                off_q |= Q(governorate__name_ar__icontains=g_name)
            qs = qs.filter(off_q)

        # فلاتر المدارس الأكاديمية
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

        exams = list(qs[:100])
        exam_ids = [e.id for e in exams]

        # تجميع أعداد التسجيل والطباعة
        reg_counts = dict(
            StudentExamRegistration.objects.filter(examVersion__exam_id__in=exam_ids, is_deleted=False)
            .values('examVersion__exam_id')
            .annotate(cnt=Count('id'))
            .values_list('examVersion__exam_id', 'cnt')
        )
        printed_counts = dict(
            StudentExamRegistration.objects.filter(examVersion__exam_id__in=exam_ids, is_deleted=False, is_printed=True)
            .values('examVersion__exam_id')
            .annotate(cnt=Count('id'))
            .values_list('examVersion__exam_id', 'cnt')
        )
        schools_counts = dict(
            StudentExamRegistration.objects.filter(examVersion__exam_id__in=exam_ids, is_deleted=False, student_profile__organization__isnull=False)
            .values('examVersion__exam_id')
            .annotate(cnt=Count('student_profile__organization_id', distinct=True))
            .values_list('examVersion__exam_id', 'cnt')
        )

        # تجميع التسليمات وحالاتها
        submissions_by_exam = {}
        for sub in Submission.objects.filter(exam_id__in=exam_ids, is_deleted=False).select_related('registration'):
            eid = sub.exam_id
            if eid not in submissions_by_exam:
                submissions_by_exam[eid] = []
            submissions_by_exam[eid].append(sub)

        gov_to_office_map = {
            o.fk_governorate_id: o.id 
            for o in CoreOrg.objects.filter(company_level=30, fk_governorate__isnull=False, is_deleted=False)
        }

        # مؤشرات إجمالية عبر كل الاختبارات المفلترة
        g_registered = 0
        g_printed = 0
        g_scanned = 0
        g_missing = 0
        g_needs_review = 0
        g_failed_scan = 0
        g_absent = 0
        g_cheating = 0
        g_passed = 0

        exams_list = []
        for exam in exams:
            total_reg = reg_counts.get(exam.id, 0)
            subs = submissions_by_exam.get(exam.id, [])
            total_scn = len(subs)
            total_prn = max(printed_counts.get(exam.id, 0), total_scn)

            completed_cnt = 0
            needs_review_cnt = 0
            failed_scan_cnt = 0
            cheating_cnt = 0
            passed_cnt = 0
            failed_score_cnt = 0
            exam_max = float(getattr(exam, 'total_score', 100) or 100)

            for s in subs:
                if s.status == Submission.Status.COMPLETED:
                    completed_cnt += 1
                    sc = float(s.total_score or 0.0)
                    if sc >= (exam_max * 0.5):
                        passed_cnt += 1
                    else:
                        failed_score_cnt += 1
                elif s.status == Submission.Status.NEEDS_REVIEW:
                    needs_review_cnt += 1
                elif s.status == Submission.Status.FAILED:
                    failed_scan_cnt += 1

                is_cheat, _ = _detect_cheating_or_violation(s)
                if is_cheat:
                    cheating_cnt += 1

            # المفقود: أوراق طُبعت ولكن لم تصل للماسح
            missing_cnt = max(0, total_prn - total_scn)
            absent_cnt = max(0, total_reg - total_scn)
            pass_rate = round((passed_cnt / max(1, completed_cnt)) * 100, 1) if completed_cnt > 0 else 0.0
            scan_rate = round((total_scn / max(1, total_reg)) * 100, 1) if total_reg > 0 else 0.0

            # حالة المطابقة العامة
            if total_reg == 0:
                verif_status = "لا يوجد طلاب مسجلين"
                verif_color = "grey"
            elif missing_cnt == 0 and total_scn > 0 and failed_scan_cnt == 0 and needs_review_cnt == 0:
                verif_status = "مطابقة مكتملة وسليمة"
                verif_color = "success"
            elif missing_cnt > 0:
                verif_status = f"يوجد {missing_cnt} ورقة مفقودة"
                verif_color = "error"
            elif failed_scan_cnt > 0 or needs_review_cnt > 0:
                verif_status = f"يتطلب مراجعة ({failed_scan_cnt + needs_review_cnt} ورقة)"
                verif_color = "warning"
            elif total_prn > 0 and total_scn == 0:
                verif_status = "بانتظار المسح الضوئي"
                verif_color = "info"
            else:
                verif_status = "بانتظار الطباعة"
                verif_color = "secondary"

            # تراكم الإحصائيات العامة
            g_registered += total_reg
            g_printed += total_prn
            g_scanned += total_scn
            g_missing += missing_cnt
            g_needs_review += needs_review_cnt
            g_failed_scan += failed_scan_cnt
            g_absent += absent_cnt
            g_cheating += cheating_cnt
            g_passed += passed_cnt

            exams_list.append({
                "id": exam.id,
                "title": exam.title,
                "uniqueCode": exam.uniqueCode,
                "institution_type": exam.institution_type,
                "institution_type_display": "مدرسي" if exam.institution_type == 'school' else ("جامعي" if exam.institution_type == 'university' else "معاهد"),
                "subject_name": getattr(exam.subject, 'name_ar', str(exam.subject)) if exam.subject else "غير محدد",
                "year_name": exam.year.gregorian_year if (exam.year and hasattr(exam.year, 'gregorian_year')) else (str(exam.year) if exam.year else "العام الحالي"),
                "office_id": gov_to_office_map.get(exam.governorate_id) or exam.governorate_id,
                "governorate_id": exam.governorate_id,
                "governorate_name": getattr(exam.governorate, 'name_ar', str(exam.governorate)) if exam.governorate else "",
                "directorate_id": exam.directorate_id,
                "directorate_name": getattr(exam.directorate, 'name_ar', str(exam.directorate)) if exam.directorate else "",
                "schools_count": schools_counts.get(exam.id, 0),
                "total_registered": total_reg,
                "total_students": total_reg,
                "total_printed": total_prn,
                "total_scanned": total_scn,
                "missing_count": missing_cnt,
                "needs_review_count": needs_review_cnt,
                "failed_scan_count": failed_scan_cnt,
                "absent_count": absent_cnt,
                "cheating_count": cheating_cnt,
                "completed_count": completed_cnt,
                "passed_count": passed_cnt,
                "failed_score_count": failed_score_cnt,
                "pass_rate": pass_rate,
                "scan_rate": scan_rate,
                "status": verif_status,
                "status_color": verif_color,
                "created_at": exam.created_at.strftime("%Y-%m-%d %H:%M") if exam.created_at else "",
            })

        global_pass_rate = round((g_passed / max(1, g_scanned)) * 100, 1) if g_scanned > 0 else 0.0

        return Response({
            "success": True,
            "count": len(exams_list),
            "results": exams_list,
            "global_stats": {
                "total_students": g_registered,
                "total_printed": g_printed,
                "total_scanned": g_scanned,
                "total_missing": g_missing,
                "total_needs_review": g_needs_review,
                "total_failed_scan": g_failed_scan,
                "total_absent": g_absent,
                "total_cheating": g_cheating,
                "total_passed": g_passed,
                "overall_pass_rate": global_pass_rate,
            }
        })

    @action(detail=False, methods=['get'], url_path='by-office')
    def by_office(self, request):
        """
        تجميع إحصائيات المطابقة والتحقق حسب مكاتب التربية والتعليم بالمحافظات (المستوى 30).
        """
        search = request.query_params.get('search', '').strip()
        office_id = request.query_params.get('office_id') or request.query_params.get('office')
        off_ids = [int(x) for x in str(office_id).split(',') if x.strip().isdigit()] if (office_id and office_id != 'all') else []
        subj_filter = request.query_params.get('subject') or request.query_params.get('subject_id')

        offices = CoreOrg.objects.filter(company_level=30, is_deleted=False).order_by('branch_no', 'id')
        if off_ids:
            offices = offices.filter(id__in=off_ids)
        if search:
            offices = offices.filter(name_ar__icontains=search)

        results = []
        for off in offices:
            child_dirs = CoreOrg.objects.filter(company_level=40, fk_parent_organization=off.id, is_deleted=False)
            child_schools = CoreOrg.objects.filter(company_level=50, fk_parent_organization__in=child_dirs.values_list('id', flat=True), is_deleted=False)
            school_names = list(child_schools.values_list('name_ar', flat=True))
            dir_names = list(child_dirs.values_list('name_ar', flat=True))
            clean_dir_names = [d.replace('إدارة التربية والتعليم - مديرية ', '').replace('إدارة التربية والتعليم - ', '').strip() for d in dir_names]

            regs = StudentExamRegistration.objects.filter(is_deleted=False, examVersion__exam__is_deleted=False).filter(
                Q(student_profile__organization__name_ar__in=school_names) |
                Q(student_profile__directorate__name_ar__in=clean_dir_names) |
                Q(student_profile__directorate__name_ar__in=dir_names)
            )
            if subj_filter and subj_filter != 'all':
                if str(subj_filter).isdigit():
                    regs = regs.filter(examVersion__exam__subject_id=int(subj_filter))
                else:
                    regs = regs.filter(Q(examVersion__exam__subject__name_ar__icontains=subj_filter) | Q(examVersion__exam__subject__name_en__icontains=subj_filter))

            tot = regs.count()
            printed = regs.filter(is_printed=True).count()
            exams_cnt = regs.values('examVersion__exam_id').distinct().count()
            subjs = [s for s in regs.values_list('examVersion__exam__subject__name_ar', flat=True).distinct() if s]

            subs = Submission.objects.filter(is_deleted=False, registration__in=regs)
            scanned = subs.count()
            printed = max(printed, scanned)
            completed = subs.filter(status=Submission.Status.COMPLETED).count()
            needs_review = subs.filter(status=Submission.Status.NEEDS_REVIEW).count()
            failed_scan = subs.filter(status=Submission.Status.FAILED).count()
            missing = max(0, printed - scanned)
            absent = max(0, tot - scanned)

            results.append({
                "id": off.id,
                "office_name": off.name_ar,
                "governorate_name": off.name_ar.replace('مكتب التربية والتعليم - ', ''),
                "directorates_count": child_dirs.count(),
                "schools_count": child_schools.count(),
                "exams_count": exams_cnt,
                "subjects": subjs,
                "subject_name": subjs[0] if len(subjs) == 1 else (", ".join(subjs[:2]) + ("..." if len(subjs) > 2 else "") if subjs else "—"),
                "total_students": tot,
                "printed_count": printed,
                "scanned_count": scanned,
                "completed_count": completed,
                "missing_count": missing,
                "needs_review_count": needs_review,
                "failed_scan_count": failed_scan,
                "absent_count": absent,
                "completion_rate": round((scanned / max(1, tot)) * 100, 1) if tot > 0 else 0.0,
            })

        return Response({"success": True, "count": len(results), "results": results})

    @action(detail=False, methods=['get'], url_path='by-directorate')
    def by_directorate(self, request):
        """
        تجميع إحصائيات المطابقة والتحقق حسب إدارات التربية والتعليم بالمديريات (المستوى 40).
        """
        search = request.query_params.get('search', '').strip()
        office_id = request.query_params.get('office_id') or request.query_params.get('office')
        off_ids = [int(x) for x in str(office_id).split(',') if x.strip().isdigit()] if (office_id and office_id != 'all') else []
        dir_id = request.query_params.get('directorate_id') or request.query_params.get('directorate')
        dir_ids = [int(x) for x in str(dir_id).split(',') if x.strip().isdigit()] if (dir_id and dir_id != 'all') else []
        subj_filter = request.query_params.get('subject') or request.query_params.get('subject_id')

        dirs_qs = CoreOrg.objects.filter(company_level=40, is_deleted=False)
        if off_ids:
            dirs_qs = dirs_qs.filter(fk_parent_organization_id__in=off_ids)
        if dir_ids:
            dirs_qs = dirs_qs.filter(id__in=dir_ids)
        if search:
            dirs_qs = dirs_qs.filter(name_ar__icontains=search)

        results = []
        for d in dirs_qs.order_by('branch_no', 'id'):
            child_schools = CoreOrg.objects.filter(company_level=50, fk_parent_organization=d.id, is_deleted=False)
            school_names = list(child_schools.values_list('name_ar', flat=True))
            clean_dir_name = d.name_ar.replace('إدارة التربية والتعليم - مديرية ', '').replace('إدارة التربية والتعليم - ', '').strip()

            regs = StudentExamRegistration.objects.filter(is_deleted=False, examVersion__exam__is_deleted=False).filter(
                Q(student_profile__organization__name_ar__in=school_names) |
                Q(student_profile__directorate__name_ar__icontains=clean_dir_name) |
                Q(student_profile__directorate__name_ar__icontains=d.name_ar)
            )
            if subj_filter and subj_filter != 'all':
                if str(subj_filter).isdigit():
                    regs = regs.filter(examVersion__exam__subject_id=int(subj_filter))
                else:
                    regs = regs.filter(Q(examVersion__exam__subject__name_ar__icontains=subj_filter) | Q(examVersion__exam__subject__name_en__icontains=subj_filter))

            tot = regs.count()
            printed = regs.filter(is_printed=True).count()
            exams_cnt = regs.values('examVersion__exam_id').distinct().count()
            subjs = [s for s in regs.values_list('examVersion__exam__subject__name_ar', flat=True).distinct() if s]

            subs = Submission.objects.filter(is_deleted=False, registration__in=regs)
            scanned = subs.count()
            printed = max(printed, scanned)
            completed = subs.filter(status=Submission.Status.COMPLETED).count()
            missing = max(0, printed - scanned)
            absent = max(0, tot - scanned)

            results.append({
                "id": d.id,
                "name": clean_dir_name,
                "full_name": d.name_ar,
                "office_id": d.fk_parent_organization_id,
                "office_name": d.fk_parent_organization.name_ar if d.fk_parent_organization else "—",
                "schools_count": child_schools.count(),
                "exams_count": exams_cnt,
                "subjects": subjs,
                "subject_name": subjs[0] if len(subjs) == 1 else (", ".join(subjs[:2]) + ("..." if len(subjs) > 2 else "") if subjs else "—"),
                "total_students": tot,
                "printed_count": printed,
                "scanned_count": scanned,
                "completed_count": completed,
                "missing_count": missing,
                "absent_count": absent,
                "completion_rate": round((scanned / max(1, tot)) * 100, 1) if tot > 0 else 0.0,
            })

        return Response({"success": True, "count": len(results), "results": results})

    @action(detail=False, methods=['get'], url_path='by-school')
    def by_school(self, request):
        """
        تجميع إحصائيات المطابقة والتحقق حسب المدارس والمراكز الامتحانية (المستوى 50) والجامعات والمعاهد.
        """
        search = request.query_params.get('search', '').strip()
        office_id = request.query_params.get('office_id') or request.query_params.get('office')
        off_ids = [int(x) for x in str(office_id).split(',') if x.strip().isdigit()] if (office_id and office_id != 'all') else []
        dir_id = request.query_params.get('directorate_id') or request.query_params.get('directorate')
        dir_ids = [int(x) for x in str(dir_id).split(',') if x.strip().isdigit()] if (dir_id and dir_id != 'all') else []
        school_id = request.query_params.get('school_id') or request.query_params.get('school')
        sch_ids = [int(x) for x in str(school_id).split(',') if x.strip().isdigit()] if (school_id and school_id != 'all') else []
        subj_filter = request.query_params.get('subject') or request.query_params.get('subject_id')
        institution_type = request.query_params.get('institution_type')

        regs_qs = StudentExamRegistration.objects.filter(
            is_deleted=False, 
            examVersion__exam__is_deleted=False,
            student_profile__organization__isnull=False
        )
        if institution_type and institution_type != 'all':
            regs_qs = regs_qs.filter(examVersion__exam__institution_type=institution_type)
        if off_ids:
            core_offs = CoreOrg.objects.filter(id__in=off_ids, company_level=30)
            gov_names = [co.name_ar.replace('مكتب التربية والتعليم - ', '').strip() for co in core_offs]
            child_dirs = CoreOrg.objects.filter(company_level=40, fk_parent_organization__in=off_ids, is_deleted=False)
            child_schools = CoreOrg.objects.filter(company_level=50, fk_parent_organization__in=child_dirs.values_list('id', flat=True), is_deleted=False)
            sch_names = list(child_schools.values_list('name_ar', flat=True))
            regs_qs = regs_qs.filter(
                Q(student_profile__directorate__fk_governorate__name_ar__in=gov_names) |
                Q(student_profile__organization__name_ar__in=sch_names)
            )
        if dir_ids:
            core_dirs = CoreOrg.objects.filter(id__in=dir_ids, company_level=40)
            clean_dirs = [cd.name_ar.replace('إدارة التربية والتعليم - مديرية ', '').replace('إدارة التربية والتعليم - ', '').strip() for cd in core_dirs]
            child_schools = CoreOrg.objects.filter(company_level=50, fk_parent_organization__in=dir_ids, is_deleted=False)
            sch_names = list(child_schools.values_list('name_ar', flat=True))
            regs_qs = regs_qs.filter(
                Q(student_profile__directorate__name_ar__in=clean_dirs) |
                Q(student_profile__organization__name_ar__in=sch_names)
            )
        if sch_ids:
            regs_qs = regs_qs.filter(student_profile__organization_id__in=sch_ids)
        if search:
            regs_qs = regs_qs.filter(student_profile__organization__name_ar__icontains=search)
        if subj_filter and subj_filter != 'all':
            if str(subj_filter).isdigit():
                regs_qs = regs_qs.filter(examVersion__exam__subject_id=int(subj_filter))
            else:
                regs_qs = regs_qs.filter(Q(examVersion__exam__subject__name_ar__icontains=subj_filter) | Q(examVersion__exam__subject__name_en__icontains=subj_filter))

        schools_agg = regs_qs.values(
            'student_profile__organization_id',
            'student_profile__organization__name_ar',
            'student_profile__organization__institution_type',
        ).annotate(
            total_students=Count('id', distinct=True),
            exams_count=Count('examVersion__exam_id', distinct=True)
        ).order_by('-total_students')[:100]

        org_ids = [s['student_profile__organization_id'] for s in schools_agg]
        subs_qs = Submission.objects.filter(
            is_deleted=False,
            registration__student_profile__organization_id__in=org_ids
        )
        subs_scanned = dict(
            subs_qs.values('registration__student_profile__organization_id')
            .annotate(cnt=Count('id'))
            .values_list('registration__student_profile__organization_id', 'cnt')
        )
        subs_completed = dict(
            subs_qs.filter(status=Submission.Status.COMPLETED)
            .values('registration__student_profile__organization_id')
            .annotate(cnt=Count('id'))
            .values_list('registration__student_profile__organization_id', 'cnt')
        )
        subs_printed = dict(
            StudentExamRegistration.objects.filter(
                is_deleted=False,
                examVersion__exam__is_deleted=False,
                student_profile__organization_id__in=org_ids,
                is_printed=True
            ).values('student_profile__organization_id')
            .annotate(cnt=Count('id'))
            .values_list('student_profile__organization_id', 'cnt')
        )

        results = []
        for s in schools_agg:
            oid = s['student_profile__organization_id']
            tot = s['total_students']
            scn = subs_scanned.get(oid, 0)
            prn = max(subs_printed.get(oid, 0), scn)
            comp = subs_completed.get(oid, 0)
            missing = max(0, prn - scn)
            absent = max(0, tot - scn)

            # استخراج المديرية والمحافظة
            one_reg = regs_qs.filter(student_profile__organization_id=oid).select_related('student_profile__directorate__fk_governorate').first()
            d_name = one_reg.student_profile.directorate.name_ar if (one_reg and one_reg.student_profile and one_reg.student_profile.directorate) else "—"
            g_name = one_reg.student_profile.directorate.fk_governorate.name_ar if (one_reg and one_reg.student_profile and one_reg.student_profile.directorate and one_reg.student_profile.directorate.fk_governorate) else "—"

            results.append({
                "id": oid,
                "name": s['student_profile__organization__name_ar'] or "مؤسسة غير محددة",
                "school_name": s['student_profile__organization__name_ar'] or "مؤسسة غير محددة",
                "institution_type": s['student_profile__organization__institution_type'] or "school",
                "directorate_name": d_name,
                "governorate_name": g_name,
                "exams_count": s['exams_count'],
                "total_students": tot,
                "printed_count": prn,
                "scanned_count": scn,
                "completed_count": comp,
                "missing_count": missing,
                "absent_count": absent,
                "completion_rate": round((scn / max(1, tot)) * 100, 1) if tot > 0 else 0.0,
            })

        return Response({"success": True, "count": len(results), "results": results})

    @action(detail=False, methods=['get'], url_path='subjects')
    def available_subjects(self, request):
        """قائمة المواد الدراسية المتاحة."""
        institution_type = request.query_params.get('institution_type')
        exams_qs = Exam.objects.filter(is_deleted=False, subject__isnull=False)
        if institution_type and institution_type != 'all':
            exams_qs = exams_qs.filter(institution_type=institution_type)

        subjects_qs = exams_qs.values(
            'subject_id', 'subject__name_ar', 'subject__name_en'
        ).distinct()

        results = [
            {
                "id": s['subject_id'],
                "name": s['subject__name_ar'] or s['subject__name_en'],
                "name_ar": s['subject__name_ar'] or '',
                "name_en": s['subject__name_en'] or ''
            }
            for s in subjects_qs if (s['subject__name_ar'] or s['subject__name_en'])
        ]
        return Response({"success": True, "results": results})

    def retrieve(self, request, pk=None):
        """
        جلب كشف تدقيق ومطابقة أوراق الطلاب التفصيلي لاختبار محدد (أو كشف الطلاب الكامل)،
        مع كشف الأوراق المفقودة، الغش، الغياب، حالات الفشل، وصور الأوراق الممسوحة.
        """
        try:
            exam = Exam.objects.select_related('subject', 'year', 'governorate', 'directorate').get(pk=pk, is_deleted=False)
        except Exam.DoesNotExist:
            return Response({"success": False, "message": "الاختبار غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        exam_max_score = float(getattr(exam, 'total_score', 100) or 100)

        # جلب كل تسليمات الاختبار لبناء الفهرس ومطابقة السجلات
        submissions_qs = Submission.objects.filter(exam=exam, is_deleted=False)
        submissions_map = {}
        for sub in submissions_qs:
            if sub.registration_id:
                submissions_map[sub.registration_id] = sub
            seat_num = str(sub.layout_result.get("seat_number", "")).strip() if sub.layout_result else ""
            if seat_num and seat_num not in submissions_map:
                submissions_map[seat_num] = sub

        # التسجيلات الأساسية للطلاب في الاختبار
        base_regs = StudentExamRegistration.objects.filter(
            examVersion__exam=exam, is_deleted=False
        ).select_related(
            'student',
            'student_profile',
            'student_profile__organization',
            'student_profile__directorate',
            'student_profile__directorate__fk_governorate',
            'examVersion'
        )

        total_registered = base_regs.count()

        # إحصائيات عامة تفصيلية للاختبار
        tot_printed = base_regs.filter(is_printed=True).count()
        tot_scanned = submissions_qs.count()
        tot_printed = max(tot_printed, tot_scanned)
        tot_missing = max(0, tot_printed - tot_scanned)
        tot_failed_scan = submissions_qs.filter(status=Submission.Status.FAILED).count()
        tot_needs_review = submissions_qs.filter(status=Submission.Status.NEEDS_REVIEW).count()
        tot_absent = max(0, total_registered - tot_scanned)
        tot_cheating = 0
        tot_passed = 0
        tot_failed_score = 0

        # قائمة خيارات الفلاتر
        schools_set = set()
        directorates_set = set()
        versions_set = set()

        for reg in base_regs:
            sub = submissions_map.get(reg.id) or submissions_map.get(str(reg.seatNumber))
            if reg.examVersion and reg.examVersion.versionCode:
                versions_set.add(reg.examVersion.versionCode)
            if reg.student_profile and reg.student_profile.organization:
                schools_set.add(reg.student_profile.organization.name_ar)
            if reg.student_profile and reg.student_profile.directorate:
                directorates_set.add(reg.student_profile.directorate.name_ar)

        # إدراج كافة المديريات والمدارس لتكون متاحة للتصفية الحرة والشاملة
        try:
            for cd in CoreOrg.objects.filter(company_level=40, is_deleted=False):
                c_name = cd.name_ar.replace('إدارة التربية والتعليم - مديرية ', '').replace('إدارة التربية والتعليم - ', '').strip()
                directorates_set.add(c_name)
            for cs in CoreOrg.objects.filter(company_level=50, is_deleted=False):
                if cs.name_ar:
                    schools_set.add(cs.name_ar.strip())
        except Exception:
            pass

            if sub:
                if sub.status == Submission.Status.COMPLETED:
                    sc = float(sub.total_score or 0.0)
                    if sc >= (exam_max_score * 0.5):
                        tot_passed += 1
                    else:
                        tot_failed_score += 1

                is_cheat, _ = _detect_cheating_or_violation(sub)
                if is_cheat:
                    tot_cheating += 1

        exam_stats = {
            "total_students": total_registered,
            "total_printed": tot_printed,
            "total_scanned": tot_scanned,
            "missing_count": tot_missing,
            "failed_scan_count": tot_failed_scan,
            "needs_review_count": tot_needs_review,
            "absent_count": tot_absent,
            "cheating_count": tot_cheating,
            "passed_count": tot_passed,
            "failed_score_count": tot_failed_score,
            "pass_rate": round((tot_passed / max(1, tot_scanned)) * 100, 1) if tot_scanned > 0 else 0.0,
        }

        # تطبيق الفلاتر على تسجيلات الطلاب
        regs = base_regs

        # 1. فلتر حالة المطابقة
        filter_status = request.query_params.get('status')
        if filter_status and filter_status != 'all':
            scanned_reg_ids = [rid for rid in submissions_map.keys() if isinstance(rid, int)]
            if filter_status == 'missing':
                # مفقودة: طُبعت ولم تُمسح
                printed_ids = set(base_regs.filter(Q(is_printed=True) | Q(id__in=scanned_reg_ids)).values_list('id', flat=True))
                missing_ids = [rid for rid in printed_ids if rid not in scanned_reg_ids]
                regs = regs.filter(id__in=missing_ids)
            elif filter_status == 'printed':
                regs = regs.filter(Q(is_printed=True) | Q(id__in=scanned_reg_ids))
            elif filter_status in ('scanned', 'verified'):
                regs = regs.filter(id__in=scanned_reg_ids)
            elif filter_status in ('failed', 'review', 'needs_review'):
                target_statuses = [Submission.Status.FAILED, Submission.Status.NEEDS_REVIEW] if filter_status == 'review' else ([Submission.Status.FAILED] if filter_status == 'failed' else [Submission.Status.NEEDS_REVIEW])
                review_reg_ids = [rid for rid, sub in submissions_map.items() if isinstance(rid, int) and sub.status in target_statuses]
                regs = regs.filter(id__in=review_reg_ids)
            elif filter_status == 'not_printed':
                regs = regs.filter(is_printed=False).exclude(id__in=scanned_reg_ids)

        # 2. فلتر الحضور والسلوك
        filter_attendance = request.query_params.get('attendance')
        if filter_attendance and filter_attendance != 'all':
            if filter_attendance == 'absent':
                scanned_reg_ids = set(submissions_map.keys())
                regs = regs.exclude(id__in=[rid for rid in scanned_reg_ids if isinstance(rid, int)])
            elif filter_attendance == 'present':
                scanned_reg_ids = [rid for rid, sub in submissions_map.items() if isinstance(rid, int)]
                regs = regs.filter(Q(id__in=scanned_reg_ids) | Q(isPresent=True))
            elif filter_attendance == 'cheating':
                cheat_reg_ids = []
                for rid, sub in submissions_map.items():
                    if isinstance(rid, int):
                        is_cheat, _ = _detect_cheating_or_violation(sub)
                        if is_cheat:
                            cheat_reg_ids.append(rid)
                regs = regs.filter(id__in=cheat_reg_ids)

        # 3. فلتر النتيجة (ناجح / راسب)
        filter_result = request.query_params.get('result') or request.query_params.get('result_status')
        if filter_result and filter_result != 'all':
            pass_threshold = exam_max_score * 0.5
            target_ids = []
            for rid, sub in submissions_map.items():
                if isinstance(rid, int) and sub.status == Submission.Status.COMPLETED:
                    sc = float(sub.total_score or 0.0)
                    is_pass = sc >= pass_threshold
                    if (filter_result == 'passed' and is_pass) or (filter_result == 'failed' and not is_pass):
                        target_ids.append(rid)
            regs = regs.filter(id__in=target_ids)

        # 4. فلتر النموذج
        filter_version = request.query_params.get('version') or request.query_params.get('model_code')
        if filter_version and filter_version != 'all':
            regs = regs.filter(examVersion__versionCode=filter_version)

        # 5. فلتر المدرسة
        filter_school = request.query_params.get('school') or request.query_params.get('school_id')
        if filter_school and filter_school != 'all':
            sch_ids = [int(x) for x in str(filter_school).split(',') if x.strip().isdigit()]
            sch_names = [x.strip() for x in str(filter_school).split(',') if not x.strip().isdigit() and x.strip()]
            q_sch = Q()
            if sch_ids:
                q_sch |= Q(student_profile__organization_id__in=sch_ids)
                core_names = list(CoreOrg.objects.filter(id__in=sch_ids, company_level=50).values_list('name_ar', flat=True))
                if core_names:
                    q_sch |= Q(student_profile__organization__name_ar__in=core_names)
            for sn in sch_names:
                q_sch |= Q(student_profile__organization__name_ar__icontains=sn)
            if q_sch:
                regs = regs.filter(q_sch)

        # 6. فلتر المديرية
        filter_directorate = request.query_params.get('directorate') or request.query_params.get('directorate_id')
        if filter_directorate and filter_directorate != 'all':
            dir_ids = [int(x) for x in str(filter_directorate).split(',') if x.strip().isdigit()]
            dir_names = [x.strip() for x in str(filter_directorate).split(',') if not x.strip().isdigit() and x.strip()]
            q_dir = Q()
            if dir_ids:
                q_dir |= Q(student_profile__directorate_id__in=dir_ids)
                core_dirs = CoreOrg.objects.filter(id__in=dir_ids, company_level=40)
                for cd in core_dirs:
                    clean = cd.name_ar.replace('إدارة التربية والتعليم - مديرية ', '').replace('إدارة التربية والتعليم - ', '').strip()
                    dir_names.extend([cd.name_ar, clean])
                child_schools = CoreOrg.objects.filter(company_level=50, fk_parent_organization__in=dir_ids, is_deleted=False)
                child_school_names = list(child_schools.values_list('name_ar', flat=True))
                if child_school_names:
                    q_dir |= Q(student_profile__organization__name_ar__in=child_school_names)
            for dn in dir_names:
                q_dir |= Q(student_profile__directorate__name_ar__icontains=dn)
            if q_dir:
                regs = regs.filter(q_dir)

        # 7. فلتر مكتب التربية (المحافظة)
        filter_office = request.query_params.get('office') or request.query_params.get('office_id')
        if filter_office and filter_office != 'all':
            off_ids = [int(x) for x in str(filter_office).split(',') if x.strip().isdigit()]
            gov_names = [x.strip() for x in str(filter_office).split(',') if not x.strip().isdigit() and x.strip()]
            child_school_names = []
            if off_ids:
                core_offs = CoreOrg.objects.filter(id__in=off_ids, company_level=30)
                for co in core_offs:
                    clean_gov = co.name_ar.replace('مكتب التربية والتعليم - ', '').strip()
                    gov_names.extend([co.name_ar, clean_gov])
                child_dirs = CoreOrg.objects.filter(company_level=40, fk_parent_organization__in=off_ids, is_deleted=False)
                child_schools = CoreOrg.objects.filter(company_level=50, fk_parent_organization__in=child_dirs.values_list('id', flat=True), is_deleted=False)
                child_school_names = list(child_schools.values_list('name_ar', flat=True))

            q_off = Q()
            if gov_names:
                for g in gov_names:
                    q_off |= Q(student_profile__directorate__fk_governorate__name_ar__icontains=g)
            if child_school_names:
                q_off |= Q(student_profile__organization__name_ar__in=child_school_names)
            if q_off:
                regs = regs.filter(q_off)

        # 7. فلتر البحث السريع
        search_q = request.query_params.get('search', '').strip()
        if search_q:
            regs = regs.filter(
                Q(seatNumber__icontains=search_q) |
                Q(secretNumber__icontains=search_q) |
                Q(student_profile__name_ar__icontains=search_q) |
                Q(student_profile__name_en__icontains=search_q) |
                Q(student_profile__academic_number__icontains=search_q) |
                Q(student_profile__organization__name_ar__icontains=search_q)
            )

        regs = regs.order_by('examVersion__versionCode', 'seatNumber')
        filtered_count = regs.count()

        # البجنشن (Pagination)
        is_fetch_all = request.query_params.get('all') == 'true' or request.query_params.get('page_size') == 'all'
        try:
            page_num = int(request.query_params.get('page', 1) or 1)
        except (ValueError, TypeError):
            page_num = 1
        try:
            page_size = int(request.query_params.get('page_size', 10) or 10)
        except (ValueError, TypeError):
            page_size = 10

        if is_fetch_all:
            paged_regs = regs[:5000]
            page_size = filtered_count
            num_pages = 1
            page_num = 1
        else:
            page_size = max(1, min(page_size, 100))
            page_num = max(1, page_num)
            start = (page_num - 1) * page_size
            end = start + page_size
            paged_regs = regs[start:end]
            num_pages = max(1, (filtered_count // page_size) + (1 if filtered_count % page_size else 0))

        # بناء سجلات الطلاب التفصيلية
        exam_gov_name = exam.governorate.name_ar if exam.governorate else ""
        students_list = []
        for reg in paged_regs:
            prof = reg.student_profile
            if prof and prof.name_ar:
                s_name = prof.name_ar
            elif reg.student:
                st = reg.student
                s_name = getattr(st, 'get_full_name', lambda: '')() or f"{st.first_name or ''} {st.last_name or ''}".strip() or st.username
            else:
                s_name = f"طالب ({reg.seatNumber})"

            sch_name = prof.organization.name_ar if (prof and prof.organization) else "المدرسة الرئيسية"
            dir_name = prof.directorate.name_ar if (prof and prof.directorate) else (exam.directorate.name_ar if exam.directorate else "")
            gov_name = (prof.directorate.fk_governorate.name_ar if (prof and prof.directorate and prof.directorate.fk_governorate) else exam_gov_name) or "المحافظة"

            sub = submissions_map.get(reg.id) or submissions_map.get(str(reg.seatNumber))
            has_scanned = sub is not None

            sub_id = sub.id if sub else None
            scan_status = sub.status if sub else "not_scanned"
            confidence = float(sub.overall_confidence or 0.95) if sub else 0.0
            error_msg = sub.error_message if sub else ""
            scanned_at = sub.processing_completed_at.strftime("%Y-%m-%d %H:%M") if (sub and sub.processing_completed_at) else (sub.created_at.strftime("%Y-%m-%d %H:%M") if sub and sub.created_at else "")

            orig_img = sub.original_image.url if (sub and sub.original_image) else None
            align_img = sub.aligned_image.url if (sub and sub.aligned_image) else None

            is_cheat, cheat_reason = _detect_cheating_or_violation(sub)
            is_present = has_scanned or reg.isPresent
            is_absent = not has_scanned and not reg.isPresent

            score_val = float(sub.total_score or 0.0) if sub else 0.0
            percent_val = round((score_val / max(1.0, exam_max_score)) * 100.0, 1) if sub else 0.0
            grade_info = _calculate_grade_letter(percent_val) if sub else {"code": "—", "name_ar": "غائب", "color": "grey"}

            is_printed_effective = reg.is_printed or has_scanned

            # حكم المطابقة النهائي (Verification Verdict)
            if is_cheat:
                verdict = "cheating"
                verdict_ar = "حالة غش / مخالفة"
                verdict_color = "purple"
            elif has_scanned and sub.status == Submission.Status.FAILED:
                verdict = "scan_failed"
                verdict_ar = "فشل المسح الضوئي"
                verdict_color = "error"
            elif has_scanned and sub.status == Submission.Status.NEEDS_REVIEW:
                verdict = "needs_review"
                verdict_ar = "يحتاج مراجعة وتدقيق"
                verdict_color = "warning"
            elif has_scanned and sub.status == Submission.Status.COMPLETED:
                verdict = "verified"
                verdict_ar = "مطابقة سليمة وممسوحة"
                verdict_color = "success"
            elif not has_scanned and is_printed_effective:
                verdict = "missing"
                verdict_ar = "ورقة مفقودة"
                verdict_color = "error"
            elif not has_scanned and not is_printed_effective:
                verdict = "not_printed"
                verdict_ar = "لم تطبع بعد"
                verdict_color = "grey"
            else:
                verdict = "unknown"
                verdict_ar = "غير محدد"
                verdict_color = "grey"

            students_list.append({
                "id": reg.id,
                "registration_id": reg.id,
                "submission_id": sub_id,
                "student_name": s_name,
                "seat_number": reg.seatNumber,
                "secret_number": reg.secretNumber or "—",
                "version_code": reg.examVersion.versionCode if reg.examVersion else "A",
                "school_name": sch_name,
                "directorate_name": dir_name,
                "governorate_name": gov_name,
                "is_printed": is_printed_effective,
                "print_status_display": "طُبعت ومُسحت" if (is_printed_effective and has_scanned) else ("طُبعت" if is_printed_effective else "لم تُطبع"),
                "printed_at": reg.printed_at.strftime("%Y-%m-%d %H:%M") if reg.printed_at else "",
                "print_batch": reg.print_batch or "—",
                "has_scanned": has_scanned,
                "scan_status": scan_status,
                "scan_confidence": confidence,
                "scan_error": error_msg,
                "scanned_at": scanned_at,
                "original_image": orig_img,
                "aligned_image": align_img,
                "is_present": is_present,
                "is_absent": is_absent,
                "is_cheating": is_cheat,
                "cheating_reason": cheat_reason,
                "score": score_val,
                "max_score": exam_max_score,
                "percentage": percent_val,
                "grade_code": grade_info["code"],
                "grade_name_ar": grade_info["name_ar"],
                "grade_color": grade_info["color"],
                "result_status": "passed" if (has_scanned and score_val >= (exam_max_score * 0.5)) else ("failed" if has_scanned else "absent"),
                "verification_verdict": verdict,
                "verdict_name_ar": verdict_ar,
                "verdict_color": verdict_color,
            })

        gov_obj = exam.governorate
        dir_obj = exam.directorate
        office_org = CoreOrg.objects.filter(company_level=30, fk_governorate=gov_obj, is_deleted=False).first() if gov_obj else None

        # بناء تفاصيل المسار (Breadcrumb) بدقة بناءً على الفلاتر المطبقة
        if filter_school and filter_school != 'all':
            if str(filter_school).isdigit():
                sch_org = CoreOrg.objects.filter(id=int(filter_school)).first()
                breadcrumb_sch = sch_org.name_ar if sch_org else str(filter_school)
            else:
                matched_sch = [s for s in schools_set if filter_school.strip().lower() in s.lower()]
                breadcrumb_sch = matched_sch[0] if matched_sch else filter_school
        elif len(schools_set) == 1:
            breadcrumb_sch = list(schools_set)[0]
        elif len(schools_set) > 1:
            breadcrumb_sch = f"كافة المدارس والمراكز ({len(schools_set)} مدارس)"
        else:
            breadcrumb_sch = "كافة المدارس"

        if filter_directorate and filter_directorate != 'all':
            if str(filter_directorate).isdigit():
                dir_org = CoreOrg.objects.filter(id=int(filter_directorate)).first()
                breadcrumb_dir = dir_org.name_ar if dir_org else str(filter_directorate)
            else:
                matched_dir = [d for d in directorates_set if filter_directorate.strip().lower() in d.lower()]
                breadcrumb_dir = matched_dir[0] if matched_dir else filter_directorate
        elif dir_obj:
            breadcrumb_dir = dir_obj.name_ar
        elif len(directorates_set) == 1:
            breadcrumb_dir = list(directorates_set)[0]
        elif len(directorates_set) > 1:
            breadcrumb_dir = f"كافة المديريات ({len(directorates_set)} مديريات)"
        else:
            breadcrumb_dir = "كافة المديريات"

        if filter_office and filter_office != 'all':
            if str(filter_office).isdigit():
                off_org = CoreOrg.objects.filter(id=int(filter_office)).first()
                breadcrumb_off = off_org.name_ar if off_org else str(filter_office)
            else:
                breadcrumb_off = filter_office
        elif office_org:
            breadcrumb_off = office_org.name_ar
        elif gov_obj:
            breadcrumb_off = f"مكتب التربية والتعليم - {gov_obj.name_ar}"
        else:
            breadcrumb_off = "كافة مكاتب التربية بالمحافظات"

        breadcrumb = {
            "institution_type_name": "التعليم الجامعي" if exam.institution_type == 'university' else ("التعليم الفني والمهني" if exam.institution_type == 'institute' else "التعليم العام"),
            "office_name": breadcrumb_off,
            "directorate_name": breadcrumb_dir,
            "school_name": breadcrumb_sch,
            "exam_title": exam.title,
        }

        return Response({
            "success": True,
            "exam_id": exam.id,
            "exam_title": exam.title,
            "breadcrumb": breadcrumb,
            "exam": {
                "id": exam.id,
                "title": exam.title,
                "uniqueCode": exam.uniqueCode,
                "institution_type": exam.institution_type,
                "subject_name": getattr(exam.subject, 'name_ar', str(exam.subject)) if exam.subject else "",
                "year_name": exam.year.gregorian_year if (exam.year and hasattr(exam.year, 'gregorian_year')) else (str(exam.year) if exam.year else ""),
                "max_score": exam_max_score,
                "governorate_name": gov_obj.name_ar if gov_obj else "",
                "directorate_name": dir_obj.name_ar if dir_obj else "",
                "school_name": breadcrumb_sch,
            },
            "stats": exam_stats,
            "count": filtered_count,
            "results": students_list,
            "students": students_list,
            "filter_options": {
                "schools": sorted(list(schools_set)),
                "directorates": sorted(list(directorates_set)),
                "versions": sorted(list(versions_set)),
                "grades": ["A+", "A", "B+", "B", "C+", "C", "D+", "D", "F"],
            }
        })
