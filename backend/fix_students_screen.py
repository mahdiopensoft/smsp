import os
import sys
import django

# Setup Django Environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from OpenSoftCoreV41.screens.models.screen import Screen

def fix_students_screen():
    print("🚀 Updating / Registering Students Screen in Database...\n")

    student_screens = Screen.objects.filter(route__in=['students', 'student'])

    fields_def = [
        {
            "icon": "card-account-details-outline",
            "name": "academic_number",
            "index": 1,
            "label": "الرقم الأكاديمي / رقم القيد",
            "required": True
        },
        {
            "icon": "account",
            "name": "name_ar",
            "index": 2,
            "label": "اسم الطالب (عربي)",
            "required": True
        },
        {
            "icon": "account-outline",
            "name": "name_en",
            "index": 3,
            "label": "اسم الطالب (إنجليزي)"
        },
        {
            "icon": "gender-male-female",
            "name": "gender",
            "index": 4,
            "label": "الجنس",
            "type": "select",
            "options": [
                {"label": "ذكر", "value": 1},
                {"label": "أنثى", "value": 2}
            ]
        },
        {
            "icon": "calendar",
            "name": "birthdate",
            "index": 5,
            "label": "تاريخ الميلاد",
            "type": "date"
        },
        {
            "icon": "map-marker-radius",
            "name": "birth_place",
            "index": 6,
            "label": "مكان الميلاد"
        },
        {
            "icon": "phone",
            "name": "phone_number",
            "index": 7,
            "label": "رقم الهاتف"
        },
        {
            "icon": "map-marker",
            "name": "address",
            "index": 8,
            "label": "العنوان"
        },
        {
            "icon": "earth",
            "name": "country",
            "index": 9,
            "name_list": "Country",
            "label": "الدولة / الجنسية"
        },
        {
            "icon": "city",
            "name": "directorate",
            "index": 10,
            "name_list": "Directorate",
            "label": "المديرية"
        },
        {
            "icon": "domain",
            "name": "organization",
            "index": 11,
            "name_list": "Organization",
            "label": "المدرسة / المؤسسة"
        },
        {
            "icon": "check-circle-outline",
            "name": "is_active",
            "index": 12,
            "label": "حالة التفعيل",
            "type": "boolean"
        }
    ]

    json_payload = {
        "fields": fields_def,
        "main_model": "Student"
    }

    if student_screens.exists():
        for s in student_screens:
            print(f"Found Screen: ID={s.id}, Name={s.name_ar}, Route={s.route}")
            s.json_fields = json_payload
            if hasattr(s, 'main_model'):
                s.main_model = "Student"
            s.save()
            print(f" ✅ Screen ID={s.id} updated with main_model='Student'!")
    else:
        print("Screen 'students' not found. Creating a new Screen entry...")
        s = Screen.objects.create(
            name_ar="الطلاب",
            name_en="Students",
            route="students",
            json_fields=json_payload
        )
        if hasattr(s, 'main_model'):
            s.main_model = "Student"
            s.save()
        print(f" ✅ Created new Screen: ID={s.id}, Route='students' with main_model='Student'!")

    # Also scan any other academic screens that may be missing main_model
    all_academic_models = {
        'academic-years': 'AcademicYear',
        'academic-year': 'AcademicYear',
        'educational-stages': 'EducationalStage',
        'educational-stage': 'EducationalStage',
        'levels': 'Level',
        'level': 'Level',
        'tracks': 'Track',
        'track': 'Track',
        'class-tracks': 'ClassTrack',
        'class-track': 'ClassTrack',
        'subjects': 'Subject',
        'subject': 'Subject',
        'class-subjects': 'ClassSubject',
        'class-subject': 'ClassSubject',
        'semesters': 'Semester',
        'semester': 'Semester',
        'units': 'Unit',
        'unit': 'Unit',
        'lessons': 'Lesson',
        'lesson': 'Lesson',
        'learning-outcomes': 'LearningOutcome',
        'learning-outcome': 'LearningOutcome',
        'colleges': 'College',
        'college': 'College',
        'departments': 'Department',
        'department': 'Department',
        'specializations': 'Specialization',
        'specialization': 'Specialization',
        'study-systems': 'StudeySystem',
        'study-system': 'StudeySystem',
        'grading-systems': 'GradingSystem',
        'grading-system': 'GradingSystem',
        'organizations': 'Organization',
        'organization': 'Organization',
    }

    print("\n🔍 Checking other academic screens for missing main_model...")
    for route_name, model_name in all_academic_models.items():
        screens = Screen.objects.filter(route=route_name)
        for sc in screens:
            jf = sc.json_fields or {}
            if not jf.get('main_model'):
                jf['main_model'] = model_name
                sc.json_fields = jf
                if hasattr(sc, 'main_model'):
                    sc.main_model = model_name
                sc.save()
                print(f" ⚙️ Fixed missing main_model for route '{route_name}' -> '{model_name}'")

    print("\n🎉 Done! All academic screens verified.")

if __name__ == '__main__':
    fix_students_screen()
