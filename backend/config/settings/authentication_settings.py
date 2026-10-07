"""
⚙️ Authentication Settings - إعدادات نظام المصادقة
===================================================
Unified authentication configuration for all modes.

Add this to your Django settings:
    from OpenSoftCoreV41.setting.authentication_settings import *
"""

from decouple import config

# ═══════════════════════════════════════════════════════════════
# 🔐 Authentication Mode Constants (defined here to avoid circular imports)
# ═══════════════════════════════════════════════════════════════
# These values must match OpenSoftCoreV41.authentication.constants.AuthMode

class AuthMode:
    """Authentication mode constants - mirrors OpenSoftCoreV41.authentication.constants.AuthMode"""
    STANDARD_USER_MANAGER = 'standard'
    SSO_KEYCLOAK = 'keycloak'
    SSO_DJANGO = 'django_sso'


class TokenValidationMethod:
    """Token validation method constants"""
    JWKS = 'jwks'
    INTROSPECTION = 'introspection'


# ═══════════════════════════════════════════════════════════════
# 🔐 Authentication Mode
# ═══════════════════════════════════════════════════════════════

def _normalize_auth_mode(mode: str) -> str:
    """
    Normalize authentication mode to standard format.
    Supports both new format (keycloak) and legacy format (SSO_KEYCLOAK).
    """
    mode_mapping = {
        # Legacy format -> new format
        'STANDARD_USER_MANAGER': AuthMode.STANDARD_USER_MANAGER,
        'SSO_KEYCLOAK': AuthMode.SSO_KEYCLOAK,
        'SSO_DJANGO': AuthMode.SSO_DJANGO,
        # Also accept lowercase
        'standard_user_manager': AuthMode.STANDARD_USER_MANAGER,
        'sso_keycloak': AuthMode.SSO_KEYCLOAK,
        'sso_django': AuthMode.SSO_DJANGO,
        # Direct values (already normalized)
        'standard': AuthMode.STANDARD_USER_MANAGER,
        'keycloak': AuthMode.SSO_KEYCLOAK,
        'django_sso': AuthMode.SSO_DJANGO,
        # Legacy shortcuts
        'jwt': AuthMode.STANDARD_USER_MANAGER,
        'sso': AuthMode.SSO_KEYCLOAK,
    }
    return mode_mapping.get(mode, mode)


# Available modes: STANDARD_USER_MANAGER, SSO_KEYCLOAK, SSO_DJANGO
_raw_auth_mode = config('AUTH_MODE', default=AuthMode.SSO_KEYCLOAK)
AUTH_MODE = _normalize_auth_mode(_raw_auth_mode)

# Enable dual authentication (Local JWT + SSO Keycloak simultaneously)
ALLOW_DUAL_AUTH = config('ALLOW_DUAL_AUTH', default=False, cast=bool)
# MAX_CONCURRENT_SESSIONS = config('MAX_CONCURRENT_SESSIONS',2)

# ═══════════════════════════════════════════════════════════════
# 🔑 Standard User Manager Settings (JWT)
# ═══════════════════════════════════════════════════════════════

# Token blacklisting behavior when session is missing
BLACKLIST_ON_MISSING_SESSION = config('BLACKLIST_ON_MISSING_SESSION', default=True, cast=bool)


# ═══════════════════════════════════════════════════════════════
# 🏰 Keycloak SSO Settings
# ═══════════════════════════════════════════════════════════════
"""
🏰 Keycloak Settings - إعدادات Keycloak
========================================
Configuration for Keycloak OAuth2/OIDC integration.

Environment Variables:
    KEYCLOAK_SERVER_URL: Keycloak server URL
    KEYCLOAK_REALM: Realm name
    KEYCLOAK_CLIENT_ID: Client ID
    KEYCLOAK_CLIENT_SECRET: Client secret
    KEYCLOAK_REDIRECT_URI: OAuth2 callback URL
    KEYCLOAK_POST_LOGOUT_REDIRECT_URI: Post-logout redirect URL
    KEYCLOAK_PKCE_ENABLED: Enable PKCE (default: True)
    KEYCLOAK_TOKEN_VALIDATION: 'jwks' or 'introspection' (default: jwks)
"""

from decouple import config

# ═══════════════════════════════════════════════════════════════
# 🌐 Server Configuration
# ═══════════════════════════════════════════════════════════════

KEYCLOAK_SERVER_URL = config('KEYCLOAK_SERVER_URL', default='http://localhost:8180')
KEYCLOAK_REALM = config('KEYCLOAK_REALM', default='testrealm')
KEYCLOAK_CLIENT_ID = config('KEYCLOAK_CLIENT_ID', default='acadmic-client-test')
KEYCLOAK_CLIENT_SECRET = config('KEYCLOAK_CLIENT_SECRET', default='')
KEYCLOAK_INTERNAL_URL = config('KEYCLOAK_INTERNAL_URL', default=None)

