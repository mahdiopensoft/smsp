from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class InstituteUnit(BaseSyncModel):
    subject = models.ForeignKey(
        'academic.InstituteSubject',
        on_delete=models.CASCADE,
        related_name='institute_units',
        verbose_name=_("المادة الدراسية للمعهد")
    )
    curriculum = models.ForeignKey(
        'academic.InstituteCurriculum',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='institute_units',
        verbose_name=_("الخطة / المنهج")
    )
    semester = models.ForeignKey(
        'academic.InstituteSemester',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='institute_units',
        verbose_name=_("الفصل التدريبي")
    )
    name_ar = models.CharField(max_length=255, verbose_name=_("اسم الوحدة (عربي)"))
    name_en = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("اسم الوحدة (إنجليزي)"))
    order = models.IntegerField(default=1, verbose_name=_("الترتيب"))
    is_active = models.BooleanField(default=True, verbose_name=_("مفعل"))

    class Meta:
        db_table = 'institutes_unit'
        ordering = ['order', 'id']
        verbose_name = _('وحدة دراسية / تدريبية للمعهد')
        verbose_name_plural = _('الوحدات الدراسية للمعاهد')

    def __str__(self):
        sub_name = self.subject.name_ar if self.subject else ''
        return f"{sub_name} - {self.name_ar}"
