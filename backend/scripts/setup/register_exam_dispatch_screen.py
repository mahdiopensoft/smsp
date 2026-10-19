"""
═══════════════════════════════════════════════════════════════════════════════
🖥️ سكريبت تسجيل شاشة "توزيع وتصدير الاختبارات" في OpenSoftCore Screen Engine
   Screen Registration: Exam Distribution & Scheduled Export Screen
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

def register_exam_dispatch_screen():
    print("🚀 جاري تسجيل وضبط شاشة 'توزيع وتصدير الاختبارات' في قاعدة بيانات OpenSoftCore...\n")

    dispatch_fields = [
        {"icon": "format-title", "name": "title", "index": 1, "label": "عنوان مهمة التوزيع", "required": True},
        {"icon": "file-document-outline", "name": "exam", "index": 2, "label": "الاختبار المعتمد", "required": True, "name_list": "Exam"},
        {"icon": "sitemap", "name": "target_level", "index": 3, "label": "مستوى الاستهداف الهرمي"},
        {"icon": "clock-start", "name": "dispatch_at", "index": 4, "label": "موعد إرسال الحزمة"},
        {"icon": "lock-open-outline", "name": "accessible_from", "index": 5, "label": "موعد إتاحة محتوى الأسئلة للطباعة"},
        {"icon": "timer-sand", "name": "exam_start_at", "index": 6, "label": "موعد بدء الامتحان الرسمي"},
        {"icon": "timer-off", "name": "exam_end_at", "index": 7, "label": "موعد انتهاء الامتحان وقفل التسليم"},
        {"icon": "printer", "name": "delivery_mode", "index": 8, "label": "نمط التسليم والتنفيذ"},
        {"icon": "shield-lock", "name": "is_encrypted", "index": 9, "label": "تشفير محتوى الأسئلة حتى موعد الإتاحة"},
        {"icon": "auto-fix", "name": "auto_unlock", "index": 10, "label": "فتح الأسئلة تلقائياً عند حلول الوقت"},
        {"icon": "check-circle-outline", "name": "status", "index": 11, "label": "حالة المهمة"},
        {"icon": "note-text", "name": "notes", "index": 12, "label": "ملاحظات وتعليمات للمدارس"},
    ]

    # البحث عن الشاشة إن كانت موجودة مسبقاً لتفادي التكرار
    screen = Screen.objects.filter(route="exam-dispatch").first()
    if not screen:
        screen = Screen.objects.filter(component="ExamDispatchView").first()

    if screen:
        screen.name_ar = "توزيع وتصدير الاختبارات"
        screen.name_en = "Exam Distribution & Export"
        screen.route = "exam-dispatch"
        screen.component = "ExamDispatchView"
        screen.path = "exam-dispatch"
        screen.fk_parent_screen = None
        screen.screen_type = 1
        screen.is_active = True
        screen.is_report = False
        screen.icon = "send-clock-outline"
        screen.type_of_screen = 3
        screen.type_of_main_system = "access-login-role-unified-educational-platform"
        screen.company_level = 20
        screen.for_admin = True
        screen.for_ministry = True
        screen.for_governorate = True
        screen.for_directorate = True
        screen.for_region = False
        screen.for_company = False
        screen.for_college = False
        screen.fk_default_system_id = 3  # نظام 3: التقييم والاختبارات
        screen.order_in_default_system = 6  # بعد سجلات الممتحنين (order 5)
        screen.view = "ExamDistributionMVS"
        screen.json_fields = {
            "fields": dispatch_fields,
            "main_model": "ExamDistribution"
        }
        screen.save()
        print(f" ✅ تم تحديث الشاشة بنجاح: ID={screen.id} - '{screen.name_ar}' تحت نظام التقييم والاختبارات (System ID: 3)")
    else:
        screen = Screen.objects.create(
            name_ar="توزيع وتصدير الاختبارات",
            name_en="Exam Distribution & Export",
            route="exam-dispatch",
            component="ExamDispatchView",
            path="exam-dispatch",
            fk_parent_screen=None,
            screen_type=1,
            is_active=True,
            is_report=False,
            icon="send-clock-outline",
            type_of_screen=3,
            type_of_main_system="access-login-role-unified-educational-platform",
            company_level=20,
            for_admin=True,
            for_ministry=True,
            for_governorate=True,
            for_directorate=True,
            for_region=False,
            for_company=False,
            for_college=False,
            fk_default_system_id=3,  # نظام 3: التقييم والاختبارات
            order_in_default_system=6,
            view="ExamDistributionMVS",
            json_fields={
                "fields": dispatch_fields,
                "main_model": "ExamDistribution"
            }
        )
        print(f" ✅ تم إنشاء وتسجيل الشاشة بنجاح: ID={screen.id} - '{screen.name_ar}' تحت نظام التقييم والاختبارات (System ID: 3)")

    print(f"\n📊 تفاصيل الشاشة المسجلة:")
    print(f"   • الاسم: {screen.name_ar} ({screen.name_en})")
    print(f"   • المسار (Path/Route): {screen.route}")
    print(f"   • اسم المكون الأمامي (Component): {screen.component}")
    print(f"   • النظام التابع له: التقييم والاختبارات (ID: {screen.fk_default_system_id})")
    print(f"   • الترتيب في السايد بار: {screen.order_in_default_system}")
    print(f"   • الـ MVS المسؤول: {screen.view}")
    print(f"   • الصلاحيات: مدير (Admin), وزارة (Ministry), محافظات (Governorate), مديريات (Directorate)")

if __name__ == '__main__':
    register_exam_dispatch_screen()
