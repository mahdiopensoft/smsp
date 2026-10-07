"""
إعدادات الترجمة واللغات - Internationalization Settings
"""
import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ═══════════════════════════════════════════════════════════════════════════════
# 🌍 إعدادات اللغة - Language Settings
# ═══════════════════════════════════════════════════════════════════════════════

# اللغة الافتراضية
LANGUAGE_CODE = config('LANGUAGE_CODE', default='ar')

# اللغات المتاحة
LANGUAGES = [
    ('ar', 'العربية'),
    ('en', 'English'),
]

# تفعيل الترجمة
USE_I18N = True

# تفعيل التنسيق المحلي
USE_L10N = True

# مسارات ملفات الترجمة
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# ═══════════════════════════════════════════════════════════════════════════════
# ⏰ إعدادات المنطقة الزمنية - Timezone Settings
# ═══════════════════════════════════════════════════════════════════════════════

# المنطقة الزمنية
TIME_ZONE = config('TIME_ZONE', default='Asia/Riyadh')

# استخدام التوقيت العالمي في قاعدة البيانات
USE_TZ = True

# ═══════════════════════════════════════════════════════════════════════════════
# 📅 تنسيقات التاريخ والوقت - Date/Time Formats
# ═══════════════════════════════════════════════════════════════════════════════

# تنسيق التاريخ
DATE_FORMAT = 'Y-m-d'
SHORT_DATE_FORMAT = 'Y-m-d'

# تنسيق الوقت
TIME_FORMAT = 'H:i:s'
SHORT_TIME_FORMAT = 'H:i'

# تنسيق التاريخ والوقت معاً
DATETIME_FORMAT = 'Y-m-d H:i:s'
SHORT_DATETIME_FORMAT = 'Y-m-d H:i'

# أول يوم في الأسبوع (0 = الاثنين، 6 = الأحد)
FIRST_DAY_OF_WEEK = 6  # السبت
