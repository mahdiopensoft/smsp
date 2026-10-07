"""
موجه قواعد البيانات الموحد - Unified Database Router
يوجه النماذج والتطبيقات إلى قواعد البيانات المناسبة

الميزات:
- توجيه حسب اسم التطبيق
- توجيه حسب اسم النموذج
- توجيه حسب خريطة DATABASE_MODEL_MAP
- دعم قواعد بيانات متعددة (default, screen, log)
- دعم النسخ المتماثلة (Read Replicas)
"""
from typing import Optional, Dict, Set, List, Any, Type
import logging
from django.conf import settings
from decouple import config

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# 📋 الإعدادات والخرائط
# ═══════════════════════════════════════════════════════════════════════════════

# قاعدة بيانات افتراضية إضافية (من متغيرات البيئة)
DEFAULT1 = config('DEFAULT1', default='default1')

# الحصول على خريطة النماذج من SETTING_LEVEL
provided = getattr(settings, 'SETTING_LEVEL', None)
if not provided:
    _DATABASE_MODEL_MAP: Dict[str, List[str]] = {}
else:
    _DATABASE_MODEL_MAP = getattr(provided, 'DATABASE_MODEL_MAP', {})


# ═══════════════════════════════════════════════════════════════════════════════
# 🗺️ بناء الخرائط الداخلية
# ═══════════════════════════════════════════════════════════════════════════════

# خريطة النموذج الكامل → قاعدة البيانات (app.model → db)
_MODEL_TO_DB: Dict[str, str] = {}

# خريطة اسم النموذج فقط → قاعدة البيانات (model → db)
_MODELNAME_TO_DB: Dict[str, str] = {}

# خريطة التطبيق → قاعدة البيانات (app → db)
_APP_TO_DB: Dict[str, str] = {}


def _build_internal_maps() -> None:
    """
    بناء الخرائط الداخلية من DATABASE_MODEL_MAP
    
    يدعم الصيغ التالية:
    - 'app.model': نموذج محدد
    - 'app.*': جميع نماذج التطبيق
    - 'app': التطبيق بأكمله
    - 'model': اسم النموذج فقط
    """
    for db_name, entries in _DATABASE_MODEL_MAP.items():
        if not entries:
            continue

        # تحويل النص إلى قائمة
        if isinstance(entries, str):
            entries = [e.strip() for e in entries.split(',') if e.strip()]

        for token in entries:
            if not isinstance(token, str):
                continue

            t = token.lower().strip()
            if not t:
                continue

            # الحالة 1: نموذج محدد (app.model)
            if "." in t and not t.endswith(".*"):
                parts = t.rsplit(".", 1)
                if len(parts) == 2:
                    app, model = parts
                    _MODEL_TO_DB[f"{app}.{model}"] = db_name
                continue

            # الحالة 2: جميع نماذج التطبيق (app.*)
            if t.endswith(".*"):
                app = t[:-2]
                _APP_TO_DB[app] = db_name
                continue

            # الحالة 3: اسم التطبيق أو النموذج
            _APP_TO_DB[t] = db_name
            _MODELNAME_TO_DB[t] = db_name


# بناء الخرائط عند تحميل الموجه
_build_internal_maps()


# ═══════════════════════════════════════════════════════════════════════════════
# 🔀 موجه قاعدة البيانات الموحد
# ═══════════════════════════════════════════════════════════════════════════════

