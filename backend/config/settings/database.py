"""
إعدادات قاعدة البيانات - Database Settings
دعم قواعد بيانات متعددة (PostgreSQL, MySQL, SQLite)
"""
import os
import json
import ast
import logging
from pathlib import Path
from decouple import config
import dj_database_url

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
# 📁 المسار الأساسي
# ═══════════════════════════════════════════════════════════════════════════════
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ═══════════════════════════════════════════════════════════════════════════════
# 🗄️ نوع قاعدة البيانات - Database Type
# ═══════════════════════════════════════════════════════════════════════════════
DB_TYPE_DEFAULT = config('DBTYPEDB', default='sqlite')
DB_TYPE_SCREEN = config('DBTYPESCREEN', default='sqlite')
DB_TYPE_LOG = config('DBTYPELOG', default='sqlite')

# ═══════════════════════════════════════════════════════════════════════════════
# 🔧 إعدادات PostgreSQL
# ═══════════════════════════════════════════════════════════════════════════════
POSTGRES_USER = config('POSTGRES_USER', default='postgres')
POSTGRES_PASSWORD = config('POSTGRES_PASSWORD', default='')
POSTGRES_HOST = config('POSTGRES_HOST', default='localhost')
POSTGRES_PORT = config('POSTGRES_PORT', default='5432')

# ═══════════════════════════════════════════════════════════════════════════════
# 🔧 إعدادات MySQL
# ═══════════════════════════════════════════════════════════════════════════════
MYSQL_USER = config('MYSQL_USER', default='root')
MYSQL_PASSWORD = config('MYSQL_PASSWORD', default='')
MYSQL_HOST = config('MYSQL_HOST', default='127.0.0.1')
MYSQL_PORT = config('MYSQL_PORT', default='3306')

# ═══════════════════════════════════════════════════════════════════════════════
# 🗃️ قواعد البيانات - Databases Configuration
# ═══════════════════════════════════════════════════════════════════════════════
DATABASES = {}

def _get_database_config(db_type: str, db_name: str, is_default: bool = False) -> dict:
    """
    إنشاء إعدادات قاعدة بيانات حسب النوع
    """
    if db_type == 'sqlite':
        return {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / f'{db_name}.sqlite3',
        }
    elif db_type == 'postgresql':
        return {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config(db_name.upper() if not is_default else 'DB', default=db_name),
            'USER': POSTGRES_USER,
            'PASSWORD': POSTGRES_PASSWORD,
            'HOST': POSTGRES_HOST,
            'PORT': POSTGRES_PORT,
            'CONN_MAX_AGE': config('DB_CONN_MAX_AGE', default=0, cast=int),
            'OPTIONS': {
                'connect_timeout': 10,
            },
        }
    elif db_type == 'mysql':
        return {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config(db_name.upper() if not is_default else 'DB', default=db_name),
            'USER': MYSQL_USER,
            'PASSWORD': MYSQL_PASSWORD,
            'HOST': MYSQL_HOST,
            'PORT': MYSQL_PORT,
            'OPTIONS': {
                'ssl': False,
                'charset': 'utf8mb4',
            },
        }
    else:
        raise ValueError(f"Unsupported database type: {db_type}")

# ─────────────────────────────────────────────────────────────────────────────
# قاعدة البيانات الافتراضية - Default Database
# ─────────────────────────────────────────────────────────────────────────────
DATABASES['default'] = _get_database_config(DB_TYPE_DEFAULT, config('DB', default='default'), is_default=True)

# ─────────────────────────────────────────────────────────────────────────────
# قاعدة بيانات الشاشات - Screen Database
# ─────────────────────────────────────────────────────────────────────────────
DATABASES['screen'] = _get_database_config(DB_TYPE_SCREEN, config('SCREEN_DB', default='screen'))

# ─────────────────────────────────────────────────────────────────────────────
# قاعدة بيانات السجلات - Log Database
# ─────────────────────────────────────────────────────────────────────────────
DATABASES['log'] = _get_database_config(DB_TYPE_LOG, config('LOG_DB', default='log'))

# ═══════════════════════════════════════════════════════════════════════════════
# 🔀 موجهات قواعد البيانات - Database Routers
# ═══════════════════════════════════════════════════════════════════════════════
DATABASE_ROUTERS = [
    'config.settings.database_router.DatabaseRouter',
]

# ═══════════════════════════════════════════════════════════════════════════════
# 📋 قواعد بيانات إضافية من متغير البيئة - Extra Databases from ENV
# ═══════════════════════════════════════════════════════════════════════════════
DB_LIST = config('DBLIST', default='[]')

def _parse_db_list(raw: str) -> list:
    """تحليل قائمة قواعد البيانات الإضافية"""
    if not raw or raw == '[]':
        return []
    
    try:
        # محاولة تحليل كـ JSON
        parsed = json.loads(raw)
        if isinstance(parsed, list):
            return parsed
    except json.JSONDecodeError:
        pass
    
    try:
        # محاولة تحليل كـ Python literal
        parsed = ast.literal_eval(raw)
        if isinstance(parsed, list):
            return parsed
    except (ValueError, SyntaxError):
        pass
    
    # تحليل كـ CSV
    entries = [p.strip() for p in raw.split(',') if p.strip()]
    result = []
    
    for entry in entries:
        if '://' in entry:
            # URL format
            try:
                parsed_cfg = dj_database_url.parse(entry)
                result.append(parsed_cfg)
            except Exception as e:
                logger.warning(f"Failed to parse DB URL: {entry}, error: {e}")
        else:
            # Compact format: name:user:pass:host:port
            parts = entry.split(':')
            if len(parts) >= 5:
                result.append({
                    'NAME': parts[0].strip(),
                    'USER': parts[1].strip(),
                    'PASSWORD': parts[2].strip(),
                    'HOST': parts[3].strip(),
                    'PORT': parts[4].strip(),
                })
    
    return result

# إضافة قواعد البيانات الإضافية
_extra_dbs = _parse_db_list(DB_LIST)
for db_config in _extra_dbs:
    db_name = db_config.get('NAME')
    if db_name and db_name not in DATABASES:
        if db_config.get('ENGINE'):
            DATABASES[db_name] = db_config
        else:
            # تحديد المحرك حسب النوع
            engine = 'django.db.backends.postgresql'  # افتراضي
            DATABASES[db_name] = {
                'ENGINE': engine,
                **db_config,
            }
        logger.info(f"Added extra database: {db_name}")
