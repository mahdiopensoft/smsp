from rest_framework import serializers
from exams.models.TableOfSpecifications import TableOfSpecifications

class TableOfSpecificationsSerializer(serializers.ModelSerializer):
    subject_name = serializers.SerializerMethodField()
    level_name = serializers.SerializerMethodField()
    institution_type_display = serializers.SerializerMethodField()
    units_count = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    # Hierarchy fields for editing (university / school / institute)
    college_id = serializers.SerializerMethodField()
    department_id = serializers.SerializerMethodField()
    specialization_id = serializers.SerializerMethodField()
    semester_subject = serializers.SerializerMethodField()
    stage_id = serializers.SerializerMethodField()
    class_track_id = serializers.SerializerMethodField()
    school_subject_id = serializers.SerializerMethodField()
    institute_field_id = serializers.SerializerMethodField()
    institute_education_system_id = serializers.SerializerMethodField()
    institute_specialization_id = serializers.SerializerMethodField()
    institute_curriculum_id = serializers.SerializerMethodField()
    institute_subject_id = serializers.SerializerMethodField()

    class Meta:
        model = TableOfSpecifications
        fields = '__all__'

    def to_internal_value(self, data):
        mutable = data.copy() if hasattr(data, 'copy') else dict(data)
        inst_type = mutable.get('institution_type') or (getattr(self.instance, 'institution_type', None) or 'school')

        if inst_type == 'school':
            school_sub_id = mutable.get('school_subject')
            if school_sub_id:
                from academic.models.schools.SchoolSubject import SchoolSubject
                from academic.models.universities.UniversitySubject import UniversitySubject as Subject
                try:
                    ssub = SchoolSubject.objects.filter(id=int(school_sub_id)).first()
                    if ssub:
                        sub = Subject.objects.filter(name_ar=ssub.name_ar).first()
                        if not sub and ssub.subject_code:
                            sub = Subject.objects.filter(subject_code=ssub.subject_code).first()
                        if not sub:
                            sub = Subject.objects.create(
                                name_ar=ssub.name_ar,
                                name_en=ssub.name_en or '',
                                subject_code=ssub.subject_code or f"SCH_{ssub.id}",
                            )
                        mutable['subject'] = sub.id
                except Exception:
                    pass

            class_track_id = mutable.get('class_track')
            if class_track_id and not mutable.get('level'):
                from academic.models.schools.SchoolClassTrack import SchoolClassTrack
                try:
                    ct = SchoolClassTrack.objects.filter(id=int(class_track_id)).first()
                    if ct and ct.level_id:
                        mutable['level'] = ct.level_id
                except Exception:
                    pass

        return super().to_internal_value(mutable)

    def get_subject_name(self, obj):
        if obj.subject:
            return getattr(obj.subject, 'name_ar', None) or getattr(obj.subject, 'name_en', None) or str(obj.subject_id)
        return ""

    def get_level_name(self, obj):
        if obj.level:
            return getattr(obj.level, 'name_ar', None) or getattr(obj.level, 'name_en', None) or str(obj.level_id)
        return ""

    def get_institution_type_display(self, obj):
        mapping = {
            'school': 'تعليم مدرسي',
            'university': 'تعليم جامعي',
            'institute': 'معاهد وتدريب مهني',
        }
        return mapping.get(obj.institution_type, obj.institution_type or '')

    def get_units_count(self, obj):
        return len(obj.matrix_data) if isinstance(obj.matrix_data, list) else 0

    def get_created_by_name(self, obj):
        if obj.createdBy:
            full_name = f"{obj.createdBy.first_name or ''} {obj.createdBy.last_name or ''}".strip()
            return full_name or obj.createdBy.username
        return ""

    def _resolve_hierarchy(self, obj):
        """Resolve sector-specific hierarchy IDs once per instance from matrix_data units or subject/level."""
        cached = getattr(obj, '_cached_tos_hierarchy', None)
        if cached is not None:
            return cached

        res = {
            'college_id': None,
            'department_id': None,
            'specialization_id': None,
            'semester_subject': None,
            'stage_id': getattr(obj.level, 'stage_id', None) if obj.level else None,
            'class_track_id': None,
            'school_subject_id': None,
            'institute_field_id': None,
            'institute_education_system_id': None,
            'institute_specialization_id': None,
            'institute_curriculum_id': None,
            'institute_subject_id': None,
        }

        unit_ids = [
            row.get('unit_id')
            for row in (obj.matrix_data or [])
            if isinstance(row, dict) and row.get('unit_id')
        ]

        try:
            if obj.institution_type == 'university':
                from academic.models.universities.UniversityUnit import UniversityUnit
                from academic.models.universities.UniversitySemesterSubject import UniversitySemesterSubject

                sem_sub = None
                if unit_ids:
                    u = (
                        UniversityUnit.objects
                        .select_related('semester_subject__fk_specialization')
                        .filter(id__in=unit_ids, semester_subject__isnull=False)
                        .first()
                    )
                    if u:
                        sem_sub = u.semester_subject
                if not sem_sub and obj.subject_id:
                    sem_sub = (
                        UniversitySemesterSubject.objects
                        .select_related('fk_specialization')
                        .filter(fk_subject_id=obj.subject_id, is_deleted=False)
                        .first()
                    )
                if sem_sub:
                    res['semester_subject'] = sem_sub.id
                    spec = getattr(sem_sub, 'fk_specialization', None)
                    if spec:
                        res['specialization_id'] = spec.id
                        res['department_id'] = spec.fk_section_id
                        res['college_id'] = spec.fk_college_id

            elif obj.institution_type == 'school':
                from academic.models.schools.SchoolUnit import SchoolUnit
                from academic.models.schools.SchoolSubject import SchoolSubject

                if unit_ids:
                    su = (
                        SchoolUnit.objects
                        .select_related('class_subject__class_track__level')
                        .filter(id__in=unit_ids)
                        .first()
                    )
                    if su:
                        res['school_subject_id'] = su.school_subject_id or (su.class_subject.school_subject_id if su.class_subject else None)
                        if su.class_subject and su.class_subject.class_track:
                            res['class_track_id'] = su.class_subject.class_track_id
                            if not res['stage_id'] and su.class_subject.class_track.level:
                                res['stage_id'] = su.class_subject.class_track.level.stage_id

                if not res['school_subject_id'] and obj.subject:
                    ssub = (
                        SchoolSubject.objects.filter(name_ar=obj.subject.name_ar, is_deleted=False).first()
                        or (SchoolSubject.objects.filter(subject_code=obj.subject.subject_code, is_deleted=False).first() if obj.subject.subject_code else None)
                    )
                    if ssub:
                        res['school_subject_id'] = ssub.id

            elif obj.institution_type == 'institute':
                from academic.models.institutes.InstituteUnit import InstituteUnit
                from academic.models.institutes.InstituteSubject import InstituteSubject

                if unit_ids:
                    iu = (
                        InstituteUnit.objects
                        .select_related('subject', 'curriculum__specialization')
                        .filter(id__in=unit_ids)
                        .first()
                    )
                    if iu:
                        res['institute_subject_id'] = iu.subject_id
                        if iu.subject:
                            res['institute_field_id'] = iu.subject.field_id
                        if iu.curriculum:
                            res['institute_curriculum_id'] = iu.curriculum_id
                            spec = iu.curriculum.specialization
                            if spec:
                                res['institute_specialization_id'] = spec.id
                                res['institute_education_system_id'] = spec.education_system_id
                                if not res['institute_field_id']:
                                    res['institute_field_id'] = spec.field_id
                if not res['institute_subject_id'] and obj.subject:
                    isub = InstituteSubject.objects.filter(name_ar=obj.subject.name_ar, is_deleted=False).first()
                    if isub:
                        res['institute_subject_id'] = isub.id
                        res['institute_field_id'] = isub.field_id
        except Exception:
            pass

        obj._cached_tos_hierarchy = res
        return res

    def get_college_id(self, obj):
        return self._resolve_hierarchy(obj)['college_id']

    def get_department_id(self, obj):
        return self._resolve_hierarchy(obj)['department_id']

    def get_specialization_id(self, obj):
        return self._resolve_hierarchy(obj)['specialization_id']

    def get_semester_subject(self, obj):
        return self._resolve_hierarchy(obj)['semester_subject']

    def get_stage_id(self, obj):
        return self._resolve_hierarchy(obj)['stage_id']

    def get_class_track_id(self, obj):
        return self._resolve_hierarchy(obj)['class_track_id']

    def get_school_subject_id(self, obj):
        return self._resolve_hierarchy(obj)['school_subject_id']

    def get_institute_field_id(self, obj):
        return self._resolve_hierarchy(obj)['institute_field_id']

    def get_institute_education_system_id(self, obj):
        return self._resolve_hierarchy(obj)['institute_education_system_id']

    def get_institute_specialization_id(self, obj):
        return self._resolve_hierarchy(obj)['institute_specialization_id']

    def get_institute_curriculum_id(self, obj):
        return self._resolve_hierarchy(obj)['institute_curriculum_id']

    def get_institute_subject_id(self, obj):
        return self._resolve_hierarchy(obj)['institute_subject_id']
