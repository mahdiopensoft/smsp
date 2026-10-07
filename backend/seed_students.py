"""
═══════════════════════════════════════════════════════════════════════════════
🇾🇪 سكريبت توليد وتعبئة بيانات الطلاب في المدارس وربطهم بالاختبارات
(Seed Students for Yemeni Schools & Auto-Link Existing Exams)
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import uuid
from datetime import date

# إعداد بيئة عمل جانغو
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
from django.db import transaction

from OpenSoftCoreV41.common.models.Branch import Organization as BranchOrg
from OpenSoftCoreV41.common.models.Country import Country
from OpenSoftCoreV41.common.models.Governorate import Governorate
from OpenSoftCoreV41.common.models.Directorate import Directorate
from OpenSoftCoreV41.usermanager.models.UserType import UserType

from academic.models.common.Organization import Organization as AcademicOrg
from academic.models.schools.SchoolStage import SchoolStage
from academic.models.schools.SchoolLevel import SchoolLevel
from academic.models.schools.SchoolTrack import SchoolTrack
from academic.models.schools.SchoolClassTrack import SchoolClassTrack
from academic.models.common.Student import Student
from exams.models.Exam import Exam
from exams.models.ExamVersion import ExamVersion
from exams.models.StudentExamRegistration import StudentExamRegistration

User = get_user_model()

# أسماء طلاب يمنيين حقيقية وواقعية
MALE_NAMES = [
    "أحمد علي محمد صالح",
    "محمد عبد الله حسن الشامي",
    "إبراهيم خليل يحيى الحميري",
    "أسامة عادل ناصر البركاني",
    "عمر عبد العزيز حسن الصبري",
    "ياسر عبد الرحمن مهدي الحداد",
    "حمزة نبيل قائد الموشكي",
    "بلال صادق محمد الزبيري",
    "زيد طارق عبد الله سنان",
    "سيف الدين يحيى علي غالب",
    "طارق وليد عبد السلام العلفي",
    "معاذ رضوان سعيد غالب",
    "مروان فيصل عبد الله الأكوع",
    "هشام فؤاد محمد المتوكل",
    "عبد الرحمن يحيى قاسم الآنسي",
]

FEMALE_NAMES = [
    "فاطمة يحيى عبد الله الأكوع",
    "مريم أحمد صالح الحيمي",
    "سارة عبد الرحمن مهدي الحداد",
    "ريم خالد قاسم المتوكل",
    "أسماء علي ناصر الوادعي",
    "شهد عادل قائد الصبري",
    "هدى محمد عبد السلام الشامي",
    "آلاء صادق عبده الحميري",
    "زينب حسن علي غالب",
    "رغد عبد العزيز محمد السالمي",
    "نور وليد إبراهيم العنسي",
    "ملاك طارق عبد الله غالب",
    "روان فيصل ناصر الحاشدي",
    "صفاء نبيل يحيى الدار",
    "يسرى معاذ علي الكبسي",
]


def seed_students():
    print("🚀 بدء إنشاء وتجهيز بيانات الطلاب للمدارس اليمنية...\n")

    # 1. التأكد من وجود الدولة
    yemen = Country.objects.filter(code="1").first() or Country.objects.filter(id=1).first() or Country.objects.first()

    # 2. فحص نوع المستخدم للطلاب
    print("👤 جلب نوع المستخدم (UserType)...")
    try:
        student_type = (
            UserType.objects.filter(name_en__iexact="student").first() or
            UserType.objects.filter(name_ar__icontains="طالب").first() or
            UserType.objects.filter(id=2).first() or
            UserType.objects.filter(id=4).first() or
            UserType.objects.first()
        )
        if not student_type:
            student_type = UserType.objects.create(
                id=2,
                name_ar="طالب",
                name_en="student",
                is_active=True
            )
        user_type_id = student_type.id
        print(f"  ✅ نوع المستخدم المعتمد للطلاب: ID={user_type_id} ({student_type.name_ar})")
    except Exception as e:
        user_type_id = 4
        print(f"  ⚠️ استخدام نوع المستخدم الافتراضي: ID={user_type_id} ({e})")

    # 3. فحص كافة مسارات الصفوف الموجودة في النظام
    print("\n📚 جلب مسارات الصفوف الموجودة في النظام (Class Tracks)...")
    existing_tracks = list(SchoolClassTrack.objects.filter(is_deleted=False).select_related('level', 'track'))
    
    if existing_tracks:
        print(f"  ✅ تم العثور على {len(existing_tracks)} مسار صف دراسي في النظام:")
        for t in existing_tracks:
            print(f"     - [ID={t.id}] {t.full_name or str(t)}")
        active_class_tracks = existing_tracks
    else:
        print("  ⚠️ لا توجد مسارات مسبقة، سيتم إنشاء المسارات القياسية...")
        stage_basic, _ = SchoolStage.objects.get_or_create(
            name_ar="المرحلة الأساسية",
            defaults={"name_en": "Basic Education", "order": 1, "is_active": True}
        )
        stage_secondary, _ = SchoolStage.objects.get_or_create(
            name_ar="المرحلة الثانوية",
            defaults={"name_en": "Secondary Education", "order": 2, "is_active": True}
        )
        track_general, _ = SchoolTrack.objects.get_or_create(
            code="general",
            defaults={"name_ar": "عام", "name_en": "General", "is_active": True}
        )
        track_scientific, _ = SchoolTrack.objects.get_or_create(
            code="scientific",
            defaults={"name_ar": "علمي", "name_en": "Scientific", "is_active": True}
        )
        level_grade9, _ = SchoolLevel.objects.get_or_create(
            name_ar="الصف التاسع الأساسي",
            defaults={"name_en": "9th Grade", "stage": stage_basic, "order": 9, "is_active": True}
        )
        level_grade12, _ = SchoolLevel.objects.get_or_create(
            name_ar="الثالث الثانوي",
            defaults={"name_en": "12th Grade", "stage": stage_secondary, "order": 12, "is_active": True}
        )
        ct9, _ = SchoolClassTrack.objects.get_or_create(level=level_grade9, track=track_general, defaults={"is_active": True})
        ct12, _ = SchoolClassTrack.objects.get_or_create(level=level_grade12, track=track_scientific, defaults={"is_active": True})
        active_class_tracks = [ct9, ct12]

    # 4. جلب المدارس من قاعدة البيانات
    print("\n🏫 البحث عن المدارس النشطة في الهيكلية...")
    schools = list(BranchOrg.objects.filter(company_level=50, is_deleted=False))
    if not schools:
        schools = list(AcademicOrg.objects.filter(institution_type="school", is_active=True))

    print(f"  ✅ تم العثور على {len(schools)} مدرسة مسجلة.")

    if not schools:
        print("❌ لم يتم العثور على مدارس! يرجى تشغيل سكريبت الهيكلية أولاً.")
        return

    # 5. توليد الطلاب لكل مدرسة ومسار
    print("\n👨‍🎓 إنشاء الطلاب وتوزيعهم على المدارس والصفوف...")
    total_students_created = 0
    total_students_updated = 0
    academic_start_number = 2024100000

    for school_idx, school in enumerate(schools, start=1):
        school_name = getattr(school, 'name_ar', str(school))
        school_dir = getattr(school, 'fk_directorate', None)
        school_gov = getattr(school, 'fk_governorate', None)

        # ضمان وجود سجل متزامن في AcademicOrg
        academic_org, _ = AcademicOrg.objects.update_or_create(
            name_ar=school_name,
            defaults={
                "name_en": getattr(school, 'name_en', None),
                "institution_type": "school",
                "difficulty_modifier": 1.0,
                "is_active": True
            }
        )

        students_per_track = 6

        for track in active_class_tracks:
            for s_i in range(students_per_track):
                is_male = (s_i % 2 == 0)
                if is_male:
                    name_ar = MALE_NAMES[(school_idx + s_i) % len(MALE_NAMES)]
                    gender = 1
                else:
                    name_ar = FEMALE_NAMES[(school_idx + s_i) % len(FEMALE_NAMES)]
                    gender = 2

                acad_num = academic_start_number + (school_idx * 1000) + (track.id * 10) + s_i
                username = f"std_{acad_num}"

                # حساب المستخدم
                user, _ = User.objects.get_or_create(
                    username=username,
                    defaults={
                        "first_name": name_ar.split()[0],
                        "last_name": " ".join(name_ar.split()[1:]),
                        "fk_user_type_id": user_type_id,
                        "is_active": True
                    }
                )
                if not getattr(user, 'fk_user_type_id', None):
                    user.fk_user_type_id = user_type_id
                    user.save(update_fields=['fk_user_type_id'])

                # سجل الطالب الأكاديمي
                student, created = Student.objects.update_or_create(
                    academic_number=acad_num,
                    defaults={
                        "user": user,
                        "name_ar": name_ar,
                        "name_en": f"Student {acad_num}",
                        "gender": gender,
                        "birthdate": date(2007 + (s_i % 3), 1 + (s_i % 12), 1 + (s_i % 28)),
                        "address": school_name,
                        "country": yemen,
                        "directorate": school_dir,
                        "organization": academic_org,
                        "class_track": track,
                        "is_active": True,
                    }
                )

                if created:
                    total_students_created += 1
                else:
                    total_students_updated += 1

        dir_name = school_dir.name_ar if school_dir else "عام"
        gov_name = school_gov.name_ar if school_gov else "عام"
        print(f"  ✅ المدرسة [{school_idx}/{len(schools)}]: {school_name} ({dir_name}) ← تم تخصيص {students_per_track * len(active_class_tracks)} طالب")

    print("\n═══════════════════════════════════════════════════════════════════════════")
    print(f"🎉 اكتملت عملية تعبئة بيانات الطلاب بنجاح!")
    print(f" ✨ طلاب جدد تم إنشاؤهم: {total_students_created}")
    print(f" 🔄 طلاب تم تحديث بياناتهم: {total_students_updated}")
    print(f" 📊 الإجمالي العام للطلاب النشطين: {Student.objects.filter(is_active=True).count()} طالب")
    print("═══════════════════════════════════════════════════════════════════════════\n")

    # 6. الربط التلقائي بأي اختبارات سابقة منشأة بدون طلاب (مثل اختبار 11)
    print("🔗 فحص وربط الاختبارات السابقة التي ليس لها طلاب مسجلون...")
    all_exams = Exam.objects.filter(is_deleted=False)
    for ex in all_exams:
        regs_count = StudentExamRegistration.objects.filter(examVersion__exam=ex, is_deleted=False).count()
        if regs_count == 0 and ex.class_track_id:
            print(f" ⏳ جاري ربط الاختبار [{ex.id}] '{ex.title}' المرتبط بالصف ID={ex.class_track_id}...")
            
            # جلب طلاب مسار هذا الاختبار
            matching_students = list(Student.objects.filter(
                is_active=True,
                is_deleted=False,
                class_track_id=ex.class_track_id
            ).order_by('academic_number'))

            # إذا كان النطاق الجغرافي محدد
            if ex.target_scope_level == 'school':
                scopes = list(ex.target_scopes.filter(is_deleted=False))
                org_ids = [s.organization_id for s in scopes if s.organization_id]
                if org_ids:
                    branch_names = list(BranchOrg.objects.filter(id__in=org_ids).values_list('name_ar', flat=True))
                    academic_ids = list(AcademicOrg.objects.filter(name_ar__in=branch_names).values_list('id', flat=True))
                    all_org_ids = list(set(org_ids + academic_ids))
                    matching_students = [st for st in matching_students if st.organization_id in all_org_ids]
            elif ex.target_scope_level == 'directorate':
                scopes = list(ex.target_scopes.filter(is_deleted=False))
                dir_ids = [s.directorate_id for s in scopes if s.directorate_id]
                if dir_ids:
                    matching_students = [st for st in matching_students if st.directorate_id in dir_ids]
            elif ex.target_scope_level == 'governorate':
                scopes = list(ex.target_scopes.filter(is_deleted=False))
                gov_ids = [s.governorate_id for s in scopes if s.governorate_id]
                if gov_ids:
                    matching_students = [st for st in matching_students if st.directorate and st.directorate.fk_governorate_id in gov_ids]

            versions = list(ExamVersion.objects.filter(exam=ex, is_deleted=False).order_by('versionCode'))
            if matching_students and versions:
                new_regs = []
                for idx, st in enumerate(matching_students):
                    v = versions[idx % len(versions)]
                    seat = f"{ex.uniqueCode}-{str(idx + 1).zfill(4)}"
                    secr = f"S{uuid.uuid4().hex[:6].upper()}"
                    new_regs.append(StudentExamRegistration(
                        student=st.user,
                        student_profile=st,
                        examVersion=v,
                        seatNumber=seat,
                        secretNumber=secr,
                        isPresent=False
                    ))
                StudentExamRegistration.objects.bulk_create(new_regs, ignore_conflicts=True)
                print(f"  🎉 تم ربط {len(new_regs)} طالب بنجاح في الاختبار [{ex.id}] '{ex.title}' موزعين على النماذج ({len(versions)} نماذج)!")
            else:
                print(f"  ⚠️ لم يتم العثور على طلاب مطابقين للاختبار [{ex.id}] (طلاب={len(matching_students)}, نماذج={len(versions)})")


if __name__ == '__main__':
    seed_students()
