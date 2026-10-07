from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class SchoolClassSubject(BaseSyncModel):
    class_track = models.ForeignKey(
        'academic.SchoolClassTrack', 
        related_name='class_subjects', 
        on_delete=models.CASCADE, 
        verbose_name=_("مسار الصف المدرسي")
    )
    subject = models.ForeignKey(
        'academic.Subject', 
        related_name='class_subjects', 
        on_delete=models.CASCADE, 
        verbose_name=_("المادة (تاريخي)"),
        null=True, 
        blank=True
    )
    school_subject = models.ForeignKey(
        'academic.SchoolSubject', 
        related_name='class_subjects', 
        on_delete=models.CASCADE, 
        verbose_name=_("المادة الدراسية المدرسية"),
        null=True, 
        blank=True
    )
    min_score = models.PositiveIntegerField(
        default=50, 
        validators=[MinValueValidator(0), MaxValueValidator(500)], 
        verbose_name=_("درجة الصغرى (الرسوب)")
    )
    max_score = models.PositiveIntegerField(
        default=100, 
        validators=[MinValueValidator(1), MaxValueValidator(500)], 
        verbose_name=_("الدرجة الكبرى")
    )
    added_to_total = models.BooleanField(default=True, verbose_name=_("مضاف إلى المجموع"))
    optional = models.BooleanField(default=False, verbose_name=_("اختياري"))
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_("نشط"))
    note = models.TextField(max_length=250, null=True, blank=True, verbose_name=_("الملاحظة"))

    class Meta:
        db_table = 'schools_class_subject'
        verbose_name = _("مادة مسار الصف المدرسي")
        verbose_name_plural = _("مواد مسارات الصفوف المدرسية")
        ordering = ['class_track', 'subject']
        constraints = [
            models.UniqueConstraint(
                fields=['class_track', 'subject'],
                name='unique_school_class_track_subject_integrity',
            ),
        ]

    def __str__(self):
        subj_name = self.school_subject.name_ar if self.school_subject else (self.subject.name_ar if self.subject else "")
        return f"{self.class_track} - {subj_name}"
