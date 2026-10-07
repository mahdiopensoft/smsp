from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
import random
import uuid
import math

from exams.models.Exam import Exam
from exams.models.ExamGenerationSetting import ExamGenerationSetting
from exams.models.ExamVersion import ExamVersion
from exams.models.ExamQuestionOrder import ExamQuestionOrder
from exams.models.StudentExamRegistration import StudentExamRegistration
from exams.models.ExamTargetScope import ExamTargetScope
from exams.models.ExamModelRegionAssignment import ExamModelRegionAssignment
from exams.models.ExamTemplate import ExamTemplate
from exams.serializers.Exam import ExamSerializer
from exams.serializers.ExamTemplate import ExamTemplateSerializer
from bank.models.Question import Question
from academic.models.common.Lesson import Lesson
from academic.models.common.Unit import Unit

class ExamCreateMVS(AllMVS):
    """
    Dedicated ModelViewSet for Exam Creation Wizard.
    Endpoint: /api/exams/exam-create/
    Used by: ExamCreateView.vue
    """
    queryset = Exam.objects.select_related('subject', 'year', 'examSchedule').prefetch_related('versions')
    serializer_class = ExamSerializer

    # ═══════════════════════════════════════════════════════════
    # Helper: Build base candidate queryset with exclusions
    # ═══════════════════════════════════════════════════════════
    def _build_candidate_qs(self, data, blueprint):
        """Build the base candidate questions queryset with all filters applied."""
        subject_id = data.get('subject') or data.get('subjectId')
        inst_type = data.get('institution_type')
        semester_subject_id = data.get('semesterSubject') or data.get('semesterSubjectId')
        institute_subject_id = data.get('instituteSubject') or data.get('instituteSubjectId')
        class_track_id = data.get('classTrack') or data.get('classTrackId')
        active_unit_ids = [u.get('id') for u in blueprint.get('units', []) if u.get('percentage', 0) > 0]

        candidate_qs = Question.objects.filter(
            status='معتمد',
            is_deleted=False
        )

        if inst_type and inst_type != 'all':
            candidate_qs = candidate_qs.filter(institution_type=inst_type)

        if active_unit_ids:
            candidate_qs = candidate_qs.filter(lesson__unit_id__in=active_unit_ids)
        elif semester_subject_id:
            candidate_qs = candidate_qs.filter(lesson__unit__semester_subject_id=semester_subject_id)
        elif institute_subject_id:
            candidate_qs = candidate_qs.filter(lesson__subject_id=institute_subject_id)
        elif class_track_id and subject_id:
            candidate_qs = candidate_qs.filter(
                lesson__unit__class_subject__class_track_id=class_track_id,
                lesson__unit__class_subject__subject_id=subject_id
            )
        elif subject_id:
            from django.db.models import Q
            candidate_qs = candidate_qs.filter(
                Q(lesson__unit__class_subject__subject_id=subject_id) |
                Q(lesson__unit__semester_subject__fk_subject_id=subject_id) |
                Q(lesson__subject_id=subject_id)
            )

        # Exclude questions from omitted/dropped curriculum units and lessons
        year_id = data.get('year') or data.get('yearId')
        if not year_id:
            from academic.models.common.AcademicYear import AcademicYear
            curr_year = AcademicYear.objects.filter(is_current=True, is_deleted=False).first() or AcademicYear.objects.filter(is_active=True, is_deleted=False).first()
            if curr_year:
                year_id = curr_year.id

        if year_id:
            from exams.models.CurriculumExclusion import CurriculumExclusion
            excl_qs = CurriculumExclusion.objects.filter(
                academic_year_id=year_id,
                is_active=True,
                is_deleted=False
            )
            if inst_type and inst_type != 'all':
                excl_qs = excl_qs.filter(institution_type=inst_type)
            
            ex_unit_ids = list(excl_qs.filter(exclusion_type='unit', unit__isnull=False).values_list('unit_id', flat=True))
            ex_lesson_ids = list(excl_qs.filter(exclusion_type='lesson', lesson__isnull=False).values_list('lesson_id', flat=True))
            if ex_unit_ids:
                unit_lesson_ids = list(Lesson.objects.filter(unit_id__in=ex_unit_ids).values_list('id', flat=True))
                ex_lesson_ids.extend(unit_lesson_ids)
                candidate_qs = candidate_qs.exclude(lesson__unit_id__in=ex_unit_ids)
            if ex_lesson_ids:
                candidate_qs = candidate_qs.exclude(lesson_id__in=ex_lesson_ids)

        # Exclude previously used questions if requested
        exclude_previously_used = data.get('exclude_previously_used', False)
        if exclude_previously_used and subject_id and year_id:
            used_question_ids = list(
                ExamQuestionOrder.objects.filter(
                    examVersion__exam__subject_id=subject_id,
                    examVersion__exam__year_id=year_id,
                    is_deleted=False
                ).values_list('question_id', flat=True).distinct()
            )
            if used_question_ids:
                candidate_qs = candidate_qs.exclude(id__in=used_question_ids)

        return candidate_qs, year_id

    # ═══════════════════════════════════════════════════════════
    # Helper: Resolve subject_id from various sources
    # ═══════════════════════════════════════════════════════════
    def _resolve_subject_id(self, data, blueprint):
        """Resolve the actual subject_id from the request data."""
        subject_id = data.get('subject') or data.get('subjectId')
        inst_type = data.get('institution_type') or 'school'
        semester_subject_id = data.get('semesterSubject') or data.get('semesterSubjectId')
        institute_subject_id = data.get('instituteSubject') or data.get('instituteSubjectId')
        schedule_id = data.get('examSchedule') or data.get('examScheduleId')

        # Resolve from institute subject
        if inst_type == 'institute' and institute_subject_id:
            from academic.models.institutes.InstituteSubject import InstituteSubject
            from academic.models.common.Subject import Subject
            try:
                inst_sub = InstituteSubject.objects.get(id=institute_subject_id)
                sub_match = Subject.objects.filter(name_ar=inst_sub.name_ar).first()
                if not sub_match:
                    sub_match = Subject.objects.create(
                        name_ar=inst_sub.name_ar,
                        name_en=inst_sub.name_en or inst_sub.name_ar,
                        subject_code=inst_sub.subject_code or f"INST_{inst_sub.id}"
                    )
                subject_id = sub_match.id
            except Exception:
                pass

        # Resolve from semester subject
        if not subject_id and semester_subject_id:
            from academic.models.universities.UniversitySemesterSubject import UniversitySemesterSubject as SemesterSubject
            try:
                ss = SemesterSubject.objects.get(id=semester_subject_id)
                subject_id = ss.fk_subject_id
            except Exception:
                pass

        # Resolve from schedule
        if schedule_id:
            from exams.models.ExamSchedule import ExamSchedule
            try:
                esch = ExamSchedule.objects.get(id=schedule_id)
                if not subject_id and esch.subject_id:
                    subject_id = esch.subject_id
            except Exception:
                pass

        # Resolve from active units in blueprint
        active_unit_ids = [u.get('id') for u in blueprint.get('units', []) if u.get('percentage', 0) > 0]
        if not subject_id and active_unit_ids:
            u = Unit.objects.filter(id__in=active_unit_ids).select_related('class_subject', 'semester_subject').first()
            if u:
                if u.class_subject_id and u.class_subject:
                    subject_id = u.class_subject.subject_id
                elif u.semester_subject_id and u.semester_subject:
                    subject_id = u.semester_subject.fk_subject_id
                elif getattr(u, 'subject_id', None):
                    subject_id = u.subject_id

        return subject_id

    # ═══════════════════════════════════════════════════════════
    # Helper: Resolve year_id
    # ═══════════════════════════════════════════════════════════
    def _resolve_year_id(self, data):
        """Resolve the academic year_id."""
        year_id = data.get('year') or data.get('yearId')
        schedule_id = data.get('examSchedule') or data.get('examScheduleId')

        if schedule_id and not year_id:
            from exams.models.ExamSchedule import ExamSchedule
            try:
                esch = ExamSchedule.objects.get(id=schedule_id)
                if hasattr(esch, 'year_id') and esch.year_id:
                    year_id = esch.year_id
            except Exception:
                pass

        if not year_id:
            from academic.models.common.AcademicYear import AcademicYear
            curr_year = AcademicYear.objects.filter(is_current=True, is_deleted=False).first()
            if not curr_year:
                curr_year = AcademicYear.objects.filter(is_active=True, is_deleted=False).first()
            if not curr_year:
                curr_year = AcademicYear.objects.first()
            if curr_year:
                year_id = curr_year.id

        return year_id

    # ═══════════════════════════════════════════════════════════
    # Helper: Normalize scope & region assignment entries
    # ═══════════════════════════════════════════════════════════
    def _normalize_scope_entry(self, entry, default_level):
        scope_level = entry.get('scope_level', default_level)
        gov_id = entry.get('governorate_id') or entry.get('governorate')
        dir_id = entry.get('directorate_id') or entry.get('directorate')
        org_id = entry.get('organization_id') or entry.get('organization')
        country_id = entry.get('country_id') or entry.get('country')
        region_id = entry.get('region_id') or entry.get('region')

        try:
            from OpenSoftCoreV41.common.models.Branch import Organization
            from OpenSoftCoreV41.common.models.Directorate import Directorate
            from OpenSoftCoreV41.common.models.Governorate import Governorate

            if scope_level == 'directorate' and dir_id:
                if not Directorate.objects.filter(id=dir_id).exists():
                    org = Organization.objects.filter(id=dir_id).first()
                    if org:
                        org_id = org.id
                        dir_id = org.fk_directorate_id
                        if not gov_id:
                            gov_id = org.fk_governorate_id
            elif scope_level == 'governorate' and gov_id:
                if not Governorate.objects.filter(id=gov_id).exists():
                    org = Organization.objects.filter(id=gov_id).first()
                    if org:
                        org_id = org.id
                        gov_id = org.fk_governorate_id
        except Exception:
            pass

        return {
            'scope_level': scope_level,
            'country_id': country_id,
            'governorate_id': gov_id,
            'directorate_id': dir_id,
            'region_id': region_id,
            'organization_id': org_id,
        }


    # ═══════════════════════════════════════════════════════════
    # Helper: Select questions by difficulty distribution
    # ═══════════════════════════════════════════════════════════
    def _select_questions_by_difficulty(self, candidate_questions, questions_count, difficulty_dist):
        """
        Select questions matching a specific difficulty distribution.
        difficulty_dist: {'easy': 60, 'medium': 30, 'hard': 10}
        """
        easy_pct = difficulty_dist.get('easy', 0)
        medium_pct = difficulty_dist.get('medium', 0)
        hard_pct = difficulty_dist.get('hard', 0)

        easy_req = round(questions_count * easy_pct / 100)
        medium_req = round(questions_count * medium_pct / 100)
        hard_req = round(questions_count * hard_pct / 100)

        # Adjust rounding
        total_req = easy_req + medium_req + hard_req
        if total_req < questions_count:
            medium_req += (questions_count - total_req)
        elif total_req > questions_count:
            medium_req -= (total_req - questions_count)

        easy_pool = [q for q in candidate_questions if q.difficulty == 1]
        medium_pool = [q for q in candidate_questions if q.difficulty == 2]
        hard_pool = [q for q in candidate_questions if q.difficulty == 3]

        random.shuffle(easy_pool)
        random.shuffle(medium_pool)
        random.shuffle(hard_pool)

        selected = []
        selected.extend(easy_pool[:easy_req])
        selected.extend(medium_pool[:medium_req])
        selected.extend(hard_pool[:hard_req])

        # Fill shortage from any pool
        if len(selected) < questions_count:
            remaining_pool = [q for q in candidate_questions if q not in selected]
            random.shuffle(remaining_pool)
            selected.extend(remaining_pool[:questions_count - len(selected)])

        return selected

    def _is_tf(self, q):
        t = str(getattr(q, 'questionType', '') or '').lower()
        return 'true' in t or 'false' in t or 'صح' in t or 'خطأ' in t

    def _order_questions_by_section(self, questions):
        """
        Groups questions by section: True/False first, then MCQ/others.
        Shuffles questions within each section independently to maintain
        strict ministerial examination standards (Part 1: T/F, Part 2: MCQ)
        and ensure 100% synchronization with OMR bubble sheet layouts.
        """
        tf_list = [q for q in questions if self._is_tf(q)]
        mcq_list = [q for q in questions if not self._is_tf(q)]
        random.shuffle(tf_list)
        random.shuffle(mcq_list)
        return tf_list + mcq_list

    # ═══════════════════════════════════════════════════════════
    # Helper: Auto-register students by classTrack + geographic scope
    # ═══════════════════════════════════════════════════════════
    def _auto_register_students(self, exam, created_versions, class_track_id,
                                 target_scope_level, target_scopes_data,
                                 governorate_id, directorate_id, region_id):
        """
        Find all active students matching the class_track and geographic scope,
        then register them into exam versions in round-robin distribution.
        Returns the count of registered students.
        """
        from academic.models.common.Student import Student
        from academic.models.schools.SchoolSection import SchoolSection

        # Build student queryset filtered by class_track
        student_qs = Student.objects.filter(
            is_active=True,
            is_deleted=False,
            class_track_id=class_track_id
        )

        # Apply geographic filters based on target scope
        if target_scope_level == 'all':
            # No geographic filtering - include all students in this class_track
            pass
        elif target_scope_level == 'school' and target_scopes_data:
            # Filter by specific school organizations
            raw_org_ids = [s.get('organization_id') or s.get('organization') for s in target_scopes_data if s.get('organization_id') or s.get('organization')]
            if raw_org_ids:
                try:
                    from OpenSoftCoreV41.common.models.Branch import Organization as BranchOrg
                    from academic.models.common.Organization import Organization as AcademicOrg
                    branch_names = list(BranchOrg.objects.filter(id__in=raw_org_ids).values_list('name_ar', flat=True))
                    academic_ids = list(AcademicOrg.objects.filter(name_ar__in=branch_names).values_list('id', flat=True))
                    all_org_ids = list(set([int(x) for x in raw_org_ids if str(x).isdigit()] + academic_ids))
                    student_qs = student_qs.filter(organization_id__in=all_org_ids)
                except Exception:
                    student_qs = student_qs.filter(organization_id__in=raw_org_ids)
        elif target_scope_level == 'directorate' and target_scopes_data:
            # Filter by directorate(s)
            raw_dir_ids = [s.get('directorate_id') or s.get('directorate') for s in target_scopes_data if s.get('directorate_id') or s.get('directorate')]
            if raw_dir_ids:
                try:
                    from OpenSoftCoreV41.common.models.Branch import Organization as BranchOrg
                    branch_dir_ids = list(BranchOrg.objects.filter(id__in=raw_dir_ids, fk_directorate__isnull=False).values_list('fk_directorate_id', flat=True))
                    all_dir_ids = list(set([int(x) for x in raw_dir_ids if str(x).isdigit()] + branch_dir_ids))
                    student_qs = student_qs.filter(directorate_id__in=all_dir_ids)
                except Exception:
                    student_qs = student_qs.filter(directorate_id__in=raw_dir_ids)
        elif target_scope_level == 'governorate' and target_scopes_data:
            # Filter by governorate(s)
            raw_gov_ids = [s.get('governorate_id') or s.get('governorate') for s in target_scopes_data if s.get('governorate_id') or s.get('governorate')]
            if raw_gov_ids:
                try:
                    from OpenSoftCoreV41.common.models.Branch import Organization as BranchOrg
                    branch_gov_ids = list(BranchOrg.objects.filter(id__in=raw_gov_ids, fk_governorate__isnull=False).values_list('fk_governorate_id', flat=True))
                    all_gov_ids = list(set([int(x) for x in raw_gov_ids if str(x).isdigit()] + branch_gov_ids))
                    student_qs = student_qs.filter(directorate__governorate_id__in=all_gov_ids)
                except Exception:
                    from django.db.models import Q
                    student_qs = student_qs.filter(
                        Q(directorate__governorate_id__in=raw_gov_ids) |
                        Q(organization__parent__fk_governorate_id__in=raw_gov_ids)
                    )
        else:
            # Fallback: use exam-level geographic fields
            if directorate_id:
                student_qs = student_qs.filter(directorate_id=directorate_id)
            elif governorate_id:
                student_qs = student_qs.filter(directorate__governorate_id=governorate_id)

        students = list(student_qs.order_by('academic_number'))
        if not students:
            return 0

        # Distribute students across versions in round-robin
        registrations_to_create = []
        num_versions = len(created_versions)

        for idx, student in enumerate(students):
            version = created_versions[idx % num_versions]
            seat_number = f"{exam.uniqueCode}-{str(idx + 1).zfill(4)}"
            secret_number = f"S{uuid.uuid4().hex[:6].upper()}"

            user_id = student.user_id
            if not user_id:
                try:
                    from django.contrib.auth import get_user_model
                    from OpenSoftCoreV41.usermanager.models.UserType import UserType
                    User = get_user_model()
                    ut = UserType.objects.filter(name_en__iexact="student").first() or UserType.objects.first()
                    username = f"std_{student.academic_number or student.id}"
                    u_defaults = {
                        'first_name': (student.name_ar or 'طالب')[:30],
                        'is_active': True
                    }
                    if ut:
                        u_defaults['fk_user_type_id'] = ut.id
                    u, _ = User.objects.get_or_create(username=username, defaults=u_defaults)
                    student.user = u
                    student.save(update_fields=['user'])
                    user_id = u.id
                except Exception:
                    pass

            registrations_to_create.append(StudentExamRegistration(
                student_id=user_id,
                student_profile=student,
                examVersion=version,
                seatNumber=seat_number,
                secretNumber=secret_number,
                isPresent=False,
            ))

        if registrations_to_create:
            StudentExamRegistration.objects.bulk_create(
                registrations_to_create,
                ignore_conflicts=True  # Skip if student already registered
            )

        return len(registrations_to_create)

    # ═══════════════════════════════════════════════════════════
    # CHECK SHORTAGE
    # ═══════════════════════════════════════════════════════════
    @action(detail=False, methods=['post'], url_path='check-shortage')
    def check_shortage(self, request):
        """
        Check if there are enough approved questions in the database
        matching the blueprint constraints.
        """
        data = request.data
        questions_count = int(data.get('questionsCount', 40))
        blueprint = data.get('blueprint', {})

        candidate_qs, year_id = self._build_candidate_qs(data, blueprint)
        candidate_questions = list(candidate_qs)
        total_avail = len(candidate_questions)

        # Requirements
        types_bp = blueprint.get('types', [])
        mcq_pct = next((t.get('percentage', 0) for t in types_bp if t.get('value') == 'mcq'), 0)
        tf_pct = next((t.get('percentage', 0) for t in types_bp if t.get('value') == 'tf'), 0)

        mcq_req = round(questions_count * mcq_pct / 100)
        tf_req = round(questions_count * tf_pct / 100)

        diff_bp = blueprint.get('difficulty', [])
        easy_pct = next((d.get('percentage', 0) for d in diff_bp if d.get('name') == 'سهل'), 0)
        med_pct = next((d.get('percentage', 0) for d in diff_bp if d.get('name') == 'متوسط'), 0)
        hard_pct = next((d.get('percentage', 0) for d in diff_bp if d.get('name') == 'صعب'), 0)

        easy_req = round(questions_count * easy_pct / 100)
        med_req = round(questions_count * med_pct / 100)
        hard_req = round(questions_count * hard_pct / 100)

        # Availability
        mcq_avail = sum(1 for q in candidate_questions if q.questionType in ['Single Choice', 'Multiple Choice'])
        tf_avail = sum(1 for q in candidate_questions if q.questionType == 'True/False')
        easy_avail = sum(1 for q in candidate_questions if q.difficulty == 1)
        med_avail = sum(1 for q in candidate_questions if q.difficulty == 2)
        hard_avail = sum(1 for q in candidate_questions if q.difficulty == 3)

        # Check model groups availability for advanced mode
        models_mode = data.get('models_mode', 'uniform')
        model_groups = data.get('model_groups', [])
        groups_shortage = []

        if models_mode == 'advanced' and model_groups:
            for idx, group in enumerate(model_groups):
                g_dist = group.get('difficulty_distribution', {})
                g_easy_req = round(questions_count * g_dist.get('easy', 0) / 100)
                g_med_req = round(questions_count * g_dist.get('medium', 0) / 100)
                g_hard_req = round(questions_count * g_dist.get('hard', 0) / 100)
                
                g_shortage = {
                    'group_index': idx,
                    'difficulty_profile': group.get('difficulty_profile', 'mixed'),
                    'easy': {'required': g_easy_req, 'available': easy_avail, 'missing': max(0, g_easy_req - easy_avail)},
                    'medium': {'required': g_med_req, 'available': med_avail, 'missing': max(0, g_med_req - med_avail)},
                    'hard': {'required': g_hard_req, 'available': hard_avail, 'missing': max(0, g_hard_req - hard_avail)},
                }
                groups_shortage.append(g_shortage)

        report = {
            "mcq": {"required": mcq_req, "available": mcq_avail, "missing": max(0, mcq_req - mcq_avail)},
            "tf": {"required": tf_req, "available": tf_avail, "missing": max(0, tf_req - tf_avail)},
            "easy": {"required": easy_req, "available": easy_avail, "missing": max(0, easy_req - easy_avail)},
            "medium": {"required": med_req, "available": med_avail, "missing": max(0, med_req - med_avail)},
            "hard": {"required": hard_req, "available": hard_avail, "missing": max(0, hard_req - hard_avail)},
            "totalMissing": max(0, questions_count - total_avail),
            "totalAvailable": total_avail,
            "totalRequired": questions_count,
            "groupsShortage": groups_shortage,
        }

        has_shortage = (report["mcq"]["missing"] > 0 or report["tf"]["missing"] > 0 or report["totalMissing"] > 0)

        return Response({
            "success": True,
            "hasShortage": has_shortage,
            "report": report
        })

    # ═══════════════════════════════════════════════════════════
    # GENERATE EXAM
    # ═══════════════════════════════════════════════════════════
    @action(detail=False, methods=['post'], url_path='generate')
    def generate(self, request):
        """
        Full Atomic Exam Generation Sequence.
        Supports both uniform mode (same questions, different order) and
        advanced mode (different difficulty distributions per model group).
        """
        data = request.data
        title = data.get('title') or 'اختبار جديد'
        inst_type = data.get('institution_type') or 'school'
        schedule_id = data.get('examSchedule') or data.get('examScheduleId')
        country_id = data.get('country') or data.get('countryId')
        governorate_id = data.get('governorate') or data.get('governorateId')
        directorate_id = data.get('directorate') or data.get('directorateId')
        region_id = data.get('region') or data.get('regionId')
        class_track_id = data.get('classTrack') or data.get('classTrackId')

        questions_count = int(data.get('questionsCount', 40))
        models_count = int(data.get('modelsCount', 4))
        blueprint = data.get('blueprint', {})

        # Advanced options
        bloom_enabled = data.get('bloom_enabled', True)
        models_mode = data.get('models_mode', 'uniform')
        model_groups = data.get('model_groups', [])
        target_scopes_data = data.get('target_scopes', [])
        target_scope_level = data.get('target_scope_level', 'all')
        model_region_assignments = data.get('model_region_assignments', [])
        exclude_previously_used = data.get('exclude_previously_used', False)

        # Resolve IDs
        subject_id = self._resolve_subject_id(data, blueprint)
        year_id = self._resolve_year_id(data)

        if not subject_id or not year_id:
            missing_items = []
            if not subject_id:
                missing_items.append("المادة الدراسية / المقرر")
            if not year_id:
                missing_items.append("السنة الأكاديمية")
            return Response({
                "success": False,
                "message": f"يجب تحديد {' و '.join(missing_items)} للاختبار"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Build candidate questions
        candidate_qs, _ = self._build_candidate_qs(data, blueprint)
        candidate_qs = candidate_qs.select_related('lesson__unit').prefetch_related('options')
        candidate_questions = list(candidate_qs)

        if not candidate_questions:
            return Response({
                "success": False,
                "message": "لا يوجد أسئلة معتمدة مطابقة للمحددات المختارة في بنك الأسئلة"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # 1. Create Generation Setting
                diff_bp = blueprint.get('difficulty', [])
                bloom_bp = blueprint.get('bloom', [])

                setting = ExamGenerationSetting.objects.create(
                    name=f"{title} - إعدادات",
                    easyPercentage=next((d.get('percentage', 0) for d in diff_bp if d.get('name') == 'سهل'), 30),
                    mediumPercentage=next((d.get('percentage', 0) for d in diff_bp if d.get('name') == 'متوسط'), 50),
                    hardPercentage=next((d.get('percentage', 0) for d in diff_bp if d.get('name') == 'صعب'), 20),
                    rememberPercentage=next((b.get('percentage', 0) for b in bloom_bp if b.get('name') == 'تذكر'), 20) if bloom_enabled else 0,
                    understandPercentage=next((b.get('percentage', 0) for b in bloom_bp if b.get('name') == 'فهم'), 25) if bloom_enabled else 0,
                    applyPercentage=next((b.get('percentage', 0) for b in bloom_bp if b.get('name') == 'تطبيق'), 25) if bloom_enabled else 0,
                    analyzePercentage=next((b.get('percentage', 0) for b in bloom_bp if b.get('name') == 'تحليل'), 15) if bloom_enabled else 0,
                    evaluatePercentage=next((b.get('percentage', 0) for b in bloom_bp if b.get('name') == 'تقويم'), 10) if bloom_enabled else 0,
                    createPercentage=next((b.get('percentage', 0) for b in bloom_bp if b.get('name') == 'إبداع'), 5) if bloom_enabled else 0,
                )

                # 2. Create Main Exam
                exam_geo = self._normalize_scope_entry({
                    'country_id': country_id,
                    'governorate_id': governorate_id,
                    'directorate_id': directorate_id,
                    'region_id': region_id,
                }, target_scope_level)

                unique_code = f"EXAM-{uuid.uuid4().hex[:8].upper()}"
                exam = Exam.objects.create(
                    title=title,
                    institution_type=inst_type,
                    uniqueCode=unique_code,
                    examGenerationSetting=setting,
                    year_id=year_id,
                    subject_id=subject_id,
                    examSchedule_id=schedule_id,
                    country_id=exam_geo.get('country_id'),
                    governorate_id=exam_geo.get('governorate_id'),
                    directorate_id=exam_geo.get('directorate_id'),
                    region_id=exam_geo.get('region_id'),
                    class_track_id=class_track_id,
                    bloom_enabled=bloom_enabled,
                    models_mode=models_mode,
                    model_groups_config=model_groups if models_mode == 'advanced' else None,
                    target_scope_level=target_scope_level,
                    exclude_previously_used=exclude_previously_used,
                )

                # 3. Save Target Scopes
                if target_scopes_data:
                    scopes_to_create = []
                    for scope in target_scopes_data:
                        norm = self._normalize_scope_entry(scope, target_scope_level)
                        scopes_to_create.append(ExamTargetScope(
                            exam=exam,
                            scope_level=norm.get('scope_level', target_scope_level),
                            country_id=norm.get('country_id'),
                            governorate_id=norm.get('governorate_id'),
                            directorate_id=norm.get('directorate_id'),
                            region_id=norm.get('region_id'),
                            organization_id=norm.get('organization_id'),
                        ))
                    if scopes_to_create:
                        ExamTargetScope.objects.bulk_create(scopes_to_create)

                # 4. Create Models (Versions) & Question Orders
                all_orders_to_create = []
                created_versions = []

                if models_mode == 'advanced' and model_groups:
                    # ═══ ADVANCED MODE: Different difficulty per group ═══
                    version_letter_idx = 0
                    for group_idx, group in enumerate(model_groups):
                        group_count = int(group.get('count', 1))
                        difficulty_profile = group.get('difficulty_profile', 'mixed')
                        difficulty_dist = group.get('difficulty_distribution', {'easy': 30, 'medium': 50, 'hard': 20})

                        # Select questions for this difficulty profile
                        group_questions = self._select_questions_by_difficulty(
                            candidate_questions, questions_count, difficulty_dist
                        )

                        for m in range(group_count):
                            version_code = chr(65 + version_letter_idx)  # A, B, C...
                            version_letter_idx += 1

                            version = ExamVersion.objects.create(
                                exam=exam,
                                versionCode=version_code,
                                model_group_index=group_idx,
                                difficulty_profile=difficulty_profile,
                                difficulty_distribution=difficulty_dist,
                            )
                            created_versions.append(version)

                            # Order questions by section (True/False 1..N, MCQ N+1..total) with intra-section shuffle
                            shuffled_questions = self._order_questions_by_section(group_questions)

                            for idx, q in enumerate(shuffled_questions):
                                all_orders_to_create.append(ExamQuestionOrder(
                                    examVersion=version,
                                    question=q,
                                    orderIndex=idx + 1
                                ))
                else:
                    # ═══ UNIFORM MODE: Same questions, different order ═══
                    if len(candidate_questions) > questions_count:
                        tf_cands = [q for q in candidate_questions if self._is_tf(q)]
                        mcq_cands = [q for q in candidate_questions if not self._is_tf(q)]
                        random.shuffle(tf_cands)
                        random.shuffle(mcq_cands)
                        combined = tf_cands + mcq_cands
                        selected_questions = combined[:questions_count]
                    else:
                        selected_questions = candidate_questions

                    for m in range(models_count):
                        version_code = chr(65 + m)  # A, B, C, D...
                        version = ExamVersion.objects.create(
                            exam=exam,
                            versionCode=version_code,
                            model_group_index=0,
                            difficulty_profile='mixed',
                        )
                        created_versions.append(version)

                        # Order questions by section (True/False 1..N, MCQ N+1..total) with intra-section shuffle
                        shuffled_questions = self._order_questions_by_section(selected_questions)

                        for idx, q in enumerate(shuffled_questions):
                            all_orders_to_create.append(ExamQuestionOrder(
                                examVersion=version,
                                question=q,
                                orderIndex=idx + 1
                            ))

                if all_orders_to_create:
                    ExamQuestionOrder.objects.bulk_create(all_orders_to_create)

                # 5. Save Model-Region Assignments
                if model_region_assignments:
                    assignments_to_create = []
                    for assignment in model_region_assignments:
                        norm = self._normalize_scope_entry(assignment, target_scope_level)
                        assignments_to_create.append(ExamModelRegionAssignment(
                            exam=exam,
                            model_group_index=assignment.get('model_group_index', 0),
                            difficulty_profile=assignment.get('difficulty_profile', 'mixed'),
                            scope_level=norm.get('scope_level', 'governorate'),
                            governorate_id=norm.get('governorate_id'),
                            directorate_id=norm.get('directorate_id'),
                            region_id=norm.get('region_id'),
                            organization_id=norm.get('organization_id'),
                        ))
                    if assignments_to_create:
                        ExamModelRegionAssignment.objects.bulk_create(assignments_to_create)

                # ═══════════════════════════════════════════════════════════
                # 6. Auto-Register Students Based on ClassTrack + Geographic Scope
                # ═══════════════════════════════════════════════════════════
                registered_students_count = 0
                if created_versions and class_track_id:
                    registered_students_count = self._auto_register_students(
                        exam, created_versions, class_track_id,
                        target_scope_level, target_scopes_data,
                        governorate_id, directorate_id, region_id
                    )

                # Calculate total models and questions
                total_models = len(created_versions)
                total_questions = len(set(q.id for q in candidate_questions[:questions_count])) if models_mode == 'uniform' else questions_count

                # Serialize full result
                serializer = ExamSerializer(exam)
                return Response({
                    "success": True,
                    "message": f"تم توليد الاختبار بنجاح مع {total_models} نماذج و {total_questions} سؤالاً و {registered_students_count} طالب مسجل",
                    "data": serializer.data,
                    "examId": exam.id,
                    "registeredStudentsCount": registered_students_count
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "success": False,
                "message": f"حدث خطأ أثناء توليد الاختبار: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)

    # ═══════════════════════════════════════════════════════════
    # TEMPLATES Management
    # ═══════════════════════════════════════════════════════════
    @action(detail=False, methods=['get'], url_path='templates')
    def list_templates(self, request):
        """List all saved exam templates."""
        inst_type = request.query_params.get('institution_type')
        qs = ExamTemplate.objects.filter(is_deleted=False)
        if inst_type:
            qs = qs.filter(institution_type=inst_type)
        serializer = ExamTemplateSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='save-template')
    def save_template(self, request):
        """Save current exam configuration as a reusable template."""
        data = request.data
        name = data.get('name', 'قالب جديد')
        description = data.get('description', '')
        institution_type = data.get('institution_type', 'school')
        config = data.get('config', {})

        template = ExamTemplate.objects.create(
            name=name,
            description=description,
            institution_type=institution_type,
            config_json=config,
        )

        serializer = ExamTemplateSerializer(template)
        return Response({
            "success": True,
            "message": "تم حفظ القالب بنجاح",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'], url_path='delete-template/(?P<template_id>[^/.]+)')
    def delete_template(self, request, template_id=None):
        """Delete a saved template."""
        try:
            template = ExamTemplate.objects.get(id=template_id, is_deleted=False)
            template.is_deleted = True
            template.save()
            return Response({"success": True, "message": "تم حذف القالب"})
        except ExamTemplate.DoesNotExist:
            return Response({"success": False, "message": "القالب غير موجود"}, status=status.HTTP_404_NOT_FOUND)
