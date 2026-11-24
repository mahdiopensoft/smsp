from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class InstituteExamPeriod(BaseSyncModel):
    name_ar = models.CharField(max_length=255, verbose_name=_("الاسم (عربي)"), null=True, blank=True)
    name_en = models.CharField(max_length=255, verbose_name=_("الاسم (إنجليزي)"), null=True, blank=True)
    fk_semester = models.ForeignKey(
        'academic.InstituteSemester',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="institute_exam_periods",
        verbose_name=_("الفصل/الفترة التدريبية")
    )
    order = models.IntegerField(default=1, verbose_name=_("الترتيب"))
    is_active = models.BooleanField(default=True, verbose_name=_("مفعل"))

    class Meta:
        db_table = 'institutes_examperiod'
        ordering = ['order', 'id']
        verbose_name = _('فترة امتحانية للمعاهد')
        verbose_name_plural = _('الفترات الامتحانية للمعاهد')

    def __str__(self):
        sem = f" - {self.fk_semester}" if self.fk_semester else ""
        return f"{self.name_ar or self.name_en or ''}{sem}"
