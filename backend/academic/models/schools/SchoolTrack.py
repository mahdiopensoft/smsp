from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from academic.models.common.BaseSyncModel import BaseSyncModel

class SchoolTrack(BaseSyncModel):
    name_ar = models.CharField(max_length=100, verbose_name=_("الاسم بالعربية"))
    name_en = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("الاسم بالإنجليزية"))
    code = models.CharField(max_length=50, verbose_name=_("الكود"))
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_("نشط"))
    note = models.TextField(max_length=250, null=True, blank=True, verbose_name=_("الملاحظة"))

    class Meta:
        db_table = 'schools_track'
        verbose_name = _("مسار تعليمي مدرسي")
        verbose_name_plural = _("المسارات التعليمية المدرسية")
        ordering = ['name_ar']
        constraints = [
            models.UniqueConstraint(
                fields=['name_ar'],
                condition=models.Q(is_deleted=False),
                name='unique_active_school_track_name_ar'
            ),
            models.UniqueConstraint(
                fields=['name_en'],
                condition=models.Q(is_deleted=False) & ~models.Q(name_en__isnull=True) & ~models.Q(name_en=''),
                name='unique_active_school_track_name_en'
            ),
            models.UniqueConstraint(
                fields=['code'],
                condition=models.Q(is_deleted=False),
                name='unique_active_school_track_code'
            ),
        ]

    def clean(self):
        super().clean()
        if self.name_ar and self.name_ar.strip():
            qs_ar = SchoolTrack.objects.filter(name_ar__iexact=self.name_ar.strip(), is_deleted=False)
            if self.pk:
                qs_ar = qs_ar.exclude(pk=self.pk)
            if qs_ar.exists():
                raise ValidationError({'name_ar': _("اسم المسار باللغة العربية مسجل مسبقاً، يرجى إدخال اسم فريد.")})

        if self.name_en and self.name_en.strip():
            qs_en = SchoolTrack.objects.filter(name_en__iexact=self.name_en.strip(), is_deleted=False)
            if self.pk:
                qs_en = qs_en.exclude(pk=self.pk)
            if qs_en.exists():
                raise ValidationError({'name_en': _("اسم المسار باللغة الإنجليزية مسجل مسبقاً، يرجى إدخال اسم فريد.")})

        if self.code and self.code.strip():
            qs_code = SchoolTrack.objects.filter(code__iexact=self.code.strip(), is_deleted=False)
            if self.pk:
                qs_code = qs_code.exclude(pk=self.pk)
            if qs_code.exists():
                raise ValidationError({'code': _("كود المسار مسجل لمسار آخر مسبقاً، يرجى اختيار كود فريد.")})

    def __str__(self):
        return self.name_ar or self.code

