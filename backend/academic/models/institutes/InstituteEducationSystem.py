from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel
from academic.choices.institute_choices import (
    InstituteEducationSystemTypeChoices,
    InstituteStudyNatureChoices,
    InstituteGradingCalculationChoices,
)

class InstituteEducationSystem(BaseSyncModel):
    name_ar = models.CharField(max_length=150, verbose_name=_("اسم نظام التعليم (عربي)"))
    name_en = models.CharField(max_length=150, null=True, blank=True, verbose_name=_("اسم نظام التعليم (إنجليزي)"))
    system_code = models.CharField(max_length=50, unique=True, verbose_name=_("كود نظام التعليم"))
    field = models.ForeignKey(
        'academic.InstituteField',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='education_systems',
        verbose_name=_("المجال الافتراضي")
    )
    system_type = models.CharField(
        max_length=50,
        choices=InstituteEducationSystemTypeChoices.choices,
        default=InstituteEducationSystemTypeChoices.TECHNICAL_DIPLOMA_2Y,
        verbose_name=_("نوع المؤهل / نظام التعليم")
    )
    study_nature = models.CharField(
        max_length=50,
        choices=InstituteStudyNatureChoices.choices,
        default=InstituteStudyNatureChoices.PRACTICAL_VOCATIONAL,
        verbose_name=_("طبيعة الدراسة")
    )
    admission_qualification = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_("مؤهل القبول المطلوب")
    )
    duration_years = models.PositiveSmallIntegerField(
        default=2,
        verbose_name=_("مدة الدراسة بالسنوات")
    )
    has_regular_curriculum = models.BooleanField(
        default=True,
        verbose_name=_("يعتمد على خطة دراسية منتظمة")
    )
    has_ministerial_exam = models.BooleanField(
        default=True,
        verbose_name=_("خاضع للاختبار الوزاري النهائي")
    )
    grading_calculation_method = models.CharField(
        max_length=50,
        choices=InstituteGradingCalculationChoices.choices,
        default=InstituteGradingCalculationChoices.CUMULATIVE_AND_MINISTERIAL,
        verbose_name=_("آلية احتساب النتائج والمعدلات")
    )
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name=_("الوصف والملاحظات"))
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_("نشط"))

    class Meta:
        db_table = 'institutes_education_system'
        verbose_name = _("نظام تعليم وتدريب")
        verbose_name_plural = _("أنظمة التعليم والتدريب")
        ordering = ['system_code', 'name_ar']

    def __str__(self):
        return self.name_ar or self.system_code
