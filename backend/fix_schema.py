import os
import django
from django.db import connection
from django.apps import apps

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
try:
    django.setup()
except Exception:
    # If the settings module is different, try to import manage and get it from there
    pass

def auto_add_missing_columns():
    app_labels = ['academic', 'exams', 'bank']
    app_models = []
    for app_label in app_labels:
        try:
            app_models.extend(apps.get_app_config(app_label).get_models())
        except Exception:
            pass
    
    with connection.cursor() as cursor:
        for model in app_models:
            table_name = model._meta.db_table
            # get existing columns
            cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
            existing_columns = [row[0] for row in cursor.fetchall()]
            
            for field in model._meta.local_fields:
                column_name = field.column
                if column_name not in existing_columns:
                    db_type = field.db_type(connection)
                    if db_type:
                        print(f"[*] Missing column found: {column_name} in {table_name}")
                        try:
                            # Add column safely
                            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {db_type} NULL;")
                            print(f"  ✅ Added {column_name} to {table_name}")
                        except Exception as e:
                            print(f"  ❌ Failed to add {column_name}: {e}")
            
            # Also find columns that are in DB but NOT in model, and drop their NOT NULL constraint
            model_columns = [f.column for f in model._meta.local_fields]
            for col in existing_columns:
                if col not in model_columns:
                    try:
                        cursor.execute(f'ALTER TABLE {table_name} ALTER COLUMN "{col}" DROP NOT NULL;')
                        print(f"  ✅ Dropped NOT NULL from legacy column {col} in {table_name}")
                    except Exception as e:
                        pass

auto_add_missing_columns()
