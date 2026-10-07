"""
🏭 إعدادات بيئة الإنتاج - Production Settings
═══════════════════════════════════════════════════════════════════════════════
⚠️ هذه الإعدادات تُطبَّق تلقائياً عندما DJANGO_ENV=production في .env

الإعدادات هنا تُعزز (override) الإعدادات الأساسية في security.py
بقيم آمنة قسرية — حتى لو كان .env يحتوي على قيم خاطئة.
═══════════════════════════════════════════════════════════════════════════════
"""
import sys
import logging

from decouple import config

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# 🛡️ التحقق من المتطلبات الإلزامية
# ═══════════════════════════════════════════════════════════════════════════════

# المفتاح السري — يجب أن يكون قوياً في الإنتاج
_SECRET_KEY = config('SECRET_KEY', default='')
if 'insecure' in _SECRET_KEY.lower() or len(_SECRET_KEY) < 30:
    raise RuntimeError(
        "\n\n"
        "🚨 خطأ أمني حرج!\n"
        "═══════════════════════════════════════════════════════════════\n"
        "المفتاح السري (SECRET_KEY) غير آمن للإنتاج!\n"
        "يجب أن يكون:\n"
        "  - فريد وعشوائي\n"
        "  - 50 حرف على الأقل\n"
        "  - لا يحتوي على كلمة 'insecure'\n\n"
        "ولّد مفتاح جديد:\n"
        '  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"\n'
        "═══════════════════════════════════════════════════════════════\n"
    )


# ═══════════════════════════════════════════════════════════════════════════════
# 🔐 فرض إعدادات الأمان — Security Overrides
# ═══════════════════════════════════════════════════════════════════════════════

# وضع التصحيح — مغلق قسرياً
DEBUG = False

# ─── Cookies عبر HTTPS فقط ─────────────────────────────────────
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ─── HTTPS Enforcement ──────────────────────────────────────────
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)

# ─── HSTS — إجبار HTTPS لمدة سنة ───────────────────────────────
SECURE_HSTS_SECONDS = 31536000  # سنة كاملة
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=False, cast=bool)

# ─── Security Headers ──────────────────────────────────────────
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'

# ─── Proxy SSL (إذا كنت خلف Nginx/Load Balancer) ───────────────
USE_PROXY_SSL = config('USE_PROXY_SSL', default=False, cast=bool)
if USE_PROXY_SSL:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# ═══════════════════════════════════════════════════════════════════════════════
# 🌐 CORS — مقيّد في الإنتاج
# ═══════════════════════════════════════════════════════════════════════════════

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOWED_ORIGINS يُقرأ من .env (CORS_ALLOWED_ORIGINS)


# ═══════════════════════════════════════════════════════════════════════════════
# 📋 تسجيل السجلات — Production Logging
# ═══════════════════════════════════════════════════════════════════════════════

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'production': {
            'format': '[{asctime}] {levelname} {name} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'production',
        },
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/security.log',
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 5,
            'formatter': 'production',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console', 'security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        # Security loggers — write to file
        'security': {
            'handlers': ['console', 'security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'security.input': {
            'handlers': ['console', 'security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'security.audit': {
            'handlers': ['console', 'security_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# 🗄️ Cache — Redis for production
# ═══════════════════════════════════════════════════════════════════════════════

_REDIS_URL = config('REDIS_URL', default='')
if _REDIS_URL:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': _REDIS_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }


# ═══════════════════════════════════════════════════════════════════════════════
# ✅ تأكيد التحميل
# ═══════════════════════════════════════════════════════════════════════════════

logger.info("🏭 Production environment loaded — security hardened!")
