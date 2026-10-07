from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class SchoolSection(BaseSyncModel):
    class GenderChoices(models.IntegerChoices):
        MALE = 1, _("بنين")
        FEMALE = 2, _("بنات")
        MIXED = 3, _("مشترك")

    name_ar = models.CharField(max_length=100, verbose_name=_("اسم الشعبة / الفصل (عربي)"))
    name_en = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("اسم الشعبة (إنجليزي)"))
    section_code = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("كود الشعبة"))
    organization = models.ForeignKey(
        'academic.Organization', 
        on_delete=models.CASCADE, 
        related_name='school_sections', 
        verbose_name=_("المدرسة / المؤسسة")
    )
    class_track = models.ForeignKey(
        'academic.SchoolClassTrack', 
        on_delete=models.CASCADE, 
        related_name='school_sections', 
        null=True, 
        blank=True, 
        verbose_name=_("مسار الصف")
    )
    academic_year = models.ForeignKey(
        'academic.AcademicYear', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='school_sections', 
        verbose_name=_("العام الدراسي")
    )
    gender = models.PositiveSmallIntegerField(
        choices=GenderChoices.choices, 
        default=GenderChoices.MALE, 
        verbose_name=_("نوع الشعبة (بنين / بنات / مشترك)")
    )
    max_capacity = models.PositiveSmallIntegerField(default=35, verbose_name=_("السعة الاستيعابية"))
    is_active = models.BooleanField(default=True, verbose_name=_("مفعل"))

    class Meta:
        db_table = 'schools_section'
        verbose_name = _('شعبة مدرسية')
        verbose_name_plural = _('الشُعب والفصول المدرسية')
        ordering = ['class_track', 'name_ar']

    def __str__(self):
        org = f"{self.organization.name_ar} - " if self.organization else ""
        track = f"{self.class_track} - " if self.class_track else ""
        return f"{org}{track}{self.name_ar}"
