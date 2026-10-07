from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel
from academic.choices.institute_choices import (
    InstituteSubjectTypeChoices,
    InstituteSubjectEntityChoices,
    InstituteSubjectAcademicCategoryChoices,
)

class InstituteSubject(BaseSyncModel):
    name_ar = models.CharField(max_length=200, verbose_name=_("اسم المادة الدراسية (عربي)"))
    name_en = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("اسم المادة الدراسية (إنجليزي)"))
    subject_code = models.CharField(max_length=50, unique=True, verbose_name=_("رمز / كود المادة"))
    field = models.ForeignKey(
        'academic.InstituteField',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subjects',
        verbose_name=_("المجال المهني / التقني التابعة له")
    )
    subject_type = models.CharField(
        max_length=30,
        choices=InstituteSubjectTypeChoices.choices,
        default=InstituteSubjectTypeChoices.THEORETICAL,
        verbose_name=_("نوع المادة (نظري / عملي)")
    )
    subject_entity = models.CharField(
        max_length=30,
        choices=InstituteSubjectEntityChoices.choices,
        default=InstituteSubjectEntityChoices.INSTITUTIONAL,
        verbose_name=_("جهة تبعية المادة (وزارية / مؤسسية)")
    )
    academic_category = models.CharField(
        max_length=30,
        choices=InstituteSubjectAcademicCategoryChoices.choices,
        default=InstituteSubjectAcademicCategoryChoices.SPECIALIZED,
        verbose_name=_("التصنيف الأكاديمي (تخصصية / مساعدة / عامة)")
    )
    theoretical_hours = models.PositiveSmallIntegerField(default=0, verbose_name=_("الساعات النظرية"))
    practical_hours = models.PositiveSmallIntegerField(default=0, verbose_name=_("الساعات العملية"))
    credit_hours = models.PositiveSmallIntegerField(default=3, verbose_name=_("الساعات المعتمدة"))
    description = models.TextField(null=True, blank=True, verbose_name=_("وصف المادة ومفرداتها"))
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_("نشط"))

    class Meta:
        db_table = 'institutes_subject'
        verbose_name = _("المادة الدراسية للمعهد")
        verbose_name_plural = _("المواد الدراسية للمعاهد")
        ordering = ['field_id', 'name_ar']

    def __str__(self):
        return f"{self.name_ar} [{self.subject_code}]"
