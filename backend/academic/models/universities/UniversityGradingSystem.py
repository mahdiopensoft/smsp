from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel
from academic.choices.university_choices import GradeSystemTypeChoices

class UniversityGradingSystem(BaseSyncModel):
    name_ar = models.CharField(max_length=100, verbose_name=_('الاسم (عربي)'))
    name_en = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('الاسم (إنجليزي)'))
    grade_total = models.PositiveSmallIntegerField(
        verbose_name=_('الدرجة الكلية'), 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=100
    )
    grade_system_type = models.PositiveSmallIntegerField(
        choices=GradeSystemTypeChoices.choices, 
        verbose_name=_('نوع نظام الدرجات'),
        default=GradeSystemTypeChoices.JUNE
    )
    success_grade = models.PositiveSmallIntegerField(
        verbose_name=_('درجة النجاح'), 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=50
    )
    is_active = models.BooleanField(default=True, verbose_name=_('حالة التفعيل'))
    types = models.ManyToManyField(
        'academic.UniversityTypeOfGrade', 
        through='academic.UniversityGradeDistribution', 
        verbose_name=_('أنواع الدرجات')
    )

    def __str__(self):
        return self.name_ar

    class Meta:
        db_table = 'universities_grading_system'
        verbose_name = _('نظام التقدير والدرجات الجامعي')
        verbose_name_plural = _('أنظمة التقدير والدرجات الجامعية')
        constraints = [
            models.UniqueConstraint(
                fields=['name_ar'],
                name='unique_name_ar_univ_grading_no_deleted',
                condition=Q(is_deleted=False),
            ),
        ]

GradingSystem = UniversityGradingSystem
