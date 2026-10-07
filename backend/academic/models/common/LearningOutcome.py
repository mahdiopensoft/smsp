from django.db import models
from django.utils.translation import gettext_lazy as _
from .BaseSyncModel import BaseSyncModel

class LearningOutcome(BaseSyncModel):
    subject = models.ForeignKey(
        'academic.Subject',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='learning_outcomes',
        verbose_name=_("المادة الدراسية")
    )
    unit = models.ForeignKey(
        'academic.Unit', 
        on_delete=models.CASCADE, 
        related_name='learning_outcomes', 
        verbose_name=_("الوحدة")
    )
    code = models.CharField(max_length=50, verbose_name=_("رمز مخرج التعلم"))
    description = models.TextField(verbose_name=_("وصف مخرج التعلم"))
    order = models.IntegerField(default=1, verbose_name=_("الترتيب"))
    is_active = models.BooleanField(default=True, verbose_name=_("مفعل"))

    class Meta:
        ordering = ['order']
        verbose_name = _('مخرج تعلم')
        verbose_name_plural = _('مخرجات التعلم')

    def save(self, *args, **kwargs):
        if self.unit and not self.subject:
            if self.unit.class_subject and self.unit.class_subject.subject:
                self.subject = self.unit.class_subject.subject
            elif self.unit.semester_subject and self.unit.semester_subject.fk_subject:
                self.subject = self.unit.semester_subject.fk_subject
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.unit.name_ar} - {self.code}"
