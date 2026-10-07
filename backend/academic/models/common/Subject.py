from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy as _
from .BaseSyncModel import BaseSyncModel

class Subject(BaseSyncModel):
    name_ar = models.CharField(max_length=100, verbose_name=_("اسم المادة (عربي)"))
    name_en = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("اسم المادة (إنجليزي)"))
    subject_code = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("كود المادة"))
    credit_hours = models.PositiveSmallIntegerField(
        null=True, 
        blank=True, 
        verbose_name=_("الساعات المعتمدة"), 
        help_text=_("للاستخدام في نظام الجامعات")
    )
    is_ministerial = models.BooleanField(default=True, db_index=True, verbose_name=_("مادة وزارية"))
    is_detailed = models.BooleanField(default=True, db_index=True, verbose_name=_("تفصيلي"))
    subject_order = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(1000)], verbose_name=_("ترتيب المادة"))
    note = models.TextField(max_length=250, null=True, blank=True, verbose_name=_("الملاحظة"))
    is_active = models.BooleanField(default=True, verbose_name=_("مفعل"))

    class Meta:
        verbose_name = _('مادة دراسية')
        verbose_name_plural = _('المواد الدراسية')
        ordering = ['subject_order', 'id']

    def __str__(self):
        return self.name_ar or self.name_en or str(self.id)
