from django.db import models
from django.utils.translation import gettext_lazy as _
from .BaseSyncModel import BaseSyncModel

class Organization(BaseSyncModel):
    name_ar = models.CharField(max_length=255, verbose_name=_("الاسم (عربي)"), null=True, blank=True)
    name_en = models.CharField(max_length=255, verbose_name=_("الاسم (إنجليزي)"), null=True, blank=True)
    institution_type = models.CharField(max_length=50, verbose_name=_("نوع المؤسسة"), default="school")
    difficulty_modifier = models.FloatField(default=1.0, verbose_name=_("معامل الصعوبة"))
    parent = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='children', 
        verbose_name=_("المنطقة الأم")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("مفعل"))

    class Meta:
        verbose_name = _('مؤسسة/منطقة')
        verbose_name_plural = _('المؤسسات/المناطق')

    def __str__(self):
        return self.name_ar or self.name_en or str(self.id)
