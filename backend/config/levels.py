
from django.db import models
from django.utils.translation import gettext_lazy as _
class BaseIntergerChoices(models.IntegerChoices):
    @classmethod
    def get_value(cls,label):
        for item in cls.choices:
            if item[1] == label:
                return item[0]
        return None
    
class CompanyLevelChoices(models.IntegerChoices):
    ADMIN = 10, _("مدير النظام")
    MINISTRY = 20, _("وزارة")
    GOVERNORATE = 30, _("محافظة")
    DIRECTORATE = 40, _("مديرية")
    COMPANY = 50, _("مدرسة/معهد/جامعة")
    COLLEGE = 60, _("كلية/فرع")

class CompanyLevel:
    """Integer-based organization level choices."""
    ADMIN = 10
    MINISTRY = 20
    GOVERNORATE = 30
    DIRECTORATE = 40
    COMPANY = 50
    COLLEGE = 60

    MAP = {
        ADMIN: 'for_admin',
        MINISTRY: 'for_ministry',
        GOVERNORATE: 'for_governorate',
        DIRECTORATE: 'for_directorate',
        COMPANY: 'for_company',
        COLLEGE: 'for_college',
    }
    
    @classmethod
    def get_name(cls,value):
        for key, val in cls.__dict__.items():
            if val == value:
                return key
        return None


required_map = {
    'ADMIN': ['fk_country'],
    'MINISTRY': ['fk_country'],
    'GOVERNORATE': ['fk_governorate'],
    'DIRECTORATE': ['fk_directorate'],
    'COMPANY': [],
    'COLLEGE': [],
}

null_map = {
    'ADMIN': ['fk_governorate'],
    'MINISTRY': ['fk_governorate'],
    'GOVERNORATE': ['fk_country'],
    'DIRECTORATE': ['fk_governorate','fk_country'],
    'COMPANY': ['fk_country', 'fk_governorate','fk_directorate'],
    'COLLEGE': ['fk_country', 'fk_governorate','fk_directorate'],
}


class OperationTypeChoices(BaseIntergerChoices):
    VIEW_SCREEN = 1, _("عرض الشاشة")            
    ADD_SCREEN = 2, _("إضافة شاشة")              
    EDIT_SCREEN = 3, _("تعديل شاشة")            
    DETAIL_SCREEN = 4, _("تفاصيل/حذف شاشة")        
    FORCE_DETAIL_SCREEN = 5, _("حذف إجباري")        
    EXPORT_SCREEN = 6, _("تصدير عناصر")  
    IMPORT_SCREEN = 7, _("استيراد عناصر")  
    VIEW_DELETED = 8, _("عرض العناصر المحذوفة")  
    RESTORE_SCREEN = 9, _("استعادة عناصر")  
    SELECT_SCREEN = 10, _("اختيار عناصر")  
    LOG = 11, _("سجل")  
    PRINT = 12, _("طباعة")  
    SYNC_PULL = 13, _("مزامنة البيانات من مصدر خارحي الى داخل النظام")  
    SYNC_PUSH = 14, _("مزامنة البيانات من النظام الى مصدر خارجي")  
    SAVE_PRINT_REPORT_SETTING = 15, _("حفظ إعدادات الطباعة")
    DELETE_PRINT_REPORT_SETTING = 16, _("حذف إعدادات الطباعة")


ACTION_OPERATION_MAP = {
    "list": OperationTypeChoices.VIEW_SCREEN,
    "retrieve": OperationTypeChoices.VIEW_SCREEN,
    "create": OperationTypeChoices.ADD_SCREEN,
    "update": OperationTypeChoices.EDIT_SCREEN,
    "partial_update": OperationTypeChoices.EDIT_SCREEN,
    "destroy": OperationTypeChoices.DETAIL_SCREEN,
    "force_delete": OperationTypeChoices.FORCE_DETAIL_SCREEN,
    "restore": OperationTypeChoices.RESTORE_SCREEN,
    "export": OperationTypeChoices.EXPORT_SCREEN,
    "import_data": OperationTypeChoices.IMPORT_SCREEN,
    "log": OperationTypeChoices.LOG,
    "log_details": OperationTypeChoices.LOG,
    "select": OperationTypeChoices.SELECT_SCREEN,
    "all": OperationTypeChoices.SELECT_SCREEN,
    "filter_by_fields": OperationTypeChoices.SELECT_SCREEN,
    "disactive": OperationTypeChoices.VIEW_DELETED,
    "data_for_add": OperationTypeChoices.VIEW_SCREEN,
    "filter_by_field_paginate": OperationTypeChoices.VIEW_SCREEN,
    "get_second_list": OperationTypeChoices.VIEW_SCREEN,
    "get_second_retrieve": OperationTypeChoices.VIEW_SCREEN,
    "sync_push": OperationTypeChoices.SYNC_PUSH,
    "sync_pull": OperationTypeChoices.SYNC_PULL,
    
}

