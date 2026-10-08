
PLATFORM_SYNC_ALLOWED_SYSTEMS = {
    'uep-001': 'b30d1f4437513f44f498d19464c5a348efda2cd4ed645d8b8be15b610c848b7f',
}

# SETUP FOR THIS SYSTEM (as a SENDER / Server):
# If this system pushes sync data TO other sub-systems:
PLATFORM_SYNC_SYSTEM_ID = "school-001"
PLATFORM_SYNC_SECRET_KEY = "b30d1f4437513f44f498d19464c5a348efda2cd4ed645d8b8be15b610c848b7f"

# Performance tuning
PLATFORM_SYNC_REQUEST_TIMEOUT = 5     # seconds per request (keep low to avoid dev server timeout)
PLATFORM_SYNC_MAX_RETRIES = 2         # max attempts per system before giving up
PLATFORM_SYNC_RETRY_DELAY = 0.5       # seconds between retry attempts
PLATFORM_SYNC_TIMESTAMP_TOLERANCE = 600  # seconds (10 min) — reject older requests

from decouple import config

# =============================================================================
# Gate Sync Settings (SYNC_*) — COMPLETELY SEPARATE, DO NOT MIX
# =============================================================================
SYNC_REMOTE_BASE_URL = config("PORTAL_BACKEND_URL", default="http://localhost:33364")
SYNC_SYSTEM_ID = "school-001"
SYNC_SECRET_KEY = "b30d1f4437513f44f498d19464c5a348efda2cd4ed645d8b8be15b610c848b7d"
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

import base64

