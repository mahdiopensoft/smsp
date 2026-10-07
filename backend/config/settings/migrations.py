
"""
إعدادات الهجرات - Migration Settings
═══════════════════════════════════════════════════════════════════════════════
إعداد مجلدات هجرات منفصلة لكل بيئة (تطوير، اختبار، إنتاج)
═══════════════════════════════════════════════════════════════════════════════

🔧 كيف تعمل الهجرات المنفصلة؟
============================

1️⃣ الوضع الافتراضي (MIGRATIONS_SEPARATE_ENVS=False):
   - جميع الهجرات تُحفظ في مجلد migrations داخل كل تطبيق
   - مثال: system_management/migrations/0001_initial.py
   - ✅ مناسب لمعظم المشاريع

2️⃣ الوضع المنفصل (MIGRATIONS_SEPARATE_ENVS=True):
   - كل بيئة لها مجلد هجرات خاص
   - الهيكل:
     migrations/
     ├── development/
     │   ├── system_management/
     │   │   └── 0001_initial.py
     │   └── control/
     │       └── 0001_initial.py
     ├── production/
     │   └── ...
     └── testing/
         └── ...
   
   - ⚠️ استخدم فقط إذا كنت تحتاج قواعد بيانات مختلفة لكل بيئة

3️⃣ متى تحتاج هجرات منفصلة؟
   - عندما يكون هيكل قاعدة البيانات مختلف بين البيئات
   - في بيئات المؤسسات الكبيرة  
   - عند استخدام قواعد بيانات من أنواع مختلفة

4️⃣ تشغيل الهجرات:
   # إنشاء الهجرات
   python manage.py makemigrations
   
   # تطبيق الهجرات
   python manage.py migrate
   
   # مع تحديد البيئة
   set DJANGO_ENV=production
   python manage.py migrate
"""
from decouple import config

# ═══════════════════════════════════════════════════════════════════════════════
# ⚙️ إعدادات من متغيرات البيئة
# ═══════════════════════════════════════════════════════════════════════════════

# البيئة الحالية
DJANGO_ENV = config('DJANGO_ENV', default='development')

# هل نستخدم هجرات منفصلة لكل بيئة؟
MIGRATIONS_SEPARATE_ENVS = config('MIGRATIONS_SEPARATE_ENVS', default=False, cast=bool)


# ═══════════════════════════════════════════════════════════════════════════════
# 📱 جميع تطبيقات المشروع
# ═══════════════════════════════════════════════════════════════════════════════

# تطبيقات Django الأساسية
DJANGO_APPS_MIGRATIONS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
]

# تطبيقات الطرف الثالث
THIRD_PARTY_APPS_MIGRATIONS = [
    'rest_framework_simplejwt.token_blacklist',
    'captcha',
]

# تطبيقات OpenSoftCoreV41
CORE_APPS_MIGRATIONS = [
    'OpenSoftCoreV41.screens',
    'OpenSoftCoreV41.log',
    'OpenSoftCoreV41.user_management',
    'OpenSoftCoreV41.hijri_dates',
    'OpenSoftCoreV41.common',
    'OpenSoftCoreV41.usermanager',
    'OpenSoftCoreV41.gate_sync',
    'OpenSoftCoreV41.platform_sync',
    'OpenSoftCoreV41.advanced_chat',
]

# تطبيقات المشروع
PROJECT_APPS_MIGRATIONS = [
    'academic',
    'bank',
    'exams',
    'omr',
    'submissions',
    'templates_engine',
]

# جميع التطبيقات
ALL_APPS_MIGRATIONS = (
    DJANGO_APPS_MIGRATIONS + 
    THIRD_PARTY_APPS_MIGRATIONS + 
    CORE_APPS_MIGRATIONS + 
    PROJECT_APPS_MIGRATIONS
)


# ═══════════════════════════════════════════════════════════════════════════════
# 🔄 بناء MIGRATION_MODULES حسب البيئة
# ═══════════════════════════════════════════════════════════════════════════════

def get_migration_modules(env: str, separate_envs: bool = False) -> dict:
    """
    إنشاء قاموس MIGRATION_MODULES
    
    Args:
        env: البيئة (development/production/testing)
        separate_envs: هل نفصل الهجرات حسب البيئة؟
    
    Returns:
        قاموس MIGRATION_MODULES
    """
    migration_modules = {
    }
    
    if not separate_envs:
        # الوضع الافتراضي - الهجرات في مجلد التطبيق
        return migration_modules
    
    # الوضع المنفصل - كل بيئة لها مجلد خاص
    
    # قائمة تطبيقات third party (بدون نقطة)
    third_party_simple = {'captcha'}
    
    for app in ALL_APPS_MIGRATIONS:
        app_name = app.split('.')[-1]
        
        if app.startswith('django.'):
            # Django core - نتركها افتراضية
            continue
        elif app.startswith('OpenSoftCoreV41.'):
            # تطبيقات OpenSoftCore
            migration_modules[app_name] = f'migrations.{env}.opensoftcore.{app_name}'
        elif '.' in app:
            # تطبيقات third party مع نقطة (مثل rest_framework_simplejwt.token_blacklist)
            migration_modules[app_name] = f'migrations.{env}.third_party.{app_name}'
        elif app in third_party_simple:
            # تطبيقات third party بسيطة (مثل captcha)
            migration_modules[app_name] = f'migrations.{env}.{app_name}'
        else:
            # تطبيقات المشروع
            migration_modules[app_name] = f'migrations.{env}.{app_name}'
    
    return migration_modules


# ═══════════════════════════════════════════════════════════════════════════════
# 📋 إعدادات الهجرات الافتراضية
# ═══════════════════════════════════════════════════════════════════════════════

MIGRATION_MODULES_DEFAULT = {
    # لا نعطل أي هجرات
}


# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 تحديد MIGRATION_MODULES تلقائياً من .env
# ═══════════════════════════════════════════════════════════════════════════════

if MIGRATIONS_SEPARATE_ENVS:
    # الخيار 2: هجرات منفصلة لكل بيئة
    MIGRATION_MODULES = get_migration_modules(DJANGO_ENV, separate_envs=True)
else:
    # الخيار 1: الهجرات الافتراضية (أبسط وموصى به)
    MIGRATION_MODULES = MIGRATION_MODULES_DEFAULT
