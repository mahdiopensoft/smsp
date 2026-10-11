"""
═══════════════════════════════════════════════════════════════════════════════
🎯 سكريبت تهيئة شاشات نظام التصحيح الضوئي والآلي (OMR) في OpenSoftCore
    تسجيل كافة شاشات التصحيح العشر تحت النظام رقم 4 (التصحيح الالي)
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import django

# إعداد بيئة عمل جانغو
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from OpenSoftCoreV41.screens.models.screen import Screen
from OpenSoftCoreV41.screens.models.system import System

def setup_omr_screens():
    print("🚀 بدء تهيئة وتسجيل شاشات التصحيح الضوئي OMR تحت النظام 4 (التصحيح الالي)...\n")

    # التأكد من وجود نظام التصحيح الآلي (ID: 4)
    omr_system, _ = System.objects.get_or_create(id=4, defaults={
        "name_ar": "التصحيح الالي",
        "name_en": "OMR Engine",
        "is_main": True,
        "is_deleted": False,
        "order": 4
    })
    omr_system.name_ar = "التصحيح الالي"
    omr_system.is_main = True
    omr_system.is_deleted = False
    omr_system.save()

    # قائمة الشاشات العشر الكاملة لنظام التصحيح
    screens_config = [
        {
            "route": "omr-dashboard",
            "name_ar": "لوحة تحكم التصحيح الضوئي",
            "name_en": "OMR Dashboard",
            "icon": "view-dashboard-outline",
            "order": 1,
            "component": "OMRDashboardView"
        },
        {
            "route": "omr-exams",
            "name_ar": "استلام الاختبارات والكشوفات",
            "name_en": "OMR Exams & Roster",
            "icon": "link-box-variant-outline",
            "order": 2,
            "component": "OMRExamsView"
        },
        {
            "route": "omr-template-builder",
            "name_ar": "مصمم قوالب التصحيح",
            "name_en": "OMR Template Builder",
            "icon": "draw-pen",
            "order": 3,
            "component": "OMRTemplateBuilderView"
        },
        {
            "route": "omr-templates",
            "name_ar": "مكتبة القوالب المعيارية",
            "name_en": "OMR Templates Library",
            "icon": "card-text-outline",
            "order": 4,
            "component": "OMRTemplatesView"
        },
        {
            "route": "omr-print-registry",
            "name_ar": "سجل الطباعة وتصدير الأوراق",
            "name_en": "OMR Print Registry",
            "icon": "printer-check",
            "order": 5,
            "component": "OMRPrintRegistryView"
        },
        {
            "route": "omr-scanner-lab",
            "name_ar": "مختبر المسح والتصحيح الضوئي",
            "name_en": "OMR Scanner Lab",
            "icon": "scanner",
            "order": 6,
            "component": "OMRScannerLabView"
        },
        {
            "route": "omr-verification",
            "name_ar": "المطابقة والتحقق الهندسي",
            "name_en": "OMR Quality Verification",
            "icon": "shield-check-outline",
            "order": 7,
            "component": "OMRVerificationView"
        },
        {
            "route": "omr-submissions",
            "name_ar": "سجل أوراق الإجابة المصححة",
            "name_en": "OMR Submissions",
            "icon": "file-document-check-outline",
            "order": 8,
            "component": "OMRSubmissionsView"
        },
        {
            "route": "omr-human-review",
            "name_ar": "المراجعة البشرية والتدقيق",
            "name_en": "OMR Human Review",
            "icon": "account-search-outline",
            "order": 9,
            "component": "OMRHumanReviewView"
        },
        {
            "route": "omr-gradebook",
            "name_ar": "كشف الدرجات ورصد النتائج",
            "name_en": "OMR Gradebook",
            "icon": "book-education-outline",
            "order": 10,
            "component": "OMRGradebookView"
        }
    ]

    # مسح أي مجلد قديم omr-system-folder كان يعزل الشاشات
    Screen.objects.filter(route="omr-system-folder").delete()

    for cfg in screens_config:
        screen = Screen.objects.filter(route=cfg["route"]).first()
        if not screen:
            screen = Screen(route=cfg["route"])
        
        screen.name_ar = cfg["name_ar"]
        screen.name_en = cfg["name_en"]
        screen.component = cfg["component"]
        screen.icon = cfg["icon"]
        screen.screen_type = 1  # Standard screen
        screen.fk_parent_screen = None  # Direct root item in sidebar
        screen.is_active = True
        screen.is_deleted = False
        screen.is_report = False
        screen.company_level = 20
        screen.for_admin = True
        screen.for_ministry = True
        screen.for_college = True
        screen.for_company = True
        screen.type_of_main_system = "access-login-role-unified-educational-platform"
        screen.fk_default_system_id = 4  # System 4: التصحيح الالي
        screen.order_in_default_system = cfg["order"]
        screen.save()

        print(f"  ✓ [{cfg['order']:02d}] تم تثبيت شاشة التصحيح: {screen.name_ar} (Route: {cfg['route']}) تحت النظام 4")

    print("\n🎉 تم تحديث كافة شاشات التصحيح الضوئي (10 شاشات) بنجاح تحت نظام «التصحيح الالي»!")

if __name__ == "__main__":
    setup_omr_screens()
