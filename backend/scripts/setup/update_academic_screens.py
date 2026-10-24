"""
═══════════════════════════════════════════════════════════════════════════════
🏛️🏫 سكريبت التحديث الشامل لشاشات المدارس والجامعات في OpenSoftCore
    Comprehensive Screen & Field Schema Updater for Schools & Universities
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import django

# إعداد بيئة جانغو
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from OpenSoftCoreV41.screens.models.screen import Screen

def update_academic_screens():
    print("🚀 بدء التحديث الشامل لشاشات تهيئة المدارس والجامعات لتطابق المعمارية الجديدة...\n")

    # ═══════════════════════════════════════════════════════════════════════════
    # 1. المجلدات الرئيسية (Folders - screen_type = 3)
    # ═══════════════════════════════════════════════════════════════════════════

    # المجلد الرئيسي: التهيئة العامة المشتركة
    common_folder = Screen.objects.filter(screen_type=3, name_ar="التهيئة العامة المشتركة").exclude(id=85).first()
    if not common_folder:
        try:
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
        except Exception:
            from django.db import router, connections
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
    print(f" ✅ تم ضبط المجلد الرئيسي (ID={common_folder.id}): ⚙️ التهيئة العامة المشتركة")

    # نسخ صلاحيات العرض من مجلد المدارس 71 إلى المجلد المشترك لضمان ظهوره للجميع
    try:
        from django.apps import apps
        ScreenPermission = apps.get_model('screens', 'ScreenPermission')
        GroupScreenPermission = apps.get_model('screens', 'GroupScreenPermission')

        perm_common, _ = ScreenPermission.objects.get_or_create(
            fk_screen=common_folder,
            operation_type=1
        )
        p71 = ScreenPermission.objects.filter(fk_screen_id=71, operation_type=1).first()
        if p71:
            for gp in GroupScreenPermission.objects.filter(fk_screen_permission=p71):
                GroupScreenPermission.objects.get_or_create(
                    group_id=gp.group_id,
                    fk_screen_permission=perm_common,
                    defaults={'is_related': gp.is_related}
                )
            print(" 🔑 تم نسخ وتأكيد صلاحيات العرض لمجلد التهيئة العامة المشتركة بنجاح")
    except Exception as e:
        print(f" ⚠️ ملاحظة حول صلاحيات المجلد: {e}")

    # المجلد 71: تهيئة المدارس
    school_folder, _ = Screen.objects.get_or_create(id=71)
    school_folder.name_ar = "تهيئة المدارس"
    school_folder.name_en = "Schools Setup"
    school_folder.icon = "school"
    school_folder.route = None
    school_folder.component = None
    school_folder.path = None
    school_folder.fk_parent_screen = None
    school_folder.screen_type = 3
    school_folder.is_active = True
    school_folder.is_report = False
    school_folder.type_of_screen = None
    school_folder.type_of_main_system = "access-login-role-unified-educational-platform"
    school_folder.company_level = 20
    school_folder.for_admin = True
    school_folder.for_ministry = True
    school_folder.for_college = False
    school_folder.fk_default_system_id = 8
    school_folder.order_in_default_system = 2
    school_folder.save()
    print(" ✅ تم ضبط المجلد الرئيسي (ID=71): 🏫 تهيئة المدارس")

    # المجلد 72: تهيئة الجامعات
    univ_folder, _ = Screen.objects.get_or_create(id=72)
    univ_folder.name_ar = "تهيئة الجامعات"
    univ_folder.name_en = "Universities Setup"
    univ_folder.icon = "domain"
    univ_folder.route = None
    univ_folder.component = None
    univ_folder.path = None
    univ_folder.fk_parent_screen = None
    univ_folder.screen_type = 3
    univ_folder.is_active = True
    univ_folder.is_report = False
    univ_folder.type_of_screen = None
    univ_folder.type_of_main_system = "access-login-role-university-management-system"
    univ_folder.company_level = 50
    univ_folder.for_admin = True
    univ_folder.for_ministry = True
    univ_folder.for_college = True
    univ_folder.fk_default_system_id = 8
    univ_folder.order_in_default_system = 3
    univ_folder.save()
    print(" ✅ تم ضبط المجلد الرئيسي (ID=72): 🏛️ تهيئة الجامعات")

    # المجلد 73: تهيئة المعاهد ومراكز التدريب المهني
    inst_folder, _ = Screen.objects.get_or_create(id=73)
    inst_folder.name_ar = "تهيئة المعاهد"
    inst_folder.name_en = "Institutes Setup"
    inst_folder.icon = "domain"
    inst_folder.route = None
    inst_folder.component = None
    inst_folder.path = None
    inst_folder.fk_parent_screen = None
    inst_folder.screen_type = 3
    inst_folder.is_active = True
    inst_folder.is_report = False
    inst_folder.type_of_screen = None
    inst_folder.type_of_main_system = "access-login-role-unified-educational-platform"
    inst_folder.company_level = 30
    inst_folder.for_admin = True
    inst_folder.for_ministry = True
    inst_folder.for_college = True
    inst_folder.fk_default_system_id = 8
    inst_folder.order_in_default_system = 4
    inst_folder.save()
    print(" ✅ تم ضبط المجلد الرئيسي (ID=73): 🏢 تهيئة المعاهد")

    # المجلد 70: الهيكل الجغرافي والإقليمي
    geo_folder, _ = Screen.objects.get_or_create(id=70)
    geo_folder.name_ar = "الهيكل الجغرافي والإقليمي"
    geo_folder.name_en = "Geographical Hierarchy"
    geo_folder.icon = "earth"
    geo_folder.screen_type = 3
    geo_folder.is_active = True
    geo_folder.fk_default_system_id = 8
    geo_folder.order_in_default_system = 5
    geo_folder.save()
    print(" ✅ تم ضبط المجلد الرئيسي (ID=70): 🌍 الهيكل الجغرافي والإقليمي")

    # ═══════════════════════════════════════════════════════════════════════════
    # 2. إعداد الشاشات المشتركة لجميع المؤسسات التعليمية (fk_parent_screen = common_folder)
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n⚙️ جاري تحديث الشاشات المشتركة لجميع المؤسسات (المدارس، الجامعات، المعاهد)...")

    common_screens = [
        {
            "id": 69,
            "route": "organizations",
            "component": "OrganizationTree",
            "path": "organizations",
            "name_ar": "هيكلية المؤسسات التعليمية",
            "name_en": "Educational Institutions Structure",
            "icon": "sitemap",
            "view": "OrganizationMVS",
            "main_model": "Organization",
            "order": 1,
            "fields": [
                {"icon": "layers", "name": "company_level", "index": 1, "label": "المستوى الإداري", "name_list": "CompanyLevelFilterChoices"},
                {"icon": "sitemap", "name": "fk_parent_organization", "index": 2, "label": "الجهة الأم", "name_list": "Organization"},
                {"icon": "earth", "name": "fk_country", "index": 3, "label": "الدولة", "name_list": "Country"},
                {"icon": "map-marker", "name": "fk_governorate", "index": 4, "label": "المحافظة", "name_list": "Governorate"},
                {"icon": "city", "name": "fk_directorate", "index": 5, "label": "المديرية", "name_list": "Directorate"},
                {"icon": "map-marker-radius", "name": "fk_region", "index": 6, "label": "المنطقة / العزلة", "name_list": "Region"},
                {"icon": "label", "name": "name_ar", "index": 7, "label": "اسم المنشأة (عربي)", "required": True},
                {"icon": "label", "name": "name_en", "index": 8, "label": "اسم المنشأة (إنجليزي)"},
                {"icon": "office-building", "name": "branch_no", "index": 9, "label": "رقم الفرع"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 10, "label": "نشط"}
            ]
        },
        {
            "id": 32,
            "route": "academic-years",
            "component": "AcademicYearsView",
            "path": "academic-years",
            "name_ar": "الأعوام الدراسية",
            "name_en": "Academic Years",
            "icon": "calendar-clock",
            "view": "AcademicYearMVS",
            "main_model": "AcademicYear",
            "order": 2,
            "fields": [
                {"icon": "calendar-text", "name": "hijri_year", "index": 1, "label": "السنة الهجرية", "required": True},
                {"icon": "calendar-month", "name": "gregorian_year", "index": 2, "label": "السنة الميلادية", "required": True},
                {"icon": "calendar-check", "name": "is_current", "index": 3, "label": "السنة الحالية"}
            ]
        },
        {
            "id": 68,
            "route": "students-master",
            "component": "StudentsView",
            "path": "students-master",
            "name_ar": "الطلاب",
            "name_en": "Students",
            "icon": "account-school",
            "view": "StudentMVS",
            "main_model": "Student",
            "order": 3,
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
        },
    ]

    for cfg in common_screens:
        screen = None
        if cfg["id"]:
            screen = Screen.objects.filter(id=cfg["id"]).first()
        if not screen:
            screen = Screen.objects.filter(route=cfg["route"]).first()
        if not screen:
            screen = Screen.objects.filter(component=cfg["component"]).first()

        if screen:
            screen.fk_parent_screen = common_folder
            screen.order_in_default_system = cfg["order"]
            screen.name_ar = cfg["name_ar"]
            screen.name_en = cfg["name_en"]
            if hasattr(screen, 'name'):
                screen.name = cfg["name_ar"]
            screen.view = cfg["view"]
            screen.icon = cfg["icon"]
            screen.is_active = True
            screen.screen_type = 1
            screen.route = cfg["route"]
            screen.component = cfg["component"]
            screen.path = cfg["path"]
            screen.for_college = True
            screen.for_admin = True
            screen.for_ministry = True
            screen.for_company = True
            screen.for_governorate = True
            screen.for_directorate = True
            screen.for_region = True
            screen.fk_default_system_id = 8
            screen.json_fields = {
                "fields": cfg["fields"],
                "main_model": cfg["main_model"]
            }
            if hasattr(screen, 'main_model'):
                screen.main_model = cfg["main_model"]
            screen.save()

            # التأكد من صلاحيات العرض للشاشات المشتركة
            try:
                s_perm, _ = ScreenPermission.objects.get_or_create(
                    fk_screen=screen,
                    operation_type=1
                )
                if p71:
                    for gp in GroupScreenPermission.objects.filter(fk_screen_permission=p71):
                        GroupScreenPermission.objects.get_or_create(
                            group_id=gp.group_id,
                            fk_screen_permission=s_perm,
                            defaults={'is_related': gp.is_related}
                        )
            except Exception:
                pass

            print(f"  ✓ [{cfg['order']}] تم تحديث شاشة مشتركة: {screen.name_ar} (ID={screen.id}) تحت مجلد: {common_folder.name_ar}")

    # ═══════════════════════════════════════════════════════════════════════════
    # 3. إعداد شاشات المدارس (fk_parent_screen_id = 71)
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n🏫 جاري تحديث شاشات تهيئة المدارس (Schools Setup)...")

    schools_screens = [
        {
            "id": 42,
            "route": "educational-stages",
            "component": "EducationalStagesView",
            "path": "educational-stages",
            "name_ar": "المراحل الدراسية",
            "name_en": "Educational Stages",
            "icon": "stairs",
            "view": "SchoolStageMVS",
            "main_model": "SchoolStage",
            "order": 1,
            "fields": [
                {"icon": "abjad-arabic", "name": "name_ar", "index": 1, "label": "اسم المرحلة (عربي)", "required": True},
                {"icon": "alpha-e", "name": "name_en", "index": 2, "label": "اسم المرحلة (إنجليزي)"},
                {"icon": "sort-numeric-ascending", "name": "order", "index": 3, "label": "الترتيب"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 4, "label": "مفعل"}
            ]
        },
        {
            "id": 41,
            "route": "levels",
            "component": "LevelsView",
            "path": "levels",
            "name_ar": "الصفوف الدراسية",
            "name_en": "School Levels",
            "icon": "bookshelf",
            "view": "SchoolLevelMVS",
            "main_model": "SchoolLevel",
            "order": 2,
            "fields": [
                {"icon": "school", "name": "stage", "index": 1, "label": "المرحلة الدراسية", "name_list": "SchoolStage", "required": True},
                {"icon": "abjad-arabic", "name": "name_ar", "index": 2, "label": "اسم الصف (عربي)", "required": True},
                {"icon": "alpha-e", "name": "name_en", "index": 3, "label": "اسم الصف (إنجليزي)"},
                {"icon": "sort-numeric-ascending", "name": "order", "index": 4, "label": "الترتيب"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 5, "label": "مفعل"}
            ]
        },
        {
            "id": 40,
            "route": "tracks",
            "component": "TracksView",
            "path": "tracks",
            "name_ar": "المسارات التعليمية",
            "name_en": "School Tracks",
            "icon": "source-branch",
            "view": "SchoolTrackMVS",
            "main_model": "SchoolTrack",
            "order": 3,
            "fields": [
                {"icon": "abjad-arabic", "name": "name_ar", "index": 1, "label": "اسم المسار (عربي)", "required": True},
                {"icon": "alpha-e", "name": "name_en", "index": 2, "label": "اسم المسار (إنجليزي)"},
                {"icon": "code-tags", "name": "code", "index": 3, "label": "كود المسار", "required": True},
                {"icon": "note-text", "name": "note", "index": 4, "label": "ملاحظات"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 5, "label": "نشط"}
            ]
        },
        {
            "id": 38,
            "route": "class-tracks",
            "component": "ClassTracksView",
            "path": "class-tracks",
            "name_ar": "مسارات الصفوف",
            "name_en": "School Class Tracks",
            "icon": "routes",
            "view": "SchoolClassTrackMVS",
            "main_model": "SchoolClassTrack",
            "order": 4,
            "fields": [
                {"icon": "bookshelf", "name": "level", "index": 1, "label": "الصف الدراسي", "name_list": "SchoolLevel", "required": True},
                {"icon": "source-branch", "name": "track", "index": 2, "label": "المسار التعليمي", "name_list": "SchoolTrack", "required": True},
                {"icon": "star-outline", "name": "is_default", "index": 3, "label": "مسار افتراضي"},
                {"icon": "note-text", "name": "note", "index": 4, "label": "ملاحظات"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 5, "label": "نشط"}
            ]
        },
        {
            "id": 33,
            "route": "subjects",
            "component": "SubjectsView",
            "path": "subjects",
            "name_ar": "المواد الدراسية",
            "name_en": "School Subjects",
            "icon": "book-open-page-variant",
            "view": "SchoolSubjectMVS",
            "main_model": "SchoolSubject",
            "order": 5,
            "fields": [
                {"icon": "abjad-arabic", "name": "name_ar", "index": 1, "label": "اسم المادة (عربي)", "required": True},
                {"icon": "alpha-e", "name": "name_en", "index": 2, "label": "اسم المادة (إنجليزي)"},
                {"icon": "barcode", "name": "subject_code", "index": 3, "label": "كود المادة الوزاري"},
                {"icon": "sort-numeric-ascending", "name": "subject_order", "index": 4, "label": "ترتيب المادة"},
                {"icon": "bank", "name": "is_ministerial", "index": 5, "label": "مادة وزارية"},
                {"icon": "note-text", "name": "note", "index": 6, "label": "ملاحظات"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 7, "label": "حالة التفعيل"}
            ]
        },
        {
            "id": 63,
            "route": "class-subjects",
            "component": "ClassSubjectsView",
            "path": "class-subjects",
            "name_ar": "مواد مسار الصف",
            "name_en": "School Class Subjects",
            "icon": "link-variant",
            "view": "SchoolClassSubjectMVS",
            "main_model": "SchoolClassSubject",
            "order": 6,
            "fields": [
                {"icon": "routes", "name": "class_track", "index": 1, "label": "مسار الصف", "name_list": "SchoolClassTrack", "required": True},
                {"icon": "book-open-page-variant", "name": "school_subject", "index": 2, "label": "المادة الدراسية المدرسية", "name_list": "SchoolSubject"},
                {"icon": "book-open-outline", "name": "subject", "index": 3, "label": "المادة (تاريخي)", "name_list": "Subject"},
                {"icon": "numeric-1-box-outline", "name": "min_score", "index": 4, "label": "درجة الصغرى (الرسوب)"},
                {"icon": "numeric-9-plus-box-outline", "name": "max_score", "index": 5, "label": "الدرجة الكبرى"},
                {"icon": "plus-box-outline", "name": "added_to_total", "index": 6, "label": "مضاف إلى المجموع"},
                {"icon": "checkbox-blank-outline", "name": "optional", "index": 7, "label": "اختياري"},
                {"icon": "note-text", "name": "note", "index": 8, "label": "ملاحظات"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 9, "label": "نشط"}
            ]
        },
        {
            "id": None,
            "route": "school-sections",
            "component": "SchoolSectionsView",
            "path": "school-sections",
            "name_ar": "الشُعب والفصول المدرسية",
            "name_en": "School Sections",
            "icon": "google-classroom",
            "view": "SchoolSectionMVS",
            "main_model": "SchoolSection",
            "order": 7,
            "fields": [
                {"icon": "domain", "name": "organization", "index": 1, "label": "المدرسة / المؤسسة", "name_list": "Organization", "required": True},
                {"icon": "routes", "name": "class_track", "index": 2, "label": "مسار الصف", "name_list": "SchoolClassTrack"},
                {"icon": "calendar-clock", "name": "academic_year", "index": 3, "label": "العام الدراسي", "name_list": "AcademicYear"},
                {"icon": "abjad-arabic", "name": "name_ar", "index": 4, "label": "اسم الشعبة / الفصل (عربي)", "required": True},
                {"icon": "alpha-e", "name": "name_en", "index": 5, "label": "اسم الشعبة (إنجليزي)"},
                {"icon": "barcode", "name": "section_code", "index": 6, "label": "كود الشعبة"},
                {"icon": "gender-male-female", "name": "gender", "index": 7, "label": "نوع الشعبة (بنين / بنات / مشترك)"},
                {"icon": "counter", "name": "max_capacity", "index": 8, "label": "السعة الاستيعابية"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 9, "label": "مفعل"}
            ]
        },
        {
            "id": 36,
            "route": "units",
            "component": "UnitsView",
            "path": "units",
            "name_ar": "الوحدات الدراسية",
            "name_en": "School Units",
            "icon": "book-multiple",
            "view": "SchoolUnitMVS",
            "main_model": "SchoolUnit",
            "order": 8,
            "fields": [
                {"icon": "link-variant", "name": "class_subject", "index": 1, "label": "مادة مسار الصف", "name_list": "SchoolClassSubject"},
                {"icon": "book-open-page-variant", "name": "school_subject", "index": 2, "label": "المادة الدراسية المدرسية", "name_list": "SchoolSubject"},
                {"icon": "abjad-arabic", "name": "name_ar", "index": 3, "label": "اسم الوحدة (عربي)", "required": True},
                {"icon": "alpha-e", "name": "name_en", "index": 4, "label": "اسم الوحدة (إنجليزي)"},
                {"icon": "sort-numeric-ascending", "name": "order", "index": 5, "label": "الترتيب"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 6, "label": "مفعل"}
            ]
        },
        {
            "id": 35,
            "route": "lessons",
            "component": "LessonsView",
            "path": "lessons",
            "name_ar": "الدروس",
            "name_en": "School Lessons",
            "icon": "bookmark-multiple",
            "view": "SchoolLessonMVS",
            "main_model": "SchoolLesson",
            "order": 9,
            "fields": [
                {"icon": "book-open-page-variant", "name": "subject", "index": 1, "label": "المادة الدراسية المدرسية", "name_list": "SchoolSubject", "required": True},
                {"icon": "folder-outline", "name": "unit", "index": 2, "label": "الوحدة الدراسية", "name_list": "SchoolUnit"},
                {"icon": "abjad-arabic", "name": "name_ar", "index": 3, "label": "اسم الدرس (عربي)", "required": True},
                {"icon": "alpha-e", "name": "name_en", "index": 4, "label": "اسم الدرس (إنجليزي)"},
                {"icon": "sort-numeric-ascending", "name": "order", "index": 5, "label": "الترتيب"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 6, "label": "مفعل"}
            ]
        },
    ]

    for cfg in schools_screens:
        screen = None
        if cfg["id"]:
            screen = Screen.objects.filter(id=cfg["id"]).first()
        if not screen:
            screen = Screen.objects.filter(route=cfg["route"]).first()
        if not screen:
            screen = Screen.objects.filter(component=cfg["component"]).first()

        if not screen and cfg["route"] == "school-sections":
            screen = Screen.objects.create(
                route=cfg["route"],
                name_ar=cfg["name_ar"],
                name_en=cfg["name_en"],
                component=cfg["component"],
                path=cfg["path"],
                fk_parent_screen_id=71,
                screen_type=1,
                is_active=True,
                is_report=False,
                icon=cfg["icon"],
                type_of_screen=3,
                company_level=20,
                for_admin=True,
                for_ministry=True,
                for_college=False,
                fk_default_system_id=8,
                order_in_default_system=cfg["order"],
                view=cfg["view"],
                json_fields={
                    "fields": cfg["fields"],
                    "main_model": cfg["main_model"]
                }
            )
            print(f"  ✓ [{cfg['order']}] تم إنشاء شاشة جديدة: {screen.name_ar} (ID={screen.id})")
        elif screen:
            screen.fk_parent_screen_id = 71
            screen.order_in_default_system = cfg["order"]
            screen.name_ar = cfg["name_ar"]
            screen.name_en = cfg["name_en"]
            screen.route = cfg["route"]
            screen.component = cfg["component"]
            screen.path = cfg["path"]
            if hasattr(screen, 'name'):
                screen.name = cfg["name_ar"]
            screen.view = cfg["view"]
            screen.icon = cfg["icon"]
            screen.is_active = True
            screen.screen_type = 1
            screen.for_college = False
            screen.json_fields = {
                "fields": cfg["fields"],
                "main_model": cfg["main_model"]
            }
            if hasattr(screen, 'main_model'):
                screen.main_model = cfg["main_model"]
            screen.save()
            print(f"  ✓ [{cfg['order']}] تم تحديث شاشة: {screen.name_ar} (ID={screen.id}, View={cfg['view']}, Model={cfg['main_model']})")

    # ═══════════════════════════════════════════════════════════════════════════
    # 3. إعداد شاشات الجامعات (fk_parent_screen_id = 72)
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n🏛️ جاري تحديث شاشات تهيئة الجامعات (Universities Setup)...")

    univ_screens = [
        {
            "id": 74,
            "route": "colleges",
            "component": "CollegesView",
            "path": "colleges",
            "name_ar": "الكليات الجامعية",
            "name_en": "Colleges",
            "icon": "school",
            "view": "UniversityCollegeMVS",
            "main_model": "UniversityCollege",
            "order": 1,
            "fields": [
                {"icon": "barcode", "name": "college_no", "index": 1, "label": "رقم الكلية"},
                {"icon": "abjad-arabic", "name": "name_ar", "index": 2, "label": "اسم الكلية (عربي)", "required": True},
                {"icon": "alpha-e", "name": "name_en", "index": 3, "label": "اسم الكلية (إنجليزي)"},
                {"icon": "sort-numeric-ascending", "name": "highest_level", "index": 4, "label": "أعلى مستوى"},
                {"icon": "calendar-range", "name": "first_year", "index": 5, "label": "سنة التأسيس"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 6, "label": "نشط"}
            ]
        },
        {
            "id": 75,
            "route": "departments",
            "component": "DepartmentsView",
            "path": "departments",
            "name_ar": "الأقسام الأكاديمية",
            "name_en": "Academic Departments",
            "icon": "domain",
            "view": "UniversityDepartmentMVS",
            "main_model": "UniversityDepartment",
            "order": 2,
            "fields": [
                {"icon": "school", "name": "fk_college", "index": 1, "label": "الكلية", "name_list": "UniversityCollege", "required": True},
                {"icon": "abjad-arabic", "name": "name_ar", "index": 2, "label": "اسم القسم (عربي)", "required": True},
                {"icon": "alpha-e", "name": "name_en", "index": 3, "label": "اسم القسم (إنجليزي)"},
                {"icon": "barcode", "name": "section_code", "index": 4, "label": "كود القسم"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 5, "label": "نشط"}
            ]
        },
        {
            "id": 80,
            "route": "specializations",
            "component": "SpecializationsView",
            "path": "specializations",
            "name_ar": "التخصصات والبرامج الأكاديمية",
            "name_en": "Specializations",
            "icon": "book-open-variant",
            "view": "UniversitySpecializationMVS",
            "main_model": "UniversitySpecialization",
            "order": 3,
            "fields": [
                {"icon": "school", "name": "fk_college", "index": 1, "label": "الكلية", "name_list": "UniversityCollege", "required": True},
                {"icon": "domain", "name": "fk_section", "index": 2, "label": "القسم الأكاديمي", "name_list": "UniversityDepartment"},
                {"icon": "abjad-arabic", "name": "name_ar", "index": 3, "label": "اسم التخصص (عربي)", "required": True},
                {"icon": "alpha-e", "name": "name_en", "index": 4, "label": "اسم التخصص (إنجليزي)"},
                {"icon": "barcode", "name": "specialization_code", "index": 5, "label": "كود التخصص"},
                {"icon": "calendar-range", "name": "number_of_levels", "index": 6, "label": "عدد المستويات"},
                {"icon": "calendar-clock", "name": "number_of_semester_each_level", "index": 7, "label": "عدد الفصول لكل مستوى"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 8, "label": "نشط"}
            ]
        },
        {
            "id": 76,
            "route": "educational-levels",
            "component": "EducationalLevelsView",
            "path": "educational-levels",
            "name_ar": "الدرجات والمستويات التعليمية",
            "name_en": "University Levels",
            "icon": "certificate",
            "view": "UniversityLevelMVS",
            "main_model": "UniversityLevel",
            "order": 4,
            "fields": [
                {"icon": "abjad-arabic", "name": "name_ar", "index": 1, "label": "اسم المستوى / الدرجة (عربي)", "required": True},
                {"icon": "alpha-e", "name": "name_en", "index": 2, "label": "اسم المستوى / الدرجة (إنجليزي)"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 3, "label": "نشط"}
            ]
        },
        {
            "id": 77,
            "route": "study-systems",
            "component": "StudySystemsView",
            "path": "study-systems",
            "name_ar": "أنظمة الدراسة",
            "name_en": "Study Systems",
            "icon": "cog-transfer",
            "view": "UniversityStudySystemMVS",
            "main_model": "UniversityStudySystem",
            "order": 5,
            "fields": [
                {"icon": "abjad-arabic", "name": "name_ar", "index": 1, "label": "اسم النظام (عربي)", "required": True},
                {"icon": "alpha-e", "name": "name_en", "index": 2, "label": "اسم النظام (إنجليزي)"},
                {"icon": "barcode", "name": "unified_code", "index": 3, "label": "الكود الموحد"},
                {"icon": "palette", "name": "banner_color", "index": 4, "label": "لون التمييز"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 5, "label": "نشط"}
            ]
        },
        {
            "id": 78,
            "route": "grading-systems",
            "component": "GradingSystemsView",
            "path": "grading-systems",
            "name_ar": "الأنظمة التقديرية والدرجات",
            "name_en": "Grading Systems",
            "icon": "chart-box-outline",
            "view": "UniversityGradingSystemMVS",
            "main_model": "UniversityGradingSystem",
            "order": 6,
            "fields": [
                {"icon": "abjad-arabic", "name": "name_ar", "index": 1, "label": "اسم النظام (عربي)", "required": True},
                {"icon": "alpha-e", "name": "name_en", "index": 2, "label": "اسم النظام (إنجليزي)"},
                {"icon": "counter", "name": "grade_total", "index": 3, "label": "المجموع الكلي"},
                {"icon": "check-decagram-outline", "name": "success_grade", "index": 4, "label": "درجة النجاح"},
                {"icon": "format-list-numbered", "name": "grade_system_type", "index": 5, "label": "نوع النظام التقديري", "name_list": "GradeSystemTypeChoices"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 6, "label": "نشط"}
            ]
        },
        {
            "id": 85,
            "route": "university-courses",
            "component": "UniversityCoursesView",
            "path": "university-courses",
            "name_ar": "المقررات الجامعية",
            "name_en": "University Courses",
            "icon": "book-education",
            "view": "UniversityCourseMVS",
            "main_model": "UniversityCourse",
            "order": 7,
            "fields": [
                {"icon": "barcode", "name": "course_code", "index": 1, "label": "كود المقرر الأكاديمي", "required": True},
                {"icon": "abjad-arabic", "name": "name_ar", "index": 2, "label": "اسم المقرر (عربي)", "required": True},
                {"icon": "alpha-e", "name": "name_en", "index": 3, "label": "اسم المقرر (إنجليزي)"},
                {"icon": "school", "name": "college", "index": 4, "label": "الكلية", "name_list": "UniversityCollege"},
                {"icon": "domain", "name": "department", "index": 5, "label": "القسم الأكاديمي", "name_list": "UniversityDepartment"},
                {"icon": "counter", "name": "credit_hours", "index": 6, "label": "الساعات المعتمدة"},
                {"icon": "book-clock", "name": "lecture_hours", "index": 7, "label": "ساعات المحاضرة (نظري)"},
                {"icon": "flask", "name": "lab_hours", "index": 8, "label": "ساعات المختبر (عملي)"},
                {"icon": "link-variant", "name": "prerequisite_course", "index": 9, "label": "المتطلب السابق", "name_list": "UniversityCourse"},
                {"icon": "format-list-bulleted-type", "name": "course_type", "index": 10, "label": "نوع المتطلب"},
                {"icon": "text", "name": "description", "index": 11, "label": "الوصف ومفردات المقرر"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 12, "label": "حالة التفعيل"}
            ]
        },
        {
            "id": 37,
            "route": "semesters",
            "component": "SemestersView",
            "path": "semesters",
            "name_ar": "الفصول الدراسية",
            "name_en": "University Semesters",
            "icon": "calendar-range",
            "view": "UniversitySemesterMVS",
            "main_model": "UniversitySemester",
            "order": 8,
            "fields": [
                {"icon": "abjad-arabic", "name": "name_ar", "index": 1, "label": "اسم الفصل الدراسي (عربي)", "required": True},
                {"icon": "alpha-e", "name": "name_en", "index": 2, "label": "اسم الفصل الدراسي (إنجليزي)"},
                {"icon": "sort-numeric-ascending", "name": "order", "index": 3, "label": "ترتيب الفصل"},
                {"icon": "calendar-check", "name": "is_current", "index": 4, "label": "الفصل الحالي"},
                {"icon": "note-text", "name": "note", "index": 5, "label": "الملاحظة"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 6, "label": "نشط"}
            ]
        },
        {
            "id": 81,
            "route": "semester-subjects",
            "component": "SemesterSubjectsView",
            "path": "semester-subjects",
            "name_ar": "مقررات الفصول والتخصصات",
            "name_en": "Semester Subjects",
            "icon": "book-cog",
            "view": "UniversitySemesterSubjectMVS",
            "main_model": "UniversitySemesterSubject",
            "order": 9,
            "fields": [
                {"icon": "book-open-variant", "name": "fk_specialization", "index": 1, "label": "التخصص الأكاديمي", "name_list": "UniversitySpecialization", "required": True},
                {"icon": "book-education-outline", "name": "course", "index": 2, "label": "المقرر الجامعي", "name_list": "UniversityCourse"},
                {"icon": "stairs", "name": "level", "index": 3, "label": "المستوى الدراسي", "name_list": "UniversityLevel"},
                {"icon": "calendar-range", "name": "semester", "index": 4, "label": "الفصل الدراسي", "name_list": "UniversitySemester"},
                {"icon": "clock-outline", "name": "number_of_hours", "index": 5, "label": "عدد الساعات المعتمدة"},
                {"icon": "star-outline", "name": "is_core_subject", "index": 6, "label": "مادة أساسية"},
                {"icon": "alert-circle-outline", "name": "is_failed", "index": 7, "label": "يرسب الطالب في المستوى عند رسوبه في هذه المادة"},
                {"icon": "chart-box-outline", "name": "fk_grading_system_june", "index": 8, "label": "نظام الدرجات للملتحقين بنظام العام", "name_list": "UniversityGradingSystem"},
                {"icon": "chart-box-outline", "name": "fk_grading_system_october", "index": 9, "label": "نظام الدرجات للملتحقين بدور أكتوبر", "name_list": "UniversityGradingSystem"},
                {"icon": "chart-box-outline", "name": "fk_grading_system_exempted", "index": 10, "label": "نظام الدرجات للمعفيين", "name_list": "UniversityGradingSystem"},
                {"icon": "chart-box-outline", "name": "fk_grading_system_withdrawn", "index": 11, "label": "نظام الدرجات للمتنازلين", "name_list": "UniversityGradingSystem"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 12, "label": "حالة التفعيل"}
            ]
        },
        {
            "id": 51,
            "route": "exam-periods",
            "component": "ExamPeriodsView",
            "path": "exam-periods",
            "name_ar": "الفترات الامتحانية",
            "name_en": "Exam Periods",
            "icon": "clock-outline",
            "view": "ExamPeriodMVS",
            "main_model": "ExamPeriod",
            "order": 10,
            "fields": [
                {"icon": "calendar-range", "name": "fk_semester", "index": 1, "label": "الفصل الدراسي الجامعي", "name_list": "UniversitySemester", "required": True},
                {"icon": "abjad-arabic", "name": "name_ar", "index": 2, "label": "الاسم (عربي)", "required": True},
                {"icon": "alpha-e", "name": "name_en", "index": 3, "label": "الاسم (إنجليزي)"},
                {"icon": "sort-numeric-ascending", "name": "order", "index": 4, "label": "الترتيب"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 5, "label": "مفعل"}
            ]
        },
    ]

    for cfg in univ_screens:
        screen = None
        if cfg["id"]:
            screen = Screen.objects.filter(id=cfg["id"]).first()
        if not screen:
            screen = Screen.objects.filter(route=cfg["route"]).first()
        if not screen:
            screen = Screen.objects.filter(component=cfg["component"]).first()

        if not screen:
            screen = Screen.objects.create(
                route=cfg["route"],
                name_ar=cfg["name_ar"],
                name_en=cfg["name_en"],
                component=cfg["component"],
                path=cfg["path"],
                fk_parent_screen_id=72,
                screen_type=1,
                is_active=True,
                is_report=False,
                icon=cfg["icon"],
                type_of_screen=3,
                company_level=50,
                for_admin=True,
                for_ministry=True,
                for_college=True,
                fk_default_system_id=8,
                order_in_default_system=cfg["order"],
                view=cfg["view"],
                json_fields={
                    "fields": cfg["fields"],
                    "main_model": cfg["main_model"]
                }
            )
            print(f"  ✓ [{cfg['order']}] تم إنشاء شاشة جامعية جديدة: {screen.name_ar} (ID={screen.id})")
        else:
            screen.fk_parent_screen_id = 72
            screen.order_in_default_system = cfg["order"]
            screen.name_ar = cfg["name_ar"]
            screen.name_en = cfg["name_en"]
            screen.route = cfg["route"]
            screen.component = cfg["component"]
            screen.path = cfg["path"]
            if hasattr(screen, 'name'):
                screen.name = cfg["name_ar"]
            screen.view = cfg["view"]
            screen.icon = cfg["icon"]
            screen.is_active = True
            screen.screen_type = 1
            screen.for_college = True
            screen.json_fields = {
                "fields": cfg["fields"],
                "main_model": cfg["main_model"]
            }
            if hasattr(screen, 'main_model'):
                screen.main_model = cfg["main_model"]
            screen.save()
            print(f"  ✓ [{cfg['order']}] تم تحديث شاشة: {screen.name_ar} (ID={screen.id}, View={cfg['view']}, Model={cfg['main_model']})")

    # ═══════════════════════════════════════════════════════════════════════════
    # 4. إعداد شاشات المعاهد ومراكز التدريب المهني (fk_parent_screen_id = 73)
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n🏢 جاري تحديث شاشات تهيئة المعاهد (Institutes Setup)...")

    inst_screens = [
        {
            "id": None,
            "route": "institutes-fields",
            "component": "InstituteFieldsView",
            "path": "institutes-fields",
            "name_ar": "المجالات المهنية والتقنية",
            "name_en": "Institute Fields",
            "icon": "shape-outline",
            "view": "InstituteFieldMVS",
            "main_model": "InstituteField",
            "order": 1,
            "fields": [
                {"icon": "abjad-arabic", "name": "name_ar", "index": 1, "label": "اسم المجال (عربي)", "required": True},
                {"icon": "alpha-e", "name": "name_en", "index": 2, "label": "اسم المجال (إنجليزي)"},
                {"icon": "barcode", "name": "field_code", "index": 3, "label": "كود المجال", "required": True},
                {"icon": "text", "name": "description", "index": 4, "label": "وصف المجال"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 5, "label": "نشط"}
            ]
        },
        {
            "id": None,
            "route": "institutes-education-systems",
            "component": "InstituteEducationSystemsView",
            "path": "institutes-education-systems",
            "name_ar": "أنظمة التعليم والتدريب",
            "name_en": "Institute Education Systems",
            "icon": "cogs",
            "view": "InstituteEducationSystemMVS",
            "main_model": "InstituteEducationSystem",
            "order": 2,
            "fields": [
                {"icon": "abjad-arabic", "name": "name_ar", "index": 1, "label": "اسم نظام التعليم (عربي)", "required": True},
                {"icon": "alpha-e", "name": "name_en", "index": 2, "label": "اسم نظام التعليم (إنجليزي)"},
                {"icon": "barcode", "name": "system_code", "index": 3, "label": "كود النظام", "required": True},
                {"icon": "format-list-bulleted-type", "name": "system_type", "index": 4, "label": "نوع نظام التعليم", "required": True},
                {"icon": "briefcase-outline", "name": "study_nature", "index": 5, "label": "طبيعة الدراسة (مهني / تقني / مشترك)", "required": True},
                {"icon": "certificate-outline", "name": "admission_qualification", "index": 6, "label": "المؤهل المطلوب للقبول"},
                {"icon": "clock-outline", "name": "duration_years", "index": 7, "label": "مدة الدراسة (بالسنوات)"},
                {"icon": "bank", "name": "has_ministerial_exam", "index": 8, "label": "خاضع للاختبار الوزاري النهائي"},
                {"icon": "calculator-variant-outline", "name": "grading_calculation_method", "index": 9, "label": "آلية احتساب النتائج والمعدلات"},
                {"icon": "text", "name": "description", "index": 10, "label": "الوصف والضوابط"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 11, "label": "نشط"}
            ]
        },
        {
            "id": None,
            "route": "institutes-specializations",
            "component": "InstituteSpecializationsView",
            "path": "institutes-specializations",
            "name_ar": "التخصصات المهنية والتقنية",
            "name_en": "Institute Specializations",
            "icon": "school-outline",
            "view": "InstituteSpecializationMVS",
            "main_model": "InstituteSpecialization",
            "order": 3,
            "fields": [
                {"icon": "abjad-arabic", "name": "name_ar", "index": 1, "label": "اسم التخصص (عربي)", "required": True},
                {"icon": "alpha-e", "name": "name_en", "index": 2, "label": "اسم التخصص (إنجليزي)"},
                {"icon": "barcode", "name": "specialization_code", "index": 3, "label": "كود التخصص", "required": True},
                {"icon": "shape-outline", "name": "field", "index": 4, "label": "المجال المهني / التقني", "name_list": "InstituteField", "required": True},
                {"icon": "cogs", "name": "education_system", "index": 5, "label": "نظام التعليم", "name_list": "InstituteEducationSystem", "required": True},
                {"icon": "domain", "name": "organization", "index": 6, "label": "المعهد / المؤسسة التعليمية", "name_list": "Organization"},
                {"icon": "certificate-outline", "name": "required_qualification", "index": 7, "label": "المؤهل المطلوب للقبول"},
                {"icon": "routes", "name": "accepted_tracks", "index": 8, "label": "المسارات المقبولة (علمي / أدبي / إعدادي)"},
                {"icon": "stairs", "name": "number_of_levels", "index": 9, "label": "عدد المستويات الدراسية"},
                {"icon": "calendar-range", "name": "number_of_semesters_per_level", "index": 10, "label": "عدد الفصول في كل مستوى"},
                {"icon": "file-document-outline", "name": "admission_requirements", "index": 11, "label": "شروط ومتطلبات القبول"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 12, "label": "نشط"}
            ]
        },
        {
            "id": None,
            "route": "institutes-curricula",
            "component": "InstituteCurriculaView",
            "path": "institutes-curricula",
            "name_ar": "الخطط الدراسية للمعاهد",
            "name_en": "Institute Curricula",
            "icon": "notebook-outline",
            "view": "InstituteCurriculumMVS",
            "main_model": "InstituteCurriculum",
            "order": 4,
            "fields": [
                {"icon": "abjad-arabic", "name": "name_ar", "index": 1, "label": "اسم الخطة الدراسية (عربي)", "required": True},
                {"icon": "alpha-e", "name": "name_en", "index": 2, "label": "اسم الخطة الدراسية (إنجليزي)"},
                {"icon": "barcode", "name": "version_code", "index": 3, "label": "رمز / إصدار الخطة", "required": True},
                {"icon": "school-outline", "name": "specialization", "index": 4, "label": "التخصص", "name_list": "InstituteSpecialization", "required": True},
                {"icon": "calendar-clock", "name": "academic_year", "index": 5, "label": "العام الدراسي للاعتماد / البداية", "name_list": "AcademicYear", "required": True},
                {"icon": "check-decagram-outline", "name": "is_approved", "index": 6, "label": "خطة معتمدة"},
                {"icon": "calendar-check", "name": "is_current", "index": 7, "label": "الخطة الحالية للتخصص"},
                {"icon": "counter", "name": "total_credit_hours", "index": 8, "label": "إجمالي الساعات المعتمدة"},
                {"icon": "note-text", "name": "note", "index": 9, "label": "ملاحظات الخطة"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 10, "label": "نشط"}
            ]
        },
        {
            "id": None,
            "route": "institutes-levels",
            "component": "InstituteLevelsView",
            "path": "institutes-levels",
            "name_ar": "المستويات الدراسية للمعاهد",
            "name_en": "Institute Levels",
            "icon": "stairs",
            "view": "InstituteLevelMVS",
            "main_model": "InstituteLevel",
            "order": 5,
            "fields": [
                {"icon": "abjad-arabic", "name": "name_ar", "index": 1, "label": "اسم المستوى (عربي)", "required": True},
                {"icon": "alpha-e", "name": "name_en", "index": 2, "label": "اسم المستوى (إنجليزي)"},
                {"icon": "sort-numeric-ascending", "name": "order", "index": 3, "label": "ترتيب المستوى"},
                {"icon": "note-text", "name": "note", "index": 4, "label": "ملاحظات"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 5, "label": "نشط"}
            ]
        },
        {
            "id": None,
            "route": "institutes-semesters",
            "component": "InstituteSemestersView",
            "path": "institutes-semesters",
            "name_ar": "الفصول والفترات الدراسية",
            "name_en": "Institute Semesters",
            "icon": "calendar-range",
            "view": "InstituteSemesterMVS",
            "main_model": "InstituteSemester",
            "order": 6,
            "fields": [
                {"icon": "abjad-arabic", "name": "name_ar", "index": 1, "label": "اسم الفصل / الفترة (عربي)", "required": True},
                {"icon": "alpha-e", "name": "name_en", "index": 2, "label": "اسم الفصل / الفترة (إنجليزي)"},
                {"icon": "sort-numeric-ascending", "name": "order", "index": 3, "label": "ترتيب الفصل"},
                {"icon": "bank", "name": "semester_nature", "index": 4, "label": "طبيعة الفصل (اعتيادي / نهائي وزاري)", "required": True},
                {"icon": "calendar-check", "name": "is_current", "index": 5, "label": "الفصل الحالي"},
                {"icon": "note-text", "name": "note", "index": 6, "label": "ملاحظات"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 7, "label": "نشط"}
            ]
        },
        {
            "id": None,
            "route": "institutes-subjects",
            "component": "InstituteSubjectsView",
            "path": "institutes-subjects",
            "name_ar": "المواد الدراسية للمعاهد",
            "name_en": "Institute Subjects",
            "icon": "book-open-page-variant",
            "view": "InstituteSubjectMVS",
            "main_model": "InstituteSubject",
            "order": 7,
            "fields": [
                {"icon": "abjad-arabic", "name": "name_ar", "index": 1, "label": "اسم المادة الدراسية (عربي)", "required": True},
                {"icon": "alpha-e", "name": "name_en", "index": 2, "label": "اسم المادة الدراسية (إنجليزي)"},
                {"icon": "barcode", "name": "subject_code", "index": 3, "label": "رمز / كود المادة", "required": True},
                {"icon": "shape-outline", "name": "field", "index": 4, "label": "المجال المهني / التقني", "name_list": "InstituteField"},
                {"icon": "file-tree", "name": "subject_type", "index": 5, "label": "نوع المادة (نظري / عملي / مشترك)", "required": True},
                {"icon": "bank", "name": "subject_entity", "index": 6, "label": "جهة تبعية المادة (وزارية / مؤسسية)", "required": True},
                {"icon": "tag-multiple-outline", "name": "academic_category", "index": 7, "label": "التصنيف الأكاديمي (تخصصية / مساعدة / عامة)", "required": True},
                {"icon": "book-clock", "name": "theoretical_hours", "index": 8, "label": "الساعات النظرية"},
                {"icon": "flask", "name": "practical_hours", "index": 9, "label": "الساعات العملية"},
                {"icon": "counter", "name": "credit_hours", "index": 10, "label": "الساعات المعتمدة"},
                {"icon": "text", "name": "description", "index": 11, "label": "وصف المادة ومفرداتها"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 12, "label": "نشط"}
            ]
        },
        {
            "id": None,
            "route": "institutes-curriculum-subjects",
            "component": "InstituteCurriculumSubjectsView",
            "path": "institutes-curriculum-subjects",
            "name_ar": "مقررات الخطط والفصول الدراسية",
            "name_en": "Curriculum Subjects",
            "icon": "book-cog",
            "view": "InstituteCurriculumSubjectMVS",
            "main_model": "InstituteCurriculumSubject",
            "order": 8,
            "fields": [
                {"icon": "notebook-outline", "name": "curriculum", "index": 1, "label": "الخطة الدراسية", "name_list": "InstituteCurriculum", "required": True},
                {"icon": "book-open-page-variant", "name": "subject", "index": 2, "label": "المادة الدراسية", "name_list": "InstituteSubject", "required": True},
                {"icon": "stairs", "name": "level", "index": 3, "label": "المستوى الدراسي", "name_list": "InstituteLevel", "required": True},
                {"icon": "calendar-range", "name": "semester", "index": 4, "label": "الفصل الدراسي", "name_list": "InstituteSemester", "required": True},
                {"icon": "bank", "name": "is_ministerial_exam", "index": 5, "label": "خاضعة للاختبار الوزاري النهائي"},
                {"icon": "domain", "name": "exam_entity", "index": 6, "label": "جهة عقد الاختبار (وزاري / مؤسسي)"},
                {"icon": "numeric-9-plus-box-outline", "name": "max_score", "index": 7, "label": "الدرجة العظمى"},
                {"icon": "numeric-1-box-outline", "name": "min_score", "index": 8, "label": "درجة النجاح (الصغرى)"},
                {"icon": "plus-box-outline", "name": "added_to_total", "index": 9, "label": "تدخل في احتساب المجموع والمعدل"},
                {"icon": "sort-numeric-ascending", "name": "order", "index": 10, "label": "ترتيب المادة في الخطة"},
                {"icon": "note-text", "name": "note", "index": 11, "label": "ملاحظات"},
                {"icon": "check-circle-outline", "name": "is_active", "index": 12, "label": "نشط"}
            ]
        },
    ]

    # حذف أي شاشات ملغاة من قاعدة البيانات
    deleted_routes = [
        'institutes-admission-requirements',
        'institutes-batches',
        'institutes-short-courses',
        'institutes-special-tracks',
        'learning-outcomes',
    ]
    Screen.objects.filter(route__in=deleted_routes).delete()


    for cfg in inst_screens:
        screen = None
        if cfg["id"]:
            screen = Screen.objects.filter(id=cfg["id"]).first()
        if not screen:
            screen = Screen.objects.filter(route=cfg["route"]).first()
        if not screen:
            screen = Screen.objects.filter(component=cfg["component"]).first()

        if not screen:
            screen = Screen.objects.create(
                route=cfg["route"],
                name_ar=cfg["name_ar"],
                name_en=cfg["name_en"],
                component=cfg["component"],
                path=cfg["path"],
                fk_parent_screen_id=73,
                screen_type=1,
                is_active=True,
                is_report=False,
                icon=cfg["icon"],
                type_of_screen=3,
                company_level=30,
                for_admin=True,
                for_ministry=True,
                for_college=True,
                fk_default_system_id=8,
                order_in_default_system=cfg["order"],
                view=cfg["view"],
                json_fields={
                    "fields": cfg["fields"],
                    "main_model": cfg["main_model"]
                }
            )
            print(f"  ✓ [{cfg['order']}] تم إنشاء شاشة جديدة للمعاهد: {screen.name_ar} (ID={screen.id})")
        else:
            screen.fk_parent_screen_id = 73
            screen.order_in_default_system = cfg["order"]
            screen.name_ar = cfg["name_ar"]
            screen.name_en = cfg["name_en"]
            if hasattr(screen, 'name'):
                screen.name = cfg["name_ar"]
            screen.view = cfg["view"]
            screen.icon = cfg["icon"]
            screen.is_active = True
            screen.screen_type = 1
            screen.for_college = True
            screen.json_fields = {
                "fields": cfg["fields"],
                "main_model": cfg["main_model"]
            }
            if hasattr(screen, 'main_model'):
                screen.main_model = cfg["main_model"]
            screen.save()
            print(f"  ✓ [{cfg['order']}] تم تحديث شاشة المعاهد: {screen.name_ar} (ID={screen.id}, View={cfg['view']}, Model={cfg['main_model']})")

    # ═══════════════════════════════════════════════════════════════════════════
    # 5. تنظيف بادئات الأسماء (م) و (ج)
    # ═══════════════════════════════════════════════════════════════════════════
    cleaned = 0
    for sc in Screen.objects.all():
        updated = False
        for prefix in ["(م) ", "(م)", "(ج) ", "(ج)"]:
            if sc.name_ar and sc.name_ar.startswith(prefix):
                sc.name_ar = sc.name_ar[len(prefix):].strip()
                updated = True
            if hasattr(sc, 'name') and sc.name and sc.name.startswith(prefix):
                sc.name = sc.name[len(prefix):].strip()
                updated = True
        if updated:
            sc.save()
            cleaned += 1

    if cleaned > 0:
        print(f"\n✨ تم تنظيف البادئات من {cleaned} شاشة.")

    # ═══════════════════════════════════════════════════════════════════════════
    # 6. حذف شاشات مخرجات التعلم المحذوفة
    # ═══════════════════════════════════════════════════════════════════════════
    deleted_count, _ = Screen.objects.filter(route__in=['learning-outcomes', 'reports-alignment-matrix']).delete()
    sc39 = Screen.objects.filter(id=39).first()
    if sc39:
        sc39.delete()
    if deleted_count > 0:
        print(f"  🗑️ تم حذف {deleted_count} شاشة لمخرجات التعلم بنجاح.")

    # 7. التأكد من وجود أعمدة الجامعات والمعاهد في جدول الطلاب academic_student
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

    print("\n🎉 اكتمل تحديث وضبط شاشات تهيئة المدارس والجامعات بنجاح تام!")

if __name__ == '__main__':
    update_academic_screens()

