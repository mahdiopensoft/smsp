from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class SchoolTrack(BaseSyncModel):
    name_ar = models.CharField(max_length=100, verbose_name=_("الاسم بالعربية"))
    name_en = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("الاسم بالإنجليزية"))
    code = models.CharField(max_length=50, verbose_name=_("الكود"), unique=True)
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_("نشط"))
    note = models.TextField(max_length=250, null=True, blank=True, verbose_name=_("الملاحظة"))

    class Meta:
        db_table = 'schools_track'
        verbose_name = _("مسار تعليمي مدرسي")
        verbose_name_plural = _("المسارات التعليمية المدرسية")
        ordering = ['name_ar']

    def __str__(self):
        return self.name_ar or self.code
