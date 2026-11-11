"""
═══════════════════════════════════════════════════════════════════════════════
📊 سكريبت تسجيل وتهيئة كافة شاشات التقارير الـ 15 في قاعدة بيانات OpenSoftCore
    Script: Register All 15 Report Screens in OpenSoftCore Engine
    System: نظام التقارير (System ID: 5)
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import django

# إعداد المسارات وبيئة جانغو تلقائياً
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.apps import apps
from OpenSoftCoreV41.screens.models.screen import Screen
from OpenSoftCoreV41.screens.models.system import System


def register_all_reports_screens():
    print("=" * 80)
    print("🚀 بدء تهيئة وتسجيل شاشات التقارير (15 شاشة) في قاعدة البيانات...")
    print("=" * 80)

    # 1. التأكد من وجود نظام التقارير (System ID: 5)
    reports_system, created = System.objects.get_or_create(
        id=5,
        defaults={
            "name_ar": "التقارير",
            "name_en": "Reports",
            "is_main": True,
            "is_deleted": False,
            "order": 5,
        }
    )
    if created:
        print("✅ تم إنشاء نظام التقارير (System ID: 5) بنجاح.")
    else:
        reports_system.name_ar = "التقارير"
        reports_system.name_en = "Reports"
        reports_system.is_main = True
        reports_system.is_deleted = False
        reports_system.save()
        print("ℹ️ نظام التقارير (System ID: 5) موجود ومفعل.")

    # 2. قائمة الـ 15 شاشة للتقارير
    reports_screens_config = [
        {
            "route": "reports-rejected-questions",
            "name_ar": "تقرير الأسئلة المرفوضة",
            "name_en": "Rejected Questions Report",
            "component": "RejectedQuestionsReportView",
            "icon": "close-octagon",
            "order": 1,
            "view": "RejectedQuestionsReportMVS",
        },
        {
            "route": "reports-exam-quality",
            "name_ar": "تقرير جودة الاختبار",
            "name_en": "Exam Quality Report",
            "component": "ExamPapersReportView",
            "icon": "file-certificate-outline",
            "order": 2,
            "view": "ExamPapersReportMVS",
        },
        {
            "route": "reports-authors",
            "name_ar": "تقرير أداء المؤلفين",
            "name_en": "Authors Performance Report",
            "component": "AuthorsReportView",
            "icon": "account-star-outline",
            "order": 3,
            "view": "AuthorsReportMVS",
        },
        {
            "route": "reports-curriculum",
            "name_ar": "تقرير التغطية الأكاديمية",
            "name_en": "Curriculum Coverage Report",
            "component": "CurriculumReportView",
            "icon": "book-open-page-variant-outline",
            "order": 4,
            "view": "CurriculumReportMVS",
        },
        {
            "route": "reports-bank-status",
            "name_ar": "تقرير حالة بنك الأسئلة",
            "name_en": "Bank Status Report",
            "component": "BankStatusReportView",
            "icon": "chart-box-outline",
            "order": 5,
            "view": "BankStatusReportMVS",
        },
        {
            "route": "reports-alignment-matrix",
            "name_ar": "مصفوفة المواءمة الأكاديمية (CLOs)",
            "name_en": "CLO Alignment Matrix Report",
            "component": "AlignmentMatrixReportView",
            "icon": "target-variant",
            "order": 6,
            "view": "AlignmentMatrixReportMVS",
        },
        {
            "route": "reports-regional",
            "name_ar": "التقرير الإقليمي والجغرافي",
            "name_en": "Regional & Geographic Report",
            "component": "RegionalReportView",
            "icon": "map-legend",
            "order": 7,
            "view": "RegionalReportMVS",
        },
        {
            "route": "reports-questions-detail",
            "name_ar": "تقرير الأسئلة التفصيلي",
            "name_en": "Questions Detail Report",
            "component": "QuestionsDetailReportView",
            "icon": "file-document-outline",
            "order": 8,
            "view": "QuestionsDetailReportMVS",
        },
        {
            "route": "reports-exams-generated",
            "name_ar": "تقرير الاختبارات المولدة",
            "name_en": "Exams Generated Report",
            "component": "ExamsGeneratedReportView",
            "icon": "file-multiple-outline",
            "order": 9,
            "view": "ExamsGeneratedReportMVS",
        },
        {
            "route": "reports-exam-distribution",
            "name_ar": "تقرير توزيع وإرسال الاختبارات",
            "name_en": "Exam Distribution Report",
            "component": "ExamDistributionReportView",
            "icon": "truck-delivery",
            "order": 10,
            "view": "ExamDistributionReportMVS",
        },
        {
            "route": "reports-curriculum-exclusions",
            "name_ar": "تقرير المحذوفات من المنهج",
            "name_en": "Curriculum Exclusions Report",
            "component": "CurriculumExclusionsReportView",
            "icon": "book-cancel",
            "order": 11,
            "view": None,
        },
        {
            "route": "reports-student-registrations",
            "name_ar": "تقرير تسجيلات الطلاب",
            "name_en": "Student Registrations Report",
            "component": "StudentRegistrationsReportView",
            "icon": "account-check",
            "order": 12,
            "view": None,
        },
        {
            "route": "reports-students",
            "name_ar": "تقرير الطلاب",
            "name_en": "Students Report",
            "component": "StudentsReportView",
            "icon": "account-school",
            "order": 13,
            "view": None,
        },
        {
            "route": "reports-omr-results",
            "name_ar": "تقرير نتائج التصحيح الآلي (OMR)",
            "name_en": "OMR Results Report",
            "component": "OMRResultsReportView",
            "icon": "checkbox-marked-circle-auto-outline",
            "order": 14,
            "view": None,
        },
        {
            "route": "reports-omr-review",
            "name_ar": "تقرير أسئلة مراجعة التصحيح (OMR)",
            "name_en": "OMR Review Questions Report",
            "component": "OMRReviewQuestionsReportView",
            "icon": "file-eye",
            "order": 15,
            "view": None,
        },
    ]

    # جلب نماذج الصلاحيات إن وجدت لربطها تلقائياً
    ScreenPermission = None
    GroupScreenPermission = None
    try:
        ScreenPermission = apps.get_model('screens', 'ScreenPermission')
        GroupScreenPermission = apps.get_model('screens', 'GroupScreenPermission')
    except Exception as e:
        print(f"⚠️ تنبيه حول الصلاحيات: {e}")

    # جلب المعرفات الخاصة بالمجموعات الإدارية المتاحة لربط الصلاحيات بها
    group_ids = []
    if GroupScreenPermission:
        group_ids = list(GroupScreenPermission.objects.values_list('group_id', flat=True).distinct())
        if not group_ids:
            group_ids = [1]

    created_count = 0
    updated_count = 0

    print("\n📋 معالجة وتسجيل الشاشات:")
    for cfg in reports_screens_config:
        route = cfg["route"]
        screen = Screen.objects.filter(route=route).first()

        is_new = False
        if not screen:
            screen = Screen(route=route)
            is_new = True

        screen.name_ar = cfg["name_ar"]
        screen.name_en = cfg["name_en"]
        screen.component = cfg["component"]
        screen.path = cfg.get("path", route)
        screen.icon = cfg["icon"]
        screen.screen_type = 1
        screen.fk_parent_screen = None
        screen.is_active = True
        screen.is_deleted = False
        screen.is_report = True
        screen.type_of_screen = 3
        screen.type_of_main_system = "access-login-role-unified-educational-platform"
        screen.company_level = 20
        screen.for_admin = True
        screen.for_ministry = True
        screen.for_governorate = True
        screen.for_directorate = True
        screen.for_college = True
        screen.for_company = True
        screen.fk_default_system_id = 5
        screen.order_in_default_system = cfg["order"]
        screen.view = cfg.get("view")
        screen.save()

        # ضبط الصلاحيات الافتراضية للشاشة
        if ScreenPermission and GroupScreenPermission:
            try:
                perm, _ = ScreenPermission.objects.get_or_create(
                    fk_screen=screen,
                    operation_type=1  # 1: عرض / Show
                )
                for gid in group_ids:
                    GroupScreenPermission.objects.get_or_create(
                        group_id=gid,
                        fk_screen_permission=perm,
                        defaults={'is_related': False}
                    )
            except Exception as pe:
                print(f"    ⚠️ تعذر ضبط صلاحية الشاشة {screen.name_ar}: {pe}")

        if is_new:
            created_count += 1
            print(f"  [+] [جديد] تم إنشاء الشاشة: {screen.name_ar} ({screen.route}) - ID: {screen.id}")
        else:
            updated_count += 1
            print(f"  [✓] [تحديث] تم تحديث الشاشة: {screen.name_ar} ({screen.route}) - ID: {screen.id}")

    print("\n" + "=" * 80)
    print(f"🎉 تمت العملية بنجاح!")
    print(f"   • إجمالي الشاشات المسجلة: {len(reports_screens_config)}")
    print(f"   • شاشات تم إنشاؤها: {created_count}")
    print(f"   • شاشات تم تحديثها: {updated_count}")
    print(f"   • النظام التابع: نظام التقارير (System ID: 5)")
    print("=" * 80)


if __name__ == "__main__":
    register_all_reports_screens()
