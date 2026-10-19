"""
═══════════════════════════════════════════════════════════════════════════════
🇾🇪 سكريبت تعبئة الهيكلية التعليمية الكاملة للمدارس اليمنية (Yemen Educational Hierarchy)
المستويات:
  1. 🏛️ الوزارة (Level 20 - Ministry)
  2. 🏢 مكاتب التربية بالمحافظات اليمنية (Level 30 - Governorates)
  3. 🏬 إدارات التربية بالمديريات (Level 40 - Directorates)
  4. 🏫 المدارس النموذجية والحكومية (Level 50 - Schools)
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import django
from datetime import date

# إعداد بيئة جانغو
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from OpenSoftCoreV41.common.models.Branch import Organization
from OpenSoftCoreV41.common.models.Address import Address
from OpenSoftCoreV41.common.models.Country import Country
from OpenSoftCoreV41.common.models.Governorate import Governorate
from OpenSoftCoreV41.common.models.Directorate import Directorate
from academic.models.common.Organization import Organization as AcademicOrganization


def get_or_create_address(country=None, governorate=None, directorate=None, street="الشارع العام"):
    """مساعد لإنشاء سجل عنوان Address مرتبط بالكيان"""
    addr = Address.objects.create(
        fk_country=country,
        fk_governorate=governorate,
        fk_directorate=directorate,
        street=street
    )
    return addr


def seed_yemen_educational_hierarchy():
    print("🚀 بدء تعبئة البيانات الهرمية للمدارس اليمنية (وزارة ← محافظات ← مديريات ← مدارس)... \n")

    # 1. التأكد من وجود دولة اليمن (Country ID = 1)
    yemen, _ = Country.objects.get_or_create(
        id=1,
        defaults={
            "name_ar": "اليمن",
            "name_en": "Yemen",
            "nationality_name_ar": "يمني",
            "nationality_name_en": "Yemeni",
            "code": "1"
        }
    )
    print(f"✅ الدولة المرجعية: {yemen.name_ar} (ID={yemen.id})")

    # التأكد من وجود العقدة الجذرية الإدارية (Level 10) إن وجدت
    root_org = Organization.objects.filter(company_level=10).first()
    if not root_org:
        root_org = Organization.objects.filter(id=1).first()

    # ═══════════════════════════════════════════════════════════════════════════
    # 🏛️ المستوى 1: وزارة التربية والتعليم والبحث العلمي (Level 20 - Ministry)
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n🏛️ [المستوى 20]: ضبط بيانات الوزارة...")
    ministry_addr = get_or_create_address(country=yemen, street="شارع القيادة - التحرير")

    ministry = Organization.objects.filter(company_level=20).first()
    if not ministry:
        ministry = Organization.objects.filter(id=2).first()

    ministry_data = {
        "name_ar": "وزارة التربية والتعليم والبحث العلمي",
        "name_en": "Ministry of Education & Scientific Research",
        "company_level": 20,
        "type_of_main_system": "access-login-role-unified-educational-platform",
        "fk_parent_organization": root_org,
        "fk_country": yemen,
        "fk_governorate": None,
        "fk_directorate": None,
        "fk_region": None,
        "fk_address": ministry_addr,
        "branch_no": "100",
        "url": "moe-ye",
        "established_date": date(1962, 9, 26),
        "description": "المقر الرئيسي لوزارة التربية والتعليم والبحث العلمي - الجمهورية اليمنية",
        "license_number": 10001,
        "boss": "وزير التربية والتعليم والبحث العلمي",
        "coordinate": "15.3582, 44.2056",
        "student_type": 1,
        "branch_type": 1,
        "academic_id_length": 12,
        "default_user_name_for_employees": "employee",
        "default_password_for_employees": "Emp@123456",
        "default_user_name_for_students": "student",
        "default_password_for_students": "Stu@123456",
        "use_hijri_calendar": True,
        "attendance_twice": False,
        "card_title": "وزارة التربية والتعليم",
        "card_title_color": "#1E3A8A",
        "card_info_title": "الجمهورية اليمنية",
        "card_info_title_color": "#047857",
        "is_deleted": False,
    }

    if ministry:
        for k, v in ministry_data.items():
            setattr(ministry, k, v)
        ministry.save()
        print(f" ✅ تم تحديث الوزارة المركزية: {ministry.name_ar} (ID={ministry.id})")
    else:
        ministry = Organization.objects.create(**ministry_data)
        print(f" ✨ تم إنشاء الوزارة المركزية: {ministry.name_ar} (ID={ministry.id})")

    # مزامنة الوزارة مع academic.Organization
    AcademicOrganization.objects.update_or_create(
        name_ar="وزارة التربية والتعليم",
        defaults={
            "name_en": "Ministry of Education",
            "institution_type": "ministry",
            "difficulty_modifier": 1.0,
            "is_active": True
        }
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # 🏢 المستوى 2: مكاتب التربية والتعليم بالمحافظات (Level 30 - Governorates)
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n🏢 [المستوى 30]: إنشاء وتحديث مكاتب التربية بالمحافظات...")

    governorates_config = [
        {"gov_id": 1, "code": "01", "name": "أمانة العاصمة", "en": "Amanat Al-Asimah", "boss": "أ. عبد القادر المهدي", "street": "شارع بغداد", "coord": "15.3500, 44.2000"},
        {"gov_id": 2, "code": "02", "name": "محافظة صنعاء", "en": "Sana'a Governorate", "boss": "أ. هادي عمار", "street": "شارع الستين الجنوبي", "coord": "15.3200, 44.2300"},
        {"gov_id": 12, "code": "12", "name": "محافظة تعز", "en": "Taiz Governorate", "boss": "أ. عبد الجليل السامعي", "street": "شارع جمال عبد الناصر", "coord": "13.5789, 44.0219"},
        {"gov_id": 4, "code": "04", "name": "محافظة الحديدة", "en": "Al-Hudaydah Governorate", "boss": "أ. عمر بحر", "street": "شارع الكورنيش", "coord": "14.7978, 42.9545"},
        {"gov_id": 8, "code": "08", "name": "محافظة إب", "en": "Ibb Governorate", "boss": "أ. محمد الغزالي", "street": "شارع العدين", "coord": "13.9667, 44.1833"},
        {"gov_id": 5, "code": "05", "name": "محافظة ذمار", "en": "Dhamar Governorate", "boss": "أ. محمد الهادي", "street": "شارع رداع", "coord": "14.5427, 44.4051"},
        {"gov_id": 6, "code": "06", "name": "محافظة عمران", "en": "Amran Governorate", "boss": "أ. أحمد الشهاري", "street": "الشارع العام - عمران", "coord": "15.6594, 43.9439"},
        {"gov_id": 7, "code": "07", "name": "محافظة حجة", "en": "Hajjah Governorate", "boss": "أ. علي القطيب", "street": "شارع النصر", "coord": "15.6942, 43.6033"},
        {"gov_id": 9, "code": "09", "name": "محافظة صعدة", "en": "Sa'ada Governorate", "boss": "أ. عبد الرحمن الظرافي", "street": "الشارع الرئيسي", "coord": "16.9402, 43.7639"},
        {"gov_id": 10, "code": "10", "name": "محافظة البيضاء", "en": "Al-Bayda Governorate", "boss": "أ. سرحان سواد", "street": "شارع الكويت", "coord": "13.9852, 45.5727"},
    ]

    gov_org_map = {}  # gov_id -> Organization object

    for idx, g_info in enumerate(governorates_config, start=1):
        gov_obj = Governorate.objects.filter(id=g_info["gov_id"]).first()
        if not gov_obj:
            gov_obj = Governorate.objects.filter(code=g_info["code"]).first()

        branch_no = f"30{idx:02d}"
        url_slug = f"gov-{g_info['code']}"

        gov_addr = get_or_create_address(country=yemen, governorate=gov_obj, street=g_info["street"])

        gov_org, created = Organization.objects.update_or_create(
            branch_no=branch_no,
            defaults={
                "name_ar": f"مكتب التربية والتعليم - {g_info['name']}",
                "name_en": f"Education Office - {g_info['en']}",
                "company_level": 30,
                "type_of_main_system": "access-login-role-unified-educational-platform",
                "fk_parent_organization": ministry,
                "fk_country": yemen,
                "fk_governorate": gov_obj,
                "fk_directorate": None,
                "fk_address": gov_addr,
                "url": url_slug,
                "established_date": date(1975, 5, 1),
                "description": f"المكتب الإشرافي للتربية والتعليم في {g_info['name']}",
                "license_number": 20000 + idx,
                "boss": g_info["boss"],
                "coordinate": g_info["coord"],
                "student_type": 1,
                "branch_type": 1,
                "academic_id_length": 12,
                "default_user_name_for_employees": "employee",
                "default_password_for_employees": "Emp@123456",
                "default_user_name_for_students": "student",
                "default_password_for_students": "Stu@123456",
                "use_hijri_calendar": True,
                "card_title": f"مكتب التربية - {g_info['name']}",
                "card_title_color": "#1E40AF",
                "card_info_title": "وزارة التربية والتعليم",
                "card_info_title_color": "#047857",
                "is_deleted": False,
            }
        )
        gov_org_map[g_info["gov_id"]] = gov_org
        status_txt = "✨ أنشئ" if created else "🔄 حُدث"
        print(f"  {status_txt}: {gov_org.name_ar} (ID={gov_org.id})")

    # ═══════════════════════════════════════════════════════════════════════════
    # 🏬 المستوى 3: إدارات التربية والتعليم بالمديريات (Level 40 - Directorates)
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n🏬 [المستوى 40]: إنشاء وتحديث إدارات التربية بالمديريات...")

    directorates_config = [
        # أمانة العاصمة (gov_id=1)
        {"gov_id": 1, "dir_name": "التحرير", "en": "Al-Tahreer", "boss": "أ. نجيب الكبسي", "street": "ميدان التحرير"},
        {"gov_id": 1, "dir_name": "السبعين", "en": "Al-Sabeyn", "boss": "أ. حميد الجرادي", "street": "جولة المصباحي"},
        {"gov_id": 1, "dir_name": "معين", "en": "Mueen", "boss": "أ. علي الديلمي", "street": "شارع الدائري الغربي"},
        {"gov_id": 1, "dir_name": "الثورة", "en": "Al-Thawrah", "boss": "أ. يحيى الشاحذي", "street": "شارع التلفزيون"},
        {"gov_id": 1, "dir_name": "صنعاء القديمة", "en": "Old Sana'a", "boss": "أ. فؤاد المؤيد", "street": "باب اليمن"},
        {"gov_id": 1, "dir_name": "بني الحارث", "en": "Bani Al-Hareth", "boss": "أ. عبد السلام الغليسي", "street": "شارع المطار"},
        {"gov_id": 1, "dir_name": "الوحدة", "en": "Al-Wahdah", "boss": "أ. قاسم الشرماني", "street": "شارع صفر"},
        
        # محافظة صنعاء (gov_id=2)
        {"gov_id": 2, "dir_name": "سنحان", "en": "Sanhan", "boss": "أ. فهد مرشد", "street": "ريمة حميد"},
        {"gov_id": 2, "dir_name": "بني مطر", "en": "Bani Matar", "boss": "أ. مقبل الجعدبي", "street": "متنة"},
        {"gov_id": 2, "dir_name": "همدان", "en": "Hamdan", "boss": "أ. راجح الجمالي", "street": "ضلاع همدان"},
        {"gov_id": 2, "dir_name": "الحيمة الداخلية", "en": "Al-Haymah Al-Dakhiliyah", "boss": "أ. عبد الكريم القرعفي", "street": "الشارع العام"},

        # محافظة تعز (gov_id=12)
        {"gov_id": 12, "dir_name": "القاهرة", "en": "Al-Qahirah", "boss": "أ. محمود عبد القادر", "street": "شارع 26 سبتمبر"},
        {"gov_id": 12, "dir_name": "المظفر", "en": "Al-Mudhaffar", "boss": "أ. عادل العليمي", "street": "شارع جمال"},
        {"gov_id": 12, "dir_name": "صالة", "en": "Salah", "boss": "أ. فضل السلامي", "street": "حي الجحملية"},
        {"gov_id": 12, "dir_name": "التعزية", "en": "Al-Ta'iziyah", "boss": "أ. توفيق الصلوي", "street": "مفرق ماوية"},

        # محافظة الحديدة (gov_id=4)
        {"gov_id": 4, "dir_name": "الحوك", "en": "Al-Hawak", "boss": "أ. مصطفى المغلس", "street": "شارع صنعاء"},
        {"gov_id": 4, "dir_name": "الحالي", "en": "Al-Hali", "boss": "أ. حسن الوهباني", "street": "شارع فلسطين"},
        {"gov_id": 4, "dir_name": "الميناء", "en": "Al-Mina", "boss": "أ. إبراهيم شامي", "street": "شارع الكورنيش"},
        {"gov_id": 4, "dir_name": "باجل", "en": "Bajil", "boss": "أ. أحمد الصغير", "street": "الشارع العام - باجل"},

        # محافظة إب (gov_id=8)
        {"gov_id": 8, "dir_name": "الظهار", "en": "Al-Dhihar", "boss": "أ. عصام البرح", "street": "شارع تعز - إب"},
        {"gov_id": 8, "dir_name": "المشنة", "en": "Al-Mashannah", "boss": "أ. هشام الصليحي", "street": "حي المشنة القديم"},
        {"gov_id": 8, "dir_name": "يريم", "en": "Yarim", "boss": "أ. عبد الخالق السراجي", "street": "الشارع العام - يريم"},
        {"gov_id": 8, "dir_name": "جبلة", "en": "Jiblah", "boss": "أ. محمد عبد الله", "street": "شارع الملكة أروى"},

        # محافظة ذمار (gov_id=5)
        {"gov_id": 5, "dir_name": "مدينة ذمار", "en": "Dhamar City", "boss": "أ. عبد الكريم الحبسي", "street": "الشارع العام"},
        {"gov_id": 5, "dir_name": "عنس", "en": "Ans", "boss": "أ. صالح الشعوبي", "street": "طريق ذمار - يريم"},
        {"gov_id": 5, "dir_name": "جهران", "en": "Jahran (Ma'bar)", "boss": "أ. حسين الصوفي", "street": "مدينة معبر"},
    ]

    dir_org_map = {}  # (gov_id, dir_name) -> Organization object

    for idx, d_info in enumerate(directorates_config, start=1):
        parent_gov_org = gov_org_map.get(d_info["gov_id"])
        if not parent_gov_org:
            continue

        gov_obj = parent_gov_org.fk_governorate

        # البحث عن سجل المديرية في جدول Directorate
        dir_obj = Directorate.objects.filter(
            fk_governorate_id=d_info["gov_id"],
            name_ar__icontains=d_info["dir_name"]
        ).first()

        branch_no = f"40{idx:03d}"
        url_slug = f"dir-{d_info['gov_id']}-{idx}"

        dir_addr = get_or_create_address(country=yemen, governorate=gov_obj, directorate=dir_obj, street=d_info["street"])

        dir_org, created = Organization.objects.update_or_create(
            branch_no=branch_no,
            defaults={
                "name_ar": f"إدارة التربية والتعليم - مديرية {d_info['dir_name']}",
                "name_en": f"Education Dept. - {d_info['en']} District",
                "company_level": 40,
                "type_of_main_system": "access-login-role-unified-educational-platform",
                "fk_parent_organization": parent_gov_org,
                "fk_country": yemen,
                "fk_governorate": gov_obj,
                "fk_directorate": dir_obj,
                "fk_address": dir_addr,
                "url": url_slug,
                "established_date": date(1980, 10, 14),
                "description": f"الإدارة التعليمية لمديرية {d_info['dir_name']} التابعة لـ {parent_gov_org.name_ar}",
                "license_number": 30000 + idx,
                "boss": d_info["boss"],
                "coordinate": parent_gov_org.coordinate,
                "student_type": 1,
                "branch_type": 1,
                "academic_id_length": 12,
                "default_user_name_for_employees": "employee",
                "default_password_for_employees": "Emp@123456",
                "default_user_name_for_students": "student",
                "default_password_for_students": "Stu@123456",
                "use_hijri_calendar": True,
                "card_title": f"إدارة التربية - مديرية {d_info['dir_name']}",
                "card_title_color": "#1E40AF",
                "card_info_title": "مكتب التربية والتعليم",
                "card_info_title_color": "#047857",
                "is_deleted": False,
            }
        )
        dir_org_map[(d_info["gov_id"], d_info["dir_name"])] = dir_org
        status_txt = "✨ أنشئ" if created else "🔄 حُدث"
        print(f"  {status_txt}: {dir_org.name_ar} (ID={dir_org.id})")

    # ═══════════════════════════════════════════════════════════════════════════
    # 🏫 المستوى 4: المدارس النموذجية والحكومية (Level 50 - Schools)
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n🏫 [المستوى 50]: إنشاء وتحديث المدارس التابعة للمديريات...")

    schools_config = [
        # مدارس أمانة العاصمة
        {"gov_id": 1, "dir_name": "التحرير", "name": "مدرسة جمال عبد الناصر للمتفوقين", "en": "Gamal Abdel Nasser High School for the Gifted", "boss": "أ. محمد القاسمي", "street": "شارع التحرير العام", "year": 1965, "coord": "15.3530, 44.2040"},
        {"gov_id": 1, "dir_name": "التحرير", "name": "مدرسة بلقيس الثانوية النموذجية للبنات", "en": "Balqees Secondary School for Girls", "boss": "أ. فاطمة الكبسي", "street": "شارع علي عبد المغني", "year": 1968, "coord": "15.3515, 44.2070"},
        {"gov_id": 1, "dir_name": "معين", "name": "مدرسة الكويت الثانوية النموذجية للبنين", "en": "Kuwait Model Secondary School", "boss": "أ. عبد الرحمن الهادي", "street": "شارع الزراعة - الدائري", "year": 1972, "coord": "15.3620, 44.1950"},
        {"gov_id": 1, "dir_name": "معين", "name": "مدرسة أسماء الثانوية للبنات", "en": "Asmaa High School for Girls", "boss": "أ. سميرة الشامي", "street": "شارع هائل سعيد", "year": 1978, "coord": "15.3600, 44.1880"},
        {"gov_id": 1, "dir_name": "معين", "name": "مدارس الرشيد الحديثة الأهلية", "en": "Al-Rasheed Modern Schools", "boss": "د. فيصل العواضي", "street": "شارع الدائري الغربي", "year": 1995, "coord": "15.3580, 44.1840"},
        {"gov_id": 1, "dir_name": "السبعين", "name": "ثانوية عبد الإله حميد النموذجية", "en": "Abdel-Ilah Humaid Secondary School", "boss": "أ. علي شرف الدين", "street": "شارع حدة - المدينة السكنية", "year": 1985, "coord": "15.3280, 44.1980"},
        {"gov_id": 1, "dir_name": "السبعين", "name": "مدرسة الشهيد الدرة الأساسية", "en": "Al-Dura Primary School", "boss": "أ. خالد المقالح", "street": "شارع 14 أكتوبر", "year": 2001, "coord": "15.3210, 44.2010"},
        {"gov_id": 1, "dir_name": "الثورة", "name": "مدرسة نشوان الحميري الثانوية", "en": "Nashwan Al-Himyari Secondary School", "boss": "أ. محمد المحبشي", "street": "شارع المطار القديم", "year": 1982, "coord": "15.3780, 44.2150"},
        {"gov_id": 1, "dir_name": "الثورة", "name": "مدرسة الشهيد الكبسي", "en": "Al-Kibsi Primary & Secondary School", "boss": "أ. حسين حيدر", "street": "حي الحصبة", "year": 1976, "coord": "15.3850, 44.2100"},
        {"gov_id": 1, "dir_name": "صنعاء القديمة", "name": "مدرسة سيف بن ذي يزن الأساسية الثانوية", "en": "Saif Ibn Dhi Yazan School", "boss": "أ. عبد الله الحيمي", "street": "سوق الملح - صنعاء القديمة", "year": 1963, "coord": "15.3540, 44.2140"},
        {"gov_id": 1, "dir_name": "بني الحارث", "name": "مدرسة اليرموك الثانوية", "en": "Al-Yarmouk High School", "boss": "أ. فؤاد الرداعي", "street": "شارع المطار الجديد", "year": 1988, "coord": "15.4200, 44.2250"},
        {"gov_id": 1, "dir_name": "الوحدة", "name": "مدرسة بغداد الأساسية الثانوية", "en": "Baghdad Secondary School", "boss": "أ. صالح المطري", "street": "شارع بغداد - حي الوحدة", "year": 1974, "coord": "15.3400, 44.2020"},

        # مدارس محافظة صنعاء
        {"gov_id": 2, "dir_name": "سنحان", "name": "مدرسة 26 سبتمبر الثانوية النموذجية", "en": "26 September Model School", "boss": "أ. يحيى مهدي", "street": "مركز مديرية سنحان", "year": 1980, "coord": "15.2800, 44.2600"},
        {"gov_id": 2, "dir_name": "بني مطر", "name": "مدرسة الإمام الشوكاني الثانوية", "en": "Al-Shawkani Secondary School", "boss": "أ. عادل المطري", "street": "طريق صنعاء - الحديدة", "year": 1984, "coord": "15.2900, 44.1100"},
        {"gov_id": 2, "dir_name": "همدان", "name": "مدرسة الفتح الأساسية الثانوية", "en": "Al-Fateh Secondary School", "boss": "أ. ناصر الجمالي", "street": "ضلاع همدان", "year": 1986, "coord": "15.4500, 44.1300"},

        # مدارس تعز
        {"gov_id": 12, "dir_name": "القاهرة", "name": "ثانوية ناصر الحديثة", "en": "Nasser Modern Secondary School", "boss": "أ. مروان الأثوري", "street": "شارع 26 سبتمبر - تعز", "year": 1970, "coord": "13.5820, 44.0180"},
        {"gov_id": 12, "dir_name": "القاهرة", "name": "مدرسة زيد الموشكي للبنات", "en": "Zaid Al-Mowshaki School for Girls", "boss": "أ. هدى الأصبحي", "street": "حي المسبح", "year": 1975, "coord": "13.5790, 44.0150"},
        {"gov_id": 12, "dir_name": "المظفر", "name": "مدرسة ابن سينا الثانوية النموذجية", "en": "Ibn Sina Model Secondary School", "boss": "أ. فهد المخلافي", "street": "شارع جمال عبد الناصر", "year": 1983, "coord": "13.5740, 44.0240"},
        {"gov_id": 12, "dir_name": "صالة", "name": "ثانوية الثلايا للبنين", "en": "Al-Thulaya Secondary School", "boss": "أ. نجيب الصامت", "street": "حي صالة", "year": 1978, "coord": "13.5900, 44.0350"},

        # مدارس الحديدة
        {"gov_id": 4, "dir_name": "الحوك", "name": "ثانوية عثمان بن عفان للبنين", "en": "Othman Ibn Affan High School", "boss": "أ. عبد القادر الهدوي", "street": "شارع الستين الساحلي", "year": 1977, "coord": "14.7890, 42.9610"},
        {"gov_id": 4, "dir_name": "الحالي", "name": "مدرسة الشهيد الزبيري الأساسية الثانوية", "en": "Al-Zubairi School", "boss": "أ. ماجد الأهدل", "street": "شارع فلسطين", "year": 1981, "coord": "14.8050, 42.9700"},
        {"gov_id": 4, "dir_name": "الميناء", "name": "مدرسة أروى الثانوية النموذجية للبنات", "en": "Arwa Model High School for Girls", "boss": "أ. مريم المعلمي", "street": "شارع الميناء التجاري", "year": 1973, "coord": "14.7950, 42.9480"},
        {"gov_id": 4, "dir_name": "باجل", "name": "ثانوية الفوز الأساسية الثانوية", "en": "Al-Fawz Secondary School", "boss": "أ. يحيى خادم", "street": "مدينة باجل", "year": 1982, "coord": "15.0580, 43.2870"},

        # مدارس إب
        {"gov_id": 8, "dir_name": "الظهار", "name": "مدرسة النهضة الثانوية النموذجية للبنين", "en": "Al-Nahda Model Secondary School", "boss": "أ. فؤاد الصبري", "street": "شارع تعز - الظهار", "year": 1975, "coord": "13.9720, 44.1750"},
        {"gov_id": 8, "dir_name": "المشنة", "name": "مدرسة خالد بن الوليد للبنين", "en": "Khaled Ibn Al-Waleed High School", "boss": "أ. محمد عبد المغني", "street": "شارع الدائري القديم", "year": 1980, "coord": "13.9610, 44.1890"},
        {"gov_id": 8, "dir_name": "جبلة", "name": "مدرسة السيدة أروى بنت أحمد النموذجية", "en": "Queen Arwa School", "boss": "أ. خديجة الهتار", "street": "مدينة جبلة التاريخية", "year": 1971, "coord": "13.9210, 44.1480"},
        {"gov_id": 8, "dir_name": "يريم", "name": "مدرسة يريم الثانوية للبنين", "en": "Yarim High School", "boss": "أ. عبد الحفيظ اليريمي", "street": "الشارع العام - يريم", "year": 1979, "coord": "14.2980, 44.3780"},

        # مدارس ذمار
        {"gov_id": 5, "dir_name": "مدينة ذمار", "name": "مدرسة الثورة الثانوية للبنين", "en": "Al-Thawra Secondary School", "boss": "أ. محمد الوشلي", "street": "شارع صنعاء - ذمار", "year": 1973, "coord": "14.5480, 44.3980"},
        {"gov_id": 5, "dir_name": "مدينة ذمار", "name": "مدرسة خولة بنت الأزور للبنات", "en": "Khawla Bint Al-Azwar School", "boss": "أ. نجلاء العنسي", "street": "حي الجمارك", "year": 1984, "coord": "14.5390, 44.4080"},
        {"gov_id": 5, "dir_name": "جهران", "name": "مدرسة النصر الثانوية النموذجية", "en": "Al-Nasr High School - Ma'bar", "boss": "أ. علي القوسي", "street": "شارع المستشفى - معبر", "year": 1987, "coord": "14.7890, 44.3210"},
    ]

    created_schools_count = 0
    updated_schools_count = 0

    for idx, s_info in enumerate(schools_config, start=1):
        parent_dir_org = dir_org_map.get((s_info["gov_id"], s_info["dir_name"]))
        if not parent_dir_org:
            continue

        gov_obj = parent_dir_org.fk_governorate
        dir_obj = parent_dir_org.fk_directorate

        branch_no = f"50{idx:03d}"
        url_slug = f"sch-{s_info['gov_id']}-{idx}"

        sch_addr = get_or_create_address(
            country=yemen,
            governorate=gov_obj,
            directorate=dir_obj,
            street=s_info["street"]
        )

        sch_org, created = Organization.objects.update_or_create(
            branch_no=branch_no,
            defaults={
                "name_ar": s_info["name"],
                "name_en": s_info["en"],
                "company_level": 50,  # مدرسة
                "type_of_main_system": "access-login-role-unified-educational-platform",
                "fk_parent_organization": parent_dir_org,
                "fk_country": yemen,
                "fk_governorate": gov_obj,
                "fk_directorate": dir_obj,
                "fk_address": sch_addr,
                "url": url_slug,
                "established_date": date(s_info["year"], 9, 1),
                "description": f"مدرسة تعليم أساسي وثانوي تابعة لـ {parent_dir_org.name_ar} - {gov_obj.name_ar if gov_obj else ''}",
                "license_number": 50000 + idx,
                "boss": s_info["boss"],
                "coordinate": s_info["coord"],
                "student_type": 1,
                "branch_type": 1,
                "academic_id_length": 12,
                "default_user_name_for_employees": "teacher",
                "default_password_for_employees": "Teacher@123",
                "default_user_name_for_students": "student",
                "default_password_for_students": "Student@123",
                "use_hijri_calendar": True,
                "attendance_twice": False,
                "card_title": s_info["name"],
                "card_title_color": "#1E3A8A",
                "card_info_title": "بطاقة طالب مدرسي",
                "card_info_title_color": "#047857",
                "is_deleted": False,
            }
        )

        # المزامنة مع academic.Organization أيضاً لتكون متاحة في شاشات الامتحانات وبنك الأسئلة
        AcademicOrganization.objects.update_or_create(
            name_ar=s_info["name"],
            defaults={
                "name_en": s_info["en"],
                "institution_type": "school",
                "difficulty_modifier": 1.0,
                "is_active": True
            }
        )

        if created:
            created_schools_count += 1
            print(f"  ✨ [مدرسة جديدة]: {sch_org.name_ar} (رقم الفرع: {sch_org.branch_no})")
        else:
            updated_schools_count += 1
            print(f"  🔄 [تحديث مدرسة]: {sch_org.name_ar} (رقم الفرع: {sch_org.branch_no})")

    # ═══════════════════════════════════════════════════════════════════════════
    # 🎉 ملخص العمليات
    # ═══════════════════════════════════════════════════════════════════════════
    total_orgs = Organization.objects.filter(is_deleted=False).count()
    print("\n═══════════════════════════════════════════════════════════════════════════")
    print(f"🎉 اكتملت عملية تعبئة الهيكلية التعليمية اليمنية بنجاح تام!")
    print(f" 🏛️ الوزارة: 1 (المستوى 20)")
    print(f" 🏢 مكاتب المحافظات: {len(governorates_config)} (المستوى 30)")
    print(f" 🏬 إدارات المديريات: {len(directorates_config)} (المستوى 40)")
    print(f" 🏫 المدارس النموذجية: {len(schools_config)} (المستوى 50) [{created_schools_count} أنشئت، {updated_schools_count} حُدثت]")
    print(f" 📊 الإجمالي العام للسجلات النشطة في شجرة الهيكلية: {total_orgs} منظمة/مدرسة")
    print("═══════════════════════════════════════════════════════════════════════════\n")


if __name__ == '__main__':
    seed_yemen_educational_hierarchy()
