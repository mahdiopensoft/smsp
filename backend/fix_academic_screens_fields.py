"""
═══════════════════════════════════════════════════════════════════════════════
🔧 سكريبت تحديث حقول الشاشات الأكاديمية في OpenSoftCore
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from update_academic_screens import update_academic_screens

if __name__ == '__main__':
    update_academic_screens()