class DatabaseRouter:
    """
    موجه قواعد البيانات الموحد
    
    يجمع بين:
    1. التوجيه الصريح للتطبيقات المعروفة (screens, log, gate_sync)
    2. التوجيه الديناميكي من DATABASE_MODEL_MAP
    3. التوجيه التلقائي حسب اسم التطبيق إذا كانت قاعدة البيانات موجودة
    
    أولوية التوجيه:
    1. التوجيه الصريح (أعلى أولوية)
    2. خريطة app.model
    3. خريطة اسم النموذج
    4. خريطة اسم التطبيق
    5. قاعدة بيانات بنفس اسم التطبيق (إن وجدت)
    6. قاعدة البيانات الافتراضية (default)
    """

    # ─────────────────────────────────────────────────────────────────────────
    # 📍 خرائط التطبيقات الصريحة
    # ─────────────────────────────────────────────────────────────────────────
    
    # التطبيقات التي تستخدم قاعدة بيانات الشاشات
    SCREEN_APPS: Set[str] = {
        'screens',
        'OpenSoftCoreV41.screens',
    }
    
    # التطبيقات التي تستخدم قاعدة بيانات السجلات
    LOG_APPS: Set[str] = {
        'log',
        'logging_app',
        'OpenSoftCoreV41.log',
        'OpenSoftCoreV41.logging_app',
    }
    
    # تطبيقات المزامنة
    SYNC_APPS: Set[str] = {
        'gate_sync',
        'OpenSoftCoreV41.gate_sync',
    }
    
    # النماذج المستثناة (تذهب لقاعدة البيانات الافتراضية)
    EXCLUDED_MODELS: Set[str] = {
        'deletedobjectlog',
    }
    
    # التطبيقات التي تستخدم قاعدة البيانات الافتراضية فقط
    DEFAULT_ONLY_APPS: Set[str] = {
        'auth',
        'contenttypes',
        'sessions',
        'admin',
        'usermanager',
        'OpenSoftCoreV41.usermanager',
    }

    # ─────────────────────────────────────────────────────────────────────────
    # 🔧 دوال مساعدة
    # ─────────────────────────────────────────────────────────────────────────

    def _get_explicit_db(
        self, 
        model: Optional[Type] = None, 
        app_label: Optional[str] = None, 
        model_name: Optional[str] = None
    ) -> Optional[str]:
        """
        الحصول على قاعدة البيانات بناءً على التوجيه الصريح
        """
        # استخراج المعلومات من النموذج
        if model is not None:
            meta = getattr(model, '_meta', None)
            if meta:
                app_label = app_label or getattr(meta, 'app_label', None)
                model_name = model_name or getattr(meta, 'model_name', None)

        if not app_label:
            return None

        app_lower = app_label.lower()
        model_lower = (model_name or '').lower()

        # التحقق من النماذج المستثناة
        if model_lower in self.EXCLUDED_MODELS:
            return 'default'

        # تطبيقات الشاشات
        if app_lower.endswith('screens') or app_label in self.SCREEN_APPS:
            return 'screen'

        # تطبيقات المزامنة → الشاشات
        if app_lower.endswith('gate_sync') or app_label in self.SYNC_APPS:
            return 'screen'

        # تطبيقات السجلات
        if app_lower == 'log' or app_label in self.LOG_APPS:
            return 'log'

        # قاعدة بيانات مخصصة من متغير البيئة
        if app_lower == DEFAULT1.lower():
            return DEFAULT1

        # التطبيقات الافتراضية فقط
        if app_label in self.DEFAULT_ONLY_APPS:
            return 'default'

        return None

    def _get_db_from_modelmap(self, model: Type) -> Optional[str]:
        """
        الحصول على قاعدة البيانات من خريطة DATABASE_MODEL_MAP
        """
        meta = getattr(model, '_meta', None)
        if not meta:
            return None

        app = meta.app_label.lower()
        model_name = meta.model_name.lower()

        # 1. البحث بالمفتاح الكامل (app.model)
        full_key = f"{app}.{model_name}"
        if full_key in _MODEL_TO_DB:
            return _MODEL_TO_DB[full_key]

        # 2. البحث باسم النموذج فقط
        if model_name in _MODELNAME_TO_DB:
            return _MODELNAME_TO_DB[model_name]

        # 3. البحث باسم التطبيق
        if app in _APP_TO_DB:
            return _APP_TO_DB[app]

        return None

    def _get_auto_db(self, app_label: str) -> Optional[str]:
        """
        التوجيه التلقائي إذا كانت هناك قاعدة بيانات بنفس اسم التطبيق
        """
        if not app_label:
            return None
        
        databases = getattr(settings, 'DATABASES', {})
        if app_label in databases:
            return app_label
        
        return None

    def _resolve_db(
        self, 
        model: Optional[Type] = None, 
        app_label: Optional[str] = None, 
        model_name: Optional[str] = None
    ) -> Optional[str]:
        """
        تحديد قاعدة البيانات المناسبة بالترتيب الصحيح
        """
        # استخراج app_label من النموذج إذا لم يُعطَ
        if model is not None and not app_label:
            meta = getattr(model, '_meta', None)
            if meta:
                app_label = getattr(meta, 'app_label', None)
                model_name = model_name or getattr(meta, 'model_name', None)

        # 1. التوجيه الصريح (أعلى أولوية)
        db = self._get_explicit_db(model, app_label, model_name)
        if db:
            return db

        # 2. خريطة DATABASE_MODEL_MAP
        if model is not None:
            db = self._get_db_from_modelmap(model)
            if db:
                return db

        # 3. التوجيه التلقائي حسب اسم التطبيق
        if app_label:
            db = self._get_auto_db(app_label)
            if db:
                return db

        # 4. الافتراضي
        return None

    # ─────────────────────────────────────────────────────────────────────────
    # 📖 دوال القراءة والكتابة
    # ─────────────────────────────────────────────────────────────────────────

    def db_for_read(self, model: Type, **hints: Any) -> Optional[str]:
        """
        تحديد قاعدة البيانات للقراءة
        """
        return self._resolve_db(model=model)

    def db_for_write(self, model: Type, **hints: Any) -> Optional[str]:
        """
        تحديد قاعدة البيانات للكتابة
        """
        return self._resolve_db(model=model)

    # ─────────────────────────────────────────────────────────────────────────
    # 🔗 السماح بالعلاقات
    # ─────────────────────────────────────────────────────────────────────────

    def allow_relation(self, obj1: Any, obj2: Any, **hints: Any) -> Optional[bool]:
        """
        السماح بالعلاقات بين النماذج
        
        يسمح بالعلاقات إذا كان النموذجان في نفس قاعدة البيانات
        """
        db1 = self.db_for_read(obj1.__class__)
        db2 = self.db_for_read(obj2.__class__)

        # إذا كان كلاهما في نفس قاعدة البيانات
        if db1 and db2:
            return db1 == db2

        # السماح بالعلاقات مع قاعدة البيانات الافتراضية
        if db1 == 'default' or db2 == 'default':
            return True

        return None

    # ─────────────────────────────────────────────────────────────────────────
    # 🔄 السماح بالهجرات
    # ─────────────────────────────────────────────────────────────────────────

    def allow_migrate(
        self, 
        db: str, 
        app_label: str, 
        model_name: Optional[str] = None, 
        **hints: Any
    ) -> Optional[bool]:
        """
        تحديد ما إذا كان يُسمح بالهجرة لتطبيق/نموذج في قاعدة بيانات محددة
        """
        # 1. التوجيه الصريح
        expected_db = self._get_explicit_db(
            app_label=app_label, 
            model_name=model_name
        )
        if expected_db:
            return db == expected_db

        # 2. خريطة DATABASE_MODEL_MAP (باستخدام نموذج وهمي)
        if model_name:
            class _FakeMeta:
                pass
            
            class _FakeModel:
                _meta = _FakeMeta()
            
            _FakeModel._meta.app_label = app_label
            _FakeModel._meta.model_name = model_name
            
            mapped_db = self._get_db_from_modelmap(_FakeModel)
            if mapped_db:
                return db == mapped_db

        # 3. التوجيه التلقائي
        auto_db = self._get_auto_db(app_label)
        if auto_db:
            return db == auto_db

        # 4. السماح فقط في قاعدة البيانات الافتراضية
        return db == 'default'


# ═══════════════════════════════════════════════════════════════════════════════
# 📊 ملخص التوجيه (للتوثيق)
# ═══════════════════════════════════════════════════════════════════════════════
"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                           خريطة توجيه قواعد البيانات                           ║
╠════════════════════════════════════════════════════════════════════════════════╣
║  التطبيق/النموذج              │  قاعدة البيانات                               ║
╠═══════════════════════════════╪════════════════════════════════════════════════╣
║  screens, gate_sync           │  screen                                        ║
║  log, logging_app             │  log                                           ║
║  auth, sessions, admin        │  default                                       ║
║  deletedobjectlog (model)     │  default (استثناء)                             ║
║  DATABASE_MODEL_MAP           │  حسب الخريطة                                   ║
║  اسم التطبيق = اسم DB         │  قاعدة بيانات بنفس الاسم                       ║
║  أي شيء آخر                   │  default                                       ║
╚═══════════════════════════════╧════════════════════════════════════════════════╝
"""
