"""
سند تعبئة البيانات التجريبية للشاشات الأساسية لمنظومة تهيئة المعاهد المهنية والتقنية (TVET)
Seeding Script for Active Institute Setup Screens (8 Screens)
"""
import os
import sys
from decimal import Decimal

# 1. إعداد بيئة جانغو
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from academic.models.common.AcademicYear import AcademicYear
from academic.models.common.Organization import Organization

from academic.models.institutes.InstituteField import InstituteField
from academic.models.institutes.InstituteEducationSystem import InstituteEducationSystem
from academic.models.institutes.InstituteSpecialization import InstituteSpecialization
from academic.models.institutes.InstituteLevel import InstituteLevel
from academic.models.institutes.InstituteSemester import InstituteSemester
from academic.models.institutes.InstituteSubject import InstituteSubject
from academic.models.institutes.InstituteCurriculum import InstituteCurriculum
from academic.models.institutes.InstituteCurriculumSubject import InstituteCurriculumSubject

from academic.choices.institute_choices import (
    InstituteEducationSystemTypeChoices,
    InstituteStudyNatureChoices,
    InstituteSubjectTypeChoices,
    InstituteSubjectEntityChoices,
    InstituteSubjectAcademicCategoryChoices,
    InstituteSemesterNatureChoices,
    InstituteGradingCalculationChoices,
)


