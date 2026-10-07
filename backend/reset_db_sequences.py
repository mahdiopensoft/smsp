import os
import sys
import django

# Setup Django Environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

def reset_all_sequences():
    print("🔄 Resetting all PostgreSQL database sequences...")
    with connection.cursor() as cursor:
        # Get all tables in the public schema
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        fixed_count = 0
        for table in sorted(tables):
            try:
                # Check for sequence on column 'id'
                cursor.execute(f"""
                    SELECT pg_get_serial_sequence('"{table}"', 'id');
                """)
                res = cursor.fetchone()
                seq = res[0] if res else None
                if seq:
                    # Set sequence to MAX(id) + 1
                    cursor.execute(f"""
                        SELECT setval('{seq}', COALESCE((SELECT MAX(id) FROM "{table}"), 0) + 1, false);
                    """)
                    print(f" ✅ Reset sequence for: {table}")
                    fixed_count += 1
            except Exception as e:
                continue
                
    print(f"\n🎉 Successfully synchronized {fixed_count} database table sequences!")

if __name__ == '__main__':
    reset_all_sequences()
