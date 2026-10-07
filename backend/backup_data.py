"""
═══════════════════════════════════════════════════════════════════════════════
📦 نظام النسخ الاحتياطي والاستعادة لقواعد البيانات المتعددة
   Multi-Database Backup & Dependency-Aware Restore Utility
═══════════════════════════════════════════════════════════════════════════════

قواعد البيانات المدعومة:
1. DB (default)       : question_bank (الأسئلة، الاختبارات، الأكاديمي، OMR، والمستخدمين)
2. SCREEN_DB (screen) : question_bank_screen (الشاشات، الأنظمة، والصلاحيات)
3. LOG_DB (log)       : question_bank_log (سجلات التدقيق والرقابة وسجلات النظام)

المميزات الرئيسية:
- ترتيب طوبولوجي ذكي (Topological Sort) لفك الاعتماديات وتحميل الجداول الأب قبل الابن.
- معالجة العلاقات الخارجية (ForeignKeys / OneToOne) لمنع أخطاء IntegrityError.
- دعم استعادة مجلد كامل دفعة واحدة أو قاعدة بيانات محددة.
- إعادة المحاولة الذكية في حال وجود علاقات دائرية.

أمثلة الاستخدام:
- أخذ نسخة احتياطية لكافة قواعد البيانات:
    python backup_data.py

- أخذ نسخة لقاعدة بيانات محددة:
    python backup_data.py --db default
    python backup_data.py --db screen
    python backup_data.py --db log

- استعادة مجلد default فقط مع مراعاة العلاقات والاعتمادية:
    python backup_data.py --restore backup/2026-08-18_11-00-00/default --db default

- استعادة كافة قواعد البيانات دفعة واحدة:
    python backup_data.py --restore backup/2026-08-18_11-00-00
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# تهيئة بيئة Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.apps import apps
from django.db import router, connections, transaction
from django.core.management import call_command
from django.conf import settings

# مسار مجلد النسخ الاحتياطية
BASE_DIR = Path(__file__).resolve().parent
BACKUP_ROOT = BASE_DIR / 'backup'

# قواعد البيانات المعرفة
DATABASES_INFO = {
    'default': {
        'alias': 'default',
        'env_name': 'DB',
        'display_name': 'question_bank (البيانات الأكاديمية والأسئلة والاختبارات)',
        'description': 'قاعدة البيانات الأساسية للبنك'
    },
    'screen': {
        'alias': 'screen',
        'env_name': 'SCREEN_DB',
        'display_name': 'question_bank_screen (الشاشات والصلاحيات)',
        'description': 'قاعدة بيانات هيكلية الشاشات والصلاحيات'
    },
    'log': {
        'alias': 'log',
        'env_name': 'LOG_DB',
        'display_name': 'question_bank_log (سجلات التدقيق والنظام)',
        'description': 'قاعدة بيانات السجلات والرقابة'
    }
}

# التطبيقات المستثناة من التصدير لتجنب تعارضات النظام
EXCLUDE_APPS = {
    'admin',
    'sessions',
    'contenttypes',
}

# النماذج المستثناة (مثل الجلسات والتوكنز المؤقتة)
EXCLUDE_MODELS = {
    'sessions.session',
    'contenttypes.contenttype',
    'token_blacklist.outstandingtoken',
    'token_blacklist.blacklistedtoken',
}


# ═══════════════════════════════════════════════════════════════════════════════
# 🔍 دوال المساعدة وتحديد التبعيات
# ═══════════════════════════════════════════════════════════════════════════════

def get_target_database_for_model(model):
    """
    تحديد قاعدة البيانات المناسبة للنموذج عبر موجه قواعد البيانات (Database Router)
    """
    try:
        db = router.db_for_read(model)
        if db in DATABASES_INFO:
            return db
    except Exception:
        pass
    
    app_label = model._meta.app_label.lower()
    if 'screen' in app_label:
        return 'screen'
    elif 'log' in app_label:
        return 'log'
    return 'default'


def get_model_from_fixture_file(json_file, backup_db_dir):
    """
    استخراج كائن النموذج من مسار ملف JSON
    المسار المتوقع: backup_dir/db_alias/app_label/model_name.json
    """
    try:
        rel_path = json_file.relative_to(backup_db_dir)
        parts = rel_path.parts
        if len(parts) >= 2:
            app_label = parts[0]
            model_name = json_file.stem
            return apps.get_model(app_label, model_name)
    except Exception:
        pass
    return None


def sort_fixtures_by_dependency(json_files, backup_db_dir):
    """
    ترتيب ملفات الـ JSON ترتيباً طوبولوجياً (Topological Sort)
    بحيث يتم تحميل الجداول الأب (الأصل) أولاً قبل الجداول الابن التي تحتوي على ForeignKeys
    
    الترتيب المنطقي:
    Country ➔ Governorate ➔ Directorate ➔ Region
    AcademicYear ➔ Subject ➔ Level ➔ Unit ➔ Lesson ➔ Question ➔ Answer ➔ QuestionMetrics
    """
    file_model_map = {}
    model_to_file = {}
    
    for f in json_files:
        model = get_model_from_fixture_file(f, backup_db_dir)
        if model:
            file_model_map[f] = model
            model_to_file[model] = f
        else:
            file_model_map[f] = None

    models_in_backup = set(m for m in file_model_map.values() if m is not None)
    
    # بناء شجرة الاعتماديات (Dependencies Graph)
    dependencies = {m: set() for m in models_in_backup}
    for m in models_in_backup:
        for field in m._meta.get_fields():
            if field.is_relation and (field.many_to_one or field.one_to_one):
                related = getattr(field, 'related_model', None)
                # إذا كان النموذج المرتبط موجوداً في نفس قاعدة البيانات وليس علاقة ذاتية
                if related and related in models_in_backup and related != m:
                    dependencies[m].add(related)

    # خوارزمية الترتيب الطوبولوجي (DFS)
    sorted_models = []
    visited = set()

    def visit(model_node, visiting_stack=None):
        if visiting_stack is None:
            visiting_stack = set()
        if model_node in visiting_stack:
            # دائرة اعتماد متبادلة (Circular Dependency) - نتجاوزها
            return
        if model_node not in visited:
            visiting_stack.add(model_node)
            for parent_node in dependencies.get(model_node, set()):
                visit(parent_node, visiting_stack)
            visiting_stack.remove(model_node)
            visited.add(model_node)
            sorted_models.append(model_node)

    for m in models_in_backup:
        visit(m)

    # تحويل النماذج المرتبة إلى مسارات ملفات
    sorted_files = [model_to_file[m] for m in sorted_models if m in model_to_file]
    
    # إضافة أي ملفات لم يتم التعرف على نموذجها في البداية
    for f in json_files:
        if f not in sorted_files:
            sorted_files.insert(0, f)

    return sorted_files


# ═══════════════════════════════════════════════════════════════════════════════
# 💾 دوال التصدير والنسخ الاحتياطي (Backup / Dump)
# ═══════════════════════════════════════════════════════════════════════════════

def dump_model_to_file(model, database_alias, backup_dir):
    """
    تصدير بيانات نموذج محدد إلى ملف JSON مع الحفاظ على المفاتيح الطبيعية
    """
    app_label = model._meta.app_label
    model_name = model._meta.model_name
    model_full_name = f"{app_label}.{model_name}"

    if app_label in EXCLUDE_APPS or model_full_name.lower() in EXCLUDE_MODELS:
        return {'status': 'skipped', 'reason': 'Excluded app/model', 'count': 0, 'size': 0}

    target_dir = backup_dir / database_alias / app_label
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / f"{model_name}.json"

    try:
        count = model.objects.using(database_alias).count()
    except Exception as e:
        return {'status': 'error', 'error': str(e), 'count': 0, 'size': 0}

    if count == 0:
        return {'status': 'empty', 'count': 0, 'size': 0}

    try:
        with open(target_file, 'w', encoding='utf-8') as f:
            call_command(
                'dumpdata',
                model_full_name,
                database=database_alias,
                stdout=f,
                indent=2,
                natural_foreign=True,
                natural_primary=True
            )
        
        file_size = target_file.stat().st_size if target_file.exists() else 0
        return {
            'status': 'success',
            'count': count,
            'size': file_size,
            'file': str(target_file.relative_to(BASE_DIR))
        }
    except Exception as e:
        return {'status': 'error', 'error': str(e), 'count': count, 'size': 0}


def create_backup(selected_db=None):
    """
    إنشاء نسخة احتياطية منظمة لجميع قواعد البيانات أو لقاعدة محددة
    """
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_dir = BACKUP_ROOT / timestamp
    backup_dir.mkdir(parents=True, exist_ok=True)

    target_dbs = [selected_db] if selected_db else list(DATABASES_INFO.keys())

    print("\n" + "═" * 80)
    print(f"🚀 بدء عملية النسخ الاحتياطي: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 مسار الحفظ: {backup_dir}")
    print("═" * 80)

    manifest = {
        'timestamp': timestamp,
        'created_at': datetime.now().isoformat(),
        'databases': {},
        'summary': {
            'total_models': 0,
            'successful_models': 0,
            'empty_models': 0,
            'error_models': 0,
            'total_records': 0,
            'total_size_bytes': 0
        }
    }

    all_models = apps.get_models()

    for db_key in target_dbs:
        db_meta = DATABASES_INFO.get(db_key, {'alias': db_key, 'display_name': db_key})
        print(f"\n📦 [قاعدة البيانات: {db_meta['display_name']}] (Alias: {db_key})")
        print("-" * 80)

        db_models = [m for m in all_models if get_target_database_for_model(m) == db_key]

        manifest['databases'][db_key] = {
            'info': db_meta,
            'models': {}
        }

        for model in db_models:
            app_label = model._meta.app_label
            model_name = model._meta.model_name
            full_name = f"{app_label}.{model_name}"

            result = dump_model_to_file(model, db_key, backup_dir)
            manifest['summary']['total_models'] += 1

            if result['status'] == 'success':
                manifest['summary']['successful_models'] += 1
                manifest['summary']['total_records'] += result['count']
                manifest['summary']['total_size_bytes'] += result['size']
                size_kb = result['size'] / 1024
                print(f"  ✅ {full_name:<35} ➔ {result['count']:>5} سجل ({size_kb:>7.2f} KB)")
            elif result['status'] == 'empty':
                manifest['summary']['empty_models'] += 1
                print(f"  ⚪ {full_name:<35} ➔ (فارغ - 0 سجلات)")
            elif result['status'] == 'skipped':
                print(f"  ⏭️ {full_name:<35} ➔ تم التخطي ({result.get('reason')})")
            elif result['status'] == 'error':
                manifest['summary']['error_models'] += 1
                print(f"  ❌ {full_name:<35} ➔ خطأ: {result.get('error')}")

            manifest['databases'][db_key]['models'][full_name] = result

    # حفظ ملف البيان التعريفي (Manifest)
    manifest_file = backup_dir / 'manifest.json'
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    total_mb = manifest['summary']['total_size_bytes'] / (1024 * 1024)
    print("\n" + "═" * 80)
    print(f"🎉 اكتملت عملية النسخ الاحتياطي بنجاح!")
    print(f"📊 إجمالي السجلات المستخرجة: {manifest['summary']['total_records']:,} سجل")
    print(f"📈 إجمالي الحجم: {total_mb:.2f} MB")
    print(f"📁 المجلد النهائي: {backup_dir}")
    print("═" * 80 + "\n")
    return backup_dir


# ═══════════════════════════════════════════════════════════════════════════════
# 🔄 دوال الاستعادة المتقدمة بفك الاعتماديات (Dependency-Aware Restore)
# ═══════════════════════════════════════════════════════════════════════════════

def restore_database_directory(db_key, db_dir, auto_migrate=False):
    """
    استعادة قاعدة بيانات محددة من مجلدها مع ترتيب الجداول حسب التبعية (الأب ثم الابن)
    """
    if not db_dir.exists():
        print(f"⚠️ مجلد قاعدة البيانات غير موجود: {db_dir}")
        return False

    # 0. إذا كانت قاعدة البيانات جديدة ونريد إنشاء الجداول أولاً (Migration)
    if auto_migrate:
        print(f"\n⚙️ جاري تجهيز وإنشاء الجداول على قاعدة البيانات الجديدة [{db_key}] عبر الهجرات (Migrate)...")
        try:
            call_command('migrate', database=db_key, interactive=False)
            print(f"✅ تم تجهيز هيكل الجداول بنجاح على [{db_key}].")
        except Exception as mig_err:
            print(f"⚠️ تنبيه أثناء تشغيل Migrate على [{db_key}]: {mig_err}")

    raw_files = list(db_dir.glob('**/*.json'))
    # استثناء ملف manifest.json إن وجد
    json_files = [f for f in raw_files if f.name != 'manifest.json']

    if not json_files:
        print(f"⚪ لا توجد ملفات JSON للاستعادة في: {db_dir}")
        return True

    print(f"\n📥 استعادة قاعدة البيانات: [{db_key}]")
    print(f"📁 المجلد: {db_dir}")
    print(f"📊 عدد الملفات المكتشفة: {len(json_files)}")
    print("-" * 80)

    # 1. الترتيب الطوبولوجي التبعي لملفات الـ JSON
    print("🧠 جاري حساب شجرة الاعتماديات وترتيب الجداول (الأصل ➔ الفرع)...")
    sorted_files = sort_fixtures_by_dependency(json_files, db_dir)

    print("📋 ترتيب الاستعادة المعتمد:")
    for idx, f in enumerate(sorted_files, 1):
        rel = f.relative_to(db_dir)
        print(f"   {idx:>2}. {str(rel)}")
    print("-" * 80)

    # 2. محاولة الاستعادة المجمعة دفعة واحدة (Batch Load)
    # تتيح لـ Django تأجيل فحص القيود (Deferred Constraint Checking) داخل معاملة واحدة
    print("🚀 محاولة الاستعادة المجمعة (Atomic Batch Load)...")
    try:
        file_paths = [str(f) for f in sorted_files]
        call_command('loaddata', *file_paths, database=db_key)
        print(f"✨ تم استيراد جميع ملفات [{db_key}] بنجاح دفعة واحدة!")
        return True
    except Exception as batch_error:
        print(f"⚠️ الاستيراد المجمع واجه ملاحظة: {batch_error}")
        print("🔄 جاري التبديل للاستيراد التسلسلي المرتب خطوة بخطوة مع إعادة المحاولة الذكية...")

    # 3. الاستعادة التسلسلية التبعية مع التكرار الذكي (Multi-Pass Retry)
    successful = []
    failed = []

    # الجولة الأولى: حسب الترتيب التبعي
    for json_file in sorted_files:
        rel_name = str(json_file.relative_to(db_dir))
        try:
            call_command('loaddata', str(json_file), database=db_key)
            successful.append(json_file)
            print(f"  ✅ تم استيراد: {rel_name}")
        except Exception as e:
            failed.append((json_file, str(e)))
            print(f"  ⏳ تأجيل استيراد: {rel_name} (بانتظار اكتمال التبعيات)")

    # الجولة الثانية: إعادة محاولة الملفات المؤجلة (في حال وجود Circular FK)
    if failed:
        print("\n🔁 جولة إعادة محاولة الملفات المؤجلة...")
        retry_failed = []
        for json_file, last_err in failed:
            rel_name = str(json_file.relative_to(db_dir))
            try:
                call_command('loaddata', str(json_file), database=db_key)
                successful.append(json_file)
                print(f"  ✅ نجح استيراد: {rel_name} في الجولة الثانية")
            except Exception as e:
                retry_failed.append((json_file, str(e)))
                print(f"  ❌ فشل نهائي لـ {rel_name}: {e}")

        if retry_failed:
            print(f"\n⚠️ عدد الملفات التي فشلت: {len(retry_failed)}")
            return False

    return True


def restore_backup(backup_folder_path, selected_db=None, auto_migrate=False):
    """
    استعادة البيانات من مجلد نسخة احتياطية سابقة
    تدعم:
    - مسار النسخة الكاملة: backup/2026-08-18_11-00-00
    - مسار قاعدة معينة مباشرة: backup/2026-08-18_11-00-00/default
    """
    backup_path = Path(backup_folder_path)
    if not backup_path.is_absolute():
        backup_path = BASE_DIR / backup_folder_path

    if not backup_path.exists():
        print(f"❌ المسار المحدد غير موجود: {backup_path}")
        return

    print("\n" + "═" * 80)
    print(f"🔄 بدء عملية الاستعادة الذكية من: {backup_path}")
    print("═" * 80)

    # التحقق مما إذا كان المسار يشير مباشرة إلى مجلد قاعدة بيانات (مثلاً: .../default)
    dir_name = backup_path.name.lower()
    if dir_name in DATABASES_INFO:
        target_db = selected_db or dir_name
        restore_database_directory(target_db, backup_path, auto_migrate=auto_migrate)
    else:
        # المسار يشير إلى المجلد الرئيسي للنسخة
        target_dbs = [selected_db] if selected_db else list(DATABASES_INFO.keys())
        for db_key in target_dbs:
            db_dir = backup_path / db_key
            if db_dir.exists():
                restore_database_directory(db_key, db_dir, auto_migrate=auto_migrate)

    print("\n" + "═" * 80)
    print("🎉 اكتملت عملية الاستعادة!")
    print("═" * 80 + "\n")


# ═══════════════════════════════════════════════════════════════════════════════
# ⚙️ نقطة الدخول الرئيسية
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="نظام النسخ الاحتياطي والاستعادة الذكي لقواعد البيانات")
    parser.add_argument(
        '--db', 
        choices=['default', 'screen', 'log'], 
        default=None,
        help="تحديد قاعدة بيانات واحدة للعملية (default, screen, log). الافتراضي: الكل"
    )
    parser.add_argument(
        '--restore', 
        type=str, 
        default=None,
        help="مسار مجلد النسخة الاحتياطية لاستعادتها (مثال: backup/2026-08-18_11-00-00 أو backup/2026-08-18_11-00-00/default)"
    )
    parser.add_argument(
        '--migrate',
        action='store_true',
        help="تشغيل migrate تلقائياً لإنشاء الجداول في قاعدة البيانات الجديدة قبل استيراد البيانات"
    )

    args = parser.parse_args()

    if args.restore:
        restore_backup(args.restore, selected_db=args.db, auto_migrate=args.migrate)
    else:
        create_backup(selected_db=args.db)
