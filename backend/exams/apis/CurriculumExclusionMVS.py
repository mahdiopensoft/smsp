from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from exams.models.CurriculumExclusion import CurriculumExclusion
from exams.serializers.CurriculumExclusion import CurriculumExclusionSerializer
from academic.models.common.AcademicYear import AcademicYear
from academic.models.universities.UniversityUnit import UniversityUnit
from academic.models.universities.UniversityLesson import UniversityLesson
from academic.models.schools.SchoolUnit import SchoolUnit
from academic.models.schools.SchoolLesson import SchoolLesson
from bank.models.AuditLog import AuditLog
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.db.models import Q

class CurriculumExclusionMVS(AllMVS):
    """
    Dedicated ModelViewSet for Curriculum Exclusions (المحذوفات من المنهج والمقررات).
    Endpoint: /api/exams/curriculum-exclusions/
    Allows defining omitted units and lessons per academic year for schools, universities, and institutes.
    """
    queryset = CurriculumExclusion.objects.select_related(
        'academic_year',
        'stage',
        'class_track',
        'subject',
        'class_subject',
        'class_subject__school_subject',
        'college',
        'department',
        'specialization',
        'semester_subject',
        'institute_field',
        'institute_education_system',
        'institute_specialization',
        'institute_curriculum',
        'institute_subject',
        'unit',
        'lesson',
        'createdBy'
    ).filter(is_deleted=False).order_by('-created_at')

    serializer_class = CurriculumExclusionSerializer
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]

    filterset_fields = {
        'academic_year': ['exact'],
        'institution_type': ['exact'],
        'stage': ['exact'],
        'class_track': ['exact'],
        'subject': ['exact'],
        'class_subject': ['exact'],
        'college': ['exact'],
        'department': ['exact'],
        'specialization': ['exact'],
        'semester_subject': ['exact'],
        'institute_field': ['exact'],
        'institute_education_system': ['exact'],
        'institute_specialization': ['exact'],
        'institute_curriculum': ['exact'],
        'institute_subject': ['exact'],
        'exclusion_type': ['exact'],
        'unit': ['exact'],
        'lesson': ['exact'],
        'is_active': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()
        academic_year_id = self.request.query_params.get('academic_year') or self.request.query_params.get('academic_year_id')
        if academic_year_id:
            qs = qs.filter(academic_year_id=academic_year_id)

        inst_type = self.request.query_params.get('institution_type')
        if inst_type and inst_type != 'all':
            qs = qs.filter(institution_type=inst_type)

        exclusion_type = self.request.query_params.get('exclusion_type')
        if exclusion_type and exclusion_type != 'all':
            qs = qs.filter(exclusion_type=exclusion_type)

        subject_id = self.request.query_params.get('subject_id') or self.request.query_params.get('subject')
        if subject_id:
            qs = qs.filter(
                Q(subject_id=subject_id) |
                Q(class_subject__school_subject_id=subject_id) |
                Q(semester_subject__fk_subject_id=subject_id) |
                Q(institute_subject_id=subject_id)
            )

        stage_id = self.request.query_params.get('stage_id') or self.request.query_params.get('stage')
        if stage_id:
            qs = qs.filter(stage_id=stage_id)

        class_track_id = self.request.query_params.get('class_track_id') or self.request.query_params.get('class_track')
        if class_track_id:
            qs = qs.filter(class_track_id=class_track_id)

        college_id = self.request.query_params.get('college_id') or self.request.query_params.get('college')
        if college_id:
            qs = qs.filter(college_id=college_id)

        department_id = self.request.query_params.get('department_id') or self.request.query_params.get('department')
        if department_id:
            qs = qs.filter(department_id=department_id)

        specialization_id = self.request.query_params.get('specialization_id') or self.request.query_params.get('specialization')
        if specialization_id:
            qs = qs.filter(specialization_id=specialization_id)

        semester_subject_id = self.request.query_params.get('semester_subject_id') or self.request.query_params.get('semester_subject')
        if semester_subject_id:
            qs = qs.filter(semester_subject_id=semester_subject_id)

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(reason__icontains=search) |
                Q(unit__name_ar__icontains=search) |
                Q(lesson__name_ar__icontains=search) |
                Q(subject__name_ar__icontains=search) |
                Q(class_subject__school_subject__name_ar__icontains=search)
            )

        return qs

    @action(detail=False, methods=['get'], url_path='tree-for-subject')
    def tree_for_subject(self, request):
        """
        Returns full hierarchy of Units and child Lessons for a specified subject,
        annotated with whether each unit or lesson is excluded for the given academic year.
        """
        year_id = request.query_params.get('year_id') or request.query_params.get('academic_year')
        inst_type = request.query_params.get('institution_type') or 'school'

        # 1. Resolve Academic Year
        if not year_id:
            current_year = AcademicYear.objects.filter(is_current=True, is_deleted=False).first()
            if not current_year:
                current_year = AcademicYear.objects.filter(is_active=True, is_deleted=False).first()
            if not current_year:
                current_year = AcademicYear.objects.first()
            year_id = current_year.id if current_year else None

        if not year_id:
            return Response({"success": False, "message": "يرجى تحديد العام الدراسي"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Query Units & Lessons based on institution type
        units = []
        lessons_by_unit = {}

        subject_id = request.query_params.get('subject_id') or request.query_params.get('subject')
        stage_id = request.query_params.get('stage_id') or request.query_params.get('stage')
        class_track_id = request.query_params.get('class_track_id') or request.query_params.get('class_track')
        semester_subject_id = request.query_params.get('semester_subject_id') or request.query_params.get('semester_subject')
        institute_subject_id = request.query_params.get('institute_subject_id') or request.query_params.get('institute_subject')

        if inst_type == 'school':
            school_units_qs = SchoolUnit.objects.filter(is_deleted=False)
            if class_track_id:
                school_units_qs = school_units_qs.filter(
                    Q(class_subject__class_track_id=class_track_id) |
                    Q(class_subject__isnull=True, school_subject__class_subjects__class_track_id=class_track_id)
                )
            if subject_id:
                school_units_qs = school_units_qs.filter(
                    Q(school_subject_id=subject_id) |
                    Q(class_subject__school_subject_id=subject_id)
                )

            units = list(school_units_qs.distinct().order_by('order', 'id'))
            unit_ids = [u.id for u in units]

            if unit_ids:
                lessons_qs = SchoolLesson.objects.filter(unit_id__in=unit_ids, is_deleted=False).order_by('order', 'id')
                for les in lessons_qs:
                    lessons_by_unit.setdefault(les.unit_id, []).append(les)

        elif inst_type == 'university':
            univ_units_qs = UniversityUnit.objects.filter(is_deleted=False)
            if semester_subject_id:
                univ_units_qs = univ_units_qs.filter(semester_subject_id=semester_subject_id)
            elif subject_id:
                univ_units_qs = univ_units_qs.filter(semester_subject__fk_subject_id=subject_id)

            units = list(univ_units_qs.distinct().order_by('order', 'id'))
            unit_ids = [u.id for u in units]

            if unit_ids:
                lessons_qs = UniversityLesson.objects.filter(unit_id__in=unit_ids, is_deleted=False).order_by('order', 'id')
                for les in lessons_qs:
                    lessons_by_unit.setdefault(les.unit_id, []).append(les)

        elif inst_type == 'institute':
            units_list = []
            if institute_subject_id:
                from academic.models.institutes.InstituteSubject import InstituteSubject
                try:
                    isub = InstituteSubject.objects.get(id=institute_subject_id)
                    u_qs = UniversityUnit.objects.filter(
                        semester_subject__name_ar=isub.name_ar, is_deleted=False
                    )
                    if u_qs.exists():
                        units_list = list(u_qs.distinct().order_by('order', 'id'))
                    else:
                        s_qs = SchoolUnit.objects.filter(name_ar=isub.name_ar, is_deleted=False)
                        if s_qs.exists():
                            units_list = list(s_qs.distinct().order_by('order', 'id'))
                except Exception:
                    pass

            units = units_list
            unit_ids = [u.id for u in units]

            if unit_ids:
                u_lessons = list(UniversityLesson.objects.filter(unit_id__in=unit_ids, is_deleted=False).order_by('order', 'id'))
                if not u_lessons:
                    u_lessons = list(SchoolLesson.objects.filter(unit_id__in=unit_ids, is_deleted=False).order_by('order', 'id'))
                for les in u_lessons:
                    lessons_by_unit.setdefault(les.unit_id, []).append(les)

        # 3. Query Existing Exclusions for this Year
        exclusions_qs = CurriculumExclusion.objects.filter(
            academic_year_id=year_id,
            is_active=True,
            is_deleted=False
        )

        all_lesson_ids = [les.id for u_lessons in lessons_by_unit.values() for les in u_lessons]
        relevant_exclusions = exclusions_qs.filter(
            Q(unit_id__in=unit_ids) | Q(lesson_id__in=all_lesson_ids)
        )

        excluded_units_map = {}
        excluded_lessons_map = {}
        for ex in relevant_exclusions:
            if ex.exclusion_type == 'unit' and ex.unit_id:
                excluded_units_map[ex.unit_id] = {
                    'exclusion_id': ex.id,
                    'reason': ex.reason or '',
                }
            elif ex.exclusion_type == 'lesson' and ex.lesson_id:
                excluded_lessons_map[ex.lesson_id] = {
                    'exclusion_id': ex.id,
                    'reason': ex.reason or '',
                }

        # 4. Build Tree Response
        tree = []
        total_lessons_count = 0
        excluded_lessons_count = 0
        excluded_units_count = 0

        for u in units:
            u_ex = excluded_units_map.get(u.id)
            is_unit_excluded = bool(u_ex)
            if is_unit_excluded:
                excluded_units_count += 1

            u_lessons = lessons_by_unit.get(u.id, [])
            serialized_lessons = []
            for l in u_lessons:
                total_lessons_count += 1
                l_ex = excluded_lessons_map.get(l.id)
                # If parent unit is excluded, lesson is effectively excluded as well
                is_lesson_excluded = is_unit_excluded or bool(l_ex)
                if is_lesson_excluded:
                    excluded_lessons_count += 1

                serialized_lessons.append({
                    'id': l.id,
                    'name': getattr(l, 'name_ar', '') or getattr(l, 'name_en', '') or f"درس #{l.id}",
                    'order': getattr(l, 'order', 1),
                    'is_excluded': is_lesson_excluded,
                    'is_directly_excluded': bool(l_ex),
                    'exclusion_id': l_ex['exclusion_id'] if l_ex else (u_ex['exclusion_id'] if u_ex else None),
                    'reason': (l_ex['reason'] if l_ex else '') or (u_ex['reason'] if u_ex else ''),
                })

            tree.append({
                'id': u.id,
                'name': getattr(u, 'name_ar', '') or getattr(u, 'name_en', '') or f"وحدة #{u.id}",
                'order': getattr(u, 'order', 1),
                'is_excluded': is_unit_excluded,
                'exclusion_id': u_ex['exclusion_id'] if u_ex else None,
                'reason': u_ex['reason'] if u_ex else '',
                'lessons_count': len(u_lessons),
                'lessons': serialized_lessons
            })

        return Response({
            'success': True,
            'academic_year_id': year_id,
            'units_count': len(units),
            'excluded_units_count': excluded_units_count,
            'total_lessons_count': total_lessons_count,
            'excluded_lessons_count': excluded_lessons_count,
            'tree': tree
        })

    @action(detail=False, methods=['post'], url_path='batch-sync')
    def batch_sync(self, request):
        """
        Atomically saves and synchronizes curriculum exclusions for a given subject & year.
        Deletes existing exclusions for the specified scope and creates new records.
        """
        data = request.data
        year_id = data.get('academic_year_id') or data.get('year_id')
        inst_type = data.get('institution_type') or 'school'

        if not year_id:
            return Response({"success": False, "message": "حقل العام الدراسي مطلوب"}, status=status.HTTP_400_BAD_REQUEST)

        excluded_unit_ids = set(data.get('excluded_unit_ids', []))
        excluded_lesson_ids = set(data.get('excluded_lesson_ids', []))
        general_reason = data.get('reason', '').strip()

        # Hierarchy Fields
        stage_id = data.get('stage_id')
        class_track_id = data.get('class_track_id')
        subject_id = data.get('subject_id')
        class_subject_id = data.get('class_subject_id')
        college_id = data.get('college_id')
        department_id = data.get('department_id')
        specialization_id = data.get('specialization_id')
        semester_subject_id = data.get('semester_subject_id')
        institute_field_id = data.get('institute_field_id')
        institute_education_system_id = data.get('institute_education_system_id')
        institute_specialization_id = data.get('institute_specialization_id')
        institute_curriculum_id = data.get('institute_curriculum_id')
        institute_subject_id = data.get('institute_subject_id')

        # Model resolution based on inst_type
        if inst_type == 'school':
            LessonModel = SchoolLesson
            if not class_subject_id and class_track_id and subject_id:
                from academic.models.schools.SchoolClassSubject import SchoolClassSubject
                cs = SchoolClassSubject.objects.filter(class_track_id=class_track_id).filter(
                    Q(school_subject_id=subject_id) | Q(subject_id=subject_id)
                ).first()
                if cs:
                    class_subject_id = cs.id
        else:
            LessonModel = UniversityLesson

        # Scope Unit IDs for targeted cleanup
        scope_unit_ids = data.get('scope_unit_ids', [])
        if not scope_unit_ids and (excluded_unit_ids or excluded_lesson_ids):
            scope_unit_ids = list(excluded_unit_ids)
            if excluded_lesson_ids:
                l_units = LessonModel.objects.filter(id__in=excluded_lesson_ids).values_list('unit_id', flat=True)
                scope_unit_ids.extend(list(l_units))

        user = request.user if request.user.is_authenticated else None

        try:
            with transaction.atomic():
                # 1. Clean up existing exclusions within this scope & year
                if scope_unit_ids:
                    scope_lessons = LessonModel.objects.filter(unit_id__in=scope_unit_ids).values_list('id', flat=True)
                    CurriculumExclusion.objects.filter(
                        academic_year_id=year_id,
                        is_deleted=False
                    ).filter(
                        Q(unit_id__in=scope_unit_ids) | Q(lesson_id__in=scope_lessons)
                    ).delete()

                created_records = []

                # 2. Create Unit Exclusions
                for uid in excluded_unit_ids:
                    created_records.append(CurriculumExclusion(
                        academic_year_id=year_id,
                        institution_type=inst_type,
                        stage_id=stage_id,
                        class_track_id=class_track_id,
                        subject_id=subject_id,
                        class_subject_id=class_subject_id,
                        college_id=college_id,
                        department_id=department_id,
                        specialization_id=specialization_id,
                        semester_subject_id=semester_subject_id,
                        institute_field_id=institute_field_id,
                        institute_education_system_id=institute_education_system_id,
                        institute_specialization_id=institute_specialization_id,
                        institute_curriculum_id=institute_curriculum_id,
                        institute_subject_id=institute_subject_id,
                        exclusion_type='unit',
                        unit_id=uid,
                        reason=general_reason,
                        is_active=True,
                        createdBy=user
                    ))

                # 3. Create Lesson Exclusions (only for lessons whose parent unit isn't already fully excluded)
                lessons_in_excluded_units = set(LessonModel.objects.filter(unit_id__in=excluded_unit_ids).values_list('id', flat=True)) if excluded_unit_ids else set()

                for lid in excluded_lesson_ids:
                    if lid not in lessons_in_excluded_units:
                        # Find lesson's unit
                        l_obj = LessonModel.objects.filter(id=lid).first()
                        created_records.append(CurriculumExclusion(
                            academic_year_id=year_id,
                            institution_type=inst_type,
                            stage_id=stage_id,
                            class_track_id=class_track_id,
                            subject_id=subject_id,
                            class_subject_id=class_subject_id,
                            college_id=college_id,
                            department_id=department_id,
                            specialization_id=specialization_id,
                            semester_subject_id=semester_subject_id,
                            institute_field_id=institute_field_id,
                            institute_education_system_id=institute_education_system_id,
                            institute_specialization_id=institute_specialization_id,
                            institute_curriculum_id=institute_curriculum_id,
                            institute_subject_id=institute_subject_id,
                            exclusion_type='lesson',
                            unit_id=l_obj.unit_id if l_obj else None,
                            lesson_id=lid,
                            reason=general_reason,
                            is_active=True,
                            createdBy=user
                        ))

                if created_records:
                    CurriculumExclusion.objects.bulk_create(created_records)

                return Response({
                    "success": True,
                    "message": "تم حفظ واعتماد المحذوفات لهذا العام الدراسي بنجاح",
                    "excluded_units_count": len(excluded_unit_ids),
                    "excluded_lessons_count": len(excluded_lesson_ids),
                    "total_saved": len(created_records)
                })

        except Exception as e:
            return Response({
                "success": False,
                "message": f"حدث خطأ أثناء حفظ المحذوفات: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='active-ids')
    def active_ids(self, request):
        """
        Fast API to get all excluded unit and lesson IDs for a specific year and subject.
        Used by ExamCreateView and TOS to filter blueprint or exclude from candidate questions.
        """
        year_id = request.query_params.get('year_id') or request.query_params.get('academic_year')
        inst_type = request.query_params.get('institution_type')

        if not year_id:
            current_year = AcademicYear.objects.filter(is_current=True, is_deleted=False).first()
            if current_year:
                year_id = current_year.id

        qs = CurriculumExclusion.objects.filter(is_active=True, is_deleted=False)
        if year_id:
            qs = qs.filter(academic_year_id=year_id)
        if inst_type and inst_type != 'all':
            qs = qs.filter(institution_type=inst_type)

        subject_id = request.query_params.get('subject_id')
        if subject_id:
            qs = qs.filter(
                Q(subject_id=subject_id) |
                Q(class_subject__school_subject_id=subject_id) |
                Q(semester_subject__fk_subject_id=subject_id) |
                Q(institute_subject_id=subject_id)
            )

        excluded_unit_ids = list(qs.filter(exclusion_type='unit', unit__isnull=False).values_list('unit_id', flat=True).distinct())
        excluded_lesson_ids = list(qs.filter(exclusion_type='lesson', lesson__isnull=False).values_list('lesson_id', flat=True).distinct())

        # Also get all lessons under excluded units
        if excluded_unit_ids:
            if inst_type == 'school':
                unit_lesson_ids = list(SchoolLesson.objects.filter(unit_id__in=excluded_unit_ids).values_list('id', flat=True).distinct())
            else:
                unit_lesson_ids = list(UniversityLesson.objects.filter(unit_id__in=excluded_unit_ids).values_list('id', flat=True).distinct())
            excluded_lesson_ids = list(set(excluded_lesson_ids + unit_lesson_ids))

        return Response({
            "success": True,
            "academic_year_id": year_id,
            "excluded_unit_ids": excluded_unit_ids,
            "excluded_lesson_ids": excluded_lesson_ids
        })
