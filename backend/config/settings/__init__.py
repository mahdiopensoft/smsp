"""
نقطة الدخول الرئيسية للإعدادات
يحدد البيئة المناسبة (development/production/testing) ويستورد الإعدادات
"""
import os
from decouple import config

# تحديد البيئة من متغير البيئة أو الافتراضي للتطوير
DJANGO_ENV = config('DJANGO_ENV', default='development')

# استيراد الإعدادات الأساسية أولاً
from .base import *

# استيراد إعدادات الأمان
from .security import *

# استيراد إعدادات قاعدة البيانات
from .database import *

# استيراد إعدادات التطبيقات
from .apps import *

# استيراد إعدادات Middleware
from .middleware import *

# استيراد إعدادات REST Framework و JWT (يتضمن AUTH_MODE)
from .authentication_settings import *
from .rest_framework_settings import *

# استيراد إعدادات Channels و ASGI
from .channels import *

# استيراد إعدادات CORS
from .cors import *

# استيراد إعدادات الترجمة واللغات
from .internationalization import *

# استيراد إعدادات التخزين المؤقت
from .cache import *

# استيراد إعدادات البريد الإلكتروني
from .email import *

# استيراد إعدادات التسجيل (Logging)
from .logging_config import *

# استيراد إعدادات الهجرات
from .migrations import *

# استيراد إعدادات Celery
from .celery import *

# استيراد إعدادات البيئة المحددة
if DJANGO_ENV == 'production':
    from .environments.production import *
elif DJANGO_ENV == 'testing':
    from .environments.testing import *
else:
    from .environments.development import *

# طباعة البيئة الحالية للتأكيد (فقط في التطوير)
if DEBUG:
    # print(f"🔧 Django Environment: {DJANGO_ENV}")
    print(f"[DEV] Django Environment: {DJANGO_ENV}")


from .sync_setting import *
