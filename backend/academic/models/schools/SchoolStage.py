from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class SchoolStage(BaseSyncModel):
    name_ar = models.CharField(max_length=255, verbose_name=_("الاسم (عربي)"), null=True, blank=True)
    name_en = models.CharField(max_length=255, verbose_name=_("الاسم (إنجليزي)"), null=True, blank=True)
    order = models.IntegerField(default=1, verbose_name=_("الترتيب"))
    is_active = models.BooleanField(default=True, verbose_name=_("مفعل"))

    class Meta:
        db_table = 'schools_stage'
        ordering = ['order', 'id']
        verbose_name = _('مرحلة دراسية')
        verbose_name_plural = _('المراحل الدراسية')

    def __str__(self):
        return self.name_ar or self.name_en or str(self.id)
