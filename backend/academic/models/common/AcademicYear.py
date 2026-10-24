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
                fields=['hijri_year'],
                name='unique_academic_year_hijri_no_deleted',
                condition=Q(is_deleted=False),
            ),
            models.UniqueConstraint(
                fields=['gregorian_year'],
                name='unique_academic_year_gregorian_no_deleted',
                condition=Q(is_deleted=False),
            ),
        ]

    def clean(self):
        super().clean()
        if self.hijri_year:
            qs = AcademicYear.objects.filter(hijri_year=self.hijri_year.strip(), is_deleted=False)
            if self.id:
                qs = qs.exclude(id=self.id)
            if qs.exists():
                raise ValidationError({'hijri_year': _("السنة الهجرية مسجلة مسبقاً في النظام.")})

        if self.gregorian_year:
            qs = AcademicYear.objects.filter(gregorian_year=self.gregorian_year.strip(), is_deleted=False)
            if self.id:
                qs = qs.exclude(id=self.id)
            if qs.exists():
                raise ValidationError({'gregorian_year': _("السنة الميلادية مسجلة مسبقاً في النظام.")})

        # Prevent deactivating the only current academic year directly
        if self.id and not self.is_current:
            old = AcademicYear.objects.filter(id=self.id).first()
            if old and old.is_current:
                other_current = AcademicYear.objects.filter(is_current=True, is_deleted=False).exclude(id=self.id).exists()
                if not other_current:
                    raise ValidationError({
                        'is_current': _("لا يمكن إلغاء العام الدراسي الحالي مباشرة؛ يجب تفعيل عام دراسي آخر بدلاً منه.")
                    })

    def save(self, *args, **kwargs):
        # Auto-set as current if this is the only active year in the database
        existing_qs = AcademicYear.objects.filter(is_deleted=False)
        if self.id:
            existing_qs = existing_qs.exclude(id=self.id)

        if not self.is_current and not existing_qs.exists():
            self.is_current = True

        if self.is_current:
            update_qs = AcademicYear.objects.filter(is_current=True, is_deleted=False)
            if self.id:
                update_qs = update_qs.exclude(id=self.id)
            update_qs.update(is_current=False)

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
