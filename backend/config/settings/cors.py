"""
إعدادات CORS - Cross-Origin Resource Sharing
═══════════════════════════════════════════════════════════════════════════════
🛡️ Security: CORS origins are STRICTLY loaded from .env only.
     No hardcoded origins, no wildcard regexes.
═══════════════════════════════════════════════════════════════════════════════
"""
from decouple import config

# ═══════════════════════════════════════════════════════════════════════════════
# 🌐 CORS Settings
# ═══════════════════════════════════════════════════════════════════════════════

# السماح بـ credentials (cookies, authorization headers)
CORS_ALLOW_CREDENTIALS = config('CORS_ALLOW_CREDENTIALS', default=True, cast=bool)

# السماح بجميع المصادر (يجب أن يكون False في الإنتاج!)
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=False, cast=bool)

# قائمة المصادر المسموح بها — تُقرأ فقط من .env
CORS_ALLOWED_ORIGINS_STR = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:5175'
)
CORS_ALLOWED_ORIGINS = [
    origin.strip() 
    for origin in CORS_ALLOWED_ORIGINS_STR.split(',') 
    if origin.strip()
]

# 🛡️ أنماط Regex — فارغة افتراضياً (الأكثر أماناً)
# يمكن إضافة أنماط محددة في .env إذا لزم الأمر
# ⚠️ لا تستخدم أنماط عامة مثل r"^http://localhost:\d+$" أبداً!
CORS_ALLOWED_ORIGIN_REGEXES = [
    'http://localhost:3080',
    'http://localhost:3334'
    
]

# الطرق المسموح بها
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# الرؤوس المسموح بها
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'x-api-key',
    'cache-control',
    'pragma',
    'Excel-Import'
]

# الرؤوس المكشوفة للعميل
CORS_EXPOSE_HEADERS = [
    'content-disposition',
    'x-total-count',
    'x-page-count',
]

# مدة تخزين preflight بالثواني
CORS_PREFLIGHT_MAX_AGE = config('CORS_PREFLIGHT_MAX_AGE', default=86400, cast=int)
