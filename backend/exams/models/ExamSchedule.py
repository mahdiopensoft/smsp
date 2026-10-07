from django.db import models
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class ExamSchedule(SoftDeleteModel):
    name = models.CharField(max_length=255, verbose_name=_("اسم الجدول"))
    date = models.DateField(verbose_name=_("تاريخ الاختبار"))
    duration = models.IntegerField(verbose_name=_("مدة الاختبار (بالدقائق)"))
    isActive = models.BooleanField(default=True, verbose_name=_("مفعل"))

    class Meta:
        verbose_name = _('جدول اختبار')
        verbose_name_plural = _('جداول الاختبارات')

    def __str__(self):
        return f"{self.name} - {self.date}"
