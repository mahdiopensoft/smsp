"""
═══════════════════════════════════════════════════════════════════════════════
🖥️ سكريبت تسجيل شاشة "المحذوفات من المنهج" في OpenSoftCore Screen Engine
   Screen Registration: Curriculum Exclusions & Omitted Topics Screen
   نظام التقييم والاختبارات (System ID: 3)
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

def register_curriculum_exclusions_screen():
    print("🚀 جاري تسجيل وضبط شاشة 'المحذوفات من المنهج' في قاعدة بيانات OpenSoftCore...\n")

    exclusion_fields = [
        {"icon": "calendar-range", "name": "academic_year", "index": 1, "label": "العام الدراسي", "required": True, "name_list": "AcademicYear"},
        {"icon": "domain", "name": "institution_type", "index": 2, "label": "نوع المؤسسة التعليمية", "required": True},
        {"icon": "book-open-outline", "name": "subject", "index": 3, "label": "المادة الدراسية", "name_list": "Subject"},
        {"icon": "format-list-bulleted", "name": "exclusion_type", "index": 4, "label": "نطاق الحذف (وحدة / درس)", "required": True},
        {"icon": "folder-table", "name": "unit", "index": 5, "label": "الوحدة المحذوفة", "name_list": "Unit"},
        {"icon": "file-document-outline", "name": "lesson", "index": 6, "label": "الدرس المحذوف", "name_list": "Lesson"},
        {"icon": "note-text", "name": "reason", "index": 7, "label": "قرار أو مبرر الحذف"},
        {"icon": "check-circle-outline", "name": "is_active", "index": 8, "label": "الحالة"},
    ]

    # البحث عن الشاشة إن كانت موجودة مسبقاً
    screen = Screen.objects.filter(route="curriculum-exclusions").first()
    if not screen:
        screen = Screen.objects.filter(component="CurriculumExclusionsView").first()

    if screen:
        screen.name_ar = "المحذوفات من المنهج"
        screen.name_en = "Curriculum Exclusions"
        screen.route = "curriculum-exclusions"
        screen.component = "CurriculumExclusionsView"
        screen.path = "curriculum-exclusions"
        screen.fk_parent_screen = None
        screen.screen_type = 1
        screen.is_active = True
        screen.is_report = False
        screen.icon = "book-remove-outline"
        screen.type_of_screen = 3
        screen.type_of_main_system = "access-login-role-unified-educational-platform"
        screen.company_level = 20
        screen.for_admin = True
        screen.for_ministry = True
        screen.for_governorate = True
        screen.for_directorate = True
        screen.for_region = False
        screen.for_company = False
        screen.for_college = True
        screen.fk_default_system_id = 3  # نظام 3: التقييم والاختبارات
        screen.order_in_default_system = 7
        screen.view = "CurriculumExclusionMVS"
        screen.json_fields = {
            "fields": exclusion_fields,
            "main_model": "CurriculumExclusion"
        }
        screen.save()
        print(f" ✅ تم تحديث الشاشة بنجاح: ID={screen.id} - '{screen.name_ar}' تحت نظام التقييم والاختبارات (System ID: 3)")
    else:
        screen = Screen.objects.create(
            name_ar="المحذوفات من المنهج",
            name_en="Curriculum Exclusions",
            route="curriculum-exclusions",
            component="CurriculumExclusionsView",
            path="curriculum-exclusions",
            fk_parent_screen=None,
            screen_type=1,
            is_active=True,
            is_report=False,
            icon="book-remove-outline",
            type_of_screen=3,
            type_of_main_system="access-login-role-unified-educational-platform",
            company_level=20,
            for_admin=True,
            for_ministry=True,
            for_governorate=True,
            for_directorate=True,
            for_region=False,
            for_company=False,
            for_college=True,
            fk_default_system_id=3,  # نظام 3: التقييم والاختبارات
            order_in_default_system=7,
            view="CurriculumExclusionMVS",
            json_fields={
                "fields": exclusion_fields,
                "main_model": "CurriculumExclusion"
            }
        )
        print(f" ✅ تم إنشاء وتسجيل الشاشة بنجاح: ID={screen.id} - '{screen.name_ar}' تحت نظام التقييم والاختبارات (System ID: 3)")

    print(f"\n📊 تفاصيل الشاشة المسجلة:")
    print(f"   • الاسم: {screen.name_ar} ({screen.name_en})")
    print(f"   • المسار (Route): {screen.route}")
    print(f"   • المكون الأمامي (Component): {screen.component}")
    print(f"   • النظام التابع له: التقييم والاختبارات (ID: {screen.fk_default_system_id})")
    print(f"   • الترتيب في السايد بار: {screen.order_in_default_system}")
    print(f"   • الـ MVS المسؤول: {screen.view}")

if __name__ == '__main__':
    register_curriculum_exclusions_screen()
