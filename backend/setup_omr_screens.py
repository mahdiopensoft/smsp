import os
import sys
import django

# إعداد بيئة جانغو
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from OpenSoftCoreV41.screens.models.screen import Screen

def setup_omr_sidebar():
    print("🚀 بدء التحديث لشاشات نظام التصحيح الضوئي (OMR)...\n")

    # 1. إنشاء المجلد الرئيسي لـ OMR
    # Screen IDs for OpenSoftCore are usually unique, we'll try to find an existing one or create a new one.
    omr_folder_route = "omr-system-folder"
    omr_folder, created = Screen.objects.get_or_create(route=omr_folder_route, defaults={
        "name_ar": "نظام التصحيح الضوئي",
        "name_en": "OMR System",
        "icon": "scanner",
        "screen_type": 3,  # 3 = Folder
        "is_active": True,
        "type_of_main_system": "access-login-role-unified-educational-platform",
        "company_level": 20,
        "for_admin": True,
        "fk_default_system_id": 8,
        "order_in_default_system": 10
    })
    
    if not created:
        omr_folder.name_ar = "نظام التصحيح الضوئي"
        omr_folder.name_en = "OMR System"
        omr_folder.icon = "scanner"
        omr_folder.screen_type = 3
        omr_folder.save()
    
    print(f" ✅ تم ضبط المجلد الرئيسي لـ OMR (ID={omr_folder.id})")

    # 2. الشاشات المتسلسلة
    screens_config = [
        {"route": "omr-dashboard", "name_ar": "لوحة التحكم", "icon": "view-dashboard", "order": 1, "component": "OMRDashboardView"},
        {"route": "omr-exams", "name_ar": "استلام الاختبارات", "icon": "inbox-arrow-down", "order": 2, "component": "OMRExamsView"},
        {"route": "omr-template-builder", "name_ar": "مصمم القوالب", "icon": "draw-pen", "order": 3, "component": "OMRTemplateBuilderView"},
        {"route": "omr-templates", "name_ar": "إدارة القوالب", "icon": "file-document-multiple-outline", "order": 4, "component": "OMRTemplatesView"},
        {"route": "omr-print-registry", "name_ar": "سجل الطباعة وتصدير الأوراق", "icon": "printer", "order": 5, "component": "OMRPrintRegistryView"},
        {"route": "omr-scanner-lab", "name_ar": "مختبر المسح الضوئي", "icon": "scanner", "order": 6, "component": "OMRScannerLabView"},
        {"route": "omr-verification", "name_ar": "المطابقة والتحقق", "icon": "shield-check", "order": 7, "component": "OMRVerificationView"},
        {"route": "omr-submissions", "name_ar": "سجل الأوراق الممسوحة", "icon": "file-document-check", "order": 8, "component": "OMRSubmissionsView"},
        {"route": "omr-human-review", "name_ar": "المراجعة البشرية", "icon": "account-search", "order": 9, "component": "OMRHumanReviewView"},
        {"route": "omr-gradebook", "name_ar": "سجل الدرجات والترحيل", "icon": "book-education", "order": 10, "component": "OMRGradebookView"}
    ]

    for cfg in screens_config:
        screen, created = Screen.objects.get_or_create(route=cfg["route"], defaults={
            "name_ar": cfg["name_ar"],
            "name_en": cfg["route"].replace('-', ' ').title(),
            "component": cfg["component"],
            "fk_parent_screen": omr_folder,
            "screen_type": 1,  # 1 = Normal Screen
            "is_active": True,
            "icon": cfg["icon"],
            "company_level": 20,
            "for_admin": True,
            "fk_default_system_id": 8,
            "order_in_default_system": cfg["order"]
        })

        if not created:
            screen.name_ar = cfg["name_ar"]
            screen.icon = cfg["icon"]
            screen.fk_parent_screen = omr_folder
            screen.order_in_default_system = cfg["order"]
            screen.component = cfg["component"]
            screen.save()
            
        print(f"  ✓ [{cfg['order']}] تم تحديث شاشة: {screen.name_ar} (Route: {cfg['route']})")

    print("\n🎉 انتهى إعداد القائمة الجانبية بنجاح!")

if __name__ == "__main__":
    setup_omr_sidebar()
