"""
═══════════════════════════════════════════════════════════════════════════════
🖥️ سكريبت تسجيل وضبط شاشات المدارس والجامعات المستقلة في OpenSoftCore
   Screen Registration Utility: School Subjects vs University Courses
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import django

# إعداد بيئة جانغو
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from OpenSoftCoreV41.screens.models.screen import Screen

def register_screens():
    print("🚀 جاري تسجيل وضبط الشاشات المستقلة للمدارس والجامعات في قاعدة البيانات...\n")

    # 1. شاشة (م) المواد الدراسية
    school_subject_fields = [
        {"icon": "abjad-arabic", "name": "name_ar", "index": 1, "label": "اسم المادة (عربي)", "required": True},
        {"icon": "alpha-e", "name": "name_en", "index": 2, "label": "اسم المادة (إنجليزي)"},
        {"icon": "barcode", "name": "subject_code", "index": 3, "label": "كود المادة الوزاري"},
        {"icon": "sort-numeric-ascending", "name": "subject_order", "index": 4, "label": "ترتيب المادة"},
        {"icon": "bank", "name": "is_ministerial", "index": 5, "label": "مادة وزارية"},
        {"icon": "file-tree", "name": "is_detailed", "index": 6, "label": "تفصيلي"},
        {"icon": "note-text", "name": "note", "index": 7, "label": "ملاحظات"},
        {"icon": "check-circle-outline", "name": "is_active", "index": 8, "label": "حالة التفعيل"},
    ]

    # البحث عن الشاشة الحالية للمواد لتحديثها وتفادي تعارض unique_component_per_parent
    sc_school = Screen.objects.filter(fk_parent_screen_id=72, component="SubjectsView").first()
    if not sc_school:
        sc_school = Screen.objects.filter(route__in=["subjects", "school-subjects"]).first()

    if sc_school:
        sc_school.name_ar = "المواد الدراسية"
        sc_school.name_en = "School Subjects"
        sc_school.view = "SchoolSubjectMVS"
        sc_school.json_fields = {
            "fields": school_subject_fields,
            "main_model": "SchoolSubject"
        }
        if hasattr(sc_school, 'main_model'):
            sc_school.main_model = "SchoolSubject"
        sc_school.save()
        print(f" ✅ تم تحديث شاشة المدارس: ID={sc_school.id} - '{sc_school.name_ar}' بنجاح! (SchoolSubjectMVS)")
    else:
        sc_school = Screen.objects.create(
            route="school-subjects",
            name_ar="المواد الدراسية",
            name_en="School Subjects",
            component="SchoolSubjectsView",
            path="school-subjects",
            fk_parent_screen_id=71,
            screen_type=1,
            is_active=True,
            is_report=False,
            icon="book-open-page-variant",
            type_of_screen=3,
            for_admin=True,
            for_ministry=True,
            for_college=False,
            fk_default_system_id=8,
            order_in_default_system=8,
            view="SchoolSubjectMVS",
            json_fields={
                "fields": school_subject_fields,
                "main_model": "SchoolSubject"
            }
        )
        print(f" ✅ تم إنشاء شاشة المدارس: ID={sc_school.id} - '{sc_school.name_ar}' (SchoolSubjectMVS)")

    # 2. شاشة (ج) المقررات الجامعية
    univ_course_fields = [
        {"icon": "barcode", "name": "course_code", "index": 1, "label": "كود المقرر الأكاديمي", "required": True},
        {"icon": "abjad-arabic", "name": "name_ar", "index": 2, "label": "اسم المقرر (عربي)", "required": True},
        {"icon": "alpha-e", "name": "name_en", "index": 3, "label": "اسم المقرر (إنجليزي)"},
        {"icon": "school", "name": "college", "index": 4, "label": "الكلية", "name_list": "College"},
        {"icon": "domain", "name": "department", "index": 5, "label": "القسم الأكاديمي", "name_list": "DepartmentByCollege"},
        {"icon": "counter", "name": "credit_hours", "index": 6, "label": "الساعات المعتمدة"},
        {"icon": "book-clock", "name": "lecture_hours", "index": 7, "label": "ساعات المحاضرة (نظري)"},
        {"icon": "flask", "name": "lab_hours", "index": 8, "label": "ساعات المختبر (عملي)"},
        {"icon": "link-variant", "name": "prerequisite_course", "index": 9, "label": "المتطلب السابق", "name_list": "UniversityCourse"},
        {"icon": "format-list-bulleted-type", "name": "course_type", "index": 10, "label": "نوع المتطلب"},
        {"icon": "text", "name": "description", "index": 11, "label": "الوصف ومفردات المقرر"},
        {"icon": "check-circle-outline", "name": "is_active", "index": 12, "label": "حالة التفعيل"},
    ]

    sc_univ = Screen.objects.filter(fk_parent_screen_id=72, component="UniversityCoursesView").first()
    if not sc_univ:
        sc_univ = Screen.objects.filter(route="university-courses").first()

    if sc_univ:
        sc_univ.name_ar = "المقررات الجامعية"
        sc_univ.name_en = "University Courses"
        sc_univ.component = "UniversityCoursesView"
        sc_univ.view = "UniversityCourseMVS"
        sc_univ.json_fields = {
            "fields": univ_course_fields,
            "main_model": "UniversityCourse"
        }
        if hasattr(sc_univ, 'main_model'):
            sc_univ.main_model = "UniversityCourse"
        sc_univ.save()
        print(f" ✅ تم تحديث شاشة المقررات الجامعية: ID={sc_univ.id} - '{sc_univ.name_ar}' (UniversityCourseMVS)")
    else:
        sc_univ = Screen.objects.create(
            route="university-courses",
            name_ar="المقررات الجامعية",
            name_en="University Courses",
            component="UniversityCoursesView",
            path="university-courses",
            fk_parent_screen_id=72,
            screen_type=1,
            is_active=True,
            is_report=False,
            icon="book-education",
            type_of_screen=3,
            for_admin=True,
            for_ministry=True,
            for_college=True,
            fk_default_system_id=8,
            order_in_default_system=7,
            view="UniversityCourseMVS",
            json_fields={
                "fields": univ_course_fields,
                "main_model": "UniversityCourse"
            }
        )
        print(f" ✅ تم إنشاء شاشة المقررات الجامعية: ID={sc_univ.id} - '{sc_univ.name_ar}' (UniversityCourseMVS)")

    print("\n🎉 تم تسجيل وضبط الشاشات بنجاح في نظام OpenSoftCore بدون أي تعارض!")

if __name__ == '__main__':
    register_screens()
