"""
═══════════════════════════════════════════════════════════════════════════════
🏛️🏫 سكريبت فصل وضبط شاشات السايد بار إلى قائمتين مستقلتين تماماً:
    1. 🏫 تهيئة المدارس (Schools Setup)
    2. 🏛️ تهيئة الجامعات (Universities Setup)
    3. 🌍 الهيكل الجغرافي والإقليمي (Geographical Hierarchy)
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import django

# إعداد بيئة جانغو
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from update_academic_screens import update_academic_screens

if __name__ == '__main__':
    update_academic_screens()
