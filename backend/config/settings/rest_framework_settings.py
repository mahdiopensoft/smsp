"""
إعدادات Django REST Framework و JWT
"""
from datetime import timedelta
from decouple import config
from .authentication_settings import get_default_authentication_classes

# ═══════════════════════════════════════════════════════════════════════════════
# 🔧 إعدادات REST Framework
# ═══════════════════════════════════════════════════════════════════════════════
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': get_default_authentication_classes(),
    'DEFAULT_PERMISSION_CLASSES': (
        'OpenSoftCoreV41.usermanager.permissions.CorePermission',
    ),
    
    # نظام الباجينيشن
    'DEFAULT_PAGINATION_CLASS': 'OpenSoftCoreV41.utils.classes.pagination.CustomPageNumberPagination',
    'PAGE_SIZE': config('API_PAGE_SIZE', default=20, cast=int),
    
    # الفلاتر
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    
    # المحللات
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    
    # المُصيِّرات
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    
    # معالجة الاستثناءات
    'EXCEPTION_HANDLER': 'OpenSoftCoreV41.utils.helpers.custom_exception_handler.custom_exception_handler',
    
    # تنسيق التاريخ والوقت
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DATE_FORMAT': '%Y-%m-%d',
    'TIME_FORMAT': '%H:%M:%S',
    
    # إعدادات Throttling
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'login': config('API_THROTTLE_LOGIN', default='3/hour'),
        'anon': config('API_THROTTLE_ANON', default='100/hour'),
        'user': config('API_THROTTLE_USER', default='1000/hour'),
    },
    # Schema
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    
    # إعدادات Unicode
    'UNICODE_JSON': True,
    'COMPACT_JSON': True,
}

# ═══════════════════════════════════════════════════════════════════════════════
# 🔑 إعدادات JWT - Simple JWT Settings
# ═══════════════════════════════════════════════════════════════════════════════
SIMPLE_JWT = {
    # مدة صلاحية الـ Tokens
    'ACCESS_TOKEN_LIFETIME': timedelta(
        minutes=config('JWT_ACCESS_TOKEN_MINUTES', default=60, cast=int)
    ),
    'REFRESH_TOKEN_LIFETIME': timedelta(
        days=config('JWT_REFRESH_TOKEN_DAYS', default=7, cast=int)
    ),
    
    # تدوير Refresh Token
    'ROTATE_REFRESH_TOKENS': config('JWT_ROTATE_REFRESH', default=True, cast=bool),
    'BLACKLIST_AFTER_ROTATION': config('JWT_BLACKLIST_AFTER_ROTATION', default=True, cast=bool),
    
    # تحديث آخر تسجيل دخول
    'UPDATE_LAST_LOGIN': True,
    
    # الخوارزمية
    'ALGORITHM': 'HS256',
    
    # إعدادات التحقق
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': config('JWT_ISSUER', default='OpenSoftCoreV41'),
    'JWK_URL': None,
    'LEEWAY': 0,
    
    # أنواع Headers
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    
    # User ID
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    
    # User Authentication
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'SIGNING_KEY': config('SECRET_KEY'),
    'TOKEN_OBTAIN_SERIALIZER':'OpenSoftCoreV41.usermanager.serializers.User.CustomTokenObtainPairSerializer',
    # Token Classes
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    
    # JTI Claim
    'JTI_CLAIM': 'jti',
    
    # Sliding Token
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# ═══════════════════════════════════════════════════════════════════════════════
# 📚 إعدادات DRF Spectacular (API Documentation)
# ═══════════════════════════════════════════════════════════════════════════════
SPECTACULAR_SETTINGS = {
    'TITLE': config('API_TITLE', default='Academic Management System API'),
    'DESCRIPTION': config('API_DESCRIPTION', default='Professional Academic Management System API'),
    'VERSION': config('API_VERSION', default='1.0.0'),
    'SERVE_INCLUDE_SCHEMA': False,
    
    # Swagger UI Settings
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': False,
        'filter': True,
        'tagsSorter': 'alpha',
        'operationsSorter': 'alpha',
    },
    'COMPONENTS': {
        'securitySchemes': {
            'BearerAuth': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
            }
        }
    },
    'SECURITY': [{'BearerAuth': []}],
    # Schema Settings
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': '/',
}
