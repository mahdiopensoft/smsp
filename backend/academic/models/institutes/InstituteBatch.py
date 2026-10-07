from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class InstituteBatch(BaseSyncModel):
    name_ar = models.CharField(max_length=150, verbose_name=_("اسم الدفعة / الفوج (عربي)"))
    name_en = models.CharField(max_length=150, null=True, blank=True, verbose_name=_("اسم الدفعة / الفوج (إنجليزي)"))
    batch_number = models.PositiveIntegerField(default=1, verbose_name=_("رقم الدفعة"))
    specialization = models.ForeignKey(
        'academic.InstituteSpecialization',
        on_delete=models.CASCADE,
        related_name='batches',
        verbose_name=_("التخصص")
    )
    curriculum = models.ForeignKey(
        'academic.InstituteCurriculum',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='batches',
        verbose_name=_("الخطة الدراسية المعتمدة للدفعة")
    )
    academic_year = models.ForeignKey(
        'academic.AcademicYear',
        on_delete=models.PROTECT,
        related_name='institute_batches',
        verbose_name=_("عام الالتحاق / البدء")
    )
    start_date = models.DateField(null=True, blank=True, verbose_name=_("تاريخ البدء"))
    end_date = models.DateField(null=True, blank=True, verbose_name=_("تاريخ التخرج المتوقع / الفعلي"))
    is_graduated = models.BooleanField(default=False, db_index=True, verbose_name=_("دفعة متخرجة"))
    note = models.TextField(null=True, blank=True, verbose_name=_("ملاحظات"))
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_("نشط"))

    class Meta:
        db_table = 'institutes_batch'
        verbose_name = _("الدفعة / الفوج للمعهد")
        verbose_name_plural = _("الدفعات والأفواج للمعاهد")
        ordering = ['-academic_year_id', 'specialization', 'batch_number']

    def __str__(self):
        spec_str = f" - {self.specialization.name_ar}" if self.specialization else ""
        return f"{self.name_ar}{spec_str}"
