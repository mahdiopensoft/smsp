from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class SchoolUnit(BaseSyncModel):
    name_ar = models.CharField(max_length=255, verbose_name=_("اسم الوحدة (عربي)"))
    name_en = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("اسم الوحدة (إنجليزي)"))
    class_subject = models.ForeignKey(
        'academic.SchoolClassSubject', 
        on_delete=models.CASCADE, 
        related_name='school_units', 
        verbose_name=_("مادة مسار الصف"),
        null=True, 
        blank=True
    )
    school_subject = models.ForeignKey(
        'academic.SchoolSubject', 
        on_delete=models.CASCADE, 
        related_name='school_units', 
        verbose_name=_("المادة الدراسية المدرسية"),
        null=True, 
        blank=True
    )
    semester = models.ForeignKey(
        'academic.UniversitySemester', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='school_units', 
        verbose_name=_("الفصل الدراسي")
    )
    order = models.IntegerField(default=1, verbose_name=_("الترتيب"))
    enable_learning_outcomes = models.BooleanField(default=True, verbose_name=_("تفعيل مخرجات التعلم لهذه الوحدة"))
    is_active = models.BooleanField(default=True, verbose_name=_("مفعل"))

    class Meta:
        db_table = 'schools_unit'
        ordering = ['order', 'id']
        verbose_name = _('وحدة دراسية مدرسية')
        verbose_name_plural = _('الوحدات الدراسية للمدارس')

    def __str__(self):
        subj = f" ({self.class_subject or self.school_subject})" if (self.class_subject or self.school_subject) else ""
        return f"{self.name_ar}{subj}"
