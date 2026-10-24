from django.db import models
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class SchoolSubject(BaseSyncModel):
    name_ar = models.CharField(max_length=150, verbose_name=_("اسم المادة (عربي)"))
    name_en = models.CharField(max_length=150, null=True, blank=True, verbose_name=_("اسم المادة (إنجليزي)"))
    subject_code = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("كود المادة الوزاري/المدرسي"))
    is_ministerial = models.BooleanField(default=True, db_index=True, verbose_name=_("مادة وزارية"))
    subject_order = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(1000)], verbose_name=_("ترتيب المادة"))
    note = models.TextField(max_length=250, null=True, blank=True, verbose_name=_("الملاحظة"))
    is_active = models.BooleanField(default=True, verbose_name=_("مفعل"))

    class Meta:
        db_table = 'schools_subject'
        verbose_name = _('مادة دراسية مدرسية')
        verbose_name_plural = _('المواد الدراسية للمدارس')
        ordering = ['subject_order', 'id']
        constraints = [
            models.UniqueConstraint(
                fields=['name_ar'],
                condition=models.Q(is_deleted=False),
                name='unique_active_school_subject_name_ar'
            ),
            models.UniqueConstraint(
                fields=['name_en'],
                condition=models.Q(is_deleted=False) & ~models.Q(name_en__isnull=True) & ~models.Q(name_en=''),
                name='unique_active_school_subject_name_en'
            ),
            models.UniqueConstraint(
                fields=['subject_code'],
                condition=models.Q(is_deleted=False) & ~models.Q(subject_code__isnull=True) & ~models.Q(subject_code=''),
                name='unique_active_school_subject_code'
            ),
            models.UniqueConstraint(
                fields=['subject_order'],
                condition=models.Q(is_deleted=False),
                name='unique_active_school_subject_order'
            ),
        ]

    def clean(self):
        super().clean()
        if self.name_ar and self.name_ar.strip():
            qs_ar = SchoolSubject.objects.filter(name_ar__iexact=self.name_ar.strip(), is_deleted=False)
            if self.pk:
                qs_ar = qs_ar.exclude(pk=self.pk)
            if qs_ar.exists():
                raise ValidationError({'name_ar': _("اسم المادة باللغة العربية مسجل مسبقاً، يرجى إدخال اسم فريد.")})

        if self.name_en and self.name_en.strip():
            qs_en = SchoolSubject.objects.filter(name_en__iexact=self.name_en.strip(), is_deleted=False)
            if self.pk:
                qs_en = qs_en.exclude(pk=self.pk)
            if qs_en.exists():
                raise ValidationError({'name_en': _("اسم المادة باللغة الإنجليزية مسجل مسبقاً، يرجى إدخال اسم فريد.")})

        if self.subject_code and self.subject_code.strip():
            qs_code = SchoolSubject.objects.filter(subject_code__iexact=self.subject_code.strip(), is_deleted=False)
            if self.pk:
                qs_code = qs_code.exclude(pk=self.pk)
            if qs_code.exists():
                raise ValidationError({'subject_code': _("كود المادة مسجل مسبقاً، يرجى اختيار كود فريد.")})

        if self.subject_order is not None:
            qs_order = SchoolSubject.objects.filter(subject_order=self.subject_order, is_deleted=False)
            if self.pk:
                qs_order = qs_order.exclude(pk=self.pk)
            if qs_order.exists():
                raise ValidationError({'subject_order': _("ترتيب المادة مسجل مسبقاً، يرجى اختيار ترتيب آخر.")})

    def __str__(self):
        return self.name_ar or self.name_en or str(self.id)