# ═══════════════════════════════════════════════════════════════
# 🔗 Redirect URIs
# ═══════════════════════════════════════════════════════════════

REDIRECT_URI = config('KEYCLOAK_REDIRECT_URI', default='http://localhost:8000/sso/callback')
POST_LOGOUT_REDIRECT_URI = config('KEYCLOAK_POST_LOGOUT_REDIRECT_URI', default='http://localhost:8000/sso/logout-callback')

# ═══════════════════════════════════════════════════════════════
# 🔒 Security Settings
# ═══════════════════════════════════════════════════════════════

# Enable PKCE (Proof Key for Code Exchange) - recommended for security
KEYCLOAK_PKCE_ENABLED = config('KEYCLOAK_PKCE_ENABLED', default=True, cast=bool)

# Token validation method: 'jwks' (recommended) or 'introspection'
# JWKS validates locally using public keys - faster
# Introspection calls Keycloak endpoint - more accurate but slower
KEYCLOAK_TOKEN_VALIDATION = config('KEYCLOAK_TOKEN_VALIDATION', default='jwks')

# ═══════════════════════════════════════════════════════════════
# 🔑 OIDC Endpoints (auto-generated from server URL and realm)
# ═══════════════════════════════════════════════════════════════

KEYCLOAK_WELL_KNOWN = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/.well-known/openid-configuration"
KEYCLOAK_JWKS_URL = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/certs"

# ═══════════════════════════════════════════════════════════════
# 👥 Role Mapping (Keycloak role -> Django group)
# ═══════════════════════════════════════════════════════════════

# Map Keycloak realm/client roles to Django groups
# Users will be automatically added to these groups upon login
KEYCLOAK_ROLE_MAPPING = {
    # 'realm_admin': 'Administrators',
    # 'realm_user': 'Users',
    # 'manager': 'Managers',
}

# ═══════════════════════════════════════════════════════════════
# 📱 Allowed Client Applications (HMAC-SHA256 Signature Auth)
# ═══════════════════════════════════════════════════════════════

# Each client uses HMAC-SHA256 signatures for authentication.
# The secret_key is NEVER transmitted - only used to compute/verify signatures.
# Signature = HMAC-SHA256(secret_key, client_id + ":" + timestamp)

# Maximum age (seconds) for a signature timestamp to be considered valid
CLIENT_SIGNATURE_MAX_AGE = 10000  # 5 minutes

ALLOWED_CLIENTS = []
_clients_json = config('ALLOWED_CLIENTS_JSON', default='')
if _clients_json:
    import json as _json
    try:
        ALLOWED_CLIENTS = _json.loads(_clients_json)
    except (ValueError, TypeError):
        import logging as _logging
        _logging.getLogger(__name__).warning(
            "⚠️ ALLOWED_CLIENTS_JSON is not valid JSON — no clients configured!"
        )
else:
    # Fallback: build from individual env vars (development convenience)
    _client_url = config('CLIENT_WEB_URL', default='')
    _client_secret = config('CLIENT_WEB_SECRET_KEY', default='')
    _client_id = config('CLIENT_WEB_ID', default='web')
    if _client_url and _client_secret:
        ALLOWED_CLIENTS = [{
            'url': _client_url,
            'secret_key': _client_secret,
            'client_id': _client_id,
            'name': 'Web Application',
        }]


# ═══════════════════════════════════════════════════════════════
# ⏰ Token Lifetimes
# ═══════════════════════════════════════════════════════════════

# These are informational - actual lifetimes are configured in Keycloak
KEYCLOAK_ACCESS_TOKEN_LIFESPAN = 1000 # 100 minutes (Keycloak default)
KEYCLOAK_REFRESH_TOKEN_LIFESPAN = 1800  # 30 minutes (Keycloak default)

# ═══════════════════════════════════════════════════════════════
# 🔄 Session Behavior
# ═══════════════════════════════════════════════════════════════

# When session cookie is missing, should we blacklist the JWT?
KEYCLOAK_BLACKLIST_ON_MISSING_SESSION = config(
    'KEYCLOAK_BLACKLIST_ON_MISSING_SESSION', 
    default=False, 
    cast=bool
)

# السماح بإنشاء مستخدم جديد تلقائياً عند تسجيل الدخول عبر SSO
# ⚠️ اضبط على False بعد إنشاء أول مستخدم!
KEYCLOAK_AUTO_CREATE_USER = config(
    'KEYCLOAK_AUTO_CREATE_USER',
    default=False,
    cast=bool
)

# ═══════════════════════════════════════════════════════════════
# 🔄 Keycloak User Sync Settings (Admin API)
# ═══════════════════════════════════════════════════════════════

