import os
import sys

# تحديد مسار المجلد الأساسي ومجلد الباك إند
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# استدعاء سكريبت التسجيل المباشر
from scripts.setup.register_all_reports_screens import register_all_reports_screens

if __name__ == "__main__":
    print("\n" + "═" * 70)
    print("  📊 أداة تسجيل شاشات التقارير الـ 15 في قاعدة بيانات OpenSoftCore")
    print("═" * 70 + "\n")
    register_all_reports_screens()

