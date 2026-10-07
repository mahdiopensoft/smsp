from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class InstituteCurriculum(BaseSyncModel):
    name_ar = models.CharField(max_length=200, verbose_name=_("اسم الخطة الدراسية (عربي)"))
    name_en = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("اسم الخطة الدراسية (إنجليزي)"))
    version_code = models.CharField(max_length=50, verbose_name=_("رمز / إصدار الخطة"))
    specialization = models.ForeignKey(
        'academic.InstituteSpecialization',
        on_delete=models.CASCADE,
        related_name='curricula',
        verbose_name=_("التخصص")
    )
    academic_year = models.ForeignKey(
        'academic.AcademicYear',
        on_delete=models.PROTECT,
        related_name='institute_curricula',
        verbose_name=_("العام الدراسي للاعتماد / البداية")
    )
    is_approved = models.BooleanField(default=False, db_index=True, verbose_name=_("خطة معتمدة"))
    is_current = models.BooleanField(default=True, db_index=True, verbose_name=_("الخطة الحالية للتخصص"))
    total_credit_hours = models.PositiveSmallIntegerField(default=0, verbose_name=_("إجمالي الساعات المعتمدة"))
    note = models.TextField(null=True, blank=True, verbose_name=_("ملاحظات الخطة"))
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_("نشط"))

    class Meta:
        db_table = 'institutes_curriculum'
        verbose_name = _("الخطة الدراسية للمعهد")
        verbose_name_plural = _("الخطط الدراسية للمعاهد")
        ordering = ['-academic_year_id', 'specialization', 'name_ar']

    def __str__(self):
        year_str = f" ({self.academic_year})" if self.academic_year else ""
        return f"{self.name_ar} [{self.version_code}]{year_str}"
