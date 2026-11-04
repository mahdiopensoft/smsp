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
from exams.serializers.Exam import ExamSerializer
from bank.models.Question import Question
from bank.models.Answer import Answer
from django.db.models import Q
from academic.models.universities.UniversityLesson import UniversityLesson as Lesson
from academic.models.universities.UniversityUnit import UniversityUnit as Unit

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
            from academic.models.universities.UniversitySubject import UniversitySubject as Subject
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
            curr_year = (
                AcademicYear.objects.filter(is_current=True, is_deleted=False).first() or
                AcademicYear.objects.filter(is_active=True, is_deleted=False).first() or
                AcademicYear.objects.filter(is_deleted=False).first()
            )
            if not curr_year:
                curr_year, _ = AcademicYear.objects.get_or_create(
                    gregorian_year="2025-2026",
                    defaults={"hijri_year": "1447", "is_active": True, "is_current": True}
                )
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

    def _select_questions_by_units_and_difficulty(self, candidate_questions, questions_count, difficulty_dist, group_units=None, group_types=None):
        """
        Select questions matching group's specific question types, unit distribution, and difficulty profile.
        """
        # If question types are specified with percentages > 0, partition by types first
        active_types = [t for t in (group_types or []) if t.get('percentage', 0) > 0]
        if active_types and len(active_types) > 0:
            type_allocations = []
            total_type_cnt = 0
            for t in active_types:
                pct = t.get('percentage', 0)
                cnt = round(questions_count * pct / 100)
                t_val = t.get('value') or t.get('id')
                type_allocations.append({'type_val': t_val, 'count': cnt})
                total_type_cnt += cnt

            # Adjust rounding
            if total_type_cnt < questions_count and type_allocations:
                type_allocations[0]['count'] += (questions_count - total_type_cnt)
            elif total_type_cnt > questions_count and type_allocations:
                diff = total_type_cnt - questions_count
                for a in type_allocations:
                    if a['count'] >= diff:
                        a['count'] -= diff
                        break

            selected = []
            selected_ids = set()

            for a in type_allocations:
                t_val = a['type_val']
                needed = a['count']
                if needed <= 0:
                    continue
                type_pool = [q for q in candidate_questions if self._match_question_type(q, t_val) and q.id not in selected_ids]
                # Apply unit and difficulty selection on this type pool
                chosen = self._select_questions_by_units_and_difficulty(
                    type_pool, needed, difficulty_dist, group_units=group_units, group_types=None
                )
                for q in chosen:
                    if q.id not in selected_ids:
                        selected.append(q)
                        selected_ids.add(q.id)

            # Fill any remaining shortage from overall pool
            if len(selected) < questions_count:
                remaining = [q for q in candidate_questions if q.id not in selected_ids]
                needed = questions_count - len(selected)
                filler = self._select_questions_by_difficulty(remaining, needed, difficulty_dist)
                for q in filler:
                    if len(selected) >= questions_count:
                        break
                    if q.id not in selected_ids:
                        selected.append(q)
                        selected_ids.add(q.id)

            return selected

        if not group_units:
            return self._select_questions_by_difficulty(candidate_questions, questions_count, difficulty_dist)

        active_units = [u for u in group_units if u.get('percentage', 0) > 0 and not u.get('isExcluded', False)]
        if not active_units:
            return self._select_questions_by_difficulty(candidate_questions, questions_count, difficulty_dist)

        allocated = []
        total_allocated = 0
        for u in active_units:
            pct = u.get('percentage', 0)
            cnt = round(questions_count * pct / 100)
            allocated.append({'unit_id': u.get('id'), 'count': cnt})
            total_allocated += cnt

        # Adjust rounding difference
        if total_allocated < questions_count and allocated:
            allocated[0]['count'] += (questions_count - total_allocated)
        elif total_allocated > questions_count and allocated:
            diff = total_allocated - questions_count
            for a in allocated:
                if a['count'] >= diff:
                    a['count'] -= diff
                    break

        unit_questions_map = {}
        for q in candidate_questions:
            uid = getattr(getattr(q, 'lesson', None), 'unit_id', None)
            if uid:
                unit_questions_map.setdefault(uid, []).append(q)

        selected = []
        selected_ids = set()

        for a in allocated:
            u_pool = unit_questions_map.get(a['unit_id'], [])
            if not u_pool or a['count'] <= 0:
                continue
            u_selected = self._select_questions_by_difficulty(u_pool, a['count'], difficulty_dist)
            for q in u_selected:
                if q.id not in selected_ids:
                    selected.append(q)
                    selected_ids.add(q.id)

        # Fill any remaining shortage from overall candidate pool
        if len(selected) < questions_count:
            remaining = [q for q in candidate_questions if q.id not in selected_ids]
            needed = questions_count - len(selected)
            filler = self._select_questions_by_difficulty(remaining, needed, difficulty_dist)
            for q in filler:
                if len(selected) >= questions_count:
                    break
                if q.id not in selected_ids:
                    selected.append(q)
                    selected_ids.add(q.id)

        return selected

    def _match_question_type(self, q, type_val):
        """Matches a question to a blueprint question type identifier."""
        t = str(getattr(q, 'questionType', '') or '').lower()
        type_val = str(type_val or '').lower()
        if type_val in ['single_choice', 'mcq', 'single choice']:
            return 'single' in t or ('mcq' in t and 'multiple' not in t) or 'فردي' in t or (not t and hasattr(q, 'options') and q.options.count() > 1)
        elif type_val in ['true_false', 'tf', 'true/false']:
            return 'true' in t or 'false' in t or 'صواب' in t or 'صح' in t or 'خطأ' in t
        elif type_val in ['multiple_choice', 'multiple choice']:
            return 'multiple' in t or 'متعدد' in t
        elif type_val in ['essay']:
            return 'essay' in t or 'مقالي' in t or 'إنشائي' in t
        elif type_val in ['fill_blanks', 'fill in the blanks']:
            return 'blank' in t or 'فراغ' in t or 'إكمال' in t
        elif type_val in ['matching']:
            return 'match' in t or 'توصيل' in t or 'مطابقة' in t or 'مزاوجة' in t
        elif type_val in ['ordering']:
            return 'order' in t or 'ترتيب' in t
        return type_val in t

    def _is_tf(self, q):
        return self._match_question_type(q, 'true_false')

    def _is_mcq(self, q):
        return self._match_question_type(q, 'single_choice') or self._match_question_type(q, 'multiple_choice')

    def _is_essay(self, q):
        return self._match_question_type(q, 'essay')

    def _resolve_question_mark(self, q, types_list):
        if types_list:
            for t in types_list:
                t_val = t.get('value') or t.get('id')
                if self._match_question_type(q, t_val):
                    m = t.get('mark')
                    if m is not None:
                        try:
                            return float(m)
                        except (ValueError, TypeError):
                            pass
        return float(getattr(q, 'defaultMark', None) or 1.0)

    def _order_questions_by_section(self, questions):
        """
        Groups questions by ministerial academic sections:
        Part 1: True / False (صح وخطأ)
        Part 2: Multiple Choice / Single Choice (اختيار من متعدد)
        Part 3: Other Objective Questions (Matching, Ordering, Fill in Blanks)
        Part 4: Essay Questions (الأسئلة المقالية)
        Shuffles questions within each section independently to maintain 100% synchronization
        with OMR bubble sheet layouts and academic best practices.
        """
        tf_list = [q for q in questions if self._is_tf(q)]
        mcq_list = [q for q in questions if not self._is_tf(q) and self._is_mcq(q)]
        essay_list = [q for q in questions if not self._is_tf(q) and not self._is_mcq(q) and self._is_essay(q)]
        other_list = [q for q in questions if q not in tf_list and q not in mcq_list and q not in essay_list]

        random.shuffle(tf_list)
        random.shuffle(mcq_list)
        random.shuffle(other_list)
        random.shuffle(essay_list)

        return tf_list + mcq_list + other_list + essay_list

    # ═══════════════════════════════════════════════════════════
    # Helper: Serialize Question for Interactive Staging
    # ═══════════════════════════════════════════════════════════
    def _serialize_question_for_staging(self, q, order_index=1, mark=1.0):
        """Serialize a Question model instance into a rich dictionary for interactive staging."""
        options_data = []
        try:
            raw_options = [opt for opt in q.options.all() if not getattr(opt, 'is_deleted', False)]
            raw_options.sort(key=lambda o: getattr(o, 'order_index', 0) if getattr(o, 'order_index', None) is not None else 0)
            for idx, opt in enumerate(raw_options):
                opt_img = None
                try:
                    if opt.image:
                        opt_img = opt.image.url
                except Exception:
                    opt_img = None

                options_data.append({
                    "id": opt.id,
                    "text": opt.text or '',
                    "isTrue": bool(opt.isTrue),
                    "image": opt_img,
                    "latex": getattr(opt, 'latex', None),
                    "order_index": getattr(opt, 'order_index', idx)
                })
        except Exception:
            options_data = []

        unit_name = 'عام'
        unit_id = None
        lesson_name = 'عام'
        lesson_id = q.lesson_id

        if q.lesson:
            lesson_name = getattr(q.lesson, 'name_ar', str(q.lesson))
            if hasattr(q.lesson, 'unit') and q.lesson.unit:
                unit_name = getattr(q.lesson.unit, 'name_ar', str(q.lesson.unit))
                unit_id = q.lesson.unit.id

        q_img = None
        try:
            if q.image:
                q_img = q.image.url
        except Exception:
            q_img = None

        return {
            "id": q.id,
            "orderIndex": order_index,
            "content": q.content or '',
            "image": q_img,
            "questionType": q.questionType or 'Single Choice',
            "difficulty": q.difficulty if q.difficulty is not None else 2,
            "bloomLevel": q.bloomLevel or 'تطبيق',
            "assignedMark": round(float(mark), 2),
            "unitId": unit_id,
            "unitName": unit_name,
            "lessonId": lesson_id,
            "lessonName": lesson_name,
            "options": options_data,
            "isTrue": bool(getattr(q, 'isTrue', False)),
            "answerText": getattr(q, 'answerText', None),
        }

    # ═══════════════════════════════════════════════════════════
    # Helper: Auto-register students by classTrack + geographic scope
    # ═══════════════════════════════════════════════════════════
    def _auto_register_students(self, exam, created_versions, class_track_id,
                                 target_scope_level, target_scopes_data,
                                 governorate_id, directorate_id, region_id,
                                 model_region_assignments=None):
        """
        Find all active students matching the class_track and geographic scope,
        then register them into exam versions in round-robin distribution,
        respecting group regional assignments when present.
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

        students = list(student_qs.select_related('directorate').order_by('academic_number'))
        if not students:
            return 0

        # Distribute students across versions
        registrations_to_create = []
        num_versions = len(created_versions)

        # Build group index -> versions mapping
        group_versions_map = {}
        for v in created_versions:
            g_idx = getattr(v, 'model_group_index', 0)
            group_versions_map.setdefault(g_idx, []).append(v)

        group_counters = {g_idx: 0 for g_idx in group_versions_map}
        global_counter = 0

        for idx, student in enumerate(students):
            assigned_group_idx = None
            if model_region_assignments:
                s_org_id = student.organization_id
                s_dir_id = student.directorate_id
                s_gov_id = getattr(student.directorate, 'governorate_id', None) if student.directorate else None

                for assign in model_region_assignments:
                    g_idx = assign.get('model_group_index', 0)
                    a_org = assign.get('organization_id') or assign.get('organization')
                    a_dir = assign.get('directorate_id') or assign.get('directorate')
                    a_gov = assign.get('governorate_id') or assign.get('governorate')

                    try:
                        if a_org and s_org_id and int(a_org) == int(s_org_id):
                            assigned_group_idx = g_idx
                            break
                        elif a_dir and s_dir_id and int(a_dir) == int(s_dir_id):
                            assigned_group_idx = g_idx
                            break
                        elif a_gov and s_gov_id and int(a_gov) == int(s_gov_id):
                            assigned_group_idx = g_idx
                            break
                    except (ValueError, TypeError):
                        pass

            if assigned_group_idx is not None and group_versions_map.get(assigned_group_idx):
                vers = group_versions_map[assigned_group_idx]
                c = group_counters[assigned_group_idx]
                version = vers[c % len(vers)]
                group_counters[assigned_group_idx] += 1
            else:
                version = created_versions[global_counter % num_versions]
                global_counter += 1
            seat_number = str(student.academic_number) if student.academic_number else f"{exam.uniqueCode}-{str(idx + 1).zfill(4)}"
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

        # Requirements for all Question Types
        types_bp = blueprint.get('types', [])
        types_breakdown = {}
        for t in types_bp:
            t_key = t.get('value') or t.get('id')
            t_pct = t.get('percentage', 0)
            req = round(questions_count * t_pct / 100)
            avail = sum(1 for q in candidate_questions if self._match_question_type(q, t_key))
            types_breakdown[t_key] = {
                'required': req,
                'available': avail,
                'missing': max(0, req - avail),
                'name': t.get('name', t_key)
            }

        mcq_req = types_breakdown.get('single_choice', {}).get('required', 0) or types_breakdown.get('mcq', {}).get('required', 0)
        tf_req = types_breakdown.get('true_false', {}).get('required', 0) or types_breakdown.get('tf', {}).get('required', 0)
        mcq_avail = types_breakdown.get('single_choice', {}).get('available', 0) or types_breakdown.get('mcq', {}).get('available', 0)
        tf_avail = types_breakdown.get('true_false', {}).get('available', 0) or types_breakdown.get('tf', {}).get('available', 0)

        diff_bp = blueprint.get('difficulty', [])
        easy_pct = next((d.get('percentage', 0) for d in diff_bp if d.get('name') == 'سهل'), 0)
        med_pct = next((d.get('percentage', 0) for d in diff_bp if d.get('name') == 'متوسط'), 0)
        hard_pct = next((d.get('percentage', 0) for d in diff_bp if d.get('name') == 'صعب'), 0)

        easy_req = round(questions_count * easy_pct / 100)
        med_req = round(questions_count * med_pct / 100)
        hard_req = round(questions_count * hard_pct / 100)

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
            "typesBreakdown": types_breakdown,
            "easy": {"required": easy_req, "available": easy_avail, "missing": max(0, easy_req - easy_avail)},
            "medium": {"required": med_req, "available": med_avail, "missing": max(0, med_req - med_avail)},
            "hard": {"required": hard_req, "available": hard_avail, "missing": max(0, hard_req - hard_avail)},
            "totalMissing": max(0, questions_count - total_avail),
            "totalAvailable": total_avail,
            "totalRequired": questions_count,
            "groupsShortage": groups_shortage,
        }

        any_type_missing = any(t.get('missing', 0) > 0 for t in types_breakdown.values())
        diff_missing = (report["easy"]["missing"] > 0 or report["medium"]["missing"] > 0 or report["hard"]["missing"] > 0)
        group_missing = any((g.get('easy', {}).get('missing', 0) > 0 or g.get('medium', {}).get('missing', 0) > 0 or g.get('hard', {}).get('missing', 0) > 0) for g in groups_shortage)

        has_shortage = bool(report["totalMissing"] > 0 or any_type_missing or diff_missing or group_missing)

        return Response({
            "success": True,
            "hasShortage": has_shortage,
            "report": report
        })

    # ═══════════════════════════════════════════════════════════
    # INTERACTIVE STAGING: Preview & Draft Selection (Step 4)
    # ═══════════════════════════════════════════════════════════
    @action(detail=False, methods=['post'], url_path='preview-staging')
    def preview_staging(self, request):
        """
        Generates an in-memory draft staging of all exam models and question selections
        WITHOUT persisting any Exam, ExamVersion, or ExamQuestionOrder records to the database.
        Allows interactive inspection, question swapping, reordering, and on-the-fly authoring.
        """
        data = request.data
        title = data.get('title') or 'اختبار جديد'
        inst_type = data.get('institution_type') or 'school'
        questions_count = int(data.get('questionsCount', 40))
        models_count = int(data.get('modelsCount', 4))
        blueprint = data.get('blueprint', {})
        bloom_enabled = bool(data.get('bloom_enabled', False))
        models_mode = data.get('models_mode', 'uniform')
        model_groups = data.get('model_groups', [])
        total_marks = float(data.get('total_marks') or data.get('totalMarks') or blueprint.get('total_marks') or 100.0)

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

        candidate_qs, _ = self._build_candidate_qs(data, blueprint)
        candidate_qs = candidate_qs.select_related('lesson__unit').prefetch_related('options')
        candidate_questions = list(candidate_qs)

        if not candidate_questions:
            return Response({
                "success": False,
                "message": "لا يوجد أسئلة معتمدة مطابقة للمحددات المختارة في بنك الأسئلة"
            }, status=status.HTTP_400_BAD_REQUEST)

        if len(candidate_questions) < questions_count:
            return Response({
                "success": False,
                "hasShortage": True,
                "message": f"عجز في رصيد الأسئلة: رصيد الأسئلة المعتمدة المتاحة ({len(candidate_questions)} سؤالاً) أقل من العدد الإجمالي المطلوب للاختبار ({questions_count} سؤالاً). لا يمكن توليد اختبار بأسئلة ناقصة."
            }, status=status.HTTP_400_BAD_REQUEST)

        staged_versions = []

        if models_mode == 'advanced' and model_groups:
            version_letter_idx = 0
            for group_idx, group in enumerate(model_groups):
                group_count = int(group.get('count', 1))
                difficulty_profile = group.get('difficulty_profile', 'mixed')
                difficulty_dist = group.get('difficulty_distribution', {'easy': 30, 'medium': 50, 'hard': 20})
                group_name = group.get('name') or f"المجموعة {group_idx + 1}"

                effective_types = group.get('types') or blueprint.get('types')
                group_questions = self._select_questions_by_units_and_difficulty(
                    candidate_questions, questions_count, difficulty_dist,
                    group_units=group.get('units'),
                    group_types=effective_types
                )

                for m in range(group_count):
                    version_code = chr(65 + version_letter_idx)
                    version_letter_idx += 1

                    shuffled_questions = self._order_questions_by_section(group_questions)
                    serialized_questions = []

                    for idx, q in enumerate(shuffled_questions):
                        q_mark = self._resolve_question_mark(q, effective_types)
                        serialized_questions.append(
                            self._serialize_question_for_staging(q, order_index=idx + 1, mark=q_mark)
                        )

                    staged_versions.append({
                        "versionCode": version_code,
                        "model_group_index": group_idx,
                        "group_name": group_name,
                        "difficulty_profile": difficulty_profile,
                        "difficulty_distribution": difficulty_dist,
                        "questions": serialized_questions
                    })
        else:
            diff_dist = {
                'easy': next((d.get('percentage', 0) for d in blueprint.get('difficulty', []) if d.get('name') == 'سهل'), 30),
                'medium': next((d.get('percentage', 0) for d in blueprint.get('difficulty', []) if d.get('name') == 'متوسط'), 50),
                'hard': next((d.get('percentage', 0) for d in blueprint.get('difficulty', []) if d.get('name') == 'صعب'), 20),
            }
            effective_types = blueprint.get('types')
            selected_questions = self._select_questions_by_units_and_difficulty(
                candidate_questions, questions_count, diff_dist,
                group_units=blueprint.get('units'),
                group_types=effective_types
            )

            for m in range(models_count):
                version_code = chr(65 + m)
                shuffled_questions = self._order_questions_by_section(selected_questions)
                serialized_questions = []

                for idx, q in enumerate(shuffled_questions):
                    q_mark = self._resolve_question_mark(q, effective_types)
                    serialized_questions.append(
                        self._serialize_question_for_staging(q, order_index=idx + 1, mark=q_mark)
                    )

                staged_versions.append({
                    "versionCode": version_code,
                    "model_group_index": 0,
                    "group_name": "المجموعة 1",
                    "difficulty_profile": 'mixed',
                    "difficulty_distribution": diff_dist,
                    "questions": serialized_questions
                })

        return Response({
            "success": True,
            "title": title,
            "total_marks": total_marks,
            "models_mode": models_mode,
            "versions": staged_versions
        })

    # ═══════════════════════════════════════════════════════════
    # FIND REPLACEMENT QUESTION FROM BANK
    # ═══════════════════════════════════════════════════════════
    @action(detail=False, methods=['post'], url_path='find-replacement')
    def find_replacement(self, request):
        """
        Finds approved candidate replacement questions from the bank
        matching the specific unit, difficulty, bloom level, and question type,
        excluding question IDs already in use in the current staging.
        """
        data = request.data
        subject_id = data.get('subjectId') or data.get('subject')
        semester_subject_id = data.get('semesterSubjectId') or data.get('semesterSubject')
        institute_subject_id = data.get('instituteSubjectId') or data.get('instituteSubject')
        inst_type = data.get('institution_type') or 'school'
        unit_id = data.get('unitId')
        difficulty = data.get('difficulty')
        bloom_level = data.get('bloomLevel')
        q_type = data.get('questionType')
        exclude_ids = data.get('excludeIds', [])
        search_query = data.get('searchQuery', '').strip()
        limit = int(data.get('limit', 15))

        qs = Question.objects.filter(status='معتمد', is_deleted=False).select_related('lesson__unit').prefetch_related('options')

        if inst_type and inst_type != 'all':
            qs = qs.filter(institution_type=inst_type)

        if unit_id:
            qs = qs.filter(lesson__unit_id=unit_id)
        elif semester_subject_id:
            qs = qs.filter(lesson__unit__semester_subject_id=semester_subject_id)
        elif institute_subject_id:
            qs = qs.filter(lesson__subject_id=institute_subject_id)
        elif subject_id:
            qs = qs.filter(
                Q(lesson__unit__class_subject__subject_id=subject_id) |
                Q(lesson__unit__semester_subject__fk_subject_id=subject_id) |
                Q(lesson__subject_id=subject_id)
            )

        if exclude_ids:
            qs = qs.exclude(id__in=exclude_ids)

        if search_query:
            qs = qs.filter(content__icontains=search_query)

        if q_type:
            if q_type in ['single_choice', 'mcq', 'Single Choice']:
                qs = qs.filter(questionType__in=['Single Choice', 'اختيار من متعدد'])
            elif q_type in ['true_false', 'tf', 'True/False']:
                qs = qs.filter(questionType__in=['True/False', 'صح وخطأ', 'صح/خطأ'])
            elif q_type in ['multiple_choice', 'Multiple Choice']:
                qs = qs.filter(questionType__in=['Multiple Choice', 'اختيارات متعددة'])
            elif q_type in ['essay', 'Essay']:
                qs = qs.filter(questionType__in=['Essay', 'مقالي'])
            elif q_type in ['fill_blanks', 'Fill in the Blanks']:
                qs = qs.filter(questionType__in=['Fill in the Blanks', 'إكمال الفراغ', 'إكمال الفراغات'])
            elif q_type in ['matching', 'Matching']:
                qs = qs.filter(questionType__in=['Matching', 'مطابقة', 'توصيل'])
            elif q_type in ['ordering', 'Ordering']:
                qs = qs.filter(questionType__in=['Ordering', 'ترتيب'])

        strict_qs = qs
        if difficulty is not None:
            try:
                strict_qs = strict_qs.filter(difficulty=int(difficulty))
            except (ValueError, TypeError):
                pass

        if bloom_level:
            strict_qs = strict_qs.filter(bloomLevel=bloom_level)

        matched_questions = list(strict_qs[:limit])
        is_relaxed = False

        if not matched_questions and difficulty is not None:
            is_relaxed = True
            matched_questions = list(qs[:limit])

        serialized = [self._serialize_question_for_staging(q) for q in matched_questions]

        return Response({
            "success": True,
            "questions": serialized,
            "total": len(serialized),
            "is_relaxed": is_relaxed
        })

    # ═══════════════════════════════════════════════════════════
    # QUICK CREATE QUESTION (ON-THE-FLY)
    # ═══════════════════════════════════════════════════════════
    @action(detail=False, methods=['post'], url_path='quick-create-question')
    def quick_create_question(self, request):
        """
        Creates a new question with options on-the-fly and adds it to the question bank,
        returning it serialized for immediate inclusion into the staged exam model.
        """
        data = request.data
        content = data.get('content', '').strip()
        q_type = data.get('questionType') or 'Single Choice'
        difficulty = int(data.get('difficulty', 2))
        bloom_level = data.get('bloomLevel') or 'تطبيق'
        default_mark = float(data.get('defaultMark', 1.0))
        unit_id = data.get('unitId')
        lesson_id = data.get('lessonId')
        inst_type = data.get('institution_type') or 'school'
        options_data = data.get('options', [])

        if not content:
            return Response({"success": False, "message": "يجب كتابة نص السؤال"}, status=status.HTTP_400_BAD_REQUEST)

        if not lesson_id and unit_id:
            lesson = Lesson.objects.filter(unit_id=unit_id, is_deleted=False).first()
            if not lesson:
                lesson = Lesson.objects.create(unit_id=unit_id, name_ar='موضوع عام')
            lesson_id = lesson.id

        if not lesson_id:
            fallback_l = Lesson.objects.filter(is_deleted=False).first()
            lesson_id = fallback_l.id if fallback_l else None

        if not lesson_id:
            return Response({"success": False, "message": "تعذر ربط السؤال بوحدة أو موضوع دراسي"}, status=status.HTTP_400_BAD_REQUEST)

        if q_type == 'single_choice':
            q_type = 'Single Choice'
        elif q_type == 'true_false':
            q_type = 'True/False'
        elif q_type == 'multiple_choice':
            q_type = 'Multiple Choice'
        elif q_type == 'essay':
            q_type = 'Essay'
        elif q_type == 'fill_blanks':
            q_type = 'Fill in the Blanks'
        elif q_type == 'matching':
            q_type = 'Matching'
        elif q_type == 'ordering':
            q_type = 'Ordering'

        created_by = request.user if request.user and request.user.is_authenticated else None

        try:
            with transaction.atomic():
                question = Question.objects.create(
                    content=content,
                    questionType=q_type,
                    difficulty=difficulty,
                    bloomLevel=bloom_level,
                    defaultMark=default_mark,
                    status='معتمد',
                    institution_type=inst_type,
                    lesson_id=lesson_id,
                    createdBy=created_by
                )

                answers_to_create = []
                for idx, opt in enumerate(options_data):
                    opt_text = opt.get('text', '').strip()
                    is_true = bool(opt.get('isTrue', False))
                    answers_to_create.append(Answer(
                        question=question,
                        text=opt_text,
                        isTrue=is_true,
                        order_index=idx
                    ))

                if answers_to_create:
                    Answer.objects.bulk_create(answers_to_create)

                fresh_q = Question.objects.select_related('lesson__unit').prefetch_related('options').get(id=question.id)
                serialized = self._serialize_question_for_staging(fresh_q, mark=default_mark)

                return Response({
                    "success": True,
                    "message": "تم إنشاء السؤال بنجاح وإدراجه في الاختبار",
                    "question": serialized
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "success": False,
                "message": f"حدث خطأ أثناء إنشاء السؤال: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)

    # ═══════════════════════════════════════════════════════════
    # GENERATE EXAM (Supports Final Staged Versions Commit)
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
        bloom_enabled = bool(data.get('bloom_enabled', False))
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
                    rememberPercentage=next((b.get('percentage', 0) for b in bloom_bp if b.get('name') == 'تذكر'), 0) if bloom_enabled else 0,
                    understandPercentage=next((b.get('percentage', 0) for b in bloom_bp if b.get('name') == 'فهم'), 0) if bloom_enabled else 0,
                    applyPercentage=next((b.get('percentage', 0) for b in bloom_bp if b.get('name') == 'تطبيق'), 0) if bloom_enabled else 0,
                    analyzePercentage=next((b.get('percentage', 0) for b in bloom_bp if b.get('name') == 'تحليل'), 0) if bloom_enabled else 0,
                    evaluatePercentage=next((b.get('percentage', 0) for b in bloom_bp if b.get('name') == 'تقويم'), 0) if bloom_enabled else 0,
                    createPercentage=next((b.get('percentage', 0) for b in bloom_bp if b.get('name') == 'إبداع'), 0) if bloom_enabled else 0,
                )

                # 2. Create Main Exam
                exam_geo = self._normalize_scope_entry({
                    'country_id': country_id,
                    'governorate_id': governorate_id,
                    'directorate_id': directorate_id,
                    'region_id': region_id,
                }, target_scope_level)

                total_marks = float(data.get('total_marks') or data.get('totalMarks') or blueprint.get('total_marks') or 100.0)
                unique_code = f"EXAM-{uuid.uuid4().hex[:8].upper()}"
                exam = Exam.objects.create(
                    title=title,
                    institution_type=inst_type,
                    uniqueCode=unique_code,
                    total_marks=total_marks,
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
                        effective_scope_lvl = scope.get('scope_level') or target_scope_level
                        norm = self._normalize_scope_entry(scope, effective_scope_lvl)
                        scopes_to_create.append(ExamTargetScope(
                            exam=exam,
                            scope_level=norm.get('scope_level', effective_scope_lvl),
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
                final_versions = data.get('final_versions')

                if final_versions and isinstance(final_versions, list) and len(final_versions) > 0:
                    # ═══ COMMITTING FINAL STAGED VERSIONS FROM STEP 4 ═══
                    for v_idx, v_data in enumerate(final_versions):
                        v_code = v_data.get('versionCode') or chr(65 + v_idx)
                        g_idx = int(v_data.get('model_group_index', 0))
                        diff_profile = v_data.get('difficulty_profile', 'mixed')
                        diff_dist = v_data.get('difficulty_distribution')

                        version = ExamVersion.objects.create(
                            exam=exam,
                            versionCode=v_code,
                            model_group_index=g_idx,
                            difficulty_profile=diff_profile,
                            difficulty_distribution=diff_dist
                        )
                        created_versions.append(version)

                        for q_idx, q_item in enumerate(v_data.get('questions', [])):
                            q_id = q_item.get('id')
                            assigned_mark = float(q_item.get('assignedMark', 1.0))
                            order_index = int(q_item.get('orderIndex', q_idx + 1))

                            all_orders_to_create.append(ExamQuestionOrder(
                                examVersion=version,
                                question_id=q_id,
                                orderIndex=order_index,
                                assigned_mark=assigned_mark
                            ))
                elif models_mode == 'advanced' and model_groups:
                    # ═══ ADVANCED MODE: Different difficulty per group ═══
                    version_letter_idx = 0
                    for group_idx, group in enumerate(model_groups):
                        group_count = int(group.get('count', 1))
                        difficulty_profile = group.get('difficulty_profile', 'mixed')
                        difficulty_dist = group.get('difficulty_distribution', {'easy': 30, 'medium': 50, 'hard': 20})

                        # Select questions for this group's difficulty profile, specific unit distribution, and question types
                        group_questions = self._select_questions_by_units_and_difficulty(
                            candidate_questions, questions_count, difficulty_dist,
                            group_units=group.get('units'),
                            group_types=group.get('types') or blueprint.get('types')
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
                            effective_types = group.get('types') or blueprint.get('types')

                            for idx, q in enumerate(shuffled_questions):
                                q_mark = self._resolve_question_mark(q, effective_types)
                                all_orders_to_create.append(ExamQuestionOrder(
                                    examVersion=version,
                                    question=q,
                                    orderIndex=idx + 1,
                                    assigned_mark=q_mark
                                ))
                else:
                    # ═══ UNIFORM MODE: Same questions, different order ═══
                    diff_dist = {
                        'easy': next((d.get('percentage', 0) for d in blueprint.get('difficulty', []) if d.get('name') == 'سهل'), 30),
                        'medium': next((d.get('percentage', 0) for d in blueprint.get('difficulty', []) if d.get('name') == 'متوسط'), 50),
                        'hard': next((d.get('percentage', 0) for d in blueprint.get('difficulty', []) if d.get('name') == 'صعب'), 20),
                    }
                    selected_questions = self._select_questions_by_units_and_difficulty(
                        candidate_questions, questions_count, diff_dist,
                        group_units=blueprint.get('units'),
                        group_types=blueprint.get('types')
                    )

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
                            q_mark = self._resolve_question_mark(q, blueprint.get('types'))
                            all_orders_to_create.append(ExamQuestionOrder(
                                examVersion=version,
                                question=q,
                                orderIndex=idx + 1,
                                assigned_mark=q_mark
                            ))

                if all_orders_to_create:
                    ExamQuestionOrder.objects.bulk_create(all_orders_to_create)

                # 5. Save Model-Region Assignments
                if model_region_assignments:
                    assignments_to_create = []
                    for assignment in model_region_assignments:
                        assign_scope_lvl = assignment.get('scope_level') or target_scope_level or 'governorate'
                        norm = self._normalize_scope_entry(assignment, assign_scope_lvl)
                        assignments_to_create.append(ExamModelRegionAssignment(
                            exam=exam,
                            model_group_index=assignment.get('model_group_index', 0),
                            difficulty_profile=assignment.get('difficulty_profile', 'mixed'),
                            scope_level=norm.get('scope_level', assign_scope_lvl),
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
                        governorate_id, directorate_id, region_id,
                        model_region_assignments=model_region_assignments
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
