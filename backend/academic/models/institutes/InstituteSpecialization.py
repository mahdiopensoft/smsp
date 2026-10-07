from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class InstituteSpecialization(BaseSyncModel):
    name_ar = models.CharField(max_length=150, verbose_name=_("اسم التخصص (عربي)"))
    name_en = models.CharField(max_length=150, null=True, blank=True, verbose_name=_("اسم التخصص (إنجليزي)"))
    specialization_code = models.CharField(max_length=50, unique=True, verbose_name=_("كود التخصص"))
    field = models.ForeignKey(
        'academic.InstituteField',
        on_delete=models.CASCADE,
        related_name='specializations',
        verbose_name=_("المجال المهني / التقني")
    )
    education_system = models.ForeignKey(
        'academic.InstituteEducationSystem',
        on_delete=models.CASCADE,
        related_name='specializations',
        verbose_name=_("نظام التعليم")
    )
    organization = models.ForeignKey(
        'academic.Organization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='institute_specializations',
        verbose_name=_("المعهد / المؤسسة التعليمية")
    )
    required_qualification = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_("المؤهل المطلوب للقبول")
    )
    accepted_tracks = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_("المسارات المقبولة (علمي / أدبي / إعدادي)")
    )
    admission_requirements = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("شروط ومتطلبات القبول")
    )
    number_of_levels = models.PositiveSmallIntegerField(
        default=2,
        verbose_name=_("عدد المستويات الدراسية")
    )
    number_of_semesters_per_level = models.PositiveSmallIntegerField(
        default=2,
        verbose_name=_("عدد الفصول في كل مستوى")
    )
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_("نشط"))

    class Meta:
        db_table = 'institutes_specialization'
        verbose_name = _("تخصص مهني / تقني")
        verbose_name_plural = _("التخصصات المهنية والتقنية")
        ordering = ['field_id', 'education_system_id', 'name_ar']

    def __str__(self):
        sys_name = f" - {self.education_system.name_ar}" if self.education_system else ""
        return f"{self.name_ar}{sys_name}"
