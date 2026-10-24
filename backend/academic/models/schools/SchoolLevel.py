from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from academic.models.common.BaseSyncModel import BaseSyncModel

class SchoolLevel(BaseSyncModel):
    name_ar = models.CharField(max_length=255, verbose_name=_("الاسم (عربي)"), null=True, blank=True)
    name_en = models.CharField(max_length=255, verbose_name=_("الاسم (إنجليزي)"), null=True, blank=True)
    stage = models.ForeignKey(
        'academic.SchoolStage', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='levels', 
        verbose_name=_("المرحلة الدراسية")
    )
    order = models.IntegerField(default=1, verbose_name=_("الترتيب"))
    is_active = models.BooleanField(default=True, verbose_name=_("مفعل"))

    class Meta:
        db_table = 'schools_level'
        ordering = ['order', 'id']
        verbose_name = _('مستوى / صف دراسي مدرسي')
        verbose_name_plural = _('المستويات / الصفوف الدراسية المدرسية')
        constraints = [
            models.UniqueConstraint(
                fields=['name_ar'],
                condition=models.Q(is_deleted=False),
                name='unique_active_school_level_name_ar'
            ),
            models.UniqueConstraint(
                fields=['name_en'],
                condition=models.Q(is_deleted=False) & ~models.Q(name_en__isnull=True) & ~models.Q(name_en=''),
                name='unique_active_school_level_name_en'
            ),
            models.UniqueConstraint(
                fields=['order'],
                condition=models.Q(is_deleted=False),
                name='unique_active_school_level_order'
            ),
        ]

    def clean(self):
        super().clean()
        if self.name_ar and self.name_ar.strip():
            qs_ar = SchoolLevel.objects.filter(name_ar__iexact=self.name_ar.strip(), is_deleted=False)
            if self.pk:
                qs_ar = qs_ar.exclude(pk=self.pk)
            if qs_ar.exists():
                raise ValidationError({'name_ar': _("اسم الصف الدراسي باللغة العربية مسجل مسبقاً، يرجى إدخال اسم فريد.")})

        if self.name_en and self.name_en.strip():
            qs_en = SchoolLevel.objects.filter(name_en__iexact=self.name_en.strip(), is_deleted=False)
            if self.pk:
                qs_en = qs_en.exclude(pk=self.pk)
            if qs_en.exists():
                raise ValidationError({'name_en': _("اسم الصف الدراسي باللغة الإنجليزية مسجل مسبقاً، يرجى إدخال اسم فريد.")})

        if self.order is not None:
            qs_order = SchoolLevel.objects.filter(order=self.order, is_deleted=False)
            if self.pk:
                qs_order = qs_order.exclude(pk=self.pk)
            if qs_order.exists():
                raise ValidationError({'order': _("رقم الترتيب مسجل لصف دراسي آخر مسبقاً، يرجى اختيار رقم ترتيب فريد.")})

    def __str__(self):
        return self.name_ar or self.name_en or str(self.id)

