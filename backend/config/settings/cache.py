"""
إعدادات التخزين المؤقت - Cache Settings
"""
from decouple import config

# ═══════════════════════════════════════════════════════════════════════════════
# 🗄️ نوع التخزين المؤقت
# ═══════════════════════════════════════════════════════════════════════════════
CACHE_TYPE = config('CACHE_TYPE', default='memory')

if CACHE_TYPE == 'redis':
    # استخدام Redis للإنتاج
    REDIS_HOST = config('REDIS_HOST', default='localhost')
    REDIS_PORT = config('REDIS_PORT', default='6379')
    REDIS_DB = config('REDIS_CACHE_DB', default='1')
    
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}',
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            },
            'KEY_PREFIX': config('CACHE_KEY_PREFIX', default='qas'),
            'TIMEOUT': config('CACHE_TIMEOUT', default=300, cast=int),
        },
    }
    
    # استخدام Redis للجلسات أيضاً
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'default'
    
elif CACHE_TYPE == 'database':
    # استخدام قاعدة البيانات
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'cache_table',
            'TIMEOUT': config('CACHE_TIMEOUT', default=300, cast=int),
        },
    }
    
elif CACHE_TYPE == 'file':
    # استخدام الملفات
    from pathlib import Path
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': str(BASE_DIR / 'cache'),
            'TIMEOUT': config('CACHE_TIMEOUT', default=300, cast=int),
        },
    }
    
else:
    # استخدام الذاكرة (للتطوير)
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
            'TIMEOUT': config('CACHE_TIMEOUT', default=300, cast=int),
        },
    }

# ═══════════════════════════════════════════════════════════════════════════════
# 🔧 إعدادات إضافية للتخزين المؤقت
# ═══════════════════════════════════════════════════════════════════════════════

# تخزين مؤقت للقوالب
CACHE_TEMPLATES = config('CACHE_TEMPLATES', default=False, cast=bool)

# مدة التخزين المؤقت للصفحات (بالثواني)
CACHE_MIDDLEWARE_SECONDS = config('CACHE_MIDDLEWARE_SECONDS', default=600, cast=int)

# بادئة مفتاح التخزين المؤقت
CACHE_MIDDLEWARE_KEY_PREFIX = config('CACHE_KEY_PREFIX', default='qas')
