from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class SchoolLearningOutcome(BaseSyncModel):
    unit = models.ForeignKey(
        'academic.SchoolUnit', 
        on_delete=models.CASCADE, 
        related_name='school_learning_outcomes', 
        verbose_name=_("الوحدة الدراسية المدرسية")
    )
    lesson = models.ForeignKey(
        'academic.SchoolLesson',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='school_learning_outcomes',
        verbose_name=_("الدرس المدرسي")
    )
    school_subject = models.ForeignKey(
        'academic.SchoolSubject',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='school_learning_outcomes',
        verbose_name=_("المادة المدرسية")
    )
    code = models.CharField(max_length=50, verbose_name=_("رمز مخرج التعلم المدرسي"))
    description = models.TextField(verbose_name=_("وصف مخرج التعلم"))
    order = models.IntegerField(default=1, verbose_name=_("الترتيب"))
    is_active = models.BooleanField(default=True, verbose_name=_("مفعل"))

    class Meta:
        db_table = 'schools_learning_outcome'
        ordering = ['order', 'id']
        verbose_name = _('مخرج تعلم مدرسي')
        verbose_name_plural = _('مخرجات التعلم للمدارس')

    def save(self, *args, **kwargs):
        if self.unit and not self.school_subject:
            if self.unit.school_subject:
                self.school_subject = self.unit.school_subject
            elif self.unit.class_subject and hasattr(self.unit.class_subject, 'school_subject'):
                self.school_subject = self.unit.class_subject.school_subject
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.unit.name_ar} - {self.code}"