def seed_institutes_full_data():
    print("🚀 بدء تعبئة البيانات التجريبية للشاشات الأساسية لمنظومة المعاهد (8 شاشات)...")

    # ─────────────────────────────────────────────────────────────
    # 0. التهيئة الأساسية (العام الدراسي والمعهد)
    # ─────────────────────────────────────────────────────────────
    academic_year = AcademicYear.objects.filter(is_deleted=False, is_current=True).first()
    if not academic_year:
        academic_year, _ = AcademicYear.objects.get_or_create(
            gregorian_year="2026/2027",
            defaults={"hijri_year": "1448/1449", "is_current": True, "is_active": True}
        )

    institute_org = Organization.objects.filter(institution_type='institute', is_deleted=False).first()
    if not institute_org:
        institute_org, _ = Organization.objects.get_or_create(
            name_ar="المعهد التقني الصناعي النموذجي - المركز الرئيسي",
            defaults={
                "name_en": "Model Industrial Technical Institute - Main Center",
                "institution_type": "institute",
                "is_active": True,
            }
        )

    print(f"📌 تم ربط المعهد: {institute_org.name_ar} | العام الدراسي: {academic_year.gregorian_year}")

    # ─────────────────────────────────────────────────────────────
    # 1. المجالات المهنية والتقنية (InstituteField)
    # ─────────────────────────────────────────────────────────────
    print("\n📂 [1/8] تعبئة المجالات المهنية والتقنية...")
    fields_data = [
        {
            "field_code": "IT_COMM",
            "name_ar": "مجال تكنولوجيا المعلومات والاتصالات",
            "name_en": "Information & Communication Technology",
            "icon": "laptop",
            "description": "يشمل تخصصات الشبكات، البرمجيات، الدعم الفني، وأمن المعلومات.",
        },
        {
            "field_code": "MECH_IND",
            "name_ar": "مجال الهندسة الميكانيكية والصناعية",
            "name_en": "Mechanical & Industrial Engineering",
            "icon": "cog",
            "description": "يشمل صيانة السيارات، الميكاترونكس، خراطة المعادن، والتشغيل الآلي.",
        },
        {
            "field_code": "ELEC_ENG",
            "name_ar": "مجال الهندسة الكهربائية والإلكترونية",
            "name_en": "Electrical & Electronic Engineering",
            "icon": "lightning-bolt",
            "description": "يشمل التمديدات الكهربائية، الطاقة الشمسية المتجددة، والتحكم الآلي.",
        },
        {
            "field_code": "HEALTH_SCI",
            "name_ar": "مجال العلوم الطبية المساعدة والمهن الصحية",
            "name_en": "Allied Health Sciences",
            "icon": "hospital-building",
            "description": "يشمل التمريض المهني، فني مختبرات، وصيانة الأجهزة الطبية.",
        },
        {
            "field_code": "BIZ_ADMIN",
            "name_ar": "مجال العلوم المالية والإدارية المهنية",
            "name_en": "Business & Financial Studies",
            "icon": "finance",
            "description": "يشمل المحاسبة الفنية، إدارة المكاتب والسكرتارية، والتسويق الرقمي.",
        },
    ]

    fields_map = {}
    for item in fields_data:
        obj, _ = InstituteField.objects.update_or_create(
            field_code=item["field_code"],
            defaults={
                "name_ar": item["name_ar"],
                "name_en": item["name_en"],
                "icon": item["icon"],
                "description": item["description"],
                "is_active": True,
            }
        )
        fields_map[item["field_code"]] = obj
        print(f"  ✓ مجال: {obj.name_ar} [{obj.field_code}]")

    # ─────────────────────────────────────────────────────────────
    # 2. أنظمة التعليم والتدريب (InstituteEducationSystem)
    # ─────────────────────────────────────────────────────────────
    print("\n⚙️ [2/8] تعبئة أنظمة التعليم والتدريب...")
    systems_data = [
        {
            "system_code": "TECH_DIP_2Y",
            "name_ar": "دبلوم تقني صناعي (سنتان بعد الثانوية العامة)",
            "name_en": "Technical Diploma (2 Years Post-Secondary)",
            "field": fields_map["IT_COMM"],
            "system_type": InstituteEducationSystemTypeChoices.TECHNICAL_DIPLOMA_2Y,
            "study_nature": InstituteStudyNatureChoices.INTEGRATED,
            "duration_years": 2,
            "admission_qualification": "ثانوية عامة (علمي)",
            "has_ministerial_exam": True,
            "grading_calculation_method": InstituteGradingCalculationChoices.CUMULATIVE_AND_MINISTERIAL,
            "description": "نظام يجمع بين النظري الهندسي والتطبيقي مع اختبار وزاري شامل بنهاية السنة الثانية.",
        },
        {
            "system_code": "VOC_DIP_3Y",
            "name_ar": "دبلوم مهني نظام 3 سنوات (بعد التعليم الأساسي)",
            "name_en": "Vocational Diploma (3 Years Post-Preparatory)",
            "field": fields_map["MECH_IND"],
            "system_type": InstituteEducationSystemTypeChoices.VOCATIONAL_DIPLOMA_PREP,
            "study_nature": InstituteStudyNatureChoices.PRACTICAL_VOCATIONAL,
            "duration_years": 3,
            "admission_qualification": "شهادة إتمام المرحلة الأساسية (الصف التاسع)",
            "has_ministerial_exam": True,
            "grading_calculation_method": InstituteGradingCalculationChoices.GENERAL_TOTAL_AND_MINISTERIAL_GPA,
            "description": "تدريب عملي تطبيقي مكثف يهدف إلى تخريج فنيين مهنيين مهرة.",
        },
        {
            "system_code": "COMP_DIP_1Y",
            "name_ar": "دبلوم تقني تكميلي (سنة بعد الدبلوم المهني)",
            "name_en": "Complementary Technical Diploma (1 Year)",
            "field": fields_map["ELEC_ENG"],
            "system_type": InstituteEducationSystemTypeChoices.COMPLEMENTARY_DIPLOMA,
            "study_nature": InstituteStudyNatureChoices.INTEGRATED,
            "duration_years": 1,
            "admission_qualification": "دبلوم مهني سابق معتمد",
            "has_ministerial_exam": True,
            "grading_calculation_method": InstituteGradingCalculationChoices.CUMULATIVE_AND_MINISTERIAL,
            "description": "برنامج تطويري يمنح خريج المهني ترقية إلى المستوى التقني.",
        },
    ]

    systems_map = {}
    for item in systems_data:
        obj, _ = InstituteEducationSystem.objects.update_or_create(
            system_code=item["system_code"],
            defaults={
                "name_ar": item["name_ar"],
                "name_en": item["name_en"],
                "field": item["field"],
                "system_type": item["system_type"],
                "study_nature": item["study_nature"],
                "duration_years": item["duration_years"],
                "admission_qualification": item["admission_qualification"],
                "has_ministerial_exam": item["has_ministerial_exam"],
                "grading_calculation_method": item["grading_calculation_method"],
                "description": item["description"],
                "is_active": True,
            }
        )
        systems_map[item["system_code"]] = obj
        print(f"  ✓ نظام: {obj.name_ar} [{obj.system_code}]")

    # ─────────────────────────────────────────────────────────────
    # 3. التخصصات المهنية والتقنية (InstituteSpecialization)
    # ─────────────────────────────────────────────────────────────
    print("\n🎓 [3/8] تعبئة التخصصات المهنية والتقنية...")
    specs_data = [
        {
            "specialization_code": "IT_NETWORKS_2Y",
            "name_ar": "شبكات ونظم الحواسيب المتقدمة",
            "name_en": "Computer Networks & Systems",
            "field": fields_map["IT_COMM"],
            "education_system": systems_map["TECH_DIP_2Y"],
            "required_qualification": "ثانوية عامة (علمي)",
            "accepted_tracks": "علمي",
            "number_of_levels": 2,
            "number_of_semesters_per_level": 2,
            "admission_requirements": "ألا يقل المعدل عن 65% واجتياز المقابلة واختبار مبادئ الحاسوب.",
        },
        {
            "specialization_code": "MECH_AUTOTRONIC_2Y",
            "name_ar": "ميكاترونكس وهندسة المركبات الحديثة",
            "name_en": "Autotronics & Modern Vehicle Engineering",
            "field": fields_map["MECH_IND"],
            "education_system": systems_map["TECH_DIP_2Y"],
            "required_qualification": "ثانوية عامة (علمي / مهني)",
            "accepted_tracks": "علمي، صناعي",
            "number_of_levels": 2,
            "number_of_semesters_per_level": 2,
            "admission_requirements": "ألا يقل المعدل عن 60% مع الكشف الطبي لسلامة النظر والقدرة البدنية.",
        },
        {
            "specialization_code": "ELEC_SOLAR_2Y",
            "name_ar": "هندسة التمديدات والمنظومات الكهروضوئية (طاقة شمسية)",
            "name_en": "Electrical Wiring & Solar PV Systems",
            "field": fields_map["ELEC_ENG"],
            "education_system": systems_map["TECH_DIP_2Y"],
            "required_qualification": "ثانوية عامة (علمي)",
            "accepted_tracks": "علمي",
            "number_of_levels": 2,
            "number_of_semesters_per_level": 2,
            "admission_requirements": "ألا يقل المعدل عن 60%.",
        },
        {
            "specialization_code": "VOC_HVAC_3Y",
            "name_ar": "التبريد والتكييف الصناعي",
            "name_en": "Industrial Refrigeration & Air Conditioning",
            "field": fields_map["MECH_IND"],
            "education_system": systems_map["VOC_DIP_3Y"],
            "required_qualification": "شهادة التعليم الأساسي (تاسع)",
            "accepted_tracks": "إعدادي / أساسي",
            "number_of_levels": 3,
            "number_of_semesters_per_level": 2,
            "admission_requirements": "ألا يقل معدل الصف التاسع عن 55%.",
        },
    ]

    specs_map = {}
    for item in specs_data:
        obj, _ = InstituteSpecialization.objects.update_or_create(
            specialization_code=item["specialization_code"],
            defaults={
                "name_ar": item["name_ar"],
                "name_en": item["name_en"],
                "field": item["field"],
                "education_system": item["education_system"],
                "organization": institute_org,
                "required_qualification": item["required_qualification"],
                "accepted_tracks": item["accepted_tracks"],
                "number_of_levels": item["number_of_levels"],
                "number_of_semesters_per_level": item["number_of_semesters_per_level"],
                "admission_requirements": item["admission_requirements"],
                "is_active": True,
            }
        )
        specs_map[item["specialization_code"]] = obj
        print(f"  ✓ تخصص: {obj.name_ar} [{obj.specialization_code}]")

    # ─────────────────────────────────────────────────────────────
    # 4. الخطط الدراسية للمعاهد (InstituteCurriculum)
    # ─────────────────────────────────────────────────────────────
    print("\n📖 [4/8] تعبئة الخطط الدراسية للمعاهد...")
    curricula_data = [
        {
            "name_ar": "الخطة الدراسية المعتمدة لدبلوم شبكات ونظم الحاسوب",
            "name_en": "Approved Curriculum for Computer Networks Diploma",
            "version_code": "CURR-IT-NET-2026",
            "specialization": specs_map["IT_NETWORKS_2Y"],
            "academic_year": academic_year,
            "is_approved": True,
            "is_current": True,
            "total_credit_hours": 72,
            "note": "الخطة الوزارية المحدثة المواكبة لشهادات Cisco و CompTIA.",
        },
        {
            "name_ar": "الخطة الدراسية المعتمدة لدبلوم ميكاترونكس السيارات",
            "name_en": "Approved Curriculum for Autotronics Engineering Diploma",
            "version_code": "CURR-AUTO-2026",
            "specialization": specs_map["MECH_AUTOTRONIC_2Y"],
            "academic_year": academic_year,
            "is_approved": True,
            "is_current": True,
            "total_credit_hours": 75,
            "note": "الخطة النموذجية للسيارات الهجينة والكهربائية المعتمدة وزارياً.",
        },
    ]

    curricula_map = {}
    for item in curricula_data:
        obj, _ = InstituteCurriculum.objects.update_or_create(
            version_code=item["version_code"],
            defaults={
                "name_ar": item["name_ar"],
                "name_en": item["name_en"],
                "specialization": item["specialization"],
                "academic_year": item["academic_year"],
                "is_approved": item["is_approved"],
                "is_current": item["is_current"],
                "total_credit_hours": item["total_credit_hours"],
                "note": item["note"],
                "is_active": True,
            }
        )
        curricula_map[item["version_code"]] = obj
        print(f"  ✓ خطة دراسية: {obj.name_ar} [{obj.version_code}]")

    # ─────────────────────────────────────────────────────────────
    # 5. المستويات الدراسية للمعاهد (InstituteLevel)
    # ─────────────────────────────────────────────────────────────
    print("\n🪜 [5/8] تعبئة المستويات الدراسية للمعاهد...")
    levels_data = [
        {"name_ar": "المستوى الأول", "name_en": "First Level", "order": 1, "note": "السنة التأسيسية الأولى"},
        {"name_ar": "المستوى الثاني", "name_en": "Second Level", "order": 2, "note": "سنة التخصص والتخرج للدبلوم سنتين"},
        {"name_ar": "المستوى الثالث", "name_en": "Third Level", "order": 3, "note": "سنة التخرج للدبلوم المهني 3 سنوات"},
    ]

    levels_map = {}
    for item in levels_data:
        obj, _ = InstituteLevel.objects.update_or_create(
            order=item["order"],
            defaults={
                "name_ar": item["name_ar"],
                "name_en": item["name_en"],
                "note": item["note"],
                "is_active": True,
            }
        )
        levels_map[item["order"]] = obj
        print(f"  ✓ مستوى: {obj.name_ar} (ترتيب {obj.order})")

    # ─────────────────────────────────────────────────────────────
    # 6. الفصول والفترات الدراسية (InstituteSemester)
    # ─────────────────────────────────────────────────────────────
    print("\n📅 [6/8] تعبئة الفصول والفترات الدراسية...")
    semesters_data = [
        {
            "name_ar": "الفصل التدريبي الأول",
            "name_en": "First Training Semester",
            "order": 1,
            "semester_nature": InstituteSemesterNatureChoices.REGULAR,
            "is_current": True,
            "note": "الفصل الأكاديمي والعملي التأسيسي",
        },
        {
            "name_ar": "الفصل التدريبي الثاني",
            "name_en": "Second Training Semester",
            "order": 2,
            "semester_nature": InstituteSemesterNatureChoices.REGULAR,
            "is_current": False,
            "note": "الفصل الاعتيادي الثاني",
        },
        {
            "name_ar": "الفصل النهائي - الاختبارات الوزارية الموحدة",
            "name_en": "Final Ministerial Exam Semester",
            "order": 3,
            "semester_nature": InstituteSemesterNatureChoices.FINAL_MINISTERIAL,
            "is_current": False,
            "note": "فصل التخرج والامتحانات الوزارية النهائية الشاملة",
        },
    ]

    semesters_map = {}
    for item in semesters_data:
        obj, _ = InstituteSemester.objects.update_or_create(
            order=item["order"],
            defaults={
                "name_ar": item["name_ar"],
                "name_en": item["name_en"],
                "semester_nature": item["semester_nature"],
                "is_current": item["is_current"],
                "note": item["note"],
                "is_active": True,
            }
        )
        semesters_map[item["order"]] = obj
        print(f"  ✓ فصل: {obj.name_ar} [{obj.get_semester_nature_display()}]")

    # ─────────────────────────────────────────────────────────────
    # 7. المواد الدراسية للمعاهد (InstituteSubject)
    # ─────────────────────────────────────────────────────────────
    print("\n📚 [7/8] تعبئة المواد الدراسية للمعاهد...")
    subjects_data = [
        # تخصص الشبكات
        {
            "subject_code": "IT_NET101",
            "name_ar": "مقدمة في شبكات الحاسوب وبروتوكول IP",
            "name_en": "Computer Networking & IP Fundamentals",
            "field": fields_map["IT_COMM"],
            "subject_type": InstituteSubjectTypeChoices.MIXED,
            "subject_entity": InstituteSubjectEntityChoices.MINISTERIAL,
            "academic_category": InstituteSubjectAcademicCategoryChoices.SPECIALIZED,
            "theoretical_hours": 30,
            "practical_hours": 45,
            "credit_hours": 3,
            "description": "دراسة طبقات OSI، عنونة IPv4/IPv6، وتكوين الموجهات والمحولات.",
        },
        {
            "subject_code": "IT_SEC201",
            "name_ar": "أمن الشبكات وجدران الحماية (Firewalls)",
            "name_en": "Network Security & Firewalls",
            "field": fields_map["IT_COMM"],
            "subject_type": InstituteSubjectTypeChoices.MIXED,
            "subject_entity": InstituteSubjectEntityChoices.MINISTERIAL,
            "academic_category": InstituteSubjectAcademicCategoryChoices.SPECIALIZED,
            "theoretical_hours": 30,
            "practical_hours": 45,
            "credit_hours": 3,
            "description": "تقنيات التشفير، الجدران النارية، كشف التسلل IDS/IPS، والشهادات الرقمية.",
        },
        {
            "subject_code": "IT_LAB102",
            "name_ar": "مختبر تجميع وصيانة الحواسيب والخوادم",
            "name_en": "PC & Server Hardware Lab",
            "field": fields_map["IT_COMM"],
            "subject_type": InstituteSubjectTypeChoices.PRACTICAL,
            "subject_entity": InstituteSubjectEntityChoices.INSTITUTIONAL,
            "academic_category": InstituteSubjectAcademicCategoryChoices.SPECIALIZED,
            "theoretical_hours": 10,
            "practical_hours": 60,
            "credit_hours": 3,
            "description": "تجميع اللوحات الأم، صيانة وحدات التغذية، والتعامل مع خوادم Rack.",
        },
        # تخصص الميكاترونكس والسيارات
        {
            "subject_code": "AUTO_ENG101",
            "name_ar": "محركات الاحتراق الداخلي وأنظمة الحقن الإلكتروني",
            "name_en": "Internal Combustion Engines & EFI Systems",
            "field": fields_map["MECH_IND"],
            "subject_type": InstituteSubjectTypeChoices.MIXED,
            "subject_entity": InstituteSubjectEntityChoices.MINISTERIAL,
            "academic_category": InstituteSubjectAcademicCategoryChoices.SPECIALIZED,
            "theoretical_hours": 40,
            "practical_hours": 60,
            "credit_hours": 4,
            "description": "مبادئ عمل المحركات رباعية الأشواط، حساسات EFI، وفحص الأعطال عبر OBD-II.",
        },
        {
            "subject_code": "ELEC_AUTO102",
            "name_ar": "كهرباء وإلكترونيات السيارات الحديثة",
            "name_en": "Automotive Electrical & Electronic Systems",
            "field": fields_map["MECH_IND"],
            "subject_type": InstituteSubjectTypeChoices.MIXED,
            "subject_entity": InstituteSubjectEntityChoices.MINISTERIAL,
            "academic_category": InstituteSubjectAcademicCategoryChoices.SPECIALIZED,
            "theoretical_hours": 30,
            "practical_hours": 45,
            "credit_hours": 3,
            "description": "شبكات CAN-Bus، بادئات التشغيل، والمولدات الذكية.",
        },
        # مواد مساعدة وثقافية عامة
        {
            "subject_code": "GEN_ENG_TECH",
            "name_ar": "اللغة الإنجليزية الفنية والتخصصية",
            "name_en": "Technical English for Technicians",
            "field": fields_map["IT_COMM"],
            "subject_type": InstituteSubjectTypeChoices.THEORETICAL,
            "subject_entity": InstituteSubjectEntityChoices.MINISTERIAL,
            "academic_category": InstituteSubjectAcademicCategoryChoices.SUPPORTIVE,
            "theoretical_hours": 30,
            "practical_hours": 0,
            "credit_hours": 2,
            "description": "المصطلحات الفنية والهندسية وقراءة الكتالوجات والمخططات.",
        },
        {
            "subject_code": "GEN_SAFETY",
            "name_ar": "السلامة والصحة المهنية والأمن البيئي",
            "name_en": "Occupational Safety & Health (OSH)",
            "field": fields_map["MECH_IND"],
            "subject_type": InstituteSubjectTypeChoices.THEORETICAL,
            "subject_entity": InstituteSubjectEntityChoices.MINISTERIAL,
            "academic_category": InstituteSubjectAcademicCategoryChoices.GENERAL_CULTURAL,
            "theoretical_hours": 30,
            "practical_hours": 0,
            "credit_hours": 2,
            "description": "إجراءات السلامة في الورش والمختبرات، مكافحة الحرائق، والإسعافات الأولية.",
        },
    ]

    subjects_map = {}
    for item in subjects_data:
        obj, _ = InstituteSubject.objects.update_or_create(
            subject_code=item["subject_code"],
            defaults={
                "name_ar": item["name_ar"],
                "name_en": item["name_en"],
                "field": item["field"],
                "subject_type": item["subject_type"],
                "subject_entity": item["subject_entity"],
                "academic_category": item["academic_category"],
                "theoretical_hours": item["theoretical_hours"],
                "practical_hours": item["practical_hours"],
                "credit_hours": item["credit_hours"],
                "description": item["description"],
                "is_active": True,
            }
        )
        subjects_map[item["subject_code"]] = obj
        print(f"  ✓ مادة: {obj.name_ar} [{obj.subject_code}]")

    # ─────────────────────────────────────────────────────────────
    # 8. مقررات الخطط والفصول الدراسية (InstituteCurriculumSubject)
    # ─────────────────────────────────────────────────────────────
    print("\n🔗 [8/8] ربط مقررات الخطط والفصول الدراسية...")
    curriculum_it = curricula_map["CURR-IT-NET-2026"]
    curriculum_subjects_data = [
        # خطة الشبكات - المستوى 1 - الفصل 1
        {
            "curriculum": curriculum_it,
            "subject": subjects_map["IT_NET101"],
            "level": levels_map[1],
            "semester": semesters_map[1],
            "is_ministerial_exam": True,
            "exam_entity": InstituteSubjectEntityChoices.MINISTERIAL,
            "max_score": Decimal("100.00"),
            "min_score": Decimal("50.00"),
            "added_to_total": True,
            "order": 1,
            "note": "مادة أساسية مشمولة بالاختبار الوزاري المشترك",
        },
        {
            "curriculum": curriculum_it,
            "subject": subjects_map["IT_LAB102"],
            "level": levels_map[1],
            "semester": semesters_map[1],
            "is_ministerial_exam": False,
            "exam_entity": InstituteSubjectEntityChoices.INSTITUTIONAL,
            "max_score": Decimal("100.00"),
            "min_score": Decimal("60.00"),
            "added_to_total": True,
            "order": 2,
            "note": "مختبر عملي يعقد في المعهد",
        },
        {
            "curriculum": curriculum_it,
            "subject": subjects_map["GEN_ENG_TECH"],
            "level": levels_map[1],
            "semester": semesters_map[1],
            "is_ministerial_exam": True,
            "exam_entity": InstituteSubjectEntityChoices.MINISTERIAL,
            "max_score": Decimal("100.00"),
            "min_score": Decimal("50.00"),
            "added_to_total": True,
            "order": 3,
            "note": "متطلب وزاري عام",
        },
        {
            "curriculum": curriculum_it,
            "subject": subjects_map["GEN_SAFETY"],
            "level": levels_map[1],
            "semester": semesters_map[1],
            "is_ministerial_exam": False,
            "exam_entity": InstituteSubjectEntityChoices.INSTITUTIONAL,
            "max_score": Decimal("100.00"),
            "min_score": Decimal("50.00"),
            "added_to_total": True,
            "order": 4,
            "note": "مادة ثقافة مهنية",
        },
        # خطة الشبكات - المستوى 2 - الفصل 2
        {
            "curriculum": curriculum_it,
            "subject": subjects_map["IT_SEC201"],
            "level": levels_map[2],
            "semester": semesters_map[2],
            "is_ministerial_exam": True,
            "exam_entity": InstituteSubjectEntityChoices.MINISTERIAL,
            "max_score": Decimal("100.00"),
            "min_score": Decimal("50.00"),
            "added_to_total": True,
            "order": 1,
            "note": "مادة التخرج الأساسية للاختبار الوزاري النهائي",
        },
    ]

    for cs in curriculum_subjects_data:
        obj, _ = InstituteCurriculumSubject.objects.update_or_create(
            curriculum=cs["curriculum"],
            subject=cs["subject"],
            level=cs["level"],
            semester=cs["semester"],
            defaults={
                "is_ministerial_exam": cs["is_ministerial_exam"],
                "exam_entity": cs["exam_entity"],
                "max_score": cs["max_score"],
                "min_score": cs["min_score"],
                "added_to_total": cs["added_to_total"],
                "order": cs["order"],
                "note": cs["note"],
                "is_active": True,
            }
        )
        exam_badge = "🏛️ وزاري" if cs["is_ministerial_exam"] else "🏫 مؤسسي"
        print(f"  ✓ مقرر خطة: [{obj.curriculum.version_code}] -> {obj.subject.name_ar} ({exam_badge})")

    print("\n🎉 تم بنجاح توليد وتعبئة كامل البيانات للشاشات الـ 8 الأساسية لتهيئة المعاهد!")


if __name__ == "__main__":
    seed_institutes_full_data()
