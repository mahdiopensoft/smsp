"""
═══════════════════════════════════════════════════════════════════════════════
🗑️ سكريبت تنظيف وإزالة الشاشات والنماذج غير المطلوبة في منظومة تهيئة المعاهد
Unneeded Institute Screens & Models Removal Script:
1. شروط وضوابط القبول والتسجيل (InstituteAdmissionRequirement)
2. الدفعات والأفواج (InstituteBatch)
3. الدورات التدريبية القصيرة (InstituteShortCourse)
4. تحقيق المهنة والمسارات الخاصة (InstituteSpecialTrack)
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import shutil

# 1. إعداد بيئة جانغو
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.db import connection
from OpenSoftCoreV41.screens.models.screen import Screen

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'frontend', 'src', 'pages', 'SystemAdmin', 'Institutes'))

TARGET_ROUTES = [
    'institutes-admission-requirements',
    'institutes-batches',
    'institutes-short-courses',
    'institutes-special-tracks',
]

TARGET_COMPONENTS = [
    'InstituteAdmissionRequirementsView',
    'InstituteBatchesView',
    'InstituteShortCoursesView',
    'InstituteSpecialTracksView',
]

FRONTEND_FOLDERS = [
    'InstituteAdmissionRequirements',
    'InstituteBatches',
    'InstituteShortCourses',
    'InstituteSpecialTracks',
]

BACKEND_FILES = [
    # Models
    os.path.join(BASE_DIR, 'academic', 'models', 'institutes', 'InstituteAdmissionRequirement.py'),
    os.path.join(BASE_DIR, 'academic', 'models', 'institutes', 'InstituteBatch.py'),
    os.path.join(BASE_DIR, 'academic', 'models', 'institutes', 'InstituteShortCourse.py'),
    os.path.join(BASE_DIR, 'academic', 'models', 'institutes', 'InstituteSpecialTrack.py'),

    # Serializers
    os.path.join(BASE_DIR, 'academic', 'serializers', 'institutes', 'InstituteAdmissionRequirement.py'),
    os.path.join(BASE_DIR, 'academic', 'serializers', 'institutes', 'InstituteBatch.py'),
    os.path.join(BASE_DIR, 'academic', 'serializers', 'institutes', 'InstituteShortCourse.py'),
    os.path.join(BASE_DIR, 'academic', 'serializers', 'institutes', 'InstituteSpecialTrack.py'),

    # APIs
    os.path.join(BASE_DIR, 'academic', 'apis', 'institutes', 'InstituteAdmissionRequirementMVS.py'),
    os.path.join(BASE_DIR, 'academic', 'apis', 'institutes', 'InstituteBatchMVS.py'),
    os.path.join(BASE_DIR, 'academic', 'apis', 'institutes', 'InstituteShortCourseMVS.py'),
    os.path.join(BASE_DIR, 'academic', 'apis', 'institutes', 'InstituteSpecialTrackMVS.py'),
]

DATABASE_TABLES = [
    'institutes_admission_requirement',
    'institutes_batch',
    'institutes_short_course',
    'institutes_special_track',
]


def run_cleanup():
    print("🚀 بدء عملية إزالة الشاشات والنماذج غير المطلوبة لمنظومة المعاهد...")

    # 1. حذف الشاشات من جدول Screen في قاعدة البيانات
    print("\n1️⃣ حذف سجلات الشاشات من السايد بار وقاعدة البيانات:")
    deleted_screens_count = 0
    for route in TARGET_ROUTES:
        screens = Screen.objects.filter(route=route)
        for s in screens:
            print(f"  ❌ حذف الشاشة: {s.name_ar} (Route: {s.route}, ID: {s.id})")
            s.delete()
            deleted_screens_count += 1

    for comp in TARGET_COMPONENTS:
        screens = Screen.objects.filter(component=comp)
        for s in screens:
            print(f"  ❌ حذف الشاشة بواسطة Component: {s.name_ar} ({s.component})")
            s.delete()
            deleted_screens_count += 1

    print(f"  ✅ تم حذف {deleted_screens_count} سجل من جدول الشاشات.")

    # 2. حذف مجلدات الفرونت إند
    print("\n2️⃣ حذف مجلدات شاشات الفرونت إند:")
    for folder in FRONTEND_FOLDERS:
        folder_path = os.path.join(FRONTEND_DIR, folder)
        if os.path.exists(folder_path):
            try:
                shutil.rmtree(folder_path)
                print(f"  🗑️ تم حذف مجلد الفرونت: {folder}")
            except Exception as e:
                print(f"  ⚠️ تعذر حذف المجلد {folder}: {e}")
        else:
            print(f"  ℹ️ المجلد غير موجود مسبقاً: {folder}")

    # 3. حذف ملفات الباك إند (Models, Serializers, APIs)
    print("\n3️⃣ حذف ملفات الباك إند:")
    for file_path in BACKEND_FILES:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"  🗑️ تم حذف ملف: {os.path.basename(file_path)}")
            except Exception as e:
                print(f"  ⚠️ تعذر حذف الملف {os.path.basename(file_path)}: {e}")
        else:
            print(f"  ℹ️ الملف غير موجود مسبقاً: {os.path.basename(file_path)}")

    # 4. حذف الجداول من قاعدة بيانات PostgreSQL
    print("\n4️⃣ حذف الجداول من قاعدة البيانات (إن وجدت):")
    with connection.cursor() as cursor:
        for table in DATABASE_TABLES:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
                print(f"  🗑️ تم إسقاط جدول قاعدة البيانات: {table}")
            except Exception as e:
                print(f"  ⚠️ خطأ أثناء إسقاط الجدول {table}: {e}")

    # 5. إعادة ترتيب الشاشات المتبقية تحت تهيئة المعاهد
    print("\n5️⃣ إعادة ترتيب الشاشات المتبقية تحت 'تهيئة المعاهد' (ID=73):")
    remaining_screens = Screen.objects.filter(fk_parent_screen_id=73).order_by('order_in_default_system', 'id')
    order = 1
    for sc in remaining_screens:
        sc.order_in_default_system = order
        sc.save()
        print(f"  ✓ [{order}] {sc.name_ar} (Route: {sc.route})")
        order += 1

    print("\n🎉 تمت عملية التنظيف والإزالة بنجاح تام!")


if __name__ == '__main__':
    run_cleanup()
