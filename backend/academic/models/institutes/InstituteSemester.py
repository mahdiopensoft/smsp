from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel
from academic.choices.institute_choices import InstituteSemesterNatureChoices

class InstituteSemester(BaseSyncModel):
    name_ar = models.CharField(max_length=150, verbose_name=_("اسم الفصل / الفترة (عربي)"))
    name_en = models.CharField(max_length=150, null=True, blank=True, verbose_name=_("اسم الفصل / الفترة (إنجليزي)"))
    order = models.PositiveSmallIntegerField(default=1, verbose_name=_("ترتيب الفصل"))
    semester_nature = models.CharField(
        max_length=30,
        choices=InstituteSemesterNatureChoices.choices,
        default=InstituteSemesterNatureChoices.REGULAR,
        verbose_name=_("طبيعة الفصل")
    )
    is_current = models.BooleanField(default=False, db_index=True, verbose_name=_("الفصل الحالي"))
    note = models.TextField(null=True, blank=True, verbose_name=_("ملاحظات"))
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_("نشط"))

    class Meta:
        db_table = 'institutes_semester'
        verbose_name = _("الفصل / الفترة الدراسية للمعهد")
        verbose_name_plural = _("الفصول والفترات الدراسية للمعاهد")
        ordering = ['order', 'id']

    def __str__(self):
        nature = f" ({self.get_semester_nature_display()})" if self.semester_nature else ""
        return f"{self.name_ar}{nature}"
