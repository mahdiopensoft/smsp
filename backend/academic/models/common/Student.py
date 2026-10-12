from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .BaseSyncModel import BaseSyncModel

class Student(BaseSyncModel):
    class GenderChoices(models.IntegerChoices):
        MALE = 1, _("ذكر")
        FEMALE = 2, _("أنثى")

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        related_name='student_profile', 
        on_delete=models.CASCADE, 
        verbose_name=_("حساب المستخدم"),
        null=True, 
        blank=True
    )
    academic_number = models.BigIntegerField(unique=True, db_index=True, verbose_name=_("الرقم الأكاديمي / رقم القيد"))
    name_ar = models.CharField(max_length=150, db_index=True, verbose_name=_("اسم الطالب (عربي)"))
    name_en = models.CharField(max_length=150, null=True, blank=True, verbose_name=_("اسم الطالب (إنجليزي)"))
    gender = models.PositiveSmallIntegerField(choices=GenderChoices.choices, default=GenderChoices.MALE, db_index=True, verbose_name=_("الجنس"))
    birthdate = models.DateField(null=True, blank=True, verbose_name=_("تاريخ الميلاد"))
    birth_place = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("مكان الميلاد"))
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("العنوان"))
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("رقم الهاتف"))
    
    country = models.ForeignKey(
        'common.Country', 
        related_name='academic_students', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name=_("الجنسية / الدولة")
    )
    directorate = models.ForeignKey(
        'common.Directorate', 
        related_name='academic_students', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name=_("المديرية")
    )
    organization = models.ForeignKey(
        'academic.Organization', 
        related_name='academic_students', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name=_("المدرسة / المؤسسة")
    )
    # ── الانتساب للمدارس ──
    class_track = models.ForeignKey(
        'academic.SchoolClassTrack',
        related_name='students',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("الصف والمسار الدراسي (المدارس)")
    )

    # ── الانتساب للجامعات ──
    university_college = models.ForeignKey(
        'academic.UniversityCollege',
        related_name='students',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("الكلية الجامعية")
    )
    university_department = models.ForeignKey(
        'academic.UniversityDepartment',
        related_name='students',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("القسم الأكاديمي")
    )
    university_specialization = models.ForeignKey(
        'academic.UniversitySpecialization',
        related_name='students',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("التخصص الجامعي")
    )
    university_level = models.ForeignKey(
        'academic.UniversityLevel',
        related_name='students',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("المستوى الجامعي")
    )

    # ── الانتساب للمعاهد ──
    institute_field = models.ForeignKey(
        'academic.InstituteField',
        related_name='students',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("المجال المهني/التقني")
    )
    institute_education_system = models.ForeignKey(
        'academic.InstituteEducationSystem',
        related_name='students',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("نظام التعليم والتدريب")
    )
    institute_specialization = models.ForeignKey(
        'academic.InstituteSpecialization',
        related_name='students',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("التخصص المهني")
    )
    institute_level = models.ForeignKey(
        'academic.InstituteLevel',
        related_name='students',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("المستوى التدريبي للمعهد")
    )

    is_active = models.BooleanField(default=True, verbose_name=_("نشط"))

    class Meta:
        verbose_name = _("طالب")
        verbose_name_plural = _("الطلاب")
        ordering = ['-academic_number']

    def __str__(self):
        return f"{self.name_ar} ({self.academic_number})"

    @property
    def institution_type(self):
        if self.organization and self.organization.institution_type:
            return self.organization.institution_type
        if self.university_specialization or self.university_college:
            return "university"
        if self.institute_specialization or self.institute_field:
            return "institute"
        return "school"
