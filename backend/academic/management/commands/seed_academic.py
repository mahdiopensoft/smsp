from django.core.management.base import BaseCommand
from django.utils import timezone
from django.apps import apps

class Command(BaseCommand):
    help = 'Seeds the academic database with default master data for Question Bank'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Starting academic database seeding...'))

        common_defaults = {
            'portal_id': 1,
            'source_system': 'local_seeder',
            'last_synced_at': timezone.now()
        }

        Organization = apps.get_model('academic', 'Organization')
        AcademicYear = apps.get_model('academic', 'AcademicYear')
        EducationalStage = apps.get_model('academic', 'EducationalStage')
        Level = apps.get_model('academic', 'Level')
        Track = apps.get_model('academic', 'Track')
        ClassTrack = apps.get_model('academic', 'ClassTrack')
        Subject = apps.get_model('academic', 'Subject')
        ClassSubject = apps.get_model('academic', 'ClassSubject')
        Semester = apps.get_model('academic', 'Semester')
        Unit = apps.get_model('academic', 'Unit')
        Lesson = apps.get_model('academic', 'Lesson')
        LearningOutcome = apps.get_model('academic', 'LearningOutcome')
        Division = apps.get_model('academic', 'Division')
        Section = apps.get_model('academic', 'Section')
        Building = apps.get_model('academic', 'Building')
        Hall = apps.get_model('academic', 'Hall')

        # 1. Organization
        org, _ = Organization.objects.get_or_create(
            name_ar="وزارة التربية والتعليم",
            defaults={**common_defaults, 'name_en': "Ministry of Education", 'institution_type': 'ministry'}
        )
        self.stdout.write(self.style.SUCCESS(f'Created/Found Organization: {org}'))

        # 2. Academic Years
        year_24, _ = AcademicYear.objects.get_or_create(
            name_ar="2025-2026", defaults={**common_defaults, 'is_current': True}
        )

        # 3. Educational Stages
        stages_data = [
            ("المرحلة الابتدائية", "Primary Stage", 1),
            ("المرحلة الإعدادية", "Middle Stage", 2),
            ("المرحلة الثانوية", "High Stage", 3),
        ]
        stages = {}
        for ar, en, order in stages_data:
            stage, _ = EducationalStage.objects.get_or_create(
                name_ar=ar, defaults={**common_defaults, 'name_en': en, 'order': order}
            )
            stages[order] = stage

        # 4. Tracks
        tracks_data = [
            ("عام", "General", "GEN"),
            ("علمي", "Science", "SCI"),
            ("أدبي", "Arts", "LIT"),
        ]
        tracks = {}
        for ar, en, code in tracks_data:
            t, _ = Track.objects.get_or_create(
                code=code,
                defaults={**common_defaults, 'name_ar': ar, 'name_en': en, 'is_active': True}
            )
            tracks[ar] = t

        # 5. Levels & ClassTracks
        levels_data = [
            (1, "الصف الأول", "Grade 1", 1), (1, "الصف الثاني", "Grade 2", 2), (1, "الصف الثالث", "Grade 3", 3),
            (1, "الصف الرابع", "Grade 4", 4), (1, "الصف الخامس", "Grade 5", 5), (1, "الصف السادس", "Grade 6", 6),
            (2, "الصف السابع", "Grade 7", 7), (2, "الصف الثامن", "Grade 8", 8), (2, "الصف التاسع", "Grade 9", 9),
            (3, "الصف العاشر", "Grade 10", 10), (3, "الصف الحادي عشر", "Grade 11", 11), (3, "الصف الثاني عشر", "Grade 12", 12),
        ]
        class_tracks = []
        for stage_order, ar, en, order in levels_data:
            level, _ = Level.objects.get_or_create(
                name_ar=ar, defaults={**common_defaults, 'name_en': en, 'stage': stages[stage_order], 'order': order}
            )
            ct, _ = ClassTrack.objects.get_or_create(
                level=level, track=tracks["عام"],
                defaults={**common_defaults, 'is_default': True, 'is_active': True}
            )
            class_tracks.append(ct)

        # 6. Subjects
        subjects_data = [
            ("الرياضيات", "Math", "MATH"), ("العلوم", "Science", "SCI"), 
            ("اللغة العربية", "Arabic", "ARB"), ("اللغة الإنجليزية", "English", "ENG"),
            ("الفيزياء", "Physics", "PHYS"), ("الكيمياء", "Chemistry", "CHEM")
        ]
        subjects = {}
        for ar, en, code in subjects_data:
            subject, _ = Subject.objects.get_or_create(
                name_ar=ar, defaults={**common_defaults, 'name_en': en, 'subject_code': code, 'subject_order': len(subjects) + 1}
            )
            subjects[ar] = subject

        # 7. Semesters
        sem1, _ = Semester.objects.get_or_create(
            name_ar="الفصل الدراسي الأول",
            defaults={**common_defaults, 'name_en': "First Semester", 'order': 1, 'is_current': True}
        )
        sem2, _ = Semester.objects.get_or_create(
            name_ar="الفصل الدراسي الثاني",
            defaults={**common_defaults, 'name_en': "Second Semester", 'order': 2}
        )

        # 8. ClassSubjects & Units
        for ct in class_tracks:
            for sub_name, subject in subjects.items():
                cs, _ = ClassSubject.objects.get_or_create(
                    class_track=ct, subject=subject,
                    defaults={**common_defaults, 'min_score': 50, 'max_score': 100, 'added_to_total': True}
                )

                if ct.level.order == 12 and sub_name == "الفيزياء":
                    unit, _ = Unit.objects.get_or_create(
                        name_ar="الميكانيكا والديناميكا", class_subject=cs, semester=sem1,
                        defaults={**common_defaults, 'name_en': "Mechanics", 'order': 1}
                    )
                    lesson, _ = Lesson.objects.get_or_create(
                        name_ar="قوانين نيوتن في الحركة", unit=unit,
                        defaults={**common_defaults, 'name_en': "Newton Laws", 'order': 1}
                    )
                    LearningOutcome.objects.get_or_create(
                        code='PHYS.1.1', unit=unit,
                        defaults={**common_defaults, 'description': "يفهم الطالب قوانين الحركة وتطبيقاتها"}
                    )

        # 9. Divisions, Sections, Buildings & Halls
        for div_name in ["أ", "ب", "ج", "د"]:
            Division.objects.get_or_create(name=div_name, defaults={**common_defaults, 'is_main': True})

        sec, _ = Section.objects.get_or_create(
            organization=org, code="SEC-B",
            defaults={**common_defaults, 'name_ar': "قسم البنين", 'name_en': "Boys Section"}
        )

        bld, _ = Building.objects.get_or_create(
            organization=org, name="المبنى الرئيسي",
            defaults={**common_defaults, 'floors_number': 3, 'rooms_number': 15}
        )

        for hall_num in range(1, 6):
            Hall.objects.get_or_create(
                building=bld, name=f"قاعة {hall_num}",
                defaults={**common_defaults, 'seats_number': 35, 'floor_number': 1}
            )

        self.stdout.write(self.style.SUCCESS('🎉 Academic master database seeded successfully with unified structure!'))
