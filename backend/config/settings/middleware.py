"""
إعدادات Middleware - Middleware Settings
"""

# ═══════════════════════════════════════════════════════════════════════════════
# 🔗 طبقات المعالجة - Middleware Stack
# ═══════════════════════════════════════════════════════════════════════════════
MIDDLEWARE = [
    # Security middleware - يجب أن يكون في البداية
    'django.middleware.security.SecurityMiddleware',
    
    # CORS middleware - يجب أن يكون مبكراً
    'corsheaders.middleware.CorsMiddleware',
    
    # Input sanitization — blocks SQL injection, XSS, path traversal
    'OpenSoftCoreV41.utils.middleware.input_sanitization.InputSanitizationMiddleware',
    
    # Whitenoise للملفات الثابتة (اختياري)
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    
    # Session middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    # Locale middleware للترجمة
    'django.middleware.locale.LocaleMiddleware',
    
    # Common middleware
    'django.middleware.common.CommonMiddleware',
    
    # CSRF protection
    'django.middleware.csrf.CsrfViewMiddleware',
    
    # Authentication
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    # ─── OpenSoftCoreV41 Security Middleware ───────────────────
    # Current user context (thread-local) — must be after AuthenticationMiddleware
    'OpenSoftCoreV41.utils.middleware.current_user.CurrentUserMiddleware',
    
    # Auto-logout after inactivity (configurable via INACTIVITY_TIMEOUT_SECONDS)
    'OpenSoftCoreV41.utils.middleware.inactivity_logout.InactivityLogoutMiddleware',
    
    # Security audit trail for write operations and auth events
    'OpenSoftCoreV41.utils.middleware.security_audit.SecurityAuditMiddleware',
    # ─────────────────────────────────────────────────────────
    
    # Messages
    'django.contrib.messages.middleware.MessageMiddleware',
    
    # Clickjacking protection
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# Patch OpenSoftCoreV41 InputSanitizationMiddleware to allow QuestionBank HTML inputs
try:
    from OpenSoftCoreV41.utils.middleware.input_sanitization import EXEMPT_PATHS
    if '/api/bank/' not in EXEMPT_PATHS:
        EXEMPT_PATHS.append('/api/bank/')
except ImportError:
    pass
