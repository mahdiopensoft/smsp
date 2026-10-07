from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class InstituteAdmissionRequirement(BaseSyncModel):
    title = models.CharField(max_length=200, verbose_name=_("عنوان الضابط / الشرط"))
    education_system = models.ForeignKey(
        'academic.InstituteEducationSystem',
        on_delete=models.CASCADE,
        related_name='admission_requirements',
        verbose_name=_("نظام التعليم")
    )
    specialization = models.ForeignKey(
        'academic.InstituteSpecialization',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='admission_rules',
        verbose_name=_("التخصص (اختياري لتخصيص الشروط)")
    )
    required_qualification = models.CharField(
        max_length=200,
        verbose_name=_("مؤهل القبول المطلوب")
    )
    accepted_tracks = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("المسارات الدراسية المقبولة")
    )
    minimum_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("الحد الأدنى للنسبة المئوية / المعدل")
    )
    required_documents = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("الوثائق والمستندات المطلوبة")
    )
    admission_conditions = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("شروط وضوابط القبول")
    )
    transfer_requirements = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("متطلبات وشروط التحويل والانتقال")
    )
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_("نشط"))

    class Meta:
        db_table = 'institutes_admission_requirement'
        verbose_name = _("شرط وضابط قبول وتسجيل")
        verbose_name_plural = _("شروط وضوابط القبول والتسجيل للمعاهد")
        ordering = ['education_system_id', 'title']

    def __str__(self):
        spec_text = f" ({self.specialization.name_ar})" if self.specialization else ""
        return f"{self.title}{spec_text} - {self.education_system.name_ar}"
