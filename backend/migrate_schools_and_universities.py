"""
═══════════════════════════════════════════════════════════════════════════════
🚀 سكريبت الترحيل الآمن لفصل بيانات المدارس والجامعات
   Safe Data Migration Script: Decoupling Schools & Universities
═══════════════════════════════════════════════════════════════════════════════
يقوم هذا السكريبت بـ:
1. نقل المواد المدرسية من Subject إلى SchoolSubject وربطها بـ ClassSubject
2. نقل المقررات الجامعية من Subject إلى UniversityCourse وربطها بـ SemesterSubject
3. ترحيل الوحدات والدروس المدرسية إلى SchoolUnit و SchoolLesson و SchoolLearningOutcome
4. ترحيل موضوعات ومخرجات المقررات الجامعية إلى CourseTopic و CourseCLO
5. تنفيذ العملية كاملة داخل transaction.atomic آمنة دون حذف البيانات الأصلية
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import django

# إعداد بيئة جانغو
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import transaction
from academic.models.common.Subject import Subject
from academic.models.schools.SchoolSubject import SchoolSubject
from academic.models.universities.UniversityCourse import UniversityCourse
from academic.models.schools.SchoolClassSubject import SchoolClassSubject as ClassSubject
from academic.models.universities.UniversitySemesterSubject import UniversitySemesterSubject as SemesterSubject
from academic.models.common.Unit import Unit
from academic.models.common.Lesson import Lesson
from academic.models.common.LearningOutcome import LearningOutcome
from academic.models.schools.SchoolUnit import SchoolUnit
from academic.models.schools.SchoolLesson import SchoolLesson
from academic.models.schools.SchoolLearningOutcome import SchoolLearningOutcome
from academic.models.universities.UniversityCourseTopic import UniversityCourseTopic as CourseTopic
from academic.models.universities.UniversityCourseCLO import UniversityCourseCLO as CourseCLO

def run_migration():
    print("\n" + "═" * 75)
    print("🚀 بدء عملية الترحيل المعماري لفصل بيانات المدارس والجامعات...")
    print("═" * 75 + "\n")

    with transaction.atomic():
        school_subjs_count = 0
        univ_courses_count = 0
        school_units_count = 0
        school_lessons_count = 0
        school_los_count = 0
        course_topics_count = 0
        course_clos_count = 0

        # خريطة لربط المعرفات القديمة بالجديدة
        old_to_school_subject = {}
        old_to_univ_course = {}

        # 1. ترحيل المواد والمقررات
        all_subjects = Subject.objects.all()
        print(f"📊 إجمالي المواد المسجلة في الجدول المشترك: {all_subjects.count()}")

        for subj in all_subjects:
            is_university = (
                (subj.credit_hours and subj.credit_hours > 0) or
                SemesterSubject.objects.filter(fk_subject=subj).exists()
            )
            is_school = (
                subj.is_ministerial or
                ClassSubject.objects.filter(subject=subj).exists() or
                not is_university
            )

            # إذا كانت مادة مدرسية
            if is_school:
                school_subj, created = SchoolSubject.objects.get_or_create(
                    id=subj.id,
                    defaults={
                        'name_ar': subj.name_ar,
                        'name_en': subj.name_en,
                        'subject_code': subj.subject_code,
                        'is_ministerial': subj.is_ministerial,
                        'is_detailed': subj.is_detailed,
                        'subject_order': subj.subject_order,
                        'note': subj.note,
                        'is_active': subj.is_active,
                        'portal_id': subj.portal_id,
                        'source_system': subj.source_system,
                    }
                )
                old_to_school_subject[subj.id] = school_subj
                school_subjs_count += 1

                # تحديث ClassSubject المرتبطة
                updated_cs = ClassSubject.objects.filter(subject=subj).update(school_subject=school_subj)
                if updated_cs:
                    print(f" 🏫 مادة مدرسية: [{subj.name_ar}] -> ربط {updated_cs} مسار صف")

            # إذا كانت مقرراً جامعياً
            if is_university:
                code = subj.subject_code or f"CRS-{subj.id:03d}"
                # التأكد من فرادة الكود
                if UniversityCourse.objects.filter(course_code=code).exclude(id=subj.id).exists():
                    code = f"{code}-{subj.id}"

                univ_course, created = UniversityCourse.objects.get_or_create(
                    id=subj.id,
                    defaults={
                        'name_ar': subj.name_ar,
                        'name_en': subj.name_en,
                        'course_code': code,
                        'credit_hours': subj.credit_hours or 3,
                        'is_active': subj.is_active,
                        'portal_id': subj.portal_id,
                        'source_system': subj.source_system,
                    }
                )
                old_to_univ_course[subj.id] = univ_course
                univ_courses_count += 1

                # تحديث SemesterSubject المرتبطة
                updated_ss = SemesterSubject.objects.filter(fk_subject=subj).update(course=univ_course)
                if updated_ss:
                    print(f" 🎓 مقرر جامعي: [{subj.name_ar}] ({code}) -> ربط {updated_ss} مقرر فصلي")

        print(f"\n✅ اكتمل ترحيل المواد: تم إنشاء {school_subjs_count} مادة مدرسية و {univ_courses_count} مقرر جامعي.")

        # 2. ترحيل الوحدات
        all_units = Unit.objects.select_related('class_subject', 'semester_subject').all()
        old_unit_to_school_unit = {}
        old_unit_to_course_topic = {}

        for u in all_units:
            # إذا كانت وحدة مدرسية
            if u.class_subject or (u.class_subject_id and u.class_subject_id in old_to_school_subject):
                cs = u.class_subject
                sch_subj = cs.school_subject if cs else None
                s_unit, _ = SchoolUnit.objects.get_or_create(
                    id=u.id,
                    defaults={
                        'name_ar': u.name_ar,
                        'name_en': u.name_en,
                        'class_subject': cs,
                        'school_subject': sch_subj,
                        'semester': u.semester,
                        'order': u.order,
                        'enable_learning_outcomes': u.enable_learning_outcomes,
                        'is_active': u.is_active,
                        'portal_id': u.portal_id,
                    }
                )
                old_unit_to_school_unit[u.id] = s_unit
                school_units_count += 1

            # إذا كانت وحدة لمقرر جامعي
            elif u.semester_subject:
                ss = u.semester_subject
                c = ss.course if hasattr(ss, 'course') and ss.course else (old_to_univ_course.get(ss.fk_subject_id) if ss.fk_subject_id else None)
                if c:
                    topic, _ = CourseTopic.objects.get_or_create(
                        id=u.id,
                        defaults={
                            'course': c,
                            'semester_subject': ss,
                            'name_ar': u.name_ar,
                            'name_en': u.name_en,
                            'order': u.order,
                            'is_active': u.is_active,
                            'portal_id': u.portal_id,
                        }
                    )
                    old_unit_to_course_topic[u.id] = topic
                    course_topics_count += 1

        print(f"✅ اكتمل ترحيل الوحدات: {school_units_count} وحدة مدرسية و {course_topics_count} موضوع جامعي.")

        # 3. ترحيل الدروس المدرسية
        all_lessons = Lesson.objects.all()
        for les in all_lessons:
            target_unit = old_unit_to_school_unit.get(les.unit_id)
            if target_unit:
                s_subj = target_unit.school_subject or (old_to_school_subject.get(les.subject_id) if les.subject_id else None)
                SchoolLesson.objects.get_or_create(
                    id=les.id,
                    defaults={
                        'unit': target_unit,
                        'school_subject': s_subj,
                        'name_ar': les.name_ar,
                        'name_en': les.name_en,
                        'order': les.order,
                        'is_active': les.is_active,
                        'portal_id': les.portal_id,
                    }
                )
                school_lessons_count += 1

        print(f"✅ اكتمل ترحيل الدروس المدرسية: {school_lessons_count} درس مدرسي.")

        # 4. ترحيل مخرجات التعلم
        all_los = LearningOutcome.objects.all()
        for lo in all_los:
            target_unit = old_unit_to_school_unit.get(lo.unit_id)
            if target_unit:
                s_subj = target_unit.school_subject or (old_to_school_subject.get(lo.subject_id) if lo.subject_id else None)
                SchoolLearningOutcome.objects.get_or_create(
                    id=lo.id,
                    defaults={
                        'unit': target_unit,
                        'school_subject': s_subj,
                        'code': lo.code,
                        'description': lo.description,
                        'order': lo.order,
                        'is_active': lo.is_active,
                        'portal_id': lo.portal_id,
                    }
                )
                school_los_count += 1
            else:
                # إذا كانت لمقرر جامعي
                target_topic = old_unit_to_course_topic.get(lo.unit_id)
                if target_topic:
                    CourseCLO.objects.get_or_create(
                        id=lo.id,
                        defaults={
                            'course': target_topic.course,
                            'topic': target_topic,
                            'clo_code': lo.code,
                            'description': lo.description,
                            'order': lo.order,
                            'is_active': lo.is_active,
                            'portal_id': lo.portal_id,
                        }
                    )
                    course_clos_count += 1

        print(f"✅ اكتمل ترحيل مخرجات التعلم: {school_los_count} مخرج مدرسي و {course_clos_count} مخرج جامعي (CLO).")

    print("\n" + "═" * 75)
    print("🎉 تم اكتمال الترحيل المعماري بنجاح تام وبدون أي أخطاء!")
    print("═" * 75 + "\n")

if __name__ == '__main__':
    run_migration()
