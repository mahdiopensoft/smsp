"""
سند تعبئة المؤسسات الجامعية والمعاهد والطلاب التجريبيين في academic.Organization و academic.Student
Seed script for Universities, Institutes, and Sample Examinees
"""
import os
import sys
import django

# إعداد بيئة جانغو
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from academic.models.common.Organization import Organization
from academic.models.common.Student import Student
from OpenSoftCoreV41.common.models.Directorate import Directorate

def seed_higher_ed_and_students():
    print("🚀 بدء مزامنة مؤسسات التعليم العالي والمعاهد والطلاب التجريبيين...")

    # 1. مؤسسات التعليم الجامعي
    universities = [
        {"name_ar": "جامعة صنعاء - كلية الحاسوب وتكنولوجيا المعلومات", "name_en": "Sana'a University - Faculty of Computer & IT", "type": "university"},
        {"name_ar": "جامعة صنعاء - كلية الطب والعلوم الصحية", "name_en": "Sana'a University - Faculty of Medicine & Health Sciences", "type": "university"},
        {"name_ar": "جامعة صنعاء - كلية الهندسة", "name_en": "Sana'a University - Faculty of Engineering", "type": "university"},
        {"name_ar": "جامعة عدن - كلية العلوم الإدارية", "name_en": "Aden University - Faculty of Administrative Sciences", "type": "university"},
        {"name_ar": "جامعة تعز - كلية العلوم التطبيقية", "name_en": "Taiz University - Faculty of Applied Sciences", "type": "university"},
    ]

    # 2. المعاهد ومراكز التدريب المهني
    institutes = [
        {"name_ar": "المعهد التقني الصناعي - بغداد (صنعاء)", "name_en": "Industrial Technical Institute - Baghdad", "type": "institute"},
        {"name_ar": "المعهد العالي للعلوم الصحية - صنعاء", "name_en": "Higher Institute of Health Sciences - Sana'a", "type": "institute"},
        {"name_ar": "المعهد التقني البيطري والزراعي", "name_en": "Veterinary & Agricultural Technical Institute", "type": "institute"},
        {"name_ar": "المعهد الفني التجاري النموذجي", "name_en": "Model Commercial Technical Institute", "type": "institute"},
    ]

    created_orgs = []
    for org_data in universities + institutes:
        org, created = Organization.objects.update_or_create(
            name_ar=org_data["name_ar"],
            defaults={
                "name_en": org_data["name_en"],
                "institution_type": org_data["type"],
                "difficulty_modifier": 1.0,
                "is_active": True,
            }
        )
        created_orgs.append(org)
        status = "✨ أنشئت" if created else "🔄 حُدثت"
        print(f" {status}: [{org.get_institution_type_display() if hasattr(org, 'get_institution_type_display') else org.institution_type}] {org.name_ar}")

    # 3. التأكد من وجود مديرية افتراضية للربط
    directorate = Directorate.objects.filter(is_deleted=False).first()

    # 4. التأكد من وجود طلاب ممتحنين لكل مؤسسة
    sample_students = [
        # طلاب كليات
        {"academic_number": 20261001, "name_ar": "أحمد عبدالله علي اليماني", "name_en": "Ahmed Abdullah Ali", "gender": 1, "org_name": "جامعة صنعاء - كلية الحاسوب وتكنولوجيا المعلومات"},
        {"academic_number": 20261002, "name_ar": "سارة محمد إبراهيم الصنعاني", "name_en": "Sara Mohammed Ibrahim", "gender": 2, "org_name": "جامعة صنعاء - كلية الحاسوب وتكنولوجيا المعلومات"},
        {"academic_number": 20261003, "name_ar": "خالد عمر سالم باحشوان", "name_en": "Khaled Omar Salem", "gender": 1, "org_name": "جامعة صنعاء - كلية الطب والعلوم الصحية"},
        {"academic_number": 20261004, "name_ar": "ريم عبدالرحمن ناصر الحداد", "name_en": "Reem Abdulrahman Nasser", "gender": 2, "org_name": "جامعة صنعاء - كلية الطب والعلوم الصحية"},
        # طلاب معاهد
        {"academic_number": 20262001, "name_ar": "يوسف طارق حسن الذماري", "name_en": "Youssef Tareq Hassan", "gender": 1, "org_name": "المعهد التقني الصناعي - بغداد (صنعاء)"},
        {"academic_number": 20262002, "name_ar": "منى وليد صادق الأهدل", "name_en": "Mona Walid Sadiq", "gender": 2, "org_name": "المعهد العالي للعلوم الصحية - صنعاء"},
    ]

    for st in sample_students:
        target_org = Organization.objects.filter(name_ar=st["org_name"]).first()
        if target_org:
            student, created = Student.objects.update_or_create(
                academic_number=st["academic_number"],
                defaults={
                    "name_ar": st["name_ar"],
                    "name_en": st["name_en"],
                    "gender": st["gender"],
                    "organization": target_org,
                    "directorate": directorate,
                    "phone_number": "777000111",
                    "is_active": True,
                }
            )
            print(f" 🎓 طالب مسجل: {student.name_ar} -> {target_org.name_ar}")

    print("\n🎉 تمت العملية بنجاح! المؤسسات الجامعية والمعاهد والطلاب جاهزون للاختبار.")

if __name__ == '__main__':
    seed_higher_ed_and_students()
