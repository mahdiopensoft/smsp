from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
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
    is_active = models.BooleanField(default=True, verbose_name=_("مفعل"))

    class Meta:
        db_table = 'schools_unit'
        ordering = ['order', 'id']
        verbose_name = _('وحدة دراسية مدرسية')
        verbose_name_plural = _('الوحدات الدراسية للمدارس')
        constraints = [
            # When semester is specified
            models.UniqueConstraint(
                fields=['class_subject', 'semester', 'name_ar'],
                condition=models.Q(is_deleted=False, class_subject__isnull=False, semester__isnull=False),
                name='unique_unit_class_sub_sem_name_ar',
            ),
            models.UniqueConstraint(
                fields=['class_subject', 'semester', 'name_en'],
                condition=models.Q(is_deleted=False, class_subject__isnull=False, semester__isnull=False, name_en__isnull=False),
                name='unique_unit_class_sub_sem_name_en',
            ),
            models.UniqueConstraint(
                fields=['class_subject', 'semester', 'order'],
                condition=models.Q(is_deleted=False, class_subject__isnull=False, semester__isnull=False),
                name='unique_unit_class_sub_sem_order',
            ),
            # When semester is null
            models.UniqueConstraint(
                fields=['class_subject', 'name_ar'],
                condition=models.Q(is_deleted=False, class_subject__isnull=False, semester__isnull=True),
                name='unique_unit_class_sub_nullsem_name_ar',
            ),
            models.UniqueConstraint(
                fields=['class_subject', 'name_en'],
                condition=models.Q(is_deleted=False, class_subject__isnull=False, semester__isnull=True, name_en__isnull=False),
                name='unique_unit_class_sub_nullsem_name_en',
            ),
            models.UniqueConstraint(
                fields=['class_subject', 'order'],
                condition=models.Q(is_deleted=False, class_subject__isnull=False, semester__isnull=True),
                name='unique_unit_class_sub_nullsem_order',
            ),
        ]

    def clean(self):
        super().clean()
        if self.class_subject_id:
            if self.order is not None:
                qs_order = SchoolUnit.objects.filter(
                    class_subject_id=self.class_subject_id,
                    semester_id=self.semester_id,
                    order=self.order,
                    is_deleted=False
                )
                if self.pk:
                    qs_order = qs_order.exclude(pk=self.pk)
                if qs_order.exists():
                    raise ValidationError({
                        'order': _('ترتيب الوحدة رقم (%s) مستخدم بالفعل لهذا الصف والمسار والمادة والفصل الدراسي.') % self.order
                    })

            if self.name_ar:
                qs_name = SchoolUnit.objects.filter(
                    class_subject_id=self.class_subject_id,
                    semester_id=self.semester_id,
                    name_ar=self.name_ar,
                    is_deleted=False
                )
                if self.pk:
                    qs_name = qs_name.exclude(pk=self.pk)
                if qs_name.exists():
                    raise ValidationError({
                        'name_ar': _('الوحدة الدراسية بهذا الاسم موجودة مسبقاً لهذا الصف والمسار والمادة والفصل الدراسي.')
                    })

    def __str__(self):
        subj = f" ({self.class_subject or self.school_subject})" if (self.class_subject or self.school_subject) else ""
        return f"{self.name_ar}{subj}"
