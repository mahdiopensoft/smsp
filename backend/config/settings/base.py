"""
الإعدادات الأساسية - Base Settings
الإعدادات المشتركة بين جميع البيئات
"""
import os
from pathlib import Path
from decouple import config
# import pymysql

# pymysql.install_as_MySQLdb()
# ═══════════════════════════════════════════════════════════════════════════════
# 📁 المسارات الأساسية - Base Paths
# ═══════════════════════════════════════════════════════════════════════════════
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ═══════════════════════════════════════════════════════════════════════════════
# 🔧 الإعدادات الأساسية - Core Settings
# ═══════════════════════════════════════════════════════════════════════════════
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ═══════════════════════════════════════════════════════════════════════════════
# 👤 نموذج المستخدم المخصص - Custom User Model
# ═══════════════════════════════════════════════════════════════════════════════
AUTH_USER_MODEL = 'usermanager.User'

# ═══════════════════════════════════════════════════════════════════════════════
# 🏢 مستويات الشركة/المؤسسة - Company Levels
# ═══════════════════════════════════════════════════════════════════════════════

# استيراد إعدادات المستويات من ملف levels.py
from config.levels import CompanyLevelChoices, CompanyLevel, required_map, null_map, SettingLevel
COMPANY_LEVEL_CHOICES = CompanyLevelChoices
COMPANY_LEVEL = CompanyLevel
REQUIRED_MAP = required_map
NULL_MAP = null_map
SETTING_LEVEL = SettingLevel()

# ═══════════════════════════════════════════════════════════════════════════════
# 🔄 إعدادات الهجرات - Migration Settings
# ═══════════════════════════════════════════════════════════════════════════════
MIGRATION_MODULES = {
    'auth': None,  # تعطيل هجرات auth لأننا نستخدم نموذج مستخدم مخصص
}

# ═══════════════════════════════════════════════════════════════════════════════
# 📄 القوالب - Templates
# ═══════════════════════════════════════════════════════════════════════════════
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# 🔐 التحقق من كلمة المرور - Password Validation
# ═══════════════════════════════════════════════════════════════════════════════
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    # ─── Custom Validators (OpenSoftCoreV41) ───────────────────
    {
        'NAME': 'OpenSoftCoreV41.usermanager.validators.UppercaseValidator',
    },
    {
        'NAME': 'OpenSoftCoreV41.usermanager.validators.LowercaseValidator',
    },
    {
        'NAME': 'OpenSoftCoreV41.usermanager.validators.DigitValidator',
    },
    {
        'NAME': 'OpenSoftCoreV41.usermanager.validators.SpecialCharacterValidator',
    },
    {
        'NAME': 'OpenSoftCoreV41.usermanager.validators.NoRepeatingCharactersValidator',
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# 📁 الملفات الثابتة والوسائط - Static & Media Files
# ═══════════════════════════════════════════════════════════════════════════════
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
] if (BASE_DIR / 'static').exists() else []

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ═══════════════════════════════════════════════════════════════════════════════
# 📚 إعدادات API Documentation
# ═══════════════════════════════════════════════════════════════════════════════
API_TITLE = config('API_TITLE', default='Academic Management System API')
API_DESCRIPTION = config('API_DESCRIPTION', default='Professional Academic Management System')
API_VERSION = config('API_VERSION', default='1.0.0')

# # ═══════════════════════════════════════════════════════════════════════════════
# # � إعدادات Keycloak SSO (مطلوبة فقط عند AUTH_MODE=sso)
# # ═══════════════════════════════════════════════════════════════════════════════
# AUTH_MODE = config('AUTH_MODE', default='jwt')

# if AUTH_MODE == 'sso':
#     # ─────────────────────────────────────────────────────────────────────────────
#     # إعدادات Keycloak الإلزامية - يجب تعريفها في .env
#     # ─────────────────────────────────────────────────────────────────────────────
#     _required_keycloak_settings = [
#         'KEYCLOAK_SERVER_URL',
#         'KEYCLOAK_REALM', 
#         'KEYCLOAK_CLIENT_ID',
#         'KEYCLOAK_CLIENT_SECRET',
#         'KEYCLOAK_REDIRECT_URI',
#         'KEYCLOAK_POST_LOGOUT_REDIRECT_URI',
#     ]
    
