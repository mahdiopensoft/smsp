from rest_framework import serializers
from exams.models.TableOfSpecifications import TableOfSpecifications

class TableOfSpecificationsSerializer(serializers.ModelSerializer):
    subject_name = serializers.SerializerMethodField()
    level_name = serializers.SerializerMethodField()

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
