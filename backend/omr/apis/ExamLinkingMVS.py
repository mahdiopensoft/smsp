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
from OpenSoftCoreV41.common.models.Branch import Organization as CoreOrg

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
        Optimized: batch annotations to avoid N+1 queries.
        """
        search = request.query_params.get('search', '').strip()
        institution_type = request.query_params.get('institution_type')
        subject_id = request.query_params.get('subject')

        qs = Exam.objects.filter(is_deleted=False).select_related(
            'subject', 'year', 'governorate', 'directorate'
        ).order_by('-created_at')

        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(uniqueCode__icontains=search))
        if institution_type and institution_type != 'all':
            qs = qs.filter(institution_type=institution_type)
        if subject_id:
            try:
                from academic.models.schools.SchoolSubject import SchoolSubject
                school_subj_names = list(SchoolSubject.objects.filter(id=subject_id).values_list('name_ar', flat=True))
            except Exception:
                school_subj_names = []
            qs = qs.filter(
                Q(subject_id=subject_id) |
                Q(subject__class_subjects__school_subject_id=subject_id) |
                (Q(subject__name_ar__in=school_subj_names) if school_subj_names else Q())
            )

        # فلترة الاختبارات حسب المركز الامتحاني / المدرسة والمحافظة والمديرية والمادة
        school_id = request.query_params.get('school_id') or request.query_params.get('school') or request.query_params.get('organization')
        directorate_id = request.query_params.get('directorate_id') or request.query_params.get('directorate')
        office_id = request.query_params.get('office_id') or request.query_params.get('office') or request.query_params.get('governorate') or request.query_params.get('governorate_id')
        subj_filter = request.query_params.get('subject') or request.query_params.get('subject_id')

        if subj_filter and subj_filter != 'all':
            if str(subj_filter).isdigit():
                qs = qs.filter(subject_id=int(subj_filter))
            else:
                qs = qs.filter(Q(subject__name_ar__icontains=subj_filter) | Q(subject__name_en__icontains=subj_filter))

        filtered_dir_name = None
        filtered_sch_name = None

        if school_id and school_id != 'all':
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

            if matched_school_names:
                filtered_sch_name = matched_school_names[0]

            exam_ids_for_school = StudentExamRegistration.objects.filter(
                is_deleted=False
            ).filter(
                Q(student_profile__organization_id=school_id) |
                Q(student_profile__organization__name_ar__in=matched_school_names)
            ).values_list('examVersion__exam_id', flat=True).distinct()

            qs = qs.filter(id__in=exam_ids_for_school)

        elif directorate_id and directorate_id != 'all':
            dir_names = []
            child_school_names = []
            if str(directorate_id).isdigit():
                core_dir = CoreOrg.objects.filter(id=int(directorate_id), company_level=40).first()
                if core_dir:
                    clean_name = core_dir.name_ar.replace('إدارة التربية والتعليم - مديرية ', '').replace('إدارة التربية والتعليم - ', '').strip()
                    dir_names.extend([core_dir.name_ar, clean_name])
                    filtered_dir_name = clean_name
                    child_schools = CoreOrg.objects.filter(company_level=50, fk_parent_organization=core_dir.id, is_deleted=False)
                    child_school_names = list(child_schools.values_list('name_ar', flat=True))
            else:
                filtered_dir_name = str(directorate_id).replace('إدارة التربية والتعليم - مديرية ', '').replace('إدارة التربية والتعليم - ', '').strip()
                dir_names.append(filtered_dir_name)

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

        elif office_id and office_id != 'all':
            gov_names = []
            child_school_names = []
            if str(office_id).isdigit():
                core_off = CoreOrg.objects.filter(id=int(office_id), company_level=30).first()
                if core_off:
                    clean_gov = core_off.name_ar.replace('مكتب التربية والتعليم - ', '').strip()
                    gov_names.extend([core_off.name_ar, clean_gov])
                    child_dirs = CoreOrg.objects.filter(company_level=40, fk_parent_organization=core_off.id, is_deleted=False)
                    child_schools = CoreOrg.objects.filter(company_level=50, fk_parent_organization__in=child_dirs.values_list('id', flat=True), is_deleted=False)
                    child_school_names = list(child_schools.values_list('name_ar', flat=True))
            else:
                gov_names.append(str(office_id).strip())

            off_exam_ids = StudentExamRegistration.objects.filter(is_deleted=False).filter(
                Q(student_profile__directorate__fk_governorate__name_ar__in=gov_names) |
                Q(student_profile__organization__name_ar__in=child_school_names)
            ).values_list('examVersion__exam_id', flat=True).distinct()

            off_q = Q(id__in=off_exam_ids)
            if str(office_id).isdigit():
                off_q |= Q(governorate_id=int(office_id))
            for g_name in gov_names:
                off_q |= Q(governorate__name_ar__icontains=g_name)

            qs = qs.filter(off_q)

        # School Filters
        stage_id = request.query_params.get('stage')
        if stage_id:
            qs = qs.filter(
                Q(class_track__level__stage_id=stage_id) |
                Q(subject__class_subjects__class_track__level__stage_id=stage_id)
            )
        class_track_id = request.query_params.get('class_track')
        if class_track_id:
            qs = qs.filter(
                Q(class_track_id=class_track_id) |
                Q(subject__class_subjects__class_track_id=class_track_id)
            )

        # University Filters
        college_id = request.query_params.get('college')
        if college_id:
            qs = qs.filter(subject__semester_subjects__fk_specialization__fk_college_id=college_id)
        dept_id = request.query_params.get('department')
        if dept_id:
            qs = qs.filter(subject__semester_subjects__fk_specialization__fk_section_id=dept_id)
        spec_id = request.query_params.get('specialization')
        if spec_id:
            qs = qs.filter(subject__semester_subjects__fk_specialization_id=spec_id)
        sem_sub_id = request.query_params.get('semester_subject')
        if sem_sub_id:
            qs = qs.filter(subject__semester_subjects__id=sem_sub_id)

        # Institute Filters
        inst_field_id = request.query_params.get('institute_field')
        if inst_field_id:
            qs = qs.filter(subject__institute_subjects__field_id=inst_field_id)
        inst_system_id = request.query_params.get('institute_education_system')
        if inst_system_id:
            qs = qs.filter(subject__institute_subjects__specialization__education_system_id=inst_system_id)
        inst_spec_id = request.query_params.get('institute_specialization')
        if inst_spec_id:
            qs = qs.filter(subject__institute_subjects__specialization_id=inst_spec_id)
        inst_sub_id = request.query_params.get('institute_subject')
        if inst_sub_id:
            qs = qs.filter(subject__institute_subjects__id=inst_sub_id)

        qs = qs.distinct()
        exams = list(qs[:100])
        exam_ids = [e.id for e in exams]

        # ── خريطة الهيكل الإداري والمؤسسي المعتمد CoreOrg (محافظات ومديريات ومدارس) ──
        core_schools = CoreOrg.objects.filter(company_level=50, is_deleted=False).select_related(
            'fk_parent_organization', 'fk_parent_organization__fk_parent_organization'
        )
        core_map = {}
        for cs in core_schools:
            d_name = cs.fk_parent_organization.name_ar.replace('إدارة التربية والتعليم - مديرية ', '').replace('إدارة التربية والتعليم - ', '').strip() if cs.fk_parent_organization else ''
            g_name = cs.fk_parent_organization.fk_parent_organization.name_ar.replace('مكتب التربية والتعليم - ', '').strip() if (cs.fk_parent_organization and cs.fk_parent_organization.fk_parent_organization) else ''
            if 'امانه' in g_name.replace('أ', 'ا').lower() or 'أمانة' in g_name:
                g_name = 'أمانة العاصمة'
            core_map[cs.name_ar.strip()] = {'directorate': d_name, 'governorate': g_name}

        # ── Batch fetch scopes & regional assignments ──
        scopes_by_exam = {}
        try:
            from exams.models.ExamTargetScope import ExamTargetScope
            for ts in ExamTargetScope.objects.filter(exam_id__in=exam_ids, is_deleted=False).select_related('governorate', 'directorate', 'organization'):
                eid = ts.exam_id
                if eid not in scopes_by_exam:
                    scopes_by_exam[eid] = {'governorates': set(), 'directorates': set(), 'schools': set()}
                if ts.governorate:
                    g = ts.governorate.name_ar.replace('مكتب التربية والتعليم - ', '').strip()
                    if 'امانه' in g.replace('أ', 'ا').lower() or 'أمانة' in g: g = 'أمانة العاصمة'
                    scopes_by_exam[eid]['governorates'].add(g)
                if ts.directorate:
                    scopes_by_exam[eid]['directorates'].add(ts.directorate.name_ar.replace('إدارة التربية والتعليم - مديرية ', '').replace('إدارة التربية والتعليم - ', '').strip())
                if ts.organization:
                    scopes_by_exam[eid]['schools'].add(ts.organization.name_ar.strip())
        except Exception:
            pass

        assignments_by_exam = {}
        try:
            from exams.models.ExamModelRegionAssignment import ExamModelRegionAssignment
            for mra in ExamModelRegionAssignment.objects.filter(exam_id__in=exam_ids, is_deleted=False).select_related('governorate', 'directorate', 'organization'):
                eid = mra.exam_id
                if eid not in assignments_by_exam:
                    assignments_by_exam[eid] = {}
                gidx = mra.model_group_index or 0
                if gidx not in assignments_by_exam[eid]:
                    assignments_by_exam[eid][gidx] = []
                r_name = mra.directorate.name_ar.replace('إدارة التربية والتعليم - مديرية ', '').replace('إدارة التربية والتعليم - ', '').strip() if mra.directorate else (mra.organization.name_ar.strip() if mra.organization else (mra.governorate.name_ar.replace('مكتب التربية والتعليم - ', '').strip() if mra.governorate else ''))
                if r_name and r_name not in assignments_by_exam[eid][gidx]:
                    assignments_by_exam[eid][gidx].append(r_name)
        except Exception:
            pass

        # ── Batch fetch versions + question counts + model groups ──
        versions_by_exam = {}
        groups_by_exam = {}
        try:
            all_versions = list(ExamVersion.objects.filter(
                exam_id__in=exam_ids, is_deleted=False
            ).values('id', 'exam_id', 'versionCode', 'model_group_index', 'difficulty_profile', 'difficulty_distribution').order_by('exam_id', 'model_group_index', 'versionCode'))

            version_ids = [v['id'] for v in all_versions]
            q_counts = dict(
                ExamQuestionOrder.objects.filter(examVersion_id__in=version_ids, is_deleted=False)
                .values('examVersion_id')
                .annotate(c=Count('id'))
                .values_list('examVersion_id', 'c')
            )
            for v in all_versions:
                v['q_count'] = q_counts.get(v['id'], 0)
                eid = v['exam_id']
                versions_by_exam.setdefault(eid, []).append(v)

                # Group tracking
                gidx = v.get('model_group_index') or 0
                if eid not in groups_by_exam:
                    groups_by_exam[eid] = {}
                if gidx not in groups_by_exam[eid]:
                    diff_p = v.get('difficulty_profile') or 'mixed'
                    diff_ar = 'صعب' if diff_p == 'hard' else ('سهل' if diff_p == 'easy' else ('متوسط' if diff_p == 'medium' else ('متوازن' if diff_p == 'balanced' else 'متنوع')))
                    groups_by_exam[eid][gidx] = {
                        'group_index': gidx,
                        'name': f"مجموعة {gidx + 1}",
                        'difficulty_profile': diff_p,
                        'difficulty_profile_ar': diff_ar,
                        'difficulty_distribution': v.get('difficulty_distribution') or {},
                        'versions': [],
                        'target_regions': [],
                    }
                groups_by_exam[eid][gidx]['versions'].append(v['versionCode'])
        except Exception:
            pass

        # ── Batch fetch submission counts ──
        sub_totals = {}
        sub_completed = {}
        sub_needs_review = {}
        try:
            for row in (Submission.objects.filter(exam_id__in=exam_ids, is_deleted=False)
                        .values('exam_id', 'status').annotate(c=Count('id'))):
                eid, st, cnt = row['exam_id'], row['status'], row['c']
                sub_totals[eid] = sub_totals.get(eid, 0) + cnt
                if st == 'completed':
                    sub_completed[eid] = cnt
                elif st == 'needs_review':
                    sub_needs_review[eid] = cnt
        except Exception:
            pass

        # ── Batch fetch registered student counts and institutions ──
        reg_counts = {}
        regs_geo_by_exam = {}
        try:
            for row in (StudentExamRegistration.objects.filter(
                examVersion__exam_id__in=exam_ids, is_deleted=False
            ).values(
                'examVersion__exam_id',
                'student_profile__organization__name_ar',
                'student_profile__directorate__name_ar',
                'student_profile__directorate__fk_governorate__name_ar'
            )):
                eid = row['examVersion__exam_id']
                reg_counts[eid] = reg_counts.get(eid, 0) + 1

                if eid not in regs_geo_by_exam:
                    regs_geo_by_exam[eid] = {'schools': set(), 'directorates': set(), 'governorates': set()}

                sch = row.get('student_profile__organization__name_ar')
                if sch:
                    clean_sch = sch.strip()
                    regs_geo_by_exam[eid]['schools'].add(clean_sch)
                    if clean_sch in core_map:
                        if core_map[clean_sch]['directorate']:
                            regs_geo_by_exam[eid]['directorates'].add(core_map[clean_sch]['directorate'])
                        if core_map[clean_sch]['governorate']:
                            regs_geo_by_exam[eid]['governorates'].add(core_map[clean_sch]['governorate'])

                d_name = row.get('student_profile__directorate__name_ar')
                if d_name:
                    regs_geo_by_exam[eid]['directorates'].add(
                        d_name.replace('إدارة التربية والتعليم - مديرية ', '').replace('إدارة التربية والتعليم - ', '').strip()
                    )
                g_name = row.get('student_profile__directorate__fk_governorate__name_ar')
                if g_name:
                    g = g_name.replace('مكتب التربية والتعليم - ', '').strip()
                    if 'امانه' in g.replace('أ', 'ا').lower() or 'أمانة' in g: g = 'أمانة العاصمة'
                    regs_geo_by_exam[eid]['governorates'].add(g)
        except Exception:
            pass

        results = []
        for exam in exams:
            versions_data = versions_by_exam.get(exam.id, [])
            max_q = max((v['q_count'] for v in versions_data), default=0)

            # ── 1. المحافظة (محددة ومفصولة بدقة) ──
            govs = set()
            if exam.governorate:
                g = exam.governorate.name_ar.replace('مكتب التربية والتعليم - ', '').strip()
                if 'امانه' in g.replace('أ', 'ا').lower() or 'أمانة' in g: g = 'أمانة العاصمة'
                govs.add(g)
            if exam.id in scopes_by_exam:
                govs.update(scopes_by_exam[exam.id]['governorates'])
            if exam.id in regs_geo_by_exam:
                govs.update(regs_geo_by_exam[exam.id]['governorates'])
            gov_list = sorted([g for g in govs if g])
            primary_gov = gov_list[0] if gov_list else "كافة المحافظات"

            # ── 2. المديرية (محددة ومفصولة بدقة) ──
            dirs = set()
            if exam.directorate:
                d = exam.directorate.name_ar.replace('إدارة التربية والتعليم - مديرية ', '').replace('إدارة التربية والتعليم - ', '').strip()
                dirs.add(d)
            if exam.id in scopes_by_exam:
                dirs.update(scopes_by_exam[exam.id]['directorates'])
            if exam.id in regs_geo_by_exam:
                dirs.update(regs_geo_by_exam[exam.id]['directorates'])
            dir_list = sorted([d for d in dirs if d])
            primary_dir = "، ".join(dir_list[:2]) if dir_list else "كافة المديريات"

            # ── 3. المركز الامتحاني / المدرسة (محددة ومفصولة بدقة) ──
            schs = set()
            if exam.id in scopes_by_exam:
                schs.update(scopes_by_exam[exam.id]['schools'])
            if exam.id in regs_geo_by_exam:
                schs.update(regs_geo_by_exam[exam.id]['schools'])
            sch_list = sorted([s for s in schs if s])

            # خريطة المدارس والمراكز التابعة لكل مديرية في هذا الاختبار
            schools_by_dir = {}
            for s in sch_list:
                d = core_map.get(s, {}).get('directorate') or primary_dir
                schools_by_dir.setdefault(d, []).append(s)

            # ── ضبط العرض التلقائي بدقة حسب الفلتر النشط ──
            if filtered_dir_name and filtered_dir_name in schools_by_dir:
                active_dir = filtered_dir_name
                matching_schs = schools_by_dir[filtered_dir_name]
                active_sch = matching_schs[0]
                active_sch_count = len(matching_schs)
                active_sch_list = matching_schs
            elif filtered_sch_name and filtered_sch_name in sch_list:
                active_sch = filtered_sch_name
                active_sch_count = 1
                active_sch_list = [filtered_sch_name]
                active_dir = core_map.get(filtered_sch_name, {}).get('directorate') or primary_dir
            else:
                active_dir = primary_dir
                active_sch = sch_list[0] if sch_list else "جميع مراكز المديرية"
                active_sch_count = len(sch_list)
                active_sch_list = sch_list

            # ── 4. مجموعات النماذج والتوزيع المناطقي ──
            model_groups = []
            is_advanced_mode = getattr(exam, 'models_mode', 'uniform') == 'advanced'

            # مجموعات الصعوبة تظهر فقط إذا كان الاختبار قد تم إنشاؤه بنمط متقدم ومناطقي (Advanced Mode)
            if is_advanced_mode and groups_by_exam.get(exam.id):
                exam_groups_dict = groups_by_exam.get(exam.id, {})
                assign_dict = assignments_by_exam.get(exam.id, {})
                cfg_groups = []
                if exam.model_groups_config and isinstance(exam.model_groups_config, list):
                    cfg_groups = exam.model_groups_config

                for gidx, gdata in sorted(exam_groups_dict.items()):
                    target_regs = list(assign_dict.get(gidx, []))
                    if not target_regs and gidx < len(cfg_groups):
                        cfg = cfg_groups[gidx]
                        if isinstance(cfg, dict):
                            if 'regions' in cfg and isinstance(cfg['regions'], list):
                                target_regs.extend(cfg['regions'])
                            elif 'directorates' in cfg and isinstance(cfg['directorates'], list):
                                target_regs.extend(cfg['directorates'])

                    gdata['target_regions'] = target_regs
                    gdata['target_regions_str'] = "، ".join(target_regs) if target_regs else "كافة المراكز المعتمدة للاختبار"
                    gdata['models_str'] = "، ".join(gdata['versions'])
                    model_groups.append(gdata)

            scope_parts = []
            if primary_gov and primary_gov != "كافة المحافظات": scope_parts.append(primary_gov)
            if active_dir and active_dir != "كافة المديريات": scope_parts.append(active_dir)
            scope_geo = " • ".join(scope_parts) if scope_parts else "عام لجميع المحافظات"

            results.append({
                "id": exam.id,
                "title": exam.title,
                "uniqueCode": exam.uniqueCode,
                "institution_type": exam.institution_type,
                "institution_type_display": exam.get_institution_type_display() if hasattr(exam, 'get_institution_type_display') else ("معاهد وتدريب مهني" if exam.institution_type == 'institute' else ("جامعي" if exam.institution_type == 'university' else "مدرسي")),
                "subject_id": exam.subject_id,
                "subject_name": getattr(exam.subject, 'name_ar', None) if exam.subject else None,
                "year_id": exam.year_id,
                "year_name": (exam.year.hijri_year + "هـ - " + exam.year.gregorian_year + "م") if (exam.year and getattr(exam.year, 'hijri_year', None) and getattr(exam.year, 'gregorian_year', None)) else (getattr(exam.year, 'gregorian_year', None) or (str(exam.year) if exam.year else None)),
                # الأعمدة الثلاثة المستقلة والمفصولة تماماً (المحدثة ديناميكياً حسب الفلتر)
                "governorate": primary_gov,
                "governorates_list": gov_list,
                "governorates_count": len(gov_list),
                "directorate": active_dir,
                "directorates_list": dir_list,
                "directorates_count": len(dir_list),
                "school_center": active_sch,
                "primary_school": active_sch,
                "schools": active_sch_list,
                "schools_list": active_sch_list,
                "schools_count": active_sch_count,
                "all_schools_count": len(sch_list),
                "all_schools_list": sch_list,
                "schools_by_directorate": schools_by_dir,
                # النماذج والتوزيع المناطقي المتقدم (فقط عند Advanced Mode)
                "models_mode": getattr(exam, 'models_mode', 'uniform') or 'uniform',
                "model_groups": model_groups,
                "scope_geo": scope_geo,
                "created_at": exam.created_at.strftime("%Y-%m-%d %H:%M") if exam.created_at else "",
                "versions_count": len(versions_data),
                "versions": [{"id": v['id'], "versionCode": v['versionCode'], "questions_count": v['q_count']} for v in versions_data],
                "total_questions": max_q,
                "submissions_total": sub_totals.get(exam.id, 0),
                "submissions_completed": sub_completed.get(exam.id, 0),
                "submissions_needs_review": sub_needs_review.get(exam.id, 0),
                "average_score": 0.0,
                "default_template": "OMR_YEMEN_180" if max_q > 60 else "OMR_YEMEN_60",
                "has_answer_keys": len(versions_data) > 0 and max_q > 0,
                "registered_students_count": reg_counts.get(exam.id, 0),
            })

        return Response({
            "success": True,
            "count": len(results),
            "results": results
        })

    @action(detail=False, methods=['get'], url_path='subjects')
    def available_subjects(self, request):
        """
        قائمة المواد الدراسية المعتمدة بالاختبارات المصدرة لفلترة شاشات الطباعة والرصد.
        """
        subjects_qs = Exam.objects.filter(is_deleted=False, subject__isnull=False).values(
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
        Get full linking details of an exam, including all its versions,
        questions, options, and model answer keys.
        """
        try:
            exam = Exam.objects.select_related(
                'subject', 'year', 'governorate', 'directorate',
                'class_track__level', 'class_track__track', 'examSchedule'
            ).get(pk=pk, is_deleted=False)
        except Exam.DoesNotExist:
            return Response({"success": False, "message": "الاختبار غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        # Stage / Track representation
        stage_name = None
        if exam.class_track:
            parts = []
            if hasattr(exam.class_track, 'level') and exam.class_track.level and exam.class_track.level.name_ar:
                parts.append(exam.class_track.level.name_ar)
            if hasattr(exam.class_track, 'track') and exam.class_track.track and exam.class_track.track.name_ar:
                parts.append(f"({exam.class_track.track.name_ar})")
            if parts:
                stage_name = " ".join(parts)

        # Academic Year representation
        year_name = None
        if exam.year:
            parts = []
            if getattr(exam.year, 'hijri_year', None):
                parts.append(f"{exam.year.hijri_year}هـ")
            if getattr(exam.year, 'gregorian_year', None):
                parts.append(f"{exam.year.gregorian_year}م")
            year_name = " - ".join(parts) if parts else str(exam.year)

        # Schedule / Time representation
        exam_date = None
        day_name = None
        time_allowed = None
        exam_time = None
        if exam.examSchedule:
            if exam.examSchedule.date:
                exam_date = exam.examSchedule.date.strftime("%Y/%m/%d")
                arabic_days = ['الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت', 'الأحد']
                try:
                    day_name = arabic_days[exam.examSchedule.date.weekday()]
                except Exception:
                    day_name = None
            if exam.examSchedule.duration:
                dur = exam.examSchedule.duration
                hours = dur // 60
                mins = dur % 60
                time_parts = []
                if hours > 0:
                    if hours == 1:
                        time_parts.append("ساعة واحدة")
                    elif hours == 2:
                        time_parts.append("ساعتان")
                    elif 3 <= hours <= 10:
                        time_parts.append(f"{hours} ساعات")
                    else:
                        time_parts.append(f"{hours} ساعة")
                if mins > 0:
                    time_parts.append(f"{mins} دقيقة")
                time_allowed = " و".join(time_parts) if time_parts else f"{dur} دقيقة"
                exam_time = time_allowed

        gov_name = exam.governorate.name_ar if exam.governorate else None
        dir_name = exam.directorate.name_ar if exam.directorate else None

        from bank.models.Answer import Answer
        from exams.models.ExamQuestionOrder import ExamQuestionOrder
        from django.db.models import Prefetch

        versions = ExamVersion.objects.filter(
            exam=exam,
            is_deleted=False
        ).prefetch_related(
            Prefetch(
                'question_orders',
                queryset=ExamQuestionOrder.objects.filter(is_deleted=False).select_related(
                    'question'
                ).prefetch_related(
                    Prefetch(
                        'question__options',
                        queryset=Answer.objects.filter(is_deleted=False).order_by('id')
                    )
                ).order_by('orderIndex'),
                to_attr='_active_q_orders'
            )
        ).order_by('versionCode')

        letters = ['A', 'B', 'C', 'D', 'E', 'F']
        arabic_letters = ['أ', 'ب', 'ج', 'د', 'هـ', 'و']

        versions_details = []
        for v in versions:
            q_orders = getattr(v, '_active_q_orders', [])
            questions_list = []
            answer_key = {}

            for qo in q_orders:
                q = qo.question
                opts = list(q.options.all())
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

                is_tf = (q.questionType in ['True/False', 'true_false', 'صح وخطأ']) or (q.isTrue is not None)
                if is_tf:
                    if not options_data:
                        options_data = [
                            {"id": f"tf_{q.id}_1", "letter": "A", "arabic_letter": "صح", "text": "صح / صواب", "isTrue": q.isTrue is True},
                            {"id": f"tf_{q.id}_2", "letter": "B", "arabic_letter": "خطأ", "text": "خطأ", "isTrue": q.isTrue is False},
                        ]
                    correct_letter = 'A' if q.isTrue is True else ('B' if q.isTrue is False else correct_letter)
                    correct_arabic = 'صح' if q.isTrue is True else ('خطأ' if q.isTrue is False else correct_arabic)

                answer_key[str(qo.orderIndex)] = correct_letter

                questions_list.append({
                    "id": q.id,
                    "orderIndex": qo.orderIndex,
                    "content": q.content,
                    "questionType": 'true_false' if is_tf else q.questionType,
                    "choicesCount": len(options_data),
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

        # Registered Students for this exam (filtered by school, directorate, or office if specified)
        from exams.models.StudentExamRegistration import StudentExamRegistration
        st_qs = StudentExamRegistration.objects.filter(
            examVersion__exam=exam, is_deleted=False
        ).select_related(
            'student_profile__organization', 'student_profile__directorate', 'student', 'examVersion'
        )

        req_school = request.query_params.get('school_id') or request.query_params.get('school') or request.query_params.get('organization')
        req_directorate = request.query_params.get('directorate_id') or request.query_params.get('directorate')
        req_office = request.query_params.get('office_id') or request.query_params.get('office')

        if req_school and req_school != 'all':
            matched_sch_names = []
            if str(req_school).isdigit():
                core_sch = CoreOrg.objects.filter(id=int(req_school), company_level=50).first()
                if core_sch:
                    matched_sch_names.append(core_sch.name_ar)
                try:
                    from academic.models.common.Organization import Organization as AcademicOrg
                    ac_sch = AcademicOrg.objects.filter(id=int(req_school)).first()
                    if ac_sch and ac_sch.name_ar not in matched_sch_names:
                        matched_sch_names.append(ac_sch.name_ar)
                except Exception:
                    pass
            else:
                matched_sch_names.append(str(req_school).strip())

            st_qs = st_qs.filter(
                Q(student_profile__organization_id=req_school) |
                Q(student_profile__organization__name_ar__in=matched_sch_names)
            )
        elif req_directorate and req_directorate != 'all':
            dir_names = []
            child_school_names = []
            if str(req_directorate).isdigit():
                core_dir = CoreOrg.objects.filter(id=int(req_directorate), company_level=40).first()
                if core_dir:
                    clean_name = core_dir.name_ar.replace('إدارة التربية والتعليم - مديرية ', '').replace('إدارة التربية والتعليم - ', '').strip()
                    dir_names.extend([core_dir.name_ar, clean_name])
                    child_schools = CoreOrg.objects.filter(company_level=50, fk_parent_organization=core_dir.id, is_deleted=False)
                    child_school_names = list(child_schools.values_list('name_ar', flat=True))
            else:
                dir_names.append(str(req_directorate).strip())

            st_qs = st_qs.filter(
                Q(student_profile__directorate__name_ar__in=dir_names) |
                Q(student_profile__organization__name_ar__in=child_school_names)
            )
        elif req_office and req_office != 'all':
            gov_names = []
            child_school_names = []
            if str(req_office).isdigit():
                core_off = CoreOrg.objects.filter(id=int(req_office), company_level=30).first()
                if core_off:
                    clean_gov = core_off.name_ar.replace('مكتب التربية والتعليم - ', '').strip()
                    gov_names.extend([core_off.name_ar, clean_gov])
                    child_dirs = CoreOrg.objects.filter(company_level=40, fk_parent_organization=core_off.id, is_deleted=False)
                    child_schools = CoreOrg.objects.filter(company_level=50, fk_parent_organization__in=child_dirs.values_list('id', flat=True), is_deleted=False)
                    child_school_names = list(child_schools.values_list('name_ar', flat=True))
            else:
                gov_names.append(str(req_office).strip())

            st_qs = st_qs.filter(
                Q(student_profile__directorate__fk_governorate__name_ar__in=gov_names) |
                Q(student_profile__organization__name_ar__in=child_school_names)
            )

        st_qs = st_qs.only(
            'id', 'seatNumber', 'secretNumber', 'isPresent', 'is_printed', 'printed_at', 'print_batch',
            'student_profile__name_ar', 'student_profile__organization__name_ar', 'student_profile__organization__id',
            'student_profile__directorate__name_ar',
            'student__username', 'student__first_name', 'student__last_name',
            'examVersion__versionCode',
        ).order_by('seatNumber')
        total_st_count = st_qs.count()
        students_list = []
        schools_involved_set = set()
        for reg in st_qs:
            if reg.student_profile and reg.student_profile.name_ar:
                s_name = reg.student_profile.name_ar
            elif reg.student:
                st = reg.student
                s_name = getattr(st, 'get_full_name', lambda: '')() or f"{st.first_name or ''} {st.last_name or ''}".strip() or st.username
            else:
                s_name = None
            inst_name = reg.student_profile.organization.name_ar if (reg.student_profile and reg.student_profile.organization) else None
            inst_id = reg.student_profile.organization.id if (reg.student_profile and reg.student_profile.organization) else None
            if inst_name:
                schools_involved_set.add(inst_name)
            st_dir = reg.student_profile.directorate.name_ar if (reg.student_profile and reg.student_profile.directorate) else dir_name
            st_photo = None

            v_code = reg.examVersion.versionCode
            students_list.append({
                "id": reg.id,
                "student_name": s_name,
                "seat_number": reg.seatNumber,
                "secret_number": reg.secretNumber or None,
                "student_photo": st_photo,
                "model_code": v_code,
                "school_name": inst_name,
                "school_id": inst_id,
                "governorate": gov_name,
                "directorate": st_dir,
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
                "subject_name": getattr(exam.subject, 'name_ar', str(exam.subject)) if exam.subject else None,
                "stage_name": stage_name,
                "year_name": year_name,
                "governorate": gov_name,
                "directorate": dir_name,
                "exam_date": exam_date,
                "day_name": day_name,
                "time_allowed": time_allowed,
                "exam_time": exam_time,
                "envelope_no": getattr(exam, 'envelope_no', None),
                "created_at": exam.created_at.strftime("%Y-%m-%d %H:%M") if exam.created_at else "",
            },
            "versions": versions_details,
            "registered_students_count": len(students_list),
            "total_registered_count": total_st_count,
            "printed_count": sum(1 for s in students_list if s.get("is_printed")),
            "schools": sorted(list(schools_involved_set)),
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
        ).only(
            'id', 'seatNumber', 'secretNumber', 'isPresent', 'is_printed', 'printed_at', 'print_batch',
            'student_profile__name_ar', 'student_profile__organization__name_ar', 'student_profile__organization__id',
            'student_profile__directorate__name_ar',
            'student__username', 'student__first_name', 'student__last_name',
            'examVersion__versionCode',
        )

        # 1. Filter by Model Code / Version
        version = request.query_params.get('version') or request.query_params.get('model_code') or request.query_params.get('versionCode')
        if version and version != 'all':
            registrations = registrations.filter(examVersion__versionCode=version)

        # 2. Filter by School / Organization / Directorate / Office
        req_school = request.query_params.get('school_id') or request.query_params.get('school') or request.query_params.get('school_name') or request.query_params.get('organization')
        req_directorate = request.query_params.get('directorate_id') or request.query_params.get('directorate')
        req_office = request.query_params.get('office_id') or request.query_params.get('office')

        if req_school and req_school != 'all':
            matched_sch_names = []
            if str(req_school).isdigit():
                core_sch = CoreOrg.objects.filter(id=int(req_school), company_level=50).first()
                if core_sch:
                    matched_sch_names.append(core_sch.name_ar)
                try:
                    from academic.models.common.Organization import Organization as AcademicOrg
                    ac_sch = AcademicOrg.objects.filter(id=int(req_school)).first()
                    if ac_sch and ac_sch.name_ar not in matched_sch_names:
                        matched_sch_names.append(ac_sch.name_ar)
                except Exception:
                    pass
            else:
                matched_sch_names.append(str(req_school).strip())

            registrations = registrations.filter(
                Q(student_profile__organization_id=req_school) |
                Q(student_profile__organization__name_ar__in=matched_sch_names)
            )
        elif req_directorate and req_directorate != 'all':
            dir_names = []
            child_school_names = []
            if str(req_directorate).isdigit():
                core_dir = CoreOrg.objects.filter(id=int(req_directorate), company_level=40).first()
                if core_dir:
                    clean_name = core_dir.name_ar.replace('إدارة التربية والتعليم - مديرية ', '').replace('إدارة التربية والتعليم - ', '').strip()
                    dir_names.extend([core_dir.name_ar, clean_name])
                    child_schools = CoreOrg.objects.filter(company_level=50, fk_parent_organization=core_dir.id, is_deleted=False)
                    child_school_names = list(child_schools.values_list('name_ar', flat=True))
            else:
                dir_names.append(str(req_directorate).strip())

            registrations = registrations.filter(
                Q(student_profile__directorate__name_ar__in=dir_names) |
                Q(student_profile__organization__name_ar__in=child_school_names)
            )
        elif req_office and req_office != 'all':
            gov_names = []
            child_school_names = []
            if str(req_office).isdigit():
                core_off = CoreOrg.objects.filter(id=int(req_office), company_level=30).first()
                if core_off:
                    clean_gov = core_off.name_ar.replace('مكتب التربية والتعليم - ', '').strip()
                    gov_names.extend([core_off.name_ar, clean_gov])
                    child_dirs = CoreOrg.objects.filter(company_level=40, fk_parent_organization=core_off.id, is_deleted=False)
                    child_schools = CoreOrg.objects.filter(company_level=50, fk_parent_organization__in=child_dirs.values_list('id', flat=True), is_deleted=False)
                    child_school_names = list(child_schools.values_list('name_ar', flat=True))
            else:
                gov_names.append(str(req_office).strip())

            registrations = registrations.filter(
                Q(student_profile__directorate__fk_governorate__name_ar__in=gov_names) |
                Q(student_profile__organization__name_ar__in=child_school_names)
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

        # Extract available schools only on initial page load (page 1) to eliminate heavy scans during pagination
        schools_list = []
        if page_num == 1:
            schools_list = list(
                StudentExamRegistration.objects.filter(examVersion__exam=exam, is_deleted=False)
                .order_by()
                .values_list('student_profile__organization__name_ar', flat=True)
                .exclude(student_profile__organization__name_ar__isnull=True)
                .exclude(student_profile__organization__name_ar__exact='')
                .distinct()
            )

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
                st = reg.student
                s_name = getattr(st, 'get_full_name', lambda: '')() or f"{st.first_name or ''} {st.last_name or ''}".strip() or st.username
            else:
                s_name = f"طالب ({reg.seatNumber})"

            inst_name = profile.organization.name_ar if (profile and profile.organization) else None
            inst_id = profile.organization.id if (profile and profile.organization) else None
            dir_name = profile.directorate.name_ar if (profile and profile.directorate) else (exam.directorate.name_ar if exam.directorate else None)
            v_code = reg.examVersion.versionCode if reg.examVersion else "-"
            st_photo = None

            students_data.append({
                "id": reg.id,
                "student_name": s_name,
                "seat_number": reg.seatNumber,
                "secret_number": reg.secretNumber or None,
                "student_photo": st_photo,
                "model_code": v_code,
                "school_name": inst_name,
                "school_id": inst_id,
                "governorate": gov_name or None,
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
        marks_result = {}
        for v in versions:
            v_key = {}
            v_marks = {}
            for qo in v.question_orders.filter(is_deleted=False).order_by('orderIndex'):
                q = qo.question
                opts = list(q.options.filter(is_deleted=False))
                ans = 'A'
                for idx, opt in enumerate(opts):
                    if opt.isTrue:
                        ans = chr(65 + idx)
                        break
                if (q.questionType in ['True/False', 'true_false', 'صح وخطأ']) or (q.isTrue is not None):
                    ans = 'A' if q.isTrue is True else ('B' if q.isTrue is False else ans)
                q_id_str = str(qo.orderIndex)
                v_key[q_id_str] = ans
                v_marks[q_id_str] = float(q.defaultMark or 1.0)

            result[v.versionCode] = v_key
            marks_result[v.versionCode] = v_marks

        return Response({
            "success": True,
            "exam_id": exam.id,
            "exam_title": exam.title,
            "keys_by_version": result,
            "marks_by_version": marks_result,
        })

    @action(detail=True, methods=['post'], url_path='seed-students')
    def seed_sample_students(self, request, pk=None):
        """
        تسجيل وربط الطلاب الفعليين المقيدين في النظام التعليمي بهذا الاختبار
        باستخدام أرقام القيد والأرقام الأكاديمية الرسمية الحقيقية (بدون أرقام جلوس وهمية).
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

        # 1. تصفية الطلاب الفعليين المنتظمين المرتبطين بمستوى ومؤسسة هذا الاختبار
        students_qs = Student.objects.filter(is_active=True).select_related('organization', 'user', 'directorate', 'class_track')

        # فلترة حسب نوع المؤسسة
        if exam.institution_type:
            org_students = students_qs.filter(organization__institution_type=exam.institution_type)
            if org_students.exists():
                students_qs = org_students

        # فلترة دقيقة حسب مسار وصف الاختبار إن وجد
        if exam.class_track_id:
            track_students = students_qs.filter(class_track_id=exam.class_track_id)
            if track_students.exists():
                students_qs = track_students

        db_students = list(students_qs[:100])
        if not db_students:
            return Response({
                "success": False,
                "message": "لا يوجد طلاب مقيدين في النظام لهذه المرحلة أو المسار. يرجى تسجيل الطلاب في شؤون الطلاب أولاً."
            }, status=status.HTTP_400_BAD_REQUEST)

        created_count = 0
        updated_count = 0

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

            # استخدام الرقم الأكاديمي الحقيقي كرقم جلوس رسمي معتمد
            seat_no = str(student_obj.academic_number)
            secret_no = str(1000 + idx + 1)

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
            else:
                # تصحيح أي رقم جلوس قديم غير حقيقي إلى الرقم الأكاديمي الرسمي
                if reg.seatNumber != seat_no or reg.student_profile != student_obj:
                    reg.student_profile = student_obj
                    reg.seatNumber = seat_no
                    reg.save(update_fields=['student_profile', 'seatNumber'])
                    updated_count += 1

        return Response({
            "success": True,
            "message": f"تم تسجيل ومطابقة {created_count + updated_count} طالباً فعلياً بالرقم الأكاديمي المعتمد بنجاح",
            "created_count": created_count,
            "updated_count": updated_count,
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
