"""
إعدادات البريد الإلكتروني - Email Settings
"""
from decouple import config

# ═══════════════════════════════════════════════════════════════════════════════
# 📧 إعدادات SMTP
# ═══════════════════════════════════════════════════════════════════════════════

# نوع الخادم
EMAIL_BACKEND = config(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.smtp.EmailBackend'
)

# خادم SMTP
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)

# بيانات المصادقة
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

# استخدام TLS/SSL
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)

# البريد الافتراضي للإرسال
DEFAULT_FROM_EMAIL = config(
    'DEFAULT_FROM_EMAIL',
    default='noreply@academicsystem.com'
)

# بريد المسؤولين
SERVER_EMAIL = config('SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)

# ═══════════════════════════════════════════════════════════════════════════════
# 👥 قائمة المسؤولين (لتلقي رسائل الأخطاء)
# ═══════════════════════════════════════════════════════════════════════════════
ADMINS_STR = config('ADMINS', default='')
ADMINS = [
    tuple(admin.split(':'))
    for admin in ADMINS_STR.split(',')
    if admin and ':' in admin
]

MANAGERS = ADMINS

# ═══════════════════════════════════════════════════════════════════════════════
# 🔧 إعدادات إضافية
# ═══════════════════════════════════════════════════════════════════════════════

# مهلة الاتصال بخادم SMTP (بالثواني)
EMAIL_TIMEOUT = config('EMAIL_TIMEOUT', default=30, cast=int)

# موضوع البريد الإلكتروني
EMAIL_SUBJECT_PREFIX = config('EMAIL_SUBJECT_PREFIX', default='[Academic System] ')

# ═══════════════════════════════════════════════════════════════════════════════
# 🔄 البريد في وضع التطوير
# ═══════════════════════════════════════════════════════════════════════════════
# في وضع التطوير، استخدم console backend لطباعة الرسائل
# يتم تفعيله في environments/development.py
