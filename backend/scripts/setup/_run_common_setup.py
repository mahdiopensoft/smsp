"""
سكريبت تشغيل مؤقت لـ apply_common_setup_screen.py مع إعداد المسارات الصحيحة
"""
import sys
import os

# إضافة مجلد backend إلى PYTHONPATH  
# __file__ = scripts/setup/_run_common_setup.py
# لذا نصعد مستويين: setup -> scripts -> backend
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BACKEND_DIR الآن = backend/scripts، نصعد مستوى آخر
BACKEND_DIR = os.path.dirname(BACKEND_DIR)  # = backend
sys.path.insert(0, BACKEND_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

# استدعاء السكريبت الأصلي
from scripts.setup.apply_common_setup_screen import apply_common_setup_screens
apply_common_setup_screens()
