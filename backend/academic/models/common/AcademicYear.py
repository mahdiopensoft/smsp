from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .BaseSyncModel import BaseSyncModel

class AcademicYear(BaseSyncModel):
    hijri_year = models.CharField(max_length=50, verbose_name=_("السنة الهجرية"))
    gregorian_year = models.CharField(max_length=50, verbose_name=_("السنة الميلادية"))
    is_active = models.BooleanField(default=True, verbose_name=_("مفعل"))
    is_current = models.BooleanField(default=False, verbose_name=_("السنة الحالية"))

    class Meta:
        verbose_name = _('سنة دراسية')
        verbose_name_plural = _('السنوات الدراسية')
        constraints = [
            models.UniqueConstraint(
                fields=['hijri_year', 'gregorian_year'],
                name='unique_academic_year_hijri_gregorian_no_deleted',
                condition=Q(is_deleted=False),
            ),
            models.UniqueConstraint(
                fields=['is_current'],
                name='unique_single_current_academic_year_no_deleted',
                condition=Q(is_current=True, is_deleted=False),
            ),
        ]

    def save(self, *args, **kwargs):
        if self.is_current:
            AcademicYear.objects.filter(is_current=True, is_deleted=False).exclude(id=self.id).update(is_current=False)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.is_current:
            raise ValidationError(_("لا يمكن حذف السنة الدراسية الحالية النشطة."))
        return super().delete(*args, **kwargs)

    def __str__(self):
        parts = []
        if self.hijri_year:
            parts.append(f"{self.hijri_year} هـ")
        if self.gregorian_year:
            parts.append(f"{self.gregorian_year} م")
        return " / ".join(parts) if parts else str(self.id)
