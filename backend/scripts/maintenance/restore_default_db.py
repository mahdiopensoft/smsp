"""
═══════════════════════════════════════════════════════════════════════════════
🚀 أداة المعالجة والاستعادة الذكية الشاملة لقاعدة بيانات default (question_bank)
═══════════════════════════════════════════════════════════════════════════════
تقوم هذه الأداة بـ:
1. تصحيح قيود قواعد البيانات للأعمدة القديمة (إزالة NOT NULL من أي حقول موروثة).
2. معالجة وتوافق ملفات النسخة الاحتياطية (حذف is_detailed، تصحيح ترتيب الصفوف، توليد order_index للإجابات).
3. استعادة كافة البيانات بالترتيب الطوبولوجي الصحيح لفك الاعتماديات والعلاقات.
"""

import os
import sys
import json
from pathlib import Path

# ضبط مخرجات الطرفية لدعم UTF-8 على ويندوز
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ضبط مسار backend وبيئة Django
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.apps import apps
from django.db import connection
from django.core.management import call_command
from scripts.maintenance.backup_data import sort_fixtures_by_dependency

DEFAULT_BACKUP_DIR = BASE_DIR / 'backup' / '2026-10-11_14-40-47' / 'default'

def step1_fix_database_schema():
    print("\n" + "═" * 80)
    print("🔧 الخطوة 1: تسوية قيود جداول قاعدة البيانات وإزالة قيود NOT NULL الموروثة...")
    print("═" * 80)

    target_apps = ['academic', 'bank', 'exams', 'omr', 'submissions', 'common', 'usermanager', 'templates_engine']
    fixed_columns = 0

    with connection.cursor() as cursor:
        for app_label in target_apps:
            try:
                models = apps.get_app_config(app_label).get_models()
            except Exception:
                continue

            for model in models:
                table_name = model._meta.db_table
                cursor.execute(f"""
                    SELECT column_name, is_nullable 
                    FROM information_schema.columns 
                    WHERE table_name = '{table_name}' AND table_schema = 'public'
                """)
                db_cols = {row[0]: row[1] for row in cursor.fetchall()}
                model_cols = {f.column for f in model._meta.local_fields}

                for col, nullable in db_cols.items():
                    if col not in model_cols and nullable == 'NO':
                        try:
                            cursor.execute(f'ALTER TABLE "{table_name}" ALTER COLUMN "{col}" DROP NOT NULL;')
                            print(f"  ✅ تم إسقاط NOT NULL عن العمود الموروث [{col}] في جدول [{table_name}]")
                            fixed_columns += 1
                        except Exception as e:
                            print(f"  ⚠️ خطأ في معالجة [{col}] في [{table_name}]: {e}")

    print(f"✨ تم فحص الجداول وتسوية ({fixed_columns}) عمود موروث بنجاح.")


