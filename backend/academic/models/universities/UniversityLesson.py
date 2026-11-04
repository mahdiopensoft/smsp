from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class UniversityLesson(BaseSyncModel):
    subject = models.ForeignKey(
        'academic.UniversitySubject',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='university_lessons',
        verbose_name=_("المادة الدراسية")
    )
    unit = models.ForeignKey(
        'academic.UniversityUnit', 
        on_delete=models.CASCADE, 
        related_name='university_lessons', 
        verbose_name=_("الوحدة")
    )
    name_ar = models.CharField(max_length=255, verbose_name=_("الاسم (عربي)"), null=True, blank=True)
    name_en = models.CharField(max_length=255, verbose_name=_("الاسم (إنجليزي)"), null=True, blank=True)
    order = models.IntegerField(default=1, verbose_name=_("الترتيب"))
    is_active = models.BooleanField(default=True, verbose_name=_("مفعل"))

    class Meta:
        db_table = 'academic_lesson'
        ordering = ['order', 'id']
        verbose_name = _('درس جامعي')
        verbose_name_plural = _('الدروس الجامعية')

    def save(self, *args, **kwargs):
        if self.unit and not self.subject:
            if getattr(self.unit, 'semester_subject', None) and getattr(self.unit.semester_subject, 'fk_subject', None):
                self.subject = self.unit.semester_subject.fk_subject
        super().save(*args, **kwargs)

    def __str__(self):
        unit_name = self.unit.name_ar if self.unit else ''
        return f"{unit_name} - {self.name_ar or ''}"

# Compatibility alias
Lesson = UniversityLesson
