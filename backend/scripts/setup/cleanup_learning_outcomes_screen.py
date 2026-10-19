"""
═══════════════════════════════════════════════════════════════════════════════
🗑️ سكريبت إزالة شاشة مخرجات التعلم من جدول الشاشات (Screen Table)
Remove Learning Outcomes Screen from System Sidebar & Screen Registry
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys

# 1. إعداد بيئة جانغو
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from OpenSoftCoreV41.screens.models.screen import Screen

def remove_learning_outcomes_screen():
    print("🚀 بدء إزالة شاشة مخرجات التعلم من السايد بار وجداول الشاشات...\n")

    # 1. البحث والحذف بالمعرف والرابط
    screens_to_delete = Screen.objects.filter(route__in=['learning-outcomes', 'reports-alignment-matrix'])
    count = screens_to_delete.count()
    if count > 0:
        for sc in screens_to_delete:
            print(f"  🗑️ تم حذف الشاشة: [ID: {sc.id}] {sc.name_ar} (Route: {sc.route})")
        screens_to_delete.delete()
    else:
        print("  ℹ️ لم يتم العثور على شاشات بالرابط 'learning-outcomes'")

    # التحقق من وجود الشاشة برقم ID=39
    sc39 = Screen.objects.filter(id=39).first()
    if sc39:
        print(f"  🗑️ تم حذف الشاشة برقم ID 39: {sc39.name_ar} (Route: {sc39.route})")
        sc39.delete()

    # 2. تنظيف حقل enable_learning_outcomes من شاشة الوحدات (ID 36) إن وجد
    sc_units = Screen.objects.filter(id=36).first() or Screen.objects.filter(route='units').first()
    if sc_units and sc_units.json_fields:
        fields = sc_units.json_fields.get('fields', [])
        new_fields = [f for f in fields if f.get('name') != 'enable_learning_outcomes']
        if len(fields) != len(new_fields):
            sc_units.json_fields['fields'] = new_fields
            sc_units.save()
            print("  ✨ تم تنظيف حقل 'تفعيل مخرجات التعلم' من شاشة الوحدات الدراسية.")

    print("\n✅ اكتملت عملية إزالة مخرجات التعلم من جدول الشاشات بنجاح!")

if __name__ == '__main__':
    remove_learning_outcomes_screen()