# Enable/disable user synchronization between Django and Keycloak
KEYCLOAK_USER_SYNC_ENABLED = config('KEYCLOAK_USER_SYNC_ENABLED', default=True, cast=bool)

# Keycloak Admin API credentials
KEYCLOAK_ADMIN_USERNAME = config('KEYCLOAK_ADMIN_USERNAME', default='admin')
KEYCLOAK_ADMIN_PASSWORD = config('KEYCLOAK_ADMIN_PASSWORD', default='')
KEYCLOAK_ADMIN_CLIENT_ID = config('KEYCLOAK_ADMIN_CLIENT_ID', default='admin-cli')
KEYCLOAK_ADMIN_CLIENT_SECRET = config('KEYCLOAK_ADMIN_CLIENT_SECRET', default='')
KEYCLOAK_REQUIRED_CLIENT_ROLE = config('KEYCLOAK_REQUIRED_CLIENT_ROLE', default='admin-cli')
KEYCLOAK_USE_SERVICE_ACCOUNT = config('KEYCLOAK_USE_SERVICE_ACCOUNT', default=True, cast=bool)
# SSL verification (set to False for development only)
KEYCLOAK_VERIFY_SSL = config('KEYCLOAK_VERIFY_SSL', default=True, cast=bool)
# Sync failure strategy: 'queue' (save and retry), 'fail' (abort operation), 'ignore' (continue without Keycloak)
KEYCLOAK_SYNC_ON_FAILURE = config('KEYCLOAK_SYNC_ON_FAILURE', default='queue')

# Request timeout in seconds
KEYCLOAK_REQUEST_TIMEOUT = config('KEYCLOAK_REQUEST_TIMEOUT', default=10, cast=int)

# Retry settings
KEYCLOAK_RETRY_COUNT = config('KEYCLOAK_RETRY_COUNT', default=3, cast=int)
KEYCLOAK_RETRY_DELAY = config('KEYCLOAK_RETRY_DELAY', default=1, cast=int)

# ═══════════════════════════════════════════════════════════════
# 🔑 Keycloak Realm Roles Mapping
# ═══════════════════════════════════════════════════════════════
# Defined in config.levels.SettingLevel.KEYCLOAK_REALM_ROLES_MAP
from config.levels import KEYCLOAK_REALM_ROLES_MAP, KEYCLOAK_ROLE_ALLOWED_LEVELS, KEYCLOAK_USERTYPE_ALLOWED_ROLES, SYSTEM_LINKS, SYSTEM_BACKEND_LINKS


# ═══════════════════════════════════════════════════════════════
# 🐍 Django SSO Provider Settings
# ═══════════════════════════════════════════════════════════════

# Django OAuth Toolkit settings
DJANGO_SSO_ENABLED = config('DJANGO_SSO_ENABLED', default=False, cast=bool)

# Token lifetimes (in seconds)
DJANGO_SSO_ACCESS_TOKEN_EXPIRE = config('DJANGO_SSO_ACCESS_TOKEN_EXPIRE', default=3600, cast=int)
DJANGO_SSO_REFRESH_TOKEN_EXPIRE = config('DJANGO_SSO_REFRESH_TOKEN_EXPIRE', default=604800, cast=int)
DJANGO_SSO_ID_TOKEN_EXPIRE = config('DJANGO_SSO_ID_TOKEN_EXPIRE', default=3600, cast=int)

# OIDC settings
DJANGO_SSO_ISSUER = config('DJANGO_SSO_ISSUER', default='http://localhost:8000')
DJANGO_SSO_SCOPES = ['openid', 'profile', 'email']

# RSA key for signing tokens (path to PEM file)
DJANGO_SSO_SIGNING_KEY = config('DJANGO_SSO_SIGNING_KEY', default='')


# ═══════════════════════════════════════════════════════════════
# 📋 Authentication Backend Configuration
# ═══════════════════════════════════════════════════════════════

AUTH_BACKENDS_CONFIG = {
    AuthMode.STANDARD_USER_MANAGER: {
        'enabled': True,
        'backend': 'OpenSoftCoreV41.authentication.backends.standard.StandardAuthBackend',
        'drf_class': 'OpenSoftCoreV41.usermanager.authentication.SessionAwareJWTAuthentication',
    },
    AuthMode.SSO_KEYCLOAK: {
        'enabled': True,
        'backend': 'OpenSoftCoreV41.authentication.backends.keycloak.KeycloakAuthBackend',
        'drf_class': 'OpenSoftCoreV41.authentication.backends.keycloak.KeycloakDRFAuthentication',
    },
    AuthMode.SSO_DJANGO: {
        'enabled': DJANGO_SSO_ENABLED,
        'backend': 'OpenSoftCoreV41.authentication.backends.django_sso.DjangoSSOBackend',
        'drf_class': 'OpenSoftCoreV41.authentication.backends.django_sso.DjangoSSODRFAuthentication',
    },
}


