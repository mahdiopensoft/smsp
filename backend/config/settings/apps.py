"""
إعدادات التطبيقات المثبتة - Installed Apps Settings
"""

# ═══════════════════════════════════════════════════════════════════════════════
# 📦 التطبيقات الأساسية - Django Core Apps
# ═══════════════════════════════════════════════════════════════════════════════
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'daphne',  # يجب أن يكون قبل staticfiles
    'django.contrib.staticfiles',
]

DATA_UPLOAD_MAX_MEMORY_SIZE=262144000
FILE_UPLOAD_MAX_MEMORY_SIZE=262144000
DATA_UPLOAD_MAX_NUMBER_FIELDS=1000000
# ═══════════════════════════════════════════════════════════════════════════════
# 📚 تطبيقات الطرف الثالث - Third Party Apps
# ═══════════════════════════════════════════════════════════════════════════════
THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'modeltranslation',
    'channels',
    'django_filters',
    'drf_spectacular',
    'captcha',
]

# ═══════════════════════════════════════════════════════════════════════════════
# 🔌 تطبيقات OpenSoftCore
# ═══════════════════════════════════════════════════════════════════════════════
CORE_APPS = [
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

# ═══════════════════════════════════════════════════════════════════════════════E
# 🏢 تطبيقات المشروع - Project Apps
# ═══════════════════════════════════════════════════════════════════════════════
PROJECT_APPS = [
    'drf_yasg',
    'academic',
    'bank',
    'exams',
    'omr',
    'submissions',
    'templates_engine',
]

# ═══════════════════════════════════════════════════════════════════════════════
# 📋 جميع التطبيقات المثبتة
# ═══════════════════════════════════════════════════════════════════════════════
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + CORE_APPS + PROJECT_APPS
