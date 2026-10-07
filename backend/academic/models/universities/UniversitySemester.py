from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class UniversitySemester(BaseSyncModel):
    name_ar = models.CharField(max_length=50, verbose_name=_("اسم الفصل الدراسي (عربي)"))
    name_en = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("اسم الفصل الدراسي (إنجليزي)"))
    is_current = models.BooleanField(default=False, db_index=True, verbose_name=_("الفصل الحالي"))
    order = models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(1000)], verbose_name=_("ترتيب الفصل"))
    note = models.TextField(max_length=250, null=True, blank=True, verbose_name=_("الملاحظة"))
    is_active = models.BooleanField(default=True, verbose_name=_("نشط"))

    class Meta:
        db_table = 'universities_semester'
        verbose_name = _("فصل دراسي جامعي")
        verbose_name_plural = _("الفصول الدراسية الجامعية")
        ordering = ['order']

    def __str__(self):
        return self.name_ar or self.name_en or str(self.id)

Semester = UniversitySemester
