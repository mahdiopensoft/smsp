import os
import sys
import django

# Setup Django Environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from OpenSoftCoreV41.screens.models.screen import Screen

def update_school_sections_screen():
    print("🚀 جاري تحديث شاشة الشُعب والفصول المدرسية (school-sections) في قاعدة البيانات...\n")

    screen = Screen.objects.filter(route='school-sections').first()
    if not screen:
        screen = Screen.objects.filter(id=87).first()
    if not screen:
        screen = Screen.objects.filter(component='SchoolSectionsView').first()

    fields_def = [
        {
            "icon": "map-marker",
            "name": "governorate",
            "index": 1,
            "label": "المحافظة",
            "name_list": "Governorate",
            "required": True
        },
        {
            "icon": "city",
            "name": "directorate",
            "index": 2,
            "label": "المديرية",
            "name_list": "Directorate",
            "required": True
        },
        {
            "icon": "domain",
            "name": "organization",
            "index": 3,
            "label": "المدرسة / المؤسسة",
            "name_list": "Organization",
            "required": True
        },
        {
            "icon": "routes",
            "name": "class_track",
            "index": 4,
            "label": "مسار الصف",
            "name_list": "SchoolClassTrack",
            "required": True
        },
        {
            "icon": "calendar-clock",
            "name": "academic_year",
            "index": 5,
            "label": "العام الدراسي",
            "name_list": "AcademicYear",
            "required": True
        },
        {
            "icon": "abjad-arabic",
            "name": "name_ar",
            "index": 6,
            "label": "اسم الشعبة / الفصل (عربي)",
            "required": True
        },
        {
            "icon": "alpha-e",
            "name": "name_en",
            "index": 7,
            "label": "اسم الشعبة (إنجليزي)"
        },
        {
            "icon": "barcode",
            "name": "section_code",
            "index": 8,
            "label": "كود الشعبة"
        },
        {
            "icon": "gender-male-female",
            "name": "gender",
            "index": 9,
            "label": "نوع الشعبة",
            "type": "select",
            "options": [
                {"label": "بنين", "value": 1},
                {"label": "بنات", "value": 2},
                {"label": "مشترك", "value": 3}
            ]
        },
        {
            "icon": "counter",
            "name": "max_capacity",
            "index": 10,
            "label": "السعة الاستيعابية"
        },
        {
            "icon": "check-circle-outline",
            "name": "is_active",
            "index": 11,
            "label": "مفعل"
        }
    ]

    payload = {
        "fields": fields_def,
        "main_model": "SchoolSection"
    }

    if screen:
        screen.json_fields = payload
        screen.main_model = "SchoolSection"
        screen.save()
        print(f"✅ تم تحديث الشاشة بنجاح! ID={screen.id}, Route={screen.route}, Fields Count={len(fields_def)}")
    else:
        created = Screen.objects.create(
            route="school-sections",
            name_ar="الشُعب والفصول المدرسية",
            name_en="School Sections",
            component="SchoolSectionsView",
            path="school-sections",
            fk_parent_screen_id=71,
            screen_type=1,
            is_active=True,
            is_report=False,
            icon="google-classroom",
            type_of_screen=3,
            company_level=20,
            for_admin=True,
            for_ministry=True,
            fk_default_system_id=8,
            order_in_default_system=7,
            view="SchoolSectionMVS",
            main_model="SchoolSection",
            json_fields=payload
        )
        print(f"✅ تم إنشاء الشاشة بنجاح! ID={created.id}, Route={created.route}")

if __name__ == '__main__':
    update_school_sections_screen()
