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

        exams_list = []
        for exam in qs[:100]:
            total_registered = StudentExamRegistration.objects.filter(
                examVersion__exam=exam, is_deleted=False
            ).count()

            subs = Submission.objects.filter(exam=exam, is_deleted=False)
            total_submissions = subs.count()
            completed_subs = subs.filter(status=Submission.Status.COMPLETED).count()
            needs_review_subs = subs.filter(status=Submission.Status.NEEDS_REVIEW).count()

            # إحصائيات الدرجات
            aggregates = subs.filter(status=Submission.Status.COMPLETED).aggregate(
                avg_score=Avg('total_score'),
                max_score=Max('total_score'),
                min_score=Min('total_score')
            )
            exam_max_score = float(getattr(exam, 'total_score', 100) or 100)
            avg_val = float(aggregates['avg_score'] or 0.0)
            pass_count = subs.filter(status=Submission.Status.COMPLETED, total_score__gte=(exam_max_score * 0.5)).count()

            # التحقق من عدد السجلات المرحلة للكنترول
            dispatched_count = 0
            for s in subs:
                lr = s.layout_result or {}
                if lr.get("dispatched_to_control"):
                    dispatched_count += 1

            dispatch_status = "none"
            if dispatched_count > 0 and dispatched_count >= completed_subs and completed_subs > 0:
                dispatch_status = "full"
            elif dispatched_count > 0:
                dispatch_status = "partial"

            exams_list.append({
                "id": exam.id,
                "title": exam.title,
                "uniqueCode": exam.uniqueCode,
                "institution_type": exam.institution_type,
                "institution_type_display": "مدرسي" if exam.institution_type == 'school' else ("جامعي" if exam.institution_type == 'university' else "معاهد"),
                "subject_name": getattr(exam.subject, 'name_ar', str(exam.subject)) if exam.subject else "غير محدد",
                "year_name": exam.year.gregorian_year if (exam.year and hasattr(exam.year, 'gregorian_year')) else (str(exam.year) if exam.year else "العام الحالي"),
                "max_score": exam_max_score,
                "total_registered": total_registered,
                "total_submissions": total_submissions,
                "completed_count": completed_subs,
                "needs_review_count": needs_review_subs,
                "absent_count": max(0, total_registered - total_submissions),
                "dispatched_count": dispatched_count,
                "dispatch_status": dispatch_status,
                "average_score": round(avg_val, 2),
                "highest_score": float(aggregates['max_score'] or 0.0),
                "lowest_score": float(aggregates['min_score'] or 0.0),
                "pass_rate": round((pass_count / float(max(1, completed_subs))) * 100, 1),
                "created_at": exam.created_at.strftime("%Y-%m-%d %H:%M") if exam.created_at else "",
            })

        return Response({
            "success": True,
            "count": len(exams_list),
            "results": exams_list
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

        # استخراج خيارات التصفية المتاحة لهذا الاختبار
        schools_list = list(
            base_registrations
            .values_list('student_profile__organization__name_ar', flat=True)
            .exclude(student_profile__organization__name_ar__isnull=True)
            .exclude(student_profile__organization__name_ar__exact='')
            .distinct()
        )

        directorates_list = list(
            base_registrations
            .values_list('student_profile__directorate__name_ar', flat=True)
            .exclude(student_profile__directorate__name_ar__isnull=True)
            .exclude(student_profile__directorate__name_ar__exact='')
            .distinct()
        )
        if exam.directorate and exam.directorate.name_ar and exam.directorate.name_ar not in directorates_list:
            directorates_list.append(exam.directorate.name_ar)

        governorates_list = list(
            base_registrations
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

        # 3.1 فلتر المحافظة
        governorate = request.query_params.get('governorate') or request.query_params.get('governorate_name')
        if governorate and governorate != 'all':
            registrations = registrations.filter(
                Q(student_profile__directorate__fk_governorate__name_ar=governorate) |
                Q(student_profile__directorate__fk_governorate__name_en=governorate) |
                Q(examVersion__exam__governorate__name_ar=governorate) |
                Q(examVersion__exam__governorate__name_en=governorate)
            )

        # 3.2 فلتر المديرية
        directorate = request.query_params.get('directorate') or request.query_params.get('directorate_name')
        if directorate and directorate != 'all':
            registrations = registrations.filter(
                Q(student_profile__directorate__name_ar=directorate) |
                Q(student_profile__directorate__name_en=directorate) |
                Q(examVersion__exam__directorate__name_ar=directorate) |
                Q(examVersion__exam__directorate__name_en=directorate)
            )

        # 3.3 فلتر المدرسة / المؤسسة
        school = request.query_params.get('school') or request.query_params.get('school_name') or request.query_params.get('organization')
        if school and school != 'all':
            registrations = registrations.filter(
                Q(student_profile__organization__name_ar=school) |
                Q(student_profile__organization__name_en=school)
            )

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
                s_name = reg.student.get_full_name() or reg.student.username
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

        target_reg_ids = request.data.get('registration_ids')
        subs_qs = Submission.objects.filter(exam=exam, status=Submission.Status.COMPLETED, is_deleted=False)

        if target_reg_ids and isinstance(target_reg_ids, list):
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

        dispatched_count = 0
        with transaction.atomic():
            for sub in subs_qs:
                lr = sub.layout_result or {}
                lr["dispatched_to_control"] = True
                lr["dispatched_at"] = now_str
                lr["dispatched_by"] = user_name
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
                description=f"ترحيل رسمي لـ ({dispatched_count}) درجة في اختبار '{exam.title}' إلى نظام الكنترول الأكاديمي."
            )

        return Response({
            "success": True,
            "message": f"تم ترحيل {dispatched_count} درجة بنجاح إلى نظام الكنترول المركزي وقفل السجلات.",
            "dispatched_count": dispatched_count,
            "dispatched_at": now_str
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
