from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class SchoolLesson(BaseSyncModel):
    unit = models.ForeignKey(
        'academic.SchoolUnit', 
        on_delete=models.CASCADE, 
        related_name='school_lessons', 
        verbose_name=_("الوحدة الدراسية المدرسية")
    )
    school_subject = models.ForeignKey(
        'academic.SchoolSubject',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='school_lessons',
        verbose_name=_("المادة المدرسية")
    )
    name_ar = models.CharField(max_length=255, verbose_name=_("اسم الدرس (عربي)"))
    name_en = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("اسم الدرس (إنجليزي)"))
    order = models.IntegerField(default=1, verbose_name=_("الترتيب"))
    is_active = models.BooleanField(default=True, verbose_name=_("مفعل"))

    class Meta:
        db_table = 'schools_lesson'
        ordering = ['order', 'id']
        verbose_name = _('درس مدرسي')
        verbose_name_plural = _('الدروس المدرسية')

    def save(self, *args, **kwargs):
        if self.unit and not self.school_subject:
            if self.unit.school_subject:
                self.school_subject = self.unit.school_subject
            elif self.unit.class_subject and hasattr(self.unit.class_subject, 'school_subject'):
                self.school_subject = self.unit.class_subject.school_subject
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.unit.name_ar} - {self.name_ar}"
