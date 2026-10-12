from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Avg, Q

from rest_framework import permissions

from exams.models.Exam import Exam
from exams.models.ExamVersion import ExamVersion
from exams.models.ExamQuestionOrder import ExamQuestionOrder
from exams.models.StudentExamRegistration import StudentExamRegistration
from submissions.models.Submission import Submission

class ExamLinkingMVS(ViewSet):
    """
    Dedicated ViewSet for linking Generated Exams with OMR Scanning & Grading.
    Endpoint: /api/omr/exam-linking/
    Used by: OMRExamsView.vue (شاشة ربط الاختبارات والتصحيح)
    """
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        """
        List all generated exams with OMR statistics, versions, and grading status.
        """
        search = request.query_params.get('search', '').strip()
        institution_type = request.query_params.get('institution_type')
        subject_id = request.query_params.get('subject')

        qs = Exam.objects.filter(is_deleted=False).select_related(
            'subject', 'year', 'governorate', 'directorate'
        ).prefetch_related(
            'versions__question_orders'
        ).order_by('-created_at')

        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(uniqueCode__icontains=search))
        if institution_type and institution_type != 'all':
            qs = qs.filter(institution_type=institution_type)
        if subject_id:
            qs = qs.filter(subject_id=subject_id)

        results = []
        for exam in qs[:100]:
            versions = list(exam.versions.filter(is_deleted=False).order_by('versionCode'))
            versions_data = []
            max_q_count = 0

            for v in versions:
                q_count = v.question_orders.filter(is_deleted=False).count()
                if q_count > max_q_count:
                    max_q_count = q_count
                versions_data.append({
                    "id": v.id,
                    "versionCode": v.versionCode,
                    "questions_count": q_count,
                })

            # Submissions statistics
            subs = Submission.objects.filter(exam=exam, is_deleted=False)
            total_subs = subs.count()
            completed_subs = subs.filter(status=Submission.Status.COMPLETED).count()
            needs_review_subs = subs.filter(status=Submission.Status.NEEDS_REVIEW).count()
            avg_score = subs.filter(status=Submission.Status.COMPLETED).aggregate(avg=Avg('total_score'))['avg'] or 0.0

            results.append({
                "id": exam.id,
                "title": exam.title,
                "uniqueCode": exam.uniqueCode,
                "institution_type": exam.institution_type,
                "institution_type_display": exam.get_institution_type_display() if hasattr(exam, 'get_institution_type_display') else ("معاهد وتدريب مهني" if exam.institution_type == 'institute' else ("جامعي" if exam.institution_type == 'university' else "مدرسي")),
                "subject_id": exam.subject_id,
                "subject_name": getattr(exam.subject, 'name_ar', str(exam.subject)) if exam.subject else "غير محدد",
                "year_id": exam.year_id,
                "year_name": exam.year.gregorian_year if (exam.year and hasattr(exam.year, 'gregorian_year')) else (str(exam.year) if exam.year else "العام الحالي"),
                "created_at": exam.created_at.strftime("%Y-%m-%d %H:%M") if exam.created_at else "",
                "versions_count": len(versions_data),
                "versions": versions_data,
                "total_questions": max_q_count,
                "submissions_total": total_subs,
                "submissions_completed": completed_subs,
                "submissions_needs_review": needs_review_subs,
                "average_score": round(float(avg_score), 2),
                "default_template": "OMR_YEMEN_180" if max_q_count > 60 else "OMR_YEMEN_60",
                "has_answer_keys": len(versions_data) > 0 and max_q_count > 0,
                "registered_students_count": StudentExamRegistration.objects.filter(examVersion__exam=exam, is_deleted=False).count(),
            })

        return Response({
            "success": True,
            "count": len(results),
            "results": results
        })

    def retrieve(self, request, pk=None):
        """
        Get full linking details of an exam, including all its versions,
        questions, options, and model answer keys.
        """
        try:
            exam = Exam.objects.select_related('subject', 'year').get(pk=pk, is_deleted=False)
        except Exam.DoesNotExist:
            return Response({"success": False, "message": "الاختبار غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        versions = ExamVersion.objects.filter(
            exam=exam,
            is_deleted=False
        ).prefetch_related(
            'question_orders__question__options',
            'question_orders__question__lesson__unit'
        ).order_by('versionCode')

        letters = ['A', 'B', 'C', 'D', 'E', 'F']
        arabic_letters = ['أ', 'ب', 'ج', 'د', 'هـ', 'و']

        versions_details = []
        for v in versions:
            q_orders = v.question_orders.filter(is_deleted=False).order_by('orderIndex')
            questions_list = []
            answer_key = {}

            for qo in q_orders:
                q = qo.question
                opts = list(q.options.filter(is_deleted=False))
                options_data = []
                correct_letter = 'A'
                correct_arabic = 'أ'

                for idx, opt in enumerate(opts):
                    opt_letter = letters[idx] if idx < len(letters) else chr(65 + idx)
                    opt_ar = arabic_letters[idx] if idx < len(arabic_letters) else str(idx + 1)
                    if opt.isTrue:
                        correct_letter = opt_letter
                        correct_arabic = opt_ar

                    options_data.append({
                        "id": opt.id,
                        "letter": opt_letter,
                        "arabic_letter": opt_ar,
                        "text": opt.text,
                        "isTrue": opt.isTrue,
                    })

                if not opts and q.isTrue is not None:
                    correct_letter = 'A' if q.isTrue else 'B'
                    correct_arabic = 'صواب' if q.isTrue else 'خطأ'

                answer_key[str(qo.orderIndex)] = correct_letter

                questions_list.append({
                    "id": q.id,
                    "orderIndex": qo.orderIndex,
                    "content": q.content,
                    "questionType": q.questionType,
                    "bloomLevel": q.bloomLevel,
                    "assignedMark": q.defaultMark or 1.0,
                    "correctLetter": correct_letter,
                    "correctArabic": correct_arabic,
                    "options": options_data,
                })

            versions_details.append({
                "id": v.id,
                "versionCode": v.versionCode,
                "questionsCount": len(questions_list),
                "answerKey": answer_key,
                "questions": questions_list,
            })

        # Recent Submissions for this exam
        recent_subs = []
        for s in Submission.objects.filter(exam=exam, is_deleted=False).select_related('registration', 'registration__student_profile', 'exam_version').order_by('-created_at')[:50]:
            s_name = ""
            seat_no = ""
            if s.registration:
                seat_no = s.registration.seatNumber
                if s.registration.student_profile and s.registration.student_profile.name_ar:
                    s_name = s.registration.student_profile.name_ar
                elif s.registration.student:
                    s_name = s.registration.student.first_name or s.registration.student.username
            if not s_name and s.layout_result:
                s_name = s.layout_result.get("student_name", "")
            if not seat_no and s.layout_result:
                seat_no = s.layout_result.get("seat_number", "")

            recent_subs.append({
                "id": s.id,
                "seat_number": seat_no,
                "student_name": s_name,
                "version_code": s.exam_version.versionCode if s.exam_version else "",
                "status": s.status,
                "score": s.total_score,
                "confidence": s.overall_confidence,
                "created_at": s.created_at.strftime("%Y-%m-%d %H:%M") if s.created_at else "",
            })

        # Registered Students for this exam (returns sample for preview, full roster via paginated /students/)
        from exams.models.StudentExamRegistration import StudentExamRegistration
        st_qs = StudentExamRegistration.objects.filter(examVersion__exam=exam, is_deleted=False).select_related('student_profile__organization', 'student_profile__directorate', 'student', 'examVersion').order_by('seatNumber')
        total_st_count = st_qs.count()
        students_list = []
        for reg in st_qs:
            if reg.student_profile and reg.student_profile.name_ar:
                s_name = reg.student_profile.name_ar
            elif reg.student:
                s_name = reg.student.get_full_name() or reg.student.username
            else:
                s_name = f"طالب ({reg.seatNumber})"
            inst_name = reg.student_profile.organization.name_ar if (reg.student_profile and reg.student_profile.organization) else ""
            gov_name = exam.governorate.name_ar if exam.governorate else ""
            dir_name = reg.student_profile.directorate.name_ar if (reg.student_profile and reg.student_profile.directorate) else (exam.directorate.name_ar if exam.directorate else "")
            v_code = reg.examVersion.versionCode
            students_list.append({
                "id": reg.id,
                "student_name": s_name,
                "seat_number": reg.seatNumber,
                "secret_number": reg.secretNumber or "",
                "model_code": v_code,
                "school_name": inst_name,
                "governorate": gov_name,
                "directorate": dir_name,
                "is_present": reg.isPresent,
                "is_printed": reg.is_printed,
                "printed_at": reg.printed_at.strftime("%Y-%m-%d %H:%M:%S") if reg.printed_at else None,
                "print_batch": reg.print_batch,
                "barcode_value": f"EXAM_{exam.id}_VER_{v_code}_SEAT_{reg.seatNumber}",
                "qr_value": f"{exam.uniqueCode}|{v_code}|{reg.seatNumber}|{reg.secretNumber or ''}",
            })

        return Response({
            "success": True,
            "exam": {
                "id": exam.id,
                "title": exam.title,
                "uniqueCode": exam.uniqueCode,
                "institution_type": exam.institution_type,
                "institution_type_display": exam.get_institution_type_display() if hasattr(exam, 'get_institution_type_display') else ("معاهد وتدريب مهني" if exam.institution_type == 'institute' else ("جامعي" if exam.institution_type == 'university' else "مدرسي")),
                "subject_name": getattr(exam.subject, 'name_ar', str(exam.subject)) if exam.subject else "",
                "year_name": exam.year.gregorian_year if (exam.year and hasattr(exam.year, 'gregorian_year')) else (str(exam.year) if exam.year else ""),
                "governorate": exam.governorate.name_ar if exam.governorate else "أمانة العاصمة",
                "directorate": exam.directorate.name_ar if exam.directorate else "السبعين",
                "created_at": exam.created_at.strftime("%Y-%m-%d %H:%M") if exam.created_at else "",
            },
            "versions": versions_details,
            "registered_students_count": total_st_count,
            "registered_students": students_list,
            "recent_submissions": recent_subs,
        })

    @action(detail=True, methods=['get'], url_path='students')
    def get_students(self, request, pk=None):
        return self._fetch_paginated_students(request, pk)

    @action(detail=True, methods=['get'], url_path='registered-students')
    def get_registered_students(self, request, pk=None):
        return self._fetch_paginated_students(request, pk)

    def _fetch_paginated_students(self, request, pk=None):
        """
        Returns registered students for a specific exam with full backend pagination,
        search, version filtering, and school filtering.
        """
        try:
            exam = Exam.objects.get(pk=pk, is_deleted=False)
        except Exam.DoesNotExist:
            return Response({"success": False, "message": "الاختبار غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        registrations = StudentExamRegistration.objects.filter(
            examVersion__exam=exam,
            is_deleted=False
        ).select_related(
            'student_profile',
            'student_profile__organization',
            'student_profile__directorate',
            'student',
            'examVersion'
        ).defer('is_printed', 'printed_at', 'print_batch')

        # 1. Filter by Model Code / Version
        version = request.query_params.get('version') or request.query_params.get('model_code') or request.query_params.get('versionCode')
        if version and version != 'all':
            registrations = registrations.filter(examVersion__versionCode=version)

        # 2. Filter by School / Organization
        school = request.query_params.get('school') or request.query_params.get('school_name')
        if school and school != 'all':
            registrations = registrations.filter(
                Q(student_profile__organization__name_ar=school) |
                Q(student_profile__organization__name_en=school)
            )

        # 3. Search query
        search = request.query_params.get('search')
        if search and search.strip():
            s = search.strip()
            registrations = registrations.filter(
                Q(seatNumber__icontains=s) |
                Q(secretNumber__icontains=s) |
                Q(student_profile__name_ar__icontains=s) |
                Q(student_profile__name_en__icontains=s) |
                Q(student_profile__academic_number__icontains=s) |
                Q(student_profile__organization__name_ar__icontains=s) |
                Q(student_profile__directorate__name_ar__icontains=s)
            )

        # 4. Ordering
        registrations = registrations.order_by('examVersion__versionCode', 'seatNumber')

        total_students_count = registrations.count()

        # Extract available schools for dropdown filter
        schools_list = list(
            StudentExamRegistration.objects.filter(examVersion__exam=exam, is_deleted=False)
            .values_list('student_profile__organization__name_ar', flat=True)
            .exclude(student_profile__organization__name_ar__isnull=True)
            .exclude(student_profile__organization__name_ar__exact='')
            .distinct()
        )

        # 5. Pagination Parameters
        try:
            page_num = int(request.query_params.get('page', 1) or 1)
        except (ValueError, TypeError):
            page_num = 1
        try:
            page_size = int(request.query_params.get('page_size', request.query_params.get('perPage', 10)) or 10)
        except (ValueError, TypeError):
            page_size = 10

        page_size = max(1, min(page_size, 100))
        page_num = max(1, page_num)

        start = (page_num - 1) * page_size
        end = start + page_size
        paged_regs = registrations[start:end]

        students_data = []
        gov_name = exam.governorate.name_ar if exam.governorate else ""
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
            v_code = reg.examVersion.versionCode if reg.examVersion else "-"

            students_data.append({
                "id": reg.id,
                "student_name": s_name,
                "seat_number": reg.seatNumber,
                "secret_number": reg.secretNumber or "",
                "model_code": v_code,
                "school_name": inst_name,
                "governorate": gov_name,
                "directorate": dir_name,
                "is_present": reg.isPresent,
                "is_printed": reg.is_printed,
                "printed_at": reg.printed_at.strftime("%Y-%m-%d %H:%M:%S") if reg.printed_at else None,
                "print_batch": reg.print_batch,
                "barcode_value": f"EXAM_{exam.id}_VER_{v_code}_SEAT_{reg.seatNumber}",
                "qr_value": f"{exam.uniqueCode}|{v_code}|{reg.seatNumber}|{reg.secretNumber or ''}",
            })

        num_pages = max(1, (total_students_count // page_size) + (1 if total_students_count % page_size else 0))

        return Response({
            "success": True,
            "results": students_data,
            "students": students_data,
            "count": total_students_count,
            "schools": schools_list,
            "pagination": {
                "count": total_students_count,
                "num_pages": num_pages,
                "current_page": page_num,
                "page_size": page_size,
                "per_page": page_size,
                "total": total_students_count,
            }
        })

    @action(detail=True, methods=['get'], url_path='answer-keys')
    def get_all_answer_keys(self, request, pk=None):
        """
        Quick endpoint to get just the answer keys of all models for this exam.
        Returns: { "A": {"1":"A","2":"B",...}, "B": {...} }
        """
        try:
            exam = Exam.objects.get(pk=pk, is_deleted=False)
        except Exam.DoesNotExist:
            return Response({"success": False, "message": "الاختبار غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        versions = ExamVersion.objects.filter(
            exam=exam,
            is_deleted=False
        ).prefetch_related('question_orders__question__options')

        result = {}
        for v in versions:
            v_key = {}
            for qo in v.question_orders.filter(is_deleted=False).order_by('orderIndex'):
                opts = list(qo.question.options.filter(is_deleted=False))
                ans = 'A'
                for idx, opt in enumerate(opts):
                    if opt.isTrue:
                        ans = chr(65 + idx)
                        break
                v_key[str(qo.orderIndex)] = ans
            result[v.versionCode] = v_key

        return Response({
            "success": True,
            "exam_id": exam.id,
            "exam_title": exam.title,
            "keys_by_version": result
        })

    @action(detail=True, methods=['post'], url_path='seed-students')
    def seed_sample_students(self, request, pk=None):
        """
        Generate realistic sample registered students for this exam
        if none exist or when requested for testing / exam preparation.
        """
        try:
            exam = Exam.objects.get(pk=pk, is_deleted=False)
        except Exam.DoesNotExist:
            return Response({"success": False, "message": "الاختبار غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        versions = list(exam.versions.filter(is_deleted=False).order_by('versionCode'))
        if not versions:
            return Response({"success": False, "message": "يجب توليد نماذج للاختبار أولاً"}, status=status.HTTP_400_BAD_REQUEST)

        from academic.models.common.Student import Student
        from exams.models.StudentExamRegistration import StudentExamRegistration
        from django.contrib.auth import get_user_model
        User = get_user_model()

        # جلب الطلاب الفعليين المسجلين في النظام من قاعدة البيانات
        students_qs = Student.objects.filter(is_active=True).select_related('organization', 'user', 'directorate')
        if exam.institution_type:
            org_students = students_qs.filter(organization__institution_type=exam.institution_type)
            if org_students.exists():
                students_qs = org_students

        db_students = list(students_qs[:50])
        if not db_students:
            return Response({
                "success": False,
                "message": "لا يوجد طلاب مسجلين في قاعدة بيانات النظام. يرجى إضافة الطلاب من شاشة شؤون الطلاب أولاً."
            }, status=status.HTTP_400_BAD_REQUEST)

        created_count = 0
        base_seat = 418485
        for idx, student_obj in enumerate(db_students):
            version = versions[idx % len(versions)]
            user = student_obj.user
            if not user:
                username = f"std_{student_obj.academic_number}"
                user, _ = User.objects.get_or_create(
                    username=username,
                    defaults={
                        "first_name": student_obj.name_ar,
                        "fk_user_type_id": 4,
                    }
                )
                student_obj.user = user
                student_obj.save(update_fields=['user'])

            seat_no = str(base_seat + idx)
            secret_no = str(100 + idx + 1)
            reg, created = StudentExamRegistration.objects.get_or_create(
                student=user,
                examVersion=version,
                defaults={
                    "student_profile": student_obj,
                    "seatNumber": seat_no,
                    "secretNumber": secret_no,
                    "isPresent": True,
                }
            )
            if created:
                created_count += 1

        return Response({
            "success": True,
            "message": f"تم تسجيل {created_count} طالباً فعلياً من قاعدة البيانات في الاختبار بنجاح",
            "created_count": created_count,
        })

    @action(detail=True, methods=['post'], url_path='mark-printed')
    def mark_printed(self, request, pk=None):
        """
        Mark specific or all registered students as 'printed'.
        Payload: { "student_ids": [1, 2, 3], "batch_id": "BATCH_A4" }
        If student_ids is empty or 'all', marks all.
        """
        try:
            exam = Exam.objects.get(pk=pk, is_deleted=False)
        except Exam.DoesNotExist:
            return Response({"success": False, "message": "الاختبار غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        student_ids = request.data.get('student_ids', 'all')
        batch_id = request.data.get('batch_id', 'BATCH_DEFAULT')
        
        from django.utils import timezone
        now = timezone.now()

        qs = StudentExamRegistration.objects.filter(examVersion__exam=exam, is_deleted=False)
        if isinstance(student_ids, list) and student_ids:
            qs = qs.filter(id__in=student_ids)

        updated_count = qs.update(is_printed=True, printed_at=now, print_batch=batch_id)

        return Response({
            "success": True,
            "message": f"تم توثيق طباعة {updated_count} ورقة بنجاح في سجل الطباعة",
            "updated_count": updated_count
        })
