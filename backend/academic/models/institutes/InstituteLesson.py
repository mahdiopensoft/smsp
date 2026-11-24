from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class InstituteLesson(BaseSyncModel):
    unit = models.ForeignKey(
        'academic.InstituteUnit',
        on_delete=models.CASCADE,
        related_name='institute_lessons',
        verbose_name=_("الوحدة التدريبية / الدراسية")
    )
    subject = models.ForeignKey(
        'academic.InstituteSubject',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='institute_lessons',
        verbose_name=_("المادة الدراسية")
    )
    name_ar = models.CharField(max_length=255, verbose_name=_("اسم الدرس / التدريب (عربي)"))
    name_en = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("اسم الدرس / التدريب (إنجليزي)"))
    order = models.IntegerField(default=1, verbose_name=_("الترتيب"))
    is_active = models.BooleanField(default=True, verbose_name=_("مفعل"))

    class Meta:
        db_table = 'institutes_lesson'
        ordering = ['order', 'id']
        verbose_name = _('درس / تدريب مهني للمعهد')
        verbose_name_plural = _('دروس وتدريبات المعاهد')

    def save(self, *args, **kwargs):
        if self.unit and not self.subject:
            self.subject = self.unit.subject
        super().save(*args, **kwargs)

    def __str__(self):
        unit_name = self.unit.name_ar if self.unit else ''
        return f"{unit_name} - {self.name_ar}"
