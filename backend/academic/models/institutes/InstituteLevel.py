from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class InstituteLevel(BaseSyncModel):
    name_ar = models.CharField(max_length=150, verbose_name=_("اسم المستوى (عربي)"))
    name_en = models.CharField(max_length=150, null=True, blank=True, verbose_name=_("اسم المستوى (إنجليزي)"))
    order = models.PositiveSmallIntegerField(default=1, verbose_name=_("ترتيب المستوى"))
    note = models.TextField(null=True, blank=True, verbose_name=_("ملاحظات"))
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_("نشط"))

    class Meta:
        db_table = 'institutes_level'
        verbose_name = _("المستوى الدراسي للمعهد")
        verbose_name_plural = _("المستويات الدراسية للمعاهد")
        ordering = ['order', 'id']

    def __str__(self):
        return self.name_ar or str(self.id)
