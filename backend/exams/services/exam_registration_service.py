import uuid
from exams.models.StudentExamRegistration import StudentExamRegistration

def register_students_for_exam(exam, user=None):
    """
    Registers and distributes students for an officially approved exam across its versions,
    respecting class track / specialization, geographic scope, and model-region assignments.
    Also cryptographically freezes answer keys for the exam models.
    Returns the count of registered students.
    """
    created_versions = list(exam.versions.filter(is_deleted=False).order_by('versionCode'))
    if not created_versions:
        return 0

    existing_count = StudentExamRegistration.objects.filter(examVersion__exam=exam, is_deleted=False).count()
    if existing_count > 0:
        # Already registered! Freeze keys if needed and return existing count
        for v in created_versions:
            try:
                if v.key_status != v.KeyStatus.FROZEN:
                    v.freeze_key(user=user)
            except Exception:
                pass
        return existing_count

    from academic.models.common.Student import Student
    from OpenSoftCoreV41.common.models.Branch import Organization as BranchOrg
    from academic.models.common.Organization import Organization as AcademicOrg

    student_qs = Student.objects.filter(is_active=True, is_deleted=False)

    # Filter by class_track (Schools)
    if exam.class_track_id:
        student_qs = student_qs.filter(class_track_id=exam.class_track_id)
    elif exam.institution_type == 'university':
        try:
            sem_sub = getattr(exam.subject, 'semester_subjects', None)
            if sem_sub:
                first_ss = sem_sub.first()
                if first_ss and getattr(first_ss, 'fk_specialization_id', None):
                    student_qs = student_qs.filter(university_specialization_id=first_ss.fk_specialization_id)
        except Exception:
            pass

    # Apply Geographic Scope filtering
    target_scope_level = exam.target_scope_level or 'all'
    target_scopes = list(exam.target_scopes.filter(is_deleted=False))

    if target_scope_level == 'school' and target_scopes:
        raw_org_ids = [s.organization_id for s in target_scopes if s.organization_id]
        if raw_org_ids:
            try:
                branch_names = list(BranchOrg.objects.filter(id__in=raw_org_ids).values_list('name_ar', flat=True))
                academic_ids = list(AcademicOrg.objects.filter(name_ar__in=branch_names).values_list('id', flat=True))
                all_org_ids = list(set([int(x) for x in raw_org_ids if str(x).isdigit()] + academic_ids))
                student_qs = student_qs.filter(organization_id__in=all_org_ids)
            except Exception:
                student_qs = student_qs.filter(organization_id__in=raw_org_ids)

    elif target_scope_level == 'directorate' and target_scopes:
        raw_dir_ids = [s.directorate_id for s in target_scopes if s.directorate_id]
        if raw_dir_ids:
            try:
                branch_dir_ids = list(BranchOrg.objects.filter(id__in=raw_dir_ids, fk_directorate__isnull=False).values_list('fk_directorate_id', flat=True))
                all_dir_ids = list(set([int(x) for x in raw_dir_ids if str(x).isdigit()] + branch_dir_ids))
                student_qs = student_qs.filter(directorate_id__in=all_dir_ids)
            except Exception:
                student_qs = student_qs.filter(directorate_id__in=raw_dir_ids)

    elif target_scope_level == 'governorate' and target_scopes:
        raw_gov_ids = [s.governorate_id for s in target_scopes if s.governorate_id]
        if raw_gov_ids:
            try:
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
        # Fallback: exam-level fields
        if exam.directorate_id:
            student_qs = student_qs.filter(directorate_id=exam.directorate_id)
        elif exam.governorate_id:
            student_qs = student_qs.filter(directorate__governorate_id=exam.governorate_id)

    students = list(student_qs.select_related('directorate').order_by('academic_number'))
    if not students:
        for v in created_versions:
            try:
                if v.key_status != v.KeyStatus.FROZEN:
                    v.freeze_key(user=user)
            except Exception:
                pass
        return 0

    # Build group index -> versions mapping
    group_versions_map = {}
    for v in created_versions:
        g_idx = getattr(v, 'model_group_index', 0)
        group_versions_map.setdefault(g_idx, []).append(v)

    group_counters = {g_idx: 0 for g_idx in group_versions_map}
    global_counter = 0
    num_versions = len(created_versions)

    model_region_assignments = list(exam.model_region_assignments.filter(is_deleted=False))

    registrations_to_create = []

    for idx, student in enumerate(students):
        assigned_group_idx = None
        if model_region_assignments:
            s_org_id = student.organization_id
            s_dir_id = student.directorate_id
            s_gov_id = getattr(student.directorate, 'governorate_id', None) if student.directorate else None

            for assign in model_region_assignments:
                g_idx = assign.model_group_index
                a_org = assign.organization_id
                a_dir = assign.directorate_id
                a_gov = assign.governorate_id

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
            ignore_conflicts=True
        )

    # Freeze keys for all versions upon official approval
    for v in created_versions:
        try:
            if v.key_status != v.KeyStatus.FROZEN:
                v.freeze_key(user=user)
        except Exception:
            pass

    return len(registrations_to_create)

