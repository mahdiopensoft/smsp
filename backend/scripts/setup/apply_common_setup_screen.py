"""
═══════════════════════════════════════════════════════════════════════════════
⚙️ سكريبت تثبيت مجلد وشاشات التهيئة العامة المشتركة في السايد بار
Fix & Setup Common Academic Setup Screens and Permissions in Sidebar
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import django

# إعداد بيئة جانغو
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.apps import apps
from django.db import router, connections
from OpenSoftCoreV41.screens.models.screen import Screen

def apply_common_setup_screens():
    print("🚀 بدء تثبيت وتفعيل قائمة 'التهيئة العامة المشتركة' في السايد بار...\n")

    ScreenPermission = apps.get_model('screens', 'ScreenPermission')
    GroupScreenPermission = apps.get_model('screens', 'GroupScreenPermission')
    UserScreenPermission = None
    try:
        UserScreenPermission = apps.get_model('screens', 'UserScreenPermission')
    except Exception:
        pass

    ScreenSystemGroup = None
    try:
        ScreenSystemGroup = apps.get_model('screens', 'ScreenSystemGroup')
    except Exception:
        pass

    ScreenSystemUser = None
    try:
        ScreenSystemUser = apps.get_model('screens', 'ScreenSystemUser')
    except Exception:
        pass

    # 1. المجلد الرئيسي: التهيئة العامة المشتركة
    # البحث عن المجلد بشرط ألا يكون ID=85 (لأن 85 محجوز للمقررات الجامعية)
    common_folder = Screen.objects.filter(screen_type=3, name_ar="التهيئة العامة المشتركة").exclude(id=85).first()
    if not common_folder:
        try:
            # الإنشاء عبر ORM بدون تمرير ID لتفادي مشكلة البحث عن السجل قبل إنشائه
            common_folder = Screen(
                name_ar="التهيئة العامة المشتركة",
                name_en="Common Academic Setup",
                icon="tune-vertical",
                screen_type=3,
                is_active=True,
                is_report=False,
                type_of_main_system="access-login-role-unified-educational-platform",
                company_level=20,
                for_admin=True,
                for_ministry=True,
                for_college=True,
                for_company=True,
                for_governorate=True,
                for_directorate=True,
                for_region=True,
                fk_default_system_id=8,
                order_in_default_system=1
            )
            common_folder.save()
            print(f"  ✓ تم إنشاء المجلد عبر ORM بنجاح (ID: {common_folder.id})")
        except Exception as err:
            print(f"  ⚠️ محاولة عبر موجه قاعدة البيانات للشاشات: {err}")
            db_alias = router.db_for_write(Screen) or 'default'
            screen_conn = connections[db_alias]
            actual_table = Screen._meta.db_table
            
            with screen_conn.cursor() as cursor:
                cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{actual_table}'")
                cols = [r[0] for r in cursor.fetchall()]
                
                max_id = Screen.objects.all().order_by('-id').values_list('id', flat=True).first() or 100
                safe_id = max(max_id + 1, 100)
                
                data = {
                    'id': safe_id,
                    'name_ar': "التهيئة العامة المشتركة",
                    'name_en': "Common Academic Setup",
                    'icon': "tune-vertical",
                    'screen_type': 3,
                    'is_active': True,
                    'is_report': False,
                    'type_of_main_system': "access-login-role-unified-educational-platform",
                    'company_level': 20,
                    'for_admin': True,
                    'for_ministry': True,
                    'for_college': True,
                    'for_company': True,
                    'for_governorate': True,
                    'for_directorate': True,
                    'for_region': True,
                    'fk_default_system_id': 8,
                    'order_in_default_system': 1,
                    'is_deleted': False
                }
                filtered_data = {k: v for k, v in data.items() if k in cols}
                cols_str = ', '.join([f'"{k}"' for k in filtered_data.keys()])
                placeholders = ', '.join(['%s'] * len(filtered_data))
                sql = f'INSERT INTO "{actual_table}" ({cols_str}) VALUES ({placeholders})'
                cursor.execute(sql, list(filtered_data.values()))
            common_folder = Screen.objects.get(id=safe_id)

    common_folder.name_ar = "التهيئة العامة المشتركة"
    common_folder.name_en = "Common Academic Setup"
    common_folder.icon = "tune-vertical"
    common_folder.route = None
    common_folder.component = None
    common_folder.path = None
    common_folder.fk_parent_screen = None
    common_folder.screen_type = 3
    common_folder.is_active = True
    common_folder.is_report = False
    common_folder.type_of_screen = None
    common_folder.type_of_main_system = "access-login-role-unified-educational-platform"
    common_folder.company_level = 20
    common_folder.for_admin = True
    common_folder.for_ministry = True
    common_folder.for_college = True
    common_folder.for_company = True
    common_folder.for_governorate = True
    common_folder.for_directorate = True
    common_folder.for_region = True
    common_folder.fk_default_system_id = 8
    common_folder.order_in_default_system = 1
    common_folder.save()

    print(f"  📁 [1] تم تثبيت المجلد الرئيسي: {common_folder.name_ar} (ID: {common_folder.id})")

    # 2. جمع كل مجموعات ومستخدمي النظام 8 لضمان ظهور القائمة للجميع
    groups_in_sys8 = set(
        GroupScreenPermission.objects.filter(
            fk_screen_permission__fk_screen__fk_default_system_id=8
        ).values_list('group_id', flat=True)
    )
    p71 = ScreenPermission.objects.filter(fk_screen_id=71, operation_type=1).first()
    if p71:
        groups_in_sys8.update(
            GroupScreenPermission.objects.filter(fk_screen_permission=p71).values_list('group_id', flat=True)
        )

    users_in_sys8 = set()
    if UserScreenPermission:
        users_in_sys8 = set(
            UserScreenPermission.objects.filter(
                fk_screen_permission__fk_screen__fk_default_system_id=8
            ).values_list('user_id', flat=True)
        )
        if p71:
            users_in_sys8.update(
                UserScreenPermission.objects.filter(fk_screen_permission=p71).values_list('user_id', flat=True)
            )

    # نسخ صلاحيات العرض للمجلد المشترك
    perm_common, _ = ScreenPermission.objects.get_or_create(fk_screen=common_folder, operation_type=1)
    copied_groups = 0
    for gid in groups_in_sys8:
        GroupScreenPermission.objects.get_or_create(
            group_id=gid,
            fk_screen_permission=perm_common,
            defaults={'is_related': False}
        )
        copied_groups += 1

    if UserScreenPermission:
        for uid in users_in_sys8:
            UserScreenPermission.objects.get_or_create(
                user_id=uid,
                fk_screen_permission=perm_common
            )

    if ScreenSystemGroup:
        for gid in groups_in_sys8:
            ScreenSystemGroup.objects.get_or_create(
                group_id=gid,
                fk_screen=common_folder,
                fk_system_id=8,
                defaults={'is_active': True}
            )

    if ScreenSystemUser:
        for uid in users_in_sys8:
            ScreenSystemUser.objects.get_or_create(
                user_id=uid,
                fk_screen=common_folder,
                fk_system_id=8,
                defaults={'is_active': True, 'order': 1}
            )

    print(f"  🔑 تم منح وتأكيد صلاحية العرض للمجلد المشترك لـ ({copied_groups}) مجموعة مستخدمين.")

    # 3. إعداد الشاشات الثلاث المشتركة
    common_screens = [
        {
            "id": 69,
            "route": "organizations",
            "component": "OrganizationTree",
            "path": "organizations",
            "name_ar": "هيكلية المؤسسات التعليمية",
            "name_en": "Educational Institutions Structure",
            "icon": "sitemap",
            "order": 1,
        },
        {
            "id": 32,
            "route": "academic-years",
            "component": "AcademicYearsView",
            "path": "academic-years",
            "name_ar": "الأعوام الدراسية",
            "name_en": "Academic Years",
            "icon": "calendar-clock",
            "order": 2,
        },
        {
            "id": 68,
            "route": "students-master",
            "component": "StudentsView",
            "path": "students-master",
            "name_ar": "الطلاب",
            "name_en": "Students",
            "icon": "account-school",
            "order": 3,
        },
    ]

    for cfg in common_screens:
        screen = None
        if cfg["id"]:
            screen = Screen.objects.filter(id=cfg["id"]).first()
        if not screen:
            screen = Screen.objects.filter(route=cfg["route"]).first()

        if screen:
            screen.fk_parent_screen = common_folder
            screen.order_in_default_system = cfg["order"]
            screen.name_ar = cfg["name_ar"]
            screen.name_en = cfg["name_en"]
            if hasattr(screen, 'name'):
                screen.name = cfg["name_ar"]
            screen.icon = cfg["icon"]
            screen.route = cfg["route"]
            screen.component = cfg["component"]
            screen.path = cfg["path"]
            screen.is_active = True
            screen.screen_type = 1
            screen.for_college = True
            screen.for_admin = True
            screen.for_ministry = True
            screen.for_company = True
            screen.for_governorate = True
            screen.for_directorate = True
            screen.for_region = True
            screen.fk_default_system_id = 8

            # تحديث حقول شاشة الطلاب لتطابق النموذج المشترك
            if screen.route == "students-master":
                screen.json_fields = {
                    "main_model": "Student",
                    "fields": [
                        {"icon": "domain", "name": "organization", "index": 1, "label": "المدرسة / الكلية / المؤسسة", "name_list": "Organization"},
                        {"icon": "identifier", "name": "academic_number", "index": 2, "label": "الرقم الأكاديمي / رقم القيد", "required": True},
                        {"icon": "account", "name": "name_ar", "index": 3, "label": "اسم الطالب (عربي)", "required": True},
                        {"icon": "account", "name": "name_en", "index": 4, "label": "اسم الطالب (إنجليزي)"},
                        {"icon": "gender-male-female", "name": "gender", "index": 5, "label": "الجنس", "required": True},
                        {"icon": "calendar", "name": "birthdate", "index": 6, "label": "تاريخ الميلاد"},
                        {"icon": "map-marker", "name": "birth_place", "index": 7, "label": "مكان الميلاد"},
                        {"icon": "flag", "name": "country", "index": 8, "label": "الدولة / الجنسية", "name_list": "Country"},
                        {"icon": "city", "name": "directorate", "index": 9, "label": "المديرية", "name_list": "Directorate"},
                        {"icon": "phone", "name": "phone_number", "index": 10, "label": "رقم الهاتف"},
                        {"icon": "home", "name": "address", "index": 11, "label": "العنوان ومحل الإقامة"},
                        {"icon": "check-circle-outline", "name": "is_active", "index": 12, "label": "نشط"}
                    ]
                }

            screen.save()

            # منح الصلاحيات للشاشة
            s_perm, _ = ScreenPermission.objects.get_or_create(fk_screen=screen, operation_type=1)
            for gid in groups_in_sys8:
                GroupScreenPermission.objects.get_or_create(
                    group_id=gid,
                    fk_screen_permission=s_perm,
                    defaults={'is_related': False}
                )

            if UserScreenPermission:
                for uid in users_in_sys8:
                    UserScreenPermission.objects.get_or_create(
                        user_id=uid,
                        fk_screen_permission=s_perm
                    )

            if ScreenSystemGroup:
                for gid in groups_in_sys8:
                    ScreenSystemGroup.objects.get_or_create(
                        group_id=gid,
                        fk_screen=screen,
                        fk_system_id=8,
                        defaults={'is_active': True}
                    )

            if ScreenSystemUser:
                for uid in users_in_sys8:
                    ScreenSystemUser.objects.get_or_create(
                        user_id=uid,
                        fk_screen=screen,
                        fk_system_id=8,
                        defaults={'is_active': True, 'order': cfg["order"]}
                    )

            print(f"  ✓ [{cfg['order']}] تم ربط وتفعيل: {screen.name_ar} (ID: {screen.id}) تحت المجلد المشترك.")

    # 4. إعادة ترتيب المجلدات الرئيسية في نظام 8
    Screen.objects.filter(id=71).update(order_in_default_system=2)  # تهيئة المدارس
    Screen.objects.filter(id=72).update(order_in_default_system=3)  # تهيئة الجامعات
    Screen.objects.filter(id=73).update(order_in_default_system=4)  # تهيئة المعاهد
    Screen.objects.filter(id=70).update(order_in_default_system=5)  # الهيكل الجغرافي

    # 5. استعادة شاشة المقررات الجامعية إن كانت تأثرت بـ ID=85
    univ_courses = Screen.objects.filter(id=85).first()
    if univ_courses and univ_courses.name_ar != "المقررات الجامعية":
        univ_courses.name_ar = "المقررات الجامعية"
        univ_courses.name_en = "University Courses"
        univ_courses.route = "university-courses"
        univ_courses.component = "UniversityCoursesView"
        univ_courses.path = "university-courses"
        univ_courses.screen_type = 1
        univ_courses.fk_parent_screen_id = 72
        univ_courses.order_in_default_system = 7
        univ_courses.save()
    # 6. التأكد من وجود أعمدة الجامعات والمعاهد في جدول الطلاب academic_student
    try:
        from django.db import connection
        from academic.models.common.Student import Student
        student_table = Student._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{student_table}'")
            existing_cols = [r[0] for r in cursor.fetchall()]
            for field in Student._meta.local_fields:
                col_name = field.column
                if col_name not in existing_cols:
                    db_type = field.db_type(connection)
                    if db_type:
                        try:
                            cursor.execute(f'ALTER TABLE "{student_table}" ADD COLUMN "{col_name}" {db_type} NULL;')
                            print(f"  ✅ تم إضافة العمود {col_name} إلى جدول {student_table}")
                        except Exception as e:
                            print(f"  ⚠️ تنبيه حول العمود {col_name}: {e}")
    except Exception as e:
        print(f"  ⚠️ تنبيه حول فحص هيكلية جدول الطلاب: {e}")

    print("\n🎉 تم تحديث وحفظ كافة التغييرات ومنح الصلاحيات بنجاح تام!")

if __name__ == '__main__':
    apply_common_setup_screens()