SYSTEM_ID = SYNC_SYSTEM_ID
SYSTEM_PRIVATE_KEY_BASE64 = "LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQ0KTUlJRXBBSUJBQUtDQVFFQTlaVDhRcXZpSHpiWGpyNGQrZy9LSVM3QVBIdk9ibkNwbmZDVHBjeGtieUxxdDlPdA0KVzJXeENsbXRMM3hyc041ZW1oS2tiL1liQVJaS2tTV1ZkVWVRTUJjUnFSL1RWUUdNbCtzb2NSYjZwU1FFMXJ4cQ0KK1VoazRMVXY0OHVlUmJ6emMwcGg4MHZiekF0RlJselBtbVFvNGppOWphcERGaUxVaVU4VFVidWVtMHh0Rlc1Vw0KWXRiR0xrRjFhM3preE5RbzA4TFp1bnFuM3FEZGpFK3FxODdKNUV3QU40RHVrRmh1eTA5enZReWx0NjB5Z1NISQ0KN0IrMXRCUDNaNTIwaURaYU5Cc0cxVHBqVkwvc3hzNDJzUFlWZXZ1aTRxVFQxTlZ4aVNDbGtpRmgxYmpTWjFJZg0Kb3VONWZub3c5UmQ3L0lURzhITFZIcWFiSS84YmhhVE5IR2tYWXdJREFRQUJBb0lCQVFEQUVWMlo1MFJhbFZIUg0KV2UrbisyRml3bVdtNkUxeklyb0Z4SG8xV2IzVERjUDFNYUNMc3VUYjYzYi9oSmZWSkpWb2V0d1FsTEphRDAwUw0KYUFxVVJ2d0dJSVMzZVNTWGZ6YXVPa1RPN2VIcDlsbXllSHBSck1UNDJid3l0TFY4WldNaDhETGJUYUVCM0c2NQ0Kc1N6TTJ6aitkTklMVWZaV0FiZW9EQ2hYN0IwSDV4M1V6cnBjVTBYWmJnSCtlajBlQ2JqWktQL09GVmlrNHhwSA0KYmNwOFUwTmRpcldQUXdMd0o0S3h5dk1SNWMxWjhiOXJ1WkZtbXZLckdhVnMzRDVGclVjeXdaajNnNkhZSVBqaQ0KOXQ0c0lFK2c5ZzMwYnViY3ZvMHNCOGJKazR2N1RWUmZ3VEc4R29IQlZnd3FoQUR1S3FzcjlmelA4RUpvRzg5cg0KM1hNMVcxNkJBb0dCQVB0R0ZYeTVPSTMydXFsazFycUdUSHBsWmxaTjVOS3VTaTg5dUllYmE2ODRZSEE5MDQ3dQ0KS3lFNEZwdS9ZOUw4ZkduSFdlNTA1STAycFVVOFFXTk5WRFVKQmREclRTUEhCMnp6Rk1zdmRLRFNmazV2clJMag0KVy9QVWE4QmNEMjM4b3RCcEdoWkgrUkJYRDNoREMrVWg2anJEcStEOHV6cTNJRDlUZURNUjBtKzVBb0dCQVBveg0KZnFjdXVXdEI3NVhTcFJGNFVBY2VvNnUwWnFhV3NCdDBkL1lrZnhNOFZQT2QwSnFpRmJidTd2cnRyQzdwWW5Gaw0KMUNKaTN5SG9MSkRRTmtObFFtQWt4QXB2anI2cy9nN2tFVkZ3ZmV1NHVUQ1lpdHMzWHYyTm1zb3hxY3gwOHUyQw0Ka1BqSmFlSE5oQ1ZwN0YyKzJ5WnorVGI5WDhIMDdqN2p3WEdOTm5YN0FvR0FMUGxFUzBpVG1NVTZiNnMreTYvUg0KN0c1TnZOREFUZjBvQmdDVUVLRit5cVBhanZ4aDYwa3hxd1p3OVh0eUVJZGtkVUpiRkZVVHV6cTJwZ2U4NUZzbw0KNFQwMkwwaU9UQU1KanpTSzJqc3FNc2E2R0t2Z1hHc1pRREViQUJqNklnTi8yTEdYRzduU0dGeWN4amVwMzE4TQ0KbjJ2NlRaQ3Vxam13cWVUMHRKOVIvUEVDZ1lFQWhVRFh1NEtQRGlqWHlSdWUvbWJ0ZUYxQkhqbStVZ3IvVUIvLw0KcEFCY0RZcWNWQU5CRHBvMHBuRXFwa25lNGowNlNOcENnTzNYbU45bW5ObkhqSzFwWkhzd1RiNk1iOUVDbmp1cA0KWFk1a0FoOG53bEg3NGpUalNuY1ljWWR4djRxcHR3Vks0TFdreHJZR0kwYit0QTdwK05qYmFnWVg4ZHpZNW5XMg0KbVJ0MFhmRUNnWUJXQUpzRHJCWUhiSzd2YTNuVFZjTUZQd0JHdnVBQzIwZXdPWEpXL0dXREpzU1dEWlhZRlhHVQ0KNVp1OEhhZDVXakc2MnN4QWVHUXBETkNEYVdzb0dTUEVSSlF1NDJNQ3gveWpHSTlTMTBkWS9aTXF6L3pxZHNiTg0KQVVPR1BxaXpiL0REMW1HQzhkeEViRGxaZkU5eHRlVG03eTNYdkYzMlFrMDVjdC92bXltTExBPT0NCi0tLS0tRU5EIFJTQSBQUklWQVRFIEtFWS0tLS0tDQo="
ERP_PUBLIC_KEY_BASE64 = "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0NCk1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBdDZZZ3VrcHlJUHJ3cFY2VkJTZ3MNCmdMNktwdS9RQmpLYkpCKzVUaDVBNjBZUWVTOTJTdEVPd3R5bnl3LzB0L2pxZkRsRHVXajJBZ2tvT2Z2VzlaUUsNCnpWcU1ZN3F3U1BjcGF0eVFTbmUrN2ZFU2w3RjB3VGlkREZsZndBUzAxYTUzZDlYYUJQR3hqT2Ntb1g1alVmckgNCmp3aHJlOExlczdhdS9hWGJ3aTE4T0UySE5WYVBEeVpObWlNcnRWR0pOTFQ5bFpEMUY1UWNOUU9JRWd3TklGa1cNCkI1ODdBQ3R2ZGMvUDNzUk1obVdrMjdONDVWb3BiUitMRDJEOEdwZGkwRmhwa1U1MWJWbEJhTHFPckQrcGZFaXkNCjMyTzlIMU9CbkZENkxUS2FhNHh0bVl1ZVZsZzFrSzJNWEJRRmRtaEw4Ry9nWGZzczJxVVdZZi9BMStMdUlsSDkNCkdRSURBUUFCDQotLS0tLUVORCBQVUJMSUMgS0VZLS0tLS0NCg=="
ERP_API_URL = config('ERP_BACKEND_URL', default="http://localhost:33362")
SYSTEM_PRIVATE_KEY = base64.b64decode(SYSTEM_PRIVATE_KEY_BASE64).decode('utf-8')

TRUSTED_SYSTEMS = {
    'erp':{
        'public_key': base64.b64decode(ERP_PUBLIC_KEY_BASE64).decode('utf-8'),
        'algorithm': 'RS256',
        'audience':SYSTEM_ID
    }
}


# ═══════════════════════════════════════════════════════════════════════════
# إعدادات التكامل مع النظام المالي (financial)
# Financial System Integration Settings
# ═══════════════════════════════════════════════════════════════════════════

from decouple import config
# توكن المصادقة الداخلي بين النظامين (يجب أن يتطابق مع FINANCIAL_SYSTEM_TOKEN في .env الخاص بـ financial)
FINANCIAL_SYSTEM_TOKEN=config('FINANCIAL_SYSTEM_TOKEN', default='erp_to_university_secure_token_changeme')
