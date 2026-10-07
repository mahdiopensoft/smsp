from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class InstituteField(BaseSyncModel):
    name_ar = models.CharField(max_length=150, verbose_name=_("اسم المجال (عربي)"))
    name_en = models.CharField(max_length=150, null=True, blank=True, verbose_name=_("اسم المجال (إنجليزي)"))
    field_code = models.CharField(max_length=50, unique=True, verbose_name=_("كود المجال"))
    icon = models.CharField(max_length=100, null=True, blank=True, default="domain", verbose_name=_("أيقونة المجال"))
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name=_("وصف المجال"))
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_("نشط"))

    class Meta:
        db_table = 'institutes_field'
        verbose_name = _("مجال مهني / تقني")
        verbose_name_plural = _("المجالات المهنية والتقنية")
        ordering = ['field_code', 'name_ar']

    def __str__(self):
        return self.name_ar or self.field_code
