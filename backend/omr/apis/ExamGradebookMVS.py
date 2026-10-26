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


class ExamGradebookMVS(ViewSet):
    """
    سجل درجات الاختبارات والترحيل لنظام الكنترول المركزي.
    """
    from omr.permissions import IsControlOfficer
    permission_classes = [permissions.IsAuthenticated, IsControlOfficer]

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
        office_id = request.query_params.get('office_id') or request.query_params.get('office')
        directorate_id = request.query_params.get('directorate_id') or request.query_params.get('directorate')
        school_id = request.query_params.get('school_id') or request.query_params.get('school')

        # فلترة الاختبارات حسب المدرسة / المركز المحدد
        if school_id:
            matched_school_names = []
            if str(school_id).isdigit():
                core_sch = CoreOrg.objects.filter(id=int(school_id), company_level=50).first()
                if core_sch:
                    matched_school_names.append(core_sch.name_ar)
                try:
                    from academic.models.common.Organization import Organization as AcademicOrg
                    ac_sch = AcademicOrg.objects.filter(id=int(school_id)).first()
                    if ac_sch and ac_sch.name_ar not in matched_school_names:
                        matched_school_names.append(ac_sch.name_ar)
                except Exception:
                    pass
            else:
                matched_school_names.append(str(school_id).strip())

            exam_ids_for_school = StudentExamRegistration.objects.filter(
                is_deleted=False
            ).filter(
                Q(student_profile__organization_id=school_id) |
                Q(student_profile__organization__name_ar__in=matched_school_names)
            ).values_list('examVersion__exam_id', flat=True).distinct()

            qs = qs.filter(id__in=exam_ids_for_school)

        # فلترة الاختبارات حسب إدارة التربية بالمديرية
        elif directorate_id:
            dir_names = []
            child_school_names = []
            if str(directorate_id).isdigit():
                core_dir = CoreOrg.objects.filter(id=int(directorate_id), company_level=40).first()
                if core_dir:
                    clean_name = core_dir.name_ar.replace('إدارة التربية والتعليم - مديرية ', '').replace('إدارة التربية والتعليم - ', '').strip()
                    dir_names.extend([core_dir.name_ar, clean_name])
                    child_schools = CoreOrg.objects.filter(company_level=50, fk_parent_organization=core_dir.id, is_deleted=False)
                    child_school_names = list(child_schools.values_list('name_ar', flat=True))
            else:
                dir_names.append(str(directorate_id).strip())

            dir_exam_ids = StudentExamRegistration.objects.filter(is_deleted=False).filter(
                Q(student_profile__directorate__name_ar__in=dir_names) |
                Q(student_profile__organization__name_ar__in=child_school_names)
            ).values_list('examVersion__exam_id', flat=True).distinct()

            dir_q = Q(id__in=dir_exam_ids)
            if str(directorate_id).isdigit():
                dir_q |= Q(directorate_id=int(directorate_id))
            for d_name in dir_names:
                dir_q |= Q(directorate__name_ar__icontains=d_name)

            qs = qs.filter(dir_q)

        # فلترة الاختبارات حسب مكتب التربية والتعليم بالمحافظة
        elif office_id:
            off_ids = [int(x) for x in str(office_id).split(',') if x.strip().isdigit()] if (office_id and office_id != 'all') else []
            gov_names = []
            child_school_names = []
            gov_ids = []
            if off_ids:
                core_offs = CoreOrg.objects.filter(id__in=off_ids, company_level=30)
                for core_off in core_offs:
                    clean_gov = core_off.name_ar.replace('مكتب التربية والتعليم - ', '').strip()
                    gov_names.extend([core_off.name_ar, clean_gov])
                    if core_off.fk_governorate_id:
                        gov_ids.append(core_off.fk_governorate_id)
                child_dirs = CoreOrg.objects.filter(company_level=40, fk_parent_organization__in=off_ids, is_deleted=False)
                child_schools = CoreOrg.objects.filter(company_level=50, fk_parent_organization__in=child_dirs.values_list('id', flat=True), is_deleted=False)
                child_school_names = list(child_schools.values_list('name_ar', flat=True))
            else:
                gov_names.append(str(office_id).strip())

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

        gov_to_office_map = {
            o.fk_governorate_id: o.id 
            for o in CoreOrg.objects.filter(company_level=30, fk_governorate__isnull=False, is_deleted=False)
        }

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

            prn_cnt = StudentExamRegistration.objects.filter(is_deleted=False, examVersion__exam=exam, is_printed=True).count()
            prn_rate = round((prn_cnt / max(1, total_registered)) * 100, 1) if total_registered > 0 else 0.0

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
                "schools_count": schools_cnt,
                "max_score": exam_max_score,
                "total_registered": total_registered,
                "total_students": total_registered,
                "total_submissions": total_submissions,
                "completed_count": completed_subs,
                "needs_review_count": needs_review_subs,
                "absent_count": max(0, total_registered - total_submissions),
                "completion_rate": completion_rate,
                "printed_count": prn_cnt,
                "printed_rate": prn_rate,
                "print_status": "printed" if (prn_cnt > 0 and prn_cnt == total_registered) else ("partial" if prn_cnt > 0 else "none"),
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

    @action(detail=False, methods=['get'], url_path='by-office')
    def by_office(self, request):
        """
        تجميع إحصائيات الرصد والكنترول حسب مكاتب التربية والتعليم بالمحافظات (المستوى 30 الحقيقي).
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
            exams_cnt = regs.values('examVersion__exam_id').distinct().count()
            subjs = [s for s in regs.values_list('examVersion__exam__subject__name_ar', flat=True).distinct() if s]
            comp = Submission.objects.filter(
                is_deleted=False, 
                status=Submission.Status.COMPLETED, 
                registration__in=regs
            ).count()

            printed = regs.filter(is_printed=True).count()

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
                "completed_count": comp,
                "absent_count": max(0, tot - comp),
                "completion_rate": round((comp / max(1, tot)) * 100, 1) if tot > 0 else 0.0,
                "printed_count": printed,
                "printed_rate": round((printed / max(1, tot)) * 100, 1) if tot > 0 else 0.0,
                "print_status": "printed" if (printed > 0 and printed == tot) else ("partial" if printed > 0 else "none"),
            })

        return Response({
            "success": True,
            "count": len(results),
            "results": results
        })

    @action(detail=False, methods=['get'], url_path='by-directorate')
    def by_directorate(self, request):
        """
        تجميع إحصائيات الرصد والكنترول حسب إدارات التربية والتعليم بالمديريات (المستوى 40).
        """
        search = request.query_params.get('search', '').strip()
        office_id = request.query_params.get('office_id') or request.query_params.get('office')
        off_ids = [int(x) for x in str(office_id).split(',') if x.strip().isdigit()] if (office_id and office_id != 'all') else []
        subj_filter = request.query_params.get('subject') or request.query_params.get('subject_id')

        dirs_qs = CoreOrg.objects.filter(company_level=40, is_deleted=False)
        if off_ids:
            dirs_qs = dirs_qs.filter(fk_parent_organization_id__in=off_ids)
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
            exams_cnt = regs.values('examVersion__exam_id').distinct().count()
            subjs = [s for s in regs.values_list('examVersion__exam__subject__name_ar', flat=True).distinct() if s]
            comp = Submission.objects.filter(
                is_deleted=False, 
                status=Submission.Status.COMPLETED, 
                registration__in=regs
            ).count()

            printed = regs.filter(is_printed=True).count()

            parent_office = d.fk_parent_organization
            results.append({
                "id": d.id,
                "name": d.name_ar,
                "office_id": d.fk_parent_organization_id,
                "office_name": parent_office.name_ar if parent_office else "—",
                "governorate_name": parent_office.name_ar.replace('مكتب التربية والتعليم - ', '') if parent_office else "—",
                "schools_count": child_schools.count(),
                "exams_count": exams_cnt,
                "subjects": subjs,
                "subject_name": subjs[0] if len(subjs) == 1 else (", ".join(subjs[:2]) + ("..." if len(subjs) > 2 else "") if subjs else "—"),
                "total_students": tot,
                "completed_count": comp,
                "absent_count": max(0, tot - comp),
                "completion_rate": round((comp / max(1, tot)) * 100, 1) if tot > 0 else 0.0,
                "printed_count": printed,
                "printed_rate": round((printed / max(1, tot)) * 100, 1) if tot > 0 else 0.0,
                "print_status": "printed" if (printed > 0 and printed == tot) else ("partial" if printed > 0 else "none"),
            })

        return Response({
            "success": True,
            "count": len(results),
            "results": results
        })

    @action(detail=False, methods=['get'], url_path='by-school')
    def by_school(self, request):
        """
        تجميع إحصائيات الرصد والكنترول حسب المدرسة / المركز الامتحاني / الجامعة / المعهد.
        """
        search = request.query_params.get('search', '').strip()
        office_id = request.query_params.get('office_id') or request.query_params.get('office')
        directorate_id = request.query_params.get('directorate_id') or request.query_params.get('directorate')
        institution_type = request.query_params.get('institution_type')
        subj_filter = request.query_params.get('subject') or request.query_params.get('subject_id')

        regs_qs = StudentExamRegistration.objects.filter(
            is_deleted=False, 
            examVersion__exam__is_deleted=False,
            student_profile__organization__isnull=False
        )
        if subj_filter and subj_filter != 'all':
            if str(subj_filter).isdigit():
                regs_qs = regs_qs.filter(examVersion__exam__subject_id=int(subj_filter))
            else:
                regs_qs = regs_qs.filter(Q(examVersion__exam__subject__name_ar__icontains=subj_filter) | Q(examVersion__exam__subject__name_en__icontains=subj_filter))

        if search:
            regs_qs = regs_qs.filter(
                Q(student_profile__organization__name_ar__icontains=search) |
                Q(student_profile__organization__name_en__icontains=search)
            )

        off_ids = [int(x) for x in str(office_id).split(',') if x.strip().isdigit()] if (office_id and office_id != 'all') else []
        dir_ids = [int(x) for x in str(directorate_id).split(',') if x.strip().isdigit()] if (directorate_id and directorate_id != 'all') else []

        if dir_ids:
            core_dirs = CoreOrg.objects.filter(id__in=dir_ids, company_level=40)
            if core_dirs.exists():
                child_schools = CoreOrg.objects.filter(company_level=50, fk_parent_organization__in=core_dirs.values_list('id', flat=True), is_deleted=False)
                school_names = list(child_schools.values_list('name_ar', flat=True))
                clean_names = [d.name_ar.replace('إدارة التربية والتعليم - مديرية ', '').replace('إدارة التربية والتعليم - ', '').strip() for d in core_dirs]
                dir_names = list(core_dirs.values_list('name_ar', flat=True))
                regs_qs = regs_qs.filter(
                    Q(student_profile__organization__name_ar__in=school_names) |
                    Q(student_profile__directorate__name_ar__in=clean_names) |
                    Q(student_profile__directorate__name_ar__in=dir_names)
                )
            else:
                regs_qs = regs_qs.filter(student_profile__directorate_id__in=dir_ids)
        elif off_ids:
            core_offices = CoreOrg.objects.filter(id__in=off_ids, company_level=30)
            if core_offices.exists():
                child_dirs = CoreOrg.objects.filter(company_level=40, fk_parent_organization__in=core_offices.values_list('id', flat=True), is_deleted=False)
                child_schools = CoreOrg.objects.filter(company_level=50, fk_parent_organization__in=child_dirs.values_list('id', flat=True), is_deleted=False)
                school_names = list(child_schools.values_list('name_ar', flat=True))
                regs_qs = regs_qs.filter(student_profile__organization__name_ar__in=school_names)

        if institution_type and institution_type != 'all':
            regs_qs = regs_qs.filter(student_profile__organization__institution_type=institution_type)

        # خريطة إدارات ومحافظات المدارس من الهيكل المؤسسي المعتمد CoreOrg (المستوى 50)
        core_schools = CoreOrg.objects.filter(company_level=50, is_deleted=False).select_related(
            'fk_parent_organization', 'fk_parent_organization__fk_parent_organization'
        )
        core_map = {}
        for cs in core_schools:
            dir_name = cs.fk_parent_organization.name_ar.replace('إدارة التربية والتعليم - مديرية ', '').replace('إدارة التربية والتعليم - ', '').strip() if cs.fk_parent_organization else "—"
            gov_name = cs.fk_parent_organization.fk_parent_organization.name_ar.replace('مكتب التربية والتعليم - ', '').strip() if (cs.fk_parent_organization and cs.fk_parent_organization.fk_parent_organization) else "—"
            dir_id = cs.fk_parent_organization_id
            off_id = cs.fk_parent_organization.fk_parent_organization_id if cs.fk_parent_organization else None
            core_map[cs.name_ar] = (dir_name, gov_name, dir_id, off_id)

        student_geo_map = {}
        for row in regs_qs.values(
            'student_profile__organization_id',
            'student_profile__directorate__name_ar',
            'student_profile__directorate__fk_governorate__name_ar'
        ).exclude(student_profile__directorate__name_ar__isnull=True):
            oid = row['student_profile__organization_id']
            if oid not in student_geo_map:
                student_geo_map[oid] = (
                    row['student_profile__directorate__name_ar'] or "—",
                    row['student_profile__directorate__fk_governorate__name_ar'] or "—"
                )

        # تجميع المدارس والمؤسسات التعليمية بشكل وحيد ومطلق دون أي تكرار
        schools_agg = regs_qs.values(
            'student_profile__organization_id',
            'student_profile__organization__name_ar',
            'student_profile__organization__institution_type',
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
            org_id = s['student_profile__organization_id']
            name = s['student_profile__organization__name_ar'] or "مؤسسة تعليمية غير محددة"
            tot = s['total_students']
            comp = subs_completed.get(org_id, 0)
            avg_sc = subs_scores.get(org_id, 0.0) or 0.0
            prn = subs_printed.get(org_id, 0)

            dir_info = core_map.get(name, (None, None, None, None))
            dir_name, gov_name, dir_id, off_id = dir_info
            if not dir_name:
                geo_tuple = student_geo_map.get(org_id, ("—", "—"))
                dir_name, gov_name = geo_tuple[0], geo_tuple[1]

            # تفاصيل المواد والاختبارات التابعة للمدرسة ونماذجها المقيدة للطلاب
            school_regs = regs_qs.filter(student_profile__organization_id=org_id).select_related(
                'examVersion', 'examVersion__exam', 'examVersion__exam__subject'
            )
            school_subjs = [sb for sb in school_regs.values_list('examVersion__exam__subject__name_ar', flat=True).distinct() if sb]

            exam_groups = {}
            for reg in school_regs:
                ev = reg.examVersion
                ex = ev.exam if ev else None
                if not ex:
                    continue
                eid = ex.id
                if eid not in exam_groups:
                    sub_name = ex.subject.name_ar if ex.subject else "عام"
                    exam_groups[eid] = {
                        "id": eid,
                        "title": ex.title,
                        "code": ex.uniqueCode,
                        "subject": sub_name,
                        "models_mode": getattr(ex, 'models_mode', 'uniform'),
                        "versions_dict": {},
                        "students_count": 0,
                    }
                v_code = ev.versionCode or "A"
                exam_groups[eid]["versions_dict"][v_code] = exam_groups[eid]["versions_dict"].get(v_code, 0) + 1
                exam_groups[eid]["students_count"] += 1

            formatted_exams = []
            for eid, edata in exam_groups.items():
                v_list = [
                    {"code": code, "students_count": count}
                    for code, count in sorted(edata["versions_dict"].items())
                ]
                v_parts = []
                for code, count in sorted(edata["versions_dict"].items()):
                    if count == 1:
                        c_str = "طالب واحد"
                    elif count == 2:
                        c_str = "طالبان"
                    elif 3 <= count <= 10:
                        c_str = f"{count} طلاب"
                    else:
                        c_str = f"{count} طالب"
                    v_parts.append(f"نموذج {code} ({c_str})")
                versions_summary = "، ".join(v_parts) if v_parts else "كافة النماذج"

                formatted_exams.append({
                    "id": eid,
                    "title": edata["title"],
                    "code": edata["code"],
                    "subject": edata["subject"],
                    "models_mode": edata["models_mode"],
                    "students_count": edata["students_count"],
                    "versions": v_list,
                    "versions_summary": versions_summary,
                })

            results.append({
                "id": org_id,
                "name": name,
                "institution_type": s['student_profile__organization__institution_type'] or "school",
                "directorate_id": dir_id,
                "office_id": off_id,
                "directorate_name": dir_name or "—",
                "governorate_name": gov_name or "—",
                "total_students": tot,
                "exams_count": len(formatted_exams),
                "subjects": school_subjs,
                "subject_name": school_subjs[0] if len(school_subjs) == 1 else (", ".join(school_subjs[:2]) + ("..." if len(school_subjs) > 2 else "") if school_subjs else "—"),
                "primary_subject": school_subjs[0] if school_subjs else "—",
                "exams": formatted_exams,
                "completed_count": comp,
                "absent_count": max(0, tot - comp),
                "completion_rate": round((comp / max(1, tot)) * 100, 1) if tot > 0 else 0.0,
                "average_score": round(float(avg_sc), 1),
                "printed_count": prn,
                "printed_rate": round((prn / max(1, tot)) * 100, 1) if tot > 0 else 0.0,
                "print_status": "printed" if (prn > 0 and prn == tot) else ("partial" if prn > 0 else "none"),
            })

        return Response({
            "success": True,
            "count": len(results),
            "results": results
        })

    @action(detail=False, methods=['get'], url_path='subjects')
    def available_subjects(self, request):
        """
        قائمة المواد الدراسية المعتمدة بالاختبارات المصدرة لفلترة شاشات الطباعة والرصد،
        مع دعم التصفية الدقيقة حسب نوع المؤسسة (مدرسي / جامعي / معاهد) والمحافظات والمديريات.
        """
        from exams.models.Exam import Exam
        institution_type = request.query_params.get('institution_type')
        office_id = request.query_params.get('office_id')
        directorate_id = request.query_params.get('directorate_id')
        school_id = request.query_params.get('school_id')

        exams_qs = Exam.objects.filter(is_deleted=False, subject__isnull=False)

        if institution_type and institution_type != 'all':
            exams_qs = exams_qs.filter(institution_type=institution_type)

        from OpenSoftCoreV41.common.models.Branch import Organization as CoreOrg
        from exams.models.StudentExamRegistration import StudentExamRegistration

        if directorate_id and directorate_id != 'all':
            dir_ids = [int(x) for x in str(directorate_id).split(',') if x.strip().isdigit()]
            if dir_ids:
                core_dirs = CoreOrg.objects.filter(id__in=dir_ids, company_level=40)
                child_schools = CoreOrg.objects.filter(company_level=50, fk_parent_organization__in=core_dirs.values_list('id', flat=True), is_deleted=False)
                school_names = list(child_schools.values_list('name_ar', flat=True))
                reg_exam_ids = StudentExamRegistration.objects.filter(
                    is_deleted=False,
                    student_profile__organization__name_ar__in=school_names
                ).values_list('examVersion__exam_id', flat=True)
                exams_qs = exams_qs.filter(Q(directorate_id__in=dir_ids) | Q(id__in=reg_exam_ids))
        elif office_id and office_id != 'all':
            off_ids = [int(x) for x in str(office_id).split(',') if x.strip().isdigit()]
            if off_ids:
                core_offices = CoreOrg.objects.filter(id__in=off_ids, company_level=30)
                child_dirs = CoreOrg.objects.filter(company_level=40, fk_parent_organization__in=core_offices.values_list('id', flat=True), is_deleted=False)
                child_schools = CoreOrg.objects.filter(company_level=50, fk_parent_organization__in=child_dirs.values_list('id', flat=True), is_deleted=False)
                school_names = list(child_schools.values_list('name_ar', flat=True))
                reg_exam_ids = StudentExamRegistration.objects.filter(
                    is_deleted=False,
                    student_profile__organization__name_ar__in=school_names
                ).values_list('examVersion__exam_id', flat=True)
                exams_qs = exams_qs.filter(Q(governorate_id__in=off_ids) | Q(id__in=reg_exam_ids))

        if school_id and school_id != 'all':
            sch_ids = [int(x) for x in str(school_id).split(',') if x.strip().isdigit()]
            if sch_ids:
                reg_exam_ids = StudentExamRegistration.objects.filter(
                    is_deleted=False,
                    student_profile__organization_id__in=sch_ids
                ).values_list('examVersion__exam_id', flat=True)
                exams_qs = exams_qs.filter(id__in=reg_exam_ids)

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

        # 3.0 فلتر مكتب التربية والتعليم بالمحافظة (المستوى 30)
        office_id = request.query_params.get('office_id')
        if office_id and str(office_id).isdigit():
            child_dirs = CoreOrg.objects.filter(company_level=40, fk_parent_organization=int(office_id), is_deleted=False)
            child_schools = CoreOrg.objects.filter(company_level=50, fk_parent_organization__in=child_dirs.values_list('id', flat=True), is_deleted=False)
            school_names = list(child_schools.values_list('name_ar', flat=True))
            dir_names = list(child_dirs.values_list('name_ar', flat=True))
            clean_dir_names = [d.replace('إدارة التربية والتعليم - مديرية ', '').replace('إدارة التربية والتعليم - ', '').strip() for d in dir_names]
            registrations = registrations.filter(
                Q(student_profile__organization__name_ar__in=school_names) |
                Q(student_profile__directorate__name_ar__in=clean_dir_names) |
                Q(student_profile__directorate__name_ar__in=dir_names)
            )

        # 3.0.1 فلتر إدارة التربية والتعليم بالمديرية (المستوى 40)
        dir_id = request.query_params.get('directorate_id')
        if dir_id and str(dir_id).isdigit():
            try:
                dir_org = CoreOrg.objects.get(id=int(dir_id), is_deleted=False)
                clean_name = dir_org.name_ar.replace('إدارة التربية والتعليم - مديرية ', '').replace('إدارة التربية والتعليم - ', '').strip()
                child_schools = CoreOrg.objects.filter(company_level=50, fk_parent_organization=int(dir_id), is_deleted=False)
                school_names = list(child_schools.values_list('name_ar', flat=True))
                registrations = registrations.filter(
                    Q(student_profile__directorate__name_ar__icontains=clean_name) |
                    Q(student_profile__directorate__name_ar__icontains=dir_org.name_ar) |
                    Q(student_profile__organization__name_ar__in=school_names)
                )
            except CoreOrg.DoesNotExist:
                pass

        # 3.1 فلتر المحافظة (يدعم تحديد مفرد أو متعدد عبر المعرفات الرقمية والأسماء)
        gov_raw = request.query_params.getlist('governorate') or [request.query_params.get('governorate') or request.query_params.get('governorate_name') or '']
        gov_list = [p.strip() for item in gov_raw for p in str(item).split(',') if p.strip() and p != 'all']
        if gov_list:
            gov_ids = [int(p) for p in gov_list if p.isdigit()]
            gov_names = [p for p in gov_list if not p.isdigit()]
            gov_q = Q()
            if gov_ids:
                gov_q |= (
                    Q(student_profile__directorate__fk_governorate_id__in=gov_ids) |
                    Q(student__student_profile__directorate__fk_governorate_id__in=gov_ids) |
                    Q(examVersion__exam__governorate_id__in=gov_ids)
                )
            if gov_names:
                for g_name in gov_names:
                    gov_q |= (
                        Q(student_profile__directorate__fk_governorate__name_ar__icontains=g_name) |
                        Q(student_profile__directorate__fk_governorate__name_en__icontains=g_name) |
                        Q(student__student_profile__directorate__fk_governorate__name_ar__icontains=g_name) |
                        Q(examVersion__exam__governorate__name_ar__icontains=g_name)
                    )
            registrations = registrations.filter(gov_q)

        # 3.2 فلتر المديرية (يدعم تحديد مفرد أو متعدد عبر المعرفات والأسماء)
        dir_raw = request.query_params.getlist('directorate') or [request.query_params.get('directorate') or request.query_params.get('directorate_name') or '']
        dir_list = [p.strip() for item in dir_raw for p in str(item).split(',') if p.strip() and p != 'all']
        if dir_list:
            dir_ids = [int(p) for p in dir_list if p.isdigit()]
            dir_names = [p for p in dir_list if not p.isdigit()]
            dir_q = Q()
            if dir_ids:
                dir_q |= (
                    Q(student_profile__directorate_id__in=dir_ids) |
                    Q(student__student_profile__directorate_id__in=dir_ids) |
                    Q(examVersion__exam__directorate_id__in=dir_ids)
                )
            if dir_names:
                for d_name in dir_names:
                    dir_q |= (
                        Q(student_profile__directorate__name_ar__icontains=d_name) |
                        Q(student_profile__directorate__name_en__icontains=d_name) |
                        Q(student__student_profile__directorate__name_ar__icontains=d_name) |
                        Q(examVersion__exam__directorate__name_ar__icontains=d_name)
                    )
            registrations = registrations.filter(dir_q)

        # 3.3 فلتر المدرسة / المركز الامتحاني (يدعم تحديد مفرد أو متعدد)
        sch_raw = request.query_params.getlist('school') or [request.query_params.get('school') or request.query_params.get('school_name') or request.query_params.get('organization') or '']
        req_school_id = request.query_params.get('school_id')
        if req_school_id and str(req_school_id).strip():
            sch_raw.append(str(req_school_id).strip())
        sch_list = [p.strip() for item in sch_raw for p in str(item).split(',') if p.strip() and p != 'all']
        if sch_list:
            sch_ids = [int(p) for p in sch_list if p.isdigit()]
            sch_names = [p for p in sch_list if not p.isdigit()]
            sch_q = Q()
            if sch_ids:
                sch_q |= (
                    Q(student_profile__organization_id__in=sch_ids) |
                    Q(student__student_profile__organization_id__in=sch_ids)
                )
            if sch_names:
                for s_name in sch_names:
                    sch_q |= (
                        Q(student_profile__organization__name_ar__icontains=s_name) |
                        Q(student_profile__organization__name_en__icontains=s_name) |
                        Q(student__student_profile__organization__name_ar__icontains=s_name)
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

        # Gate 8 & P1: جلب كافة بيانات الطلاب (100%) بدون التقيد ببجنشن العرض (10 طلاب)
        req_params = request.query_params.copy()
        req_params['all'] = 'true'
        if hasattr(request, '_request'):
            request._request.GET = req_params
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