#     # التحقق من وجود جميع الإعدادات المطلوبة
#     _missing = []
#     for setting in _required_keycloak_settings:
#         try:
#             config(setting)
#         except Exception:
#             _missing.append(setting)
    
#     if _missing:
#         raise ValueError(
#             f"❌ AUTH_MODE=sso يتطلب إعدادات Keycloak التالية في ملف .env:\n"
#             f"   {', '.join(_missing)}\n"
#             f"   يرجى إضافتها أو تغيير AUTH_MODE إلى 'jwt'"
#         )
    
#     # قراءة إعدادات Keycloak من .env
#     KEYCLOAK_SERVER_URL = config('KEYCLOAK_SERVER_URL')
#     KEYCLOAK_REALM = config('KEYCLOAK_REALM')
#     KEYCLOAK_CLIENT_ID = config('KEYCLOAK_CLIENT_ID')
#     KEYCLOAK_CLIENT_SECRET = config('KEYCLOAK_CLIENT_SECRET')
#     REDIRECT_URI = config('KEYCLOAK_REDIRECT_URI')
#     POST_LOGOUT_REDIRECT_URI = config('KEYCLOAK_POST_LOGOUT_REDIRECT_URI')
    
#     # إعداد تلقائي لـ Well-Known endpoint
#     KEYCLOAK_WELL_KNOWN = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/.well-known/openid-configuration"
    
#     # ─────────────────────────────────────────────────────────────────────────────
#     # العملاء المسموح بهم (Frontend Apps)
#     # ─────────────────────────────────────────────────────────────────────────────
#     # يمكن تعريفها كـ JSON في .env أو استخدام القيم الافتراضية
#     import json
#     _allowed_clients_json = config('KEYCLOAK_ALLOWED_CLIENTS', default='')
    
#     if _allowed_clients_json:
#         try:
#             ALLOWED_CLIENTS = json.loads(_allowed_clients_json)
#         except json.JSONDecodeError:
#             raise ValueError("❌ KEYCLOAK_ALLOWED_CLIENTS يجب أن يكون JSON صالح")
#     else:
#         # قيم افتراضية للتطوير
#         ALLOWED_CLIENTS = [
#             {
#                 "url": config('KEYCLOAK_WEB_CLIENT_URL', default='http://localhost:3000'),
#                 "secret_key": config('KEYCLOAK_WEB_CLIENT_SECRET', default='change_me_in_production'),
#                 "client_id": "web",
#             },
#             {
#                 "url": config('KEYCLOAK_MOBILE_CALLBACK_URL', default='myapp://callback'),
#                 "secret_key": config('KEYCLOAK_MOBILE_CLIENT_SECRET', default='change_me_in_production'),
#                 "client_id": "mobile",
#             },
#         ]
# else:
#     # JWT Mode - لا حاجة لإعدادات Keycloak
#     KEYCLOAK_SERVER_URL = None
#     KEYCLOAK_REALM = None
#     KEYCLOAK_CLIENT_ID = None
#     KEYCLOAK_CLIENT_SECRET = None
#     REDIRECT_URI = None
#     POST_LOGOUT_REDIRECT_URI = None
#     KEYCLOAK_WELL_KNOWN = None
#     ALLOWED_CLIENTS = []


ENABLE_UNIFIED_ID_SYNC=True
UNIFIED_ID_AUTHORIZED_APPS = {
    'university_system': 'b4f8c29a1e7d3650b8941c2ef5a30d9841f27e5a6b0c3d91f8a7e2b5c4d6a9f1',
    'control_system': 'e9a3b5c2d8f14709e6c4b2a1f5d8e790321a4f6b8c0d2e9f1a3b5c7d9e2f4a6b',
    'portal_system': '7c9a1b3f5d2e8406a1c5b8d9f2e3a7c49b1d6f0e2a5c8b3d9f1e4a7c2b5d8f0a',
    'higher_education_system': 'd2f4a6b8c0e19375b4d8f2a1c9e3b5a760f1d4b8e2a5c9f3a1b7d5e9c0f4a2b6'
}