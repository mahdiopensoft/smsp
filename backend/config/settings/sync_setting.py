
import base64
from decouple import config

PLATFORM_SYNC_SECRET_KEY = config("PLATFORM_SYNC_SECRET_KEY", default="")
_UEP_001_KEY = config("PLATFORM_SYNC_ALLOWED_UEP_001_KEY", default=PLATFORM_SYNC_SECRET_KEY)
PLATFORM_SYNC_ALLOWED_SYSTEMS = {'uep-001': _UEP_001_KEY} if _UEP_001_KEY else {}

# SETUP FOR THIS SYSTEM (as a SENDER / Server):
# If this system pushes sync data TO other sub-systems:
PLATFORM_SYNC_SYSTEM_ID = "school-001"

# Performance tuning
PLATFORM_SYNC_REQUEST_TIMEOUT = 5     # seconds per request (keep low to avoid dev server timeout)
PLATFORM_SYNC_MAX_RETRIES = 2         # max attempts per system before giving up
PLATFORM_SYNC_RETRY_DELAY = 0.5       # seconds between retry attempts
PLATFORM_SYNC_TIMESTAMP_TOLERANCE = 600  # seconds (10 min) — reject older requests

# =============================================================================
# Gate Sync Settings (SYNC_*) — COMPLETELY SEPARATE, DO NOT MIX
# =============================================================================
SYNC_REMOTE_BASE_URL = config("PORTAL_BACKEND_URL", default="http://localhost:33364")
SYNC_SYSTEM_ID = "school-001"
SYNC_SECRET_KEY = config("SYNC_SECRET_KEY", default="")
FACTORIES_PATH = "sync/factories"
SYNC_IGNORED_APPS = ['gate_sync', 'screens']
SYNC_IGNORED_MODELS = [

]

MODELS_WITHOUT_EXTERNAL_ID = [


    "User",
    "Organization",
    "UserType",
    "Country",
    # "Address",
    "Governorate",
    "Directorate",
    "Region",
    "CustomGroup",
    "Currency",
    "PrintReportSetting",

# d_services
    "ServiceVersion",
    "Service",
    "GrantSource",
    "ServiceWorkflowStep",
    "WorkflowStage",
    "OrganizationServiceConfig",
    "ServiceRequest",
]

# =============================================================================
# Portal Service Sync — رابط API البوابة (عام)
# =============================================================================
PORTAL_API_URL = config("PORTAL_BACKEND_URL", default="http://localhost:33364")  # عنوان API نظام البوابة

# نوع هذا النظام — يحدد أي حقل مزامنة يخص هذا النظام
# القيم المتاحة: "university" | "school" | "institute"
PORTAL_SYNC_SYSTEM_TYPE = "school"
BATCH_SIZE=300
SYNC_REQUEST_TIMEOUT=1000



# =============================================================================
# Integration اعدادات التكامل
# =============================================================================

SYSTEM_ID = SYNC_SYSTEM_ID
SYSTEM_PRIVATE_KEY_BASE64 = config("SYSTEM_PRIVATE_KEY_BASE64", default="")
ERP_PUBLIC_KEY_BASE64 = config("ERP_PUBLIC_KEY_BASE64", default="")
ERP_API_URL = config('ERP_BACKEND_URL', default="http://localhost:33362")
SYSTEM_PRIVATE_KEY = (
    base64.b64decode(SYSTEM_PRIVATE_KEY_BASE64).decode('utf-8')
    if SYSTEM_PRIVATE_KEY_BASE64
    else ""
)

TRUSTED_SYSTEMS = {
    'erp': {
        'public_key': (
            base64.b64decode(ERP_PUBLIC_KEY_BASE64).decode('utf-8')
            if ERP_PUBLIC_KEY_BASE64
            else ""
        ),
        'algorithm': 'RS256',
        'audience': SYSTEM_ID
    }
}


# ═══════════════════════════════════════════════════════════════════════════
# إعدادات التكامل مع النظام المالي (financial)
# Financial System Integration Settings
# ═══════════════════════════════════════════════════════════════════════════

# توكن المصادقة الداخلي بين النظامين (يجب أن يتطابق مع FINANCIAL_SYSTEM_TOKEN في .env الخاص بـ financial)
FINANCIAL_SYSTEM_TOKEN = config('FINANCIAL_SYSTEM_TOKEN', default='')