METHOD_OPERATION_MAP = {
    "GET": OperationTypeChoices.VIEW_SCREEN,
    "POST": OperationTypeChoices.ADD_SCREEN,
    "PUT": OperationTypeChoices.EDIT_SCREEN,
    "PATCH": OperationTypeChoices.EDIT_SCREEN,
    "DELETE": OperationTypeChoices.DETAIL_SCREEN,
}
REPORT_OPERATION_TYPES = [
    OperationTypeChoices.VIEW_SCREEN,
    OperationTypeChoices.PRINT,
    OperationTypeChoices.EXPORT_SCREEN,
    OperationTypeChoices.SAVE_PRINT_REPORT_SETTING,
    OperationTypeChoices.DELETE_PRINT_REPORT_SETTING,
]

DEFAULT_OPERATION_TYPES = [
    OperationTypeChoices.VIEW_SCREEN,
    OperationTypeChoices.ADD_SCREEN,
    OperationTypeChoices.EDIT_SCREEN,
    OperationTypeChoices.DETAIL_SCREEN,
    OperationTypeChoices.FORCE_DETAIL_SCREEN,
    OperationTypeChoices.EXPORT_SCREEN,
    OperationTypeChoices.IMPORT_SCREEN,
    OperationTypeChoices.VIEW_DELETED,
    OperationTypeChoices.RESTORE_SCREEN,
    OperationTypeChoices.SELECT_SCREEN,
    OperationTypeChoices.LOG,
    OperationTypeChoices.PRINT,
    OperationTypeChoices.SAVE_PRINT_REPORT_SETTING,
    OperationTypeChoices.DELETE_PRINT_REPORT_SETTING,
]
SYNC_PUSH_OPERATION_TYPE = [
    # OperationTypeChoices.SYNC_PUSH,
]
SYNC_PULL_OPERATION_TYPE = [
    # OperationTypeChoices.SYNC_PULL,
]
DEFAULT_USERTYPES = [
    ("1","عام", "public", "نوع مستخدم عام"),
    ("2","طالب", "student", "نوع مستخدم طالب"),
    ("3","موظف", "employee", "نوع مستخدم موظف"),
    ("4","ولي امر", "guardian", "نوع مستخدم ولي امر"),
    ("5","مدرس", "teacher", "نوع مستخدم مدرس"),
]


# ═══════════════════════════════════════════════════════════════
# 🔑 Keycloak Realm Roles Mapping
# ═══════════════════════════════════════════════════════════════
# Key: Keycloak role name (exact match)
# Value: Arabic display name (lazy translated)
# Only roles listed here will be shown in the roles management UI.
KEYCLOAK_REALM_ROLES_MAP = {
    'access-login-role-unified-educational-platform':  _("المنصة التعليمية الموحدة"),
    'access-login-role-control': _("نظام الكنترول المركزي"),
    'access-login-role-enterprise-resource-planning': _("تخطيط موارد المؤسسة"),
    'access-login-role-portal': _("البوابة الإلكترونية"),
    'access-login-role-school': _("نظام المدارس"),
    'access-login-role-university-management-system': _("نظام الجامعات"),
    'access-login-role-institute': _("نظام المعاهد"),
}

# ═══════════════════════════════════════════════════════════════
# 🔑 Keycloak Role → Allowed Company Levels
# ═══════════════════════════════════════════════════════════════
# For each role, the set of CompanyLevelChoices values where
# the role may be assigned.  Set to ALL levels for now — narrow
# per-role when business rules are finalised.
_ALL_LEVELS = {
    CompanyLevelChoices.ADMIN,
    CompanyLevelChoices.MINISTRY,
    CompanyLevelChoices.GOVERNORATE,
    CompanyLevelChoices.DIRECTORATE,
    CompanyLevelChoices.COMPANY,
    CompanyLevelChoices.COLLEGE,
}

_GOVERNORATE_ONLY = {
    CompanyLevelChoices.ADMIN,
    CompanyLevelChoices.MINISTRY,
    CompanyLevelChoices.GOVERNORATE,
    CompanyLevelChoices.DIRECTORATE,
}
KEYCLOAK_ROLE_ALLOWED_LEVELS = {
    'access-login-role-unified-educational-platform':  set(_ALL_LEVELS),
    'access-login-role-control':                       set(_GOVERNORATE_ONLY),
    'access-login-role-enterprise-resource-planning':   set(_ALL_LEVELS),
    'access-login-role-portal':                        set(_ALL_LEVELS),
    'access-login-role-school':                        set(_ALL_LEVELS),
    'access-login-role-university-management-system':   set(_ALL_LEVELS),
    'access-login-role-institute':   set(_ALL_LEVELS),
}