def step2_patch_backup_fixtures():
    print("\n" + "═" * 80)
    print("🛠️ الخطوة 2: مواءمة بيانات النسخة الاحتياطية لتتوافق مع بنية النماذج المحدثة...")
    print("═" * 80)

    # 1. معالجة academic/subject.json (حذف is_detailed وترقيم subject_order فريداً)
    subject_file = DEFAULT_BACKUP_DIR / 'academic' / 'subject.json'
    if subject_file.exists():
        with open(subject_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for idx, item in enumerate(data, start=1):
            if 'fields' in item:
                if 'is_detailed' in item['fields']:
                    del item['fields']['is_detailed']
                item['fields']['subject_order'] = idx
        with open(subject_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("  ✅ [academic/subject.json]: تم حذف 'is_detailed' وتعيين تسلسل فريد لـ subject_order.")

    # 2. معالجة academic/schoolsubject.json (حذف is_detailed وترقيم subject_order فريداً)
    school_subject_file = DEFAULT_BACKUP_DIR / 'academic' / 'schoolsubject.json'
    if school_subject_file.exists():
        with open(school_subject_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for idx, item in enumerate(data, start=1):
            if 'fields' in item:
                if 'is_detailed' in item['fields']:
                    del item['fields']['is_detailed']
                item['fields']['subject_order'] = idx
        with open(school_subject_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("  ✅ [academic/schoolsubject.json]: تم حذف 'is_detailed' وتعيين تسلسل فريد لـ subject_order.")

    # 3. تصحيح ترتيب الصف الدراسي رقم 13 لمنع تكرار الترتيب في academic/schoollevel.json
    level_file = DEFAULT_BACKUP_DIR / 'academic' / 'schoollevel.json'
    if level_file.exists():
        with open(level_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        modified = False
        for item in data:
            if item.get('pk') == 13 and item.get('fields', {}).get('order') == 3:
                item['fields']['order'] = 13
                modified = True
        if modified:
            with open(level_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("  ✅ [academic/schoollevel.json]: تم تعديل ترتيب الصف (13) إلى 13 لمنع تعارض الفريد.")

    # 4. ترقيم خيارات الأسئلة order_index في bank/answer.json
    answer_file = DEFAULT_BACKUP_DIR / 'bank' / 'answer.json'
    if answer_file.exists():
        with open(answer_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        modified = False
        q_counters = {}
        for item in data:
            fields = item.get('fields', {})
            if 'order_index' not in fields or fields['order_index'] is None:
                q_id = fields.get('question')
                idx = q_counters.get(q_id, 0)
                fields['order_index'] = idx
                q_counters[q_id] = idx + 1
                modified = True
        if modified:
            with open(answer_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  ✅ [bank/answer.json]: تم ترقيم ({len(data)}) خيار إجابة بتسلسل order_index سليم.")


def step3_restore_fixtures():
    print("\n" + "═" * 80)
    print("🚀 الخطوة 3: استيراد ملفات النسخة الاحتياطية بالترتيب التبعي الذكي...")
    print("═" * 80)

    # قائمة الملفات المستثناة التي ينشئها جانغو تلقائياً أو تسبب تعارض
    EXCLUDED_FIXTURES = {
        'permission.json',        # الأذونات ينشئها Django تلقائياً في migrate
        'deletedobjectlog.json',  # سجلات كائنات محذوفة موروثة
    }

    all_files = list(DEFAULT_BACKUP_DIR.glob('**/*.json'))
    filtered_files = [f for f in all_files if f.name not in EXCLUDED_FIXTURES and f.name != 'manifest.json']

    # ترتيب طوبولوجي
    sorted_files = sort_fixtures_by_dependency(filtered_files, DEFAULT_BACKUP_DIR)

    print(f"📊 إجمالي الملفات المرشحة للاستيراد: {len(sorted_files)} ملفاً.\n")

    successful = set()
    failed = []

    # الجولة الأولى
    print("🔄 الجولة الأولى: الاستيراد حسب أولوية الاعتماديات...")
    for f in sorted_files:
        rel = f.relative_to(DEFAULT_BACKUP_DIR)
        try:
            call_command('loaddata', str(f), database='default', verbosity=0)
            successful.add(f)
            print(f"  ✅ تم بنجاح: {rel}")
        except Exception as err:
            failed.append((f, str(err)))
            print(f"  ⏳ تأجيل: {rel}")

    # الجولة الثانية والثالثة للملفات المؤجلة
    passes = 1
    while failed and passes <= 3:
        passes += 1
        print(f"\n🔄 الجولة {passes}: إعادة محاولة الملفات المؤجلة ({len(failed)} ملف)...")
        current_failed = list(failed)
        failed.clear()
        for f, last_err in current_failed:
            rel = f.relative_to(DEFAULT_BACKUP_DIR)
            try:
                call_command('loaddata', str(f), database='default', verbosity=0)
                successful.add(f)
                print(f"  ✅ تم بنجاح في الجولة {passes}: {rel}")
            except Exception as err:
                failed.append((f, str(err)))

    print("\n" + "═" * 80)
    print(f"🏁 ملخص الاستعادة النهائي:")
    print(f"  ✅ الملفات الناجحة: {len(successful)} من أصل {len(sorted_files)}")
    if failed:
        print(f"  ❌ الملفات التي تعثرت ({len(failed)}):")
        for f, err in failed:
            print(f"     - {f.relative_to(DEFAULT_BACKUP_DIR)}: {err}")
    else:
        print("  🎉 تم استيراد كافة البيانات بنسبة 100% بنجاح تام وبدون أي أخطاء!")
    print("═" * 80 + "\n")


if __name__ == '__main__':
    step1_fix_database_schema()
    step2_patch_backup_fixtures()
    step3_restore_fixtures()