# ═══════════════════════════════════════════════════════════════
# 📝 Helper function for REST_FRAMEWORK config
# ═══════════════════════════════════════════════════════════════

def get_default_authentication_classes():
    """
    Get the default authentication classes based on AUTH_MODE.
    
    Supports dual authentication when ALLOW_DUAL_AUTH=True,
    allowing both Keycloak SSO and local JWT login simultaneously.
    
    Usage in settings:
        REST_FRAMEWORK = {
            'DEFAULT_AUTHENTICATION_CLASSES': get_default_authentication_classes(),
        }
    """
    # Dual auth mode: support both Keycloak SSO and local JWT
    if ALLOW_DUAL_AUTH:
        # JWT first, then Keycloak - so local tokens work even if Keycloak is down
        return (
            'OpenSoftCoreV41.usermanager.authentication.SessionAwareJWTAuthentication',
            'OpenSoftCoreV41.authentication.backends.keycloak.KeycloakDRFAuthentication',
        )
    
    # Single mode: use configured backend
    backend_config = AUTH_BACKENDS_CONFIG.get(AUTH_MODE, {})
    drf_class = backend_config.get('drf_class')
    
    if drf_class:
        return (drf_class,)
    
    # Fallback to standard JWT
    return (
        'OpenSoftCoreV41.usermanager.authentication.SessionAwareJWTAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )


# ═══════════════════════════════════════════════════════════════
# 📱 Device Binding Configuration — ربط الأجهزة
# ═══════════════════════════════════════════════════════════════
# ⚠️ خاص بتطبيق Flutter (الموبايل) — Vue.js (الويب) معفى

# تفعيل/تعطيل النظام بالكامل
DEVICE_BINDING_ENABLED = config('DEVICE_BINDING_ENABLED', default=True, cast=bool)

# تطبيق على الموبايل فقط
DEVICE_BINDING_MOBILE_ONLY = config('DEVICE_BINDING_MOBILE_ONLY', default=True, cast=bool)

# الحد الأقصى للأجهزة
DEVICE_BINDING_MAX_DEVICES_PER_USER = config('DEVICE_BINDING_MAX_DEVICES_PER_USER', default=3, cast=int)

# الموافقة التلقائية على أول جهاز (الأول تلقائي، البقية تحتاج موافقة أدمن)
DEVICE_BINDING_AUTO_APPROVE_FIRST = config('DEVICE_BINDING_AUTO_APPROVE_FIRST', default=True, cast=bool)

# طلب MFA للجهاز الجديد
DEVICE_BINDING_REQUIRE_MFA_NEW_DEVICE = config('DEVICE_BINDING_REQUIRE_MFA_NEW_DEVICE', default=True, cast=bool)

# وضع كشف التبديل: 'strict' أو 'warn'
DEVICE_BINDING_ANTI_SWAP_MODE = config('DEVICE_BINDING_ANTI_SWAP_MODE', default='strict')

# أسماء الـ Headers
DEVICE_BINDING_FINGERPRINT_HEADER = config('DEVICE_BINDING_FINGERPRINT_HEADER', default='X-Device-Fingerprint')
DEVICE_BINDING_CLIENT_TYPE_HEADER = config('DEVICE_BINDING_CLIENT_TYPE_HEADER', default='X-Client-Type')

# مدة صلاحية الأجهزة المعلقة (بالساعات)
DEVICE_BINDING_PENDING_EXPIRY_HOURS = config('DEVICE_BINDING_PENDING_EXPIRY_HOURS', default=72, cast=int)


# ═══════════════════════════════════════════════════════════════
# 🛡️ MFA Enforcement — تطبيق المصادقة الثنائية
# ═══════════════════════════════════════════════════════════════

# When True, ALL users must enable MFA. Users cannot disable it themselves.
MFA_ENFORCED = config('MFA_ENFORCED', default=False, cast=bool)

# When True, superusers are exempt from mandatory MFA enrollment
MFA_EXEMPT_SUPERUSERS = config('MFA_EXEMPT_SUPERUSERS', default=True, cast=bool)


# ═══════════════════════════════════════════════════════════════
# 🍪 Token Cookie Settings — إعدادات كوكيز التوكن
# ═══════════════════════════════════════════════════════════════

TOKEN_COOKIE_SAMESITE = config('TOKEN_COOKIE_SAMESITE', default='Lax')
TOKEN_COOKIE_DOMAIN = config('TOKEN_COOKIE_DOMAIN', default=None)
JWT_REFRESH_TOKEN_DAYS = config('JWT_REFRESH_TOKEN_DAYS', default=7, cast=int)
