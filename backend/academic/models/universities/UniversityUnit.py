from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from academic.models.common.BaseSyncModel import BaseSyncModel

class UniversityUnit(BaseSyncModel):
    name_ar = models.CharField(max_length=255, verbose_name=_("اسم الوحدة (عربي)"))
    name_en = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("اسم الوحدة (إنجليزي)"))
    semester_subject = models.ForeignKey(
        'academic.UniversitySemesterSubject', 
        on_delete=models.CASCADE, 
        related_name='university_units', 
        verbose_name=_("مادة الفصل الجامعية"),
        null=True, 
        blank=True
    )
    semester = models.ForeignKey(
        'academic.UniversitySemester', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='university_units', 
        verbose_name=_("الفصل الدراسي")
    )
    order = models.IntegerField(default=1, verbose_name=_("الترتيب"))
    is_active = models.BooleanField(default=True, verbose_name=_("مفعل"))

    class Meta:
        db_table = 'academic_unit'
        ordering = ['order', 'id']
        verbose_name = _('وحدة دراسية جامعية')
        verbose_name_plural = _('الوحدات الدراسية الجامعية')
        constraints = [
            # When semester is specified
            models.UniqueConstraint(
                fields=['semester_subject', 'semester', 'name_ar'],
                condition=models.Q(is_deleted=False, semester_subject__isnull=False, semester__isnull=False),
                name='unique_univ_unit_sem_sub_sem_name_ar',
            ),
            models.UniqueConstraint(
                fields=['semester_subject', 'semester', 'name_en'],
                condition=models.Q(is_deleted=False, semester_subject__isnull=False, semester__isnull=False) & ~models.Q(name_en__isnull=True) & ~models.Q(name_en=''),
                name='unique_univ_unit_sem_sub_sem_name_en',
            ),
            models.UniqueConstraint(
                fields=['semester_subject', 'semester', 'order'],
                condition=models.Q(is_deleted=False, semester_subject__isnull=False, semester__isnull=False),
                name='unique_univ_unit_sem_sub_sem_order',
            ),
            # When semester is null
            models.UniqueConstraint(
                fields=['semester_subject', 'name_ar'],
                condition=models.Q(is_deleted=False, semester_subject__isnull=False, semester__isnull=True),
                name='unique_univ_unit_sem_sub_nullsem_name_ar',
            ),
            models.UniqueConstraint(
                fields=['semester_subject', 'name_en'],
                condition=models.Q(is_deleted=False, semester_subject__isnull=False, semester__isnull=True) & ~models.Q(name_en__isnull=True) & ~models.Q(name_en=''),
                name='unique_univ_unit_sem_sub_nullsem_name_en',
            ),
            models.UniqueConstraint(
                fields=['semester_subject', 'order'],
                condition=models.Q(is_deleted=False, semester_subject__isnull=False, semester__isnull=True),
                name='unique_univ_unit_sem_sub_nullsem_order',
            ),
        ]

    def clean(self):
        super().clean()
        if self.semester_subject_id:
            if self.order is not None:
                qs_order = UniversityUnit.objects.filter(
                    semester_subject_id=self.semester_subject_id,
                    semester_id=self.semester_id,
                    order=self.order,
                    is_deleted=False
                )
                if self.pk:
                    qs_order = qs_order.exclude(pk=self.pk)
                if qs_order.exists():
                    raise ValidationError({
                        'order': _('ترتيب الوحدة رقم (%s) مستخدم بالفعل لهذا المقرر والفصل الدراسي.') % self.order
                    })

            if self.name_ar and self.name_ar.strip():
                qs_name = UniversityUnit.objects.filter(
                    semester_subject_id=self.semester_subject_id,
                    semester_id=self.semester_id,
                    name_ar__iexact=self.name_ar.strip(),
                    is_deleted=False
                )
                if self.pk:
                    qs_name = qs_name.exclude(pk=self.pk)
                if qs_name.exists():
                    raise ValidationError({
                        'name_ar': _('الوحدة الدراسية بهذا الاسم (%s) موجودة مسبقاً لهذا المقرر والفصل الدراسي.') % self.name_ar.strip()
                    })

    def __str__(self):
        subj = f" ({self.semester_subject or self.semester})" if (self.semester_subject or self.semester) else ""
        return f"{self.name_ar}{subj}"

# Compatibility alias
Unit = UniversityUnit