# ═══════════════════════════════════════════════════════════════
# 👤 User Type → Allowed Keycloak Roles
# ═══════════════════════════════════════════════════════════════
# Key: UserType.name_ar (must match DEFAULT_USERTYPES values)
# Value: set of Keycloak role names this user type can be assigned
# If a user type is NOT listed here, ALL roles are allowed.
_ALL_ROLES = set(KEYCLOAK_REALM_ROLES_MAP.keys())
_PORTAL_ONLY = {'access-login-role-portal'}

KEYCLOAK_USERTYPE_ALLOWED_ROLES = {
    'عام':      _ALL_ROLES,
    'طالب':     _PORTAL_ONLY,
    'موظف':     _ALL_ROLES,
    'ولي امر':  _PORTAL_ONLY,
    'مدرس':     _PORTAL_ONLY,
}


class TypeOfMainSystemChoices(models.TextChoices):
    UNIFIED_EDUCATIONAL_PLATFORM = 'access-login-role-unified-educational-platform', _("المنصة التعليمية الموحدة")
    UNIVERSITY = 'access-login-role-university-management-system', _("نظام الجامعات")
    SCHOOL = 'access-login-role-school', _("نظام المدارس")
    PORTAL = 'access-login-role-portal', _("البوابة الإلكترونية")
    CONTROL = 'access-login-role-control', _("نظام الكنترول المركزي")
    ERP = 'access-login-role-enterprise-resource-planning', _("تخطيط موارد المؤسسة")
    INSTITUTE = 'access-login-role-institute', _("نظام المعاهد")
from decouple import config

SYSTEM_BACKEND_LINKS = {
    TypeOfMainSystemChoices.UNIVERSITY: config("UMS_BACKEND_URL"),
    TypeOfMainSystemChoices.SCHOOL: config("SMS_BACKEND_URL"),
    TypeOfMainSystemChoices.PORTAL: config("PORTAL_BACKEND_URL"),
    TypeOfMainSystemChoices.CONTROL: config("CONTROL_BACKEND_URL"),
    TypeOfMainSystemChoices.INSTITUTE: config("INSTITUTE_BACKEND_URL", default=""),
    TypeOfMainSystemChoices.UNIFIED_EDUCATIONAL_PLATFORM: config("UEPS_BACKEND_URL", default=""),
    TypeOfMainSystemChoices.ERP: config("ERP_BACKEND_URL"),
}
SYSTEM_LINKS = {
    'access-login-role-unified-educational-platform': config("UEPS_FRONTEND_URL"),
    'access-login-role-control': config("CONTROL_FRONTEND_URL", default="disable"),
    'access-login-role-enterprise-resource-planning': config("ERP_FRONTEND_URL"),
    'access-login-role-portal': config("PORTAL_FRONTEND_URL"),
    'access-login-role-school': config("SMS_FRONTEND_URL"),
    'access-login-role-university-management-system': config("UMS_FRONTEND_URL"),
    'access-login-role-institute': config("INSTITUTE_FRONTEND_URL", default="disable"),
}

class SettingLevel:
    """Namespace wrapper to expose level/operation related classes and
    maps under a single container. This allows usage like:

        from config.levels import SettingLevel
        SettingLevel.CompanyLevel.COMPANY
        SettingLevel.ACTION_OPERATION_MAP

    The original classes remain defined at module level for backward
    compatibility; this wrapper simply references them.
    """

    CompanyLevelChoices = CompanyLevelChoices
    CompanyLevel = CompanyLevel
    TypeOfMainSystemChoices = TypeOfMainSystemChoices

    required_map = required_map
    null_map = null_map

    OperationTypeChoices = OperationTypeChoices
    ACTION_OPERATION_MAP = ACTION_OPERATION_MAP
    METHOD_OPERATION_MAP = METHOD_OPERATION_MAP
    REPORT_OPERATION_TYPES = REPORT_OPERATION_TYPES
    DEFAULT_OPERATION_TYPES = DEFAULT_OPERATION_TYPES
    SYNC_PUSH_OPERATION_TYPE = SYNC_PUSH_OPERATION_TYPE
    SYNC_PULL_OPERATION_TYPE = SYNC_PULL_OPERATION_TYPE
    DEFAULT_USERTYPES = DEFAULT_USERTYPES
    KEYCLOAK_REALM_ROLES_MAP = KEYCLOAK_REALM_ROLES_MAP
    KEYCLOAK_ROLE_ALLOWED_LEVELS = KEYCLOAK_ROLE_ALLOWED_LEVELS
    SYSTEM_LINKS = SYSTEM_LINKS
    KEYCLOAK_USERTYPE_ALLOWED_ROLES = KEYCLOAK_USERTYPE_ALLOWED_ROLES
    DATABASE_MODEL_MAP = {}



EMPLOYEES_NAME_AR = ["موظف","مدرس"]
