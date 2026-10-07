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
    is_active = models.BooleanField(default=True, verbose_name=_("نشط"))

    class Meta:
        verbose_name = _("طالب")
        verbose_name_plural = _("الطلاب")
        ordering = ['-academic_number']

    def __str__(self):
        return f"{self.name_ar} ({self.academic_number})"
