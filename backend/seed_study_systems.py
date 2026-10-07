import os
import sys
import django

# Setup Django Environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from academic.models.universities.UniversityStudySystem import UniversityStudySystem, StudeySystem

def seed_study_systems():
    print("🌱 Seeding Study Systems (الأنظمة الدراسية)...")

    systems_data = [
        {
            "name_ar": "نظام الانتظام الكامل",
            "name_en": "Full-Time / Regular System",
            "unified_code": "REG",
            "banner_color": "#1976D2",
            "is_active": True,
        },
        {
            "name_ar": "نظام الساعات المعتمدة",
            "name_en": "Credit Hours System",
            "unified_code": "CRD",
            "banner_color": "#2E7D32",
            "is_active": True,
        },
        {
            "name_ar": "نظام التعليم المدمج",
            "name_en": "Blended Learning System",
            "unified_code": "BLN",
            "banner_color": "#7B1FA2",
            "is_active": True,
        },
        {
            "name_ar": "نظام التعليم عن بعد / الإلكتروني",
            "name_en": "Distance & Online Learning",
            "unified_code": "ONL",
            "banner_color": "#0288D1",
            "is_active": True,
        },
        {
            "name_ar": "نظام الانتساب الموجه",
            "name_en": "Affiliation / External System",
            "unified_code": "EXT",
            "banner_color": "#E65100",
            "is_active": True,
        },
        {
            "name_ar": "نظام التعليم الموازي / المسائي",
            "name_en": "Evening / Parallel Education",
            "unified_code": "PAR",
            "banner_color": "#455A64",
            "is_active": True,
        },
    ]

    created_count = 0
    updated_count = 0

    for item in systems_data:
        obj, created = StudeySystem.objects.update_or_create(
            unified_code=item["unified_code"],
            defaults={
                "name_ar": item["name_ar"],
                "name_en": item["name_en"],
                "banner_color": item["banner_color"],
                "is_active": item["is_active"],
            }
        )
        if created:
            print(f" ✨ Created: {obj.name_ar} ({obj.unified_code})")
            created_count += 1
        else:
            print(f" 🔄 Updated: {obj.name_ar} ({obj.unified_code})")
            updated_count += 1

    print(f"\n🎉 Successfully seeded Study Systems! ({created_count} created, {updated_count} updated)")

if __name__ == '__main__':
    seed_study_systems()
