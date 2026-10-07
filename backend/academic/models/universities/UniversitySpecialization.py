from django.db import models
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel
from academic.choices.university_choices import (
    NumberOfSemesterEachLevelChoices,
    LevelChoice,
    NumberOfLevelsChoices
)

class UniversitySpecialization(BaseSyncModel):
    fk_section = models.ForeignKey(
        'academic.UniversityDepartment', 
        related_name='specializations', 
        on_delete=models.CASCADE, 
        verbose_name=_('Section')
    )
    fk_college = models.ForeignKey(
        'academic.UniversityCollege', 
        related_name='specializations', 
        on_delete=models.CASCADE, 
        verbose_name=_('College')
    )
    name_ar = models.CharField(max_length=100, verbose_name=_('Name (Arabic)'))
    name_en = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Name (English)'))
    specialization_code = models.CharField(verbose_name=_("رمز التخصص"), max_length=10)
    is_active = models.BooleanField(default=True, verbose_name=_('حالة التفعيل'))
    fk_educational_levels = models.ForeignKey(
        'academic.UniversityLevel', 
        related_name='specializations', 
        on_delete=models.CASCADE, 
        verbose_name=_('المستوى التعليمي / الدرجة'),
        null=True, 
        blank=True
    )

    number_of_levels = models.PositiveSmallIntegerField(
        verbose_name=_('عدد المستويات الدراسية'), 
        choices=NumberOfLevelsChoices.choices, 
        default=NumberOfLevelsChoices.FOUR_LEVELS
    )
    max_failure_subjects = models.PositiveSmallIntegerField(
        verbose_name=_('أقصى عدد لمواد معادة في السنوات السابقة'),
        default=4
    )
    max_failure_years = models.PositiveSmallIntegerField(
        verbose_name=_('أقصى عدد من سنوات الرسوب المتراكم'), 
        blank=True, 
        null=True, 
        validators=[MinValueValidator(1), MaxValueValidator(99)]
    )

    number_of_semester_each_level = models.PositiveSmallIntegerField(
        choices=NumberOfSemesterEachLevelChoices.choices, 
        default=NumberOfSemesterEachLevelChoices.TWO_SEMESTERS, 
        verbose_name=_('عدد الفصول الدراسية للسنة')
    )
    start_from_level = models.PositiveSmallIntegerField(
        choices=LevelChoice.choices, 
        default=LevelChoice.LEVEL_1, 
        verbose_name=_('يبدأ من المستوى')
    )
    is_general = models.BooleanField(default=False, verbose_name=_('عام'))

    def __str__(self):
        return f"{self.name_ar} ({self.fk_college.name_ar})"

    class Meta:
        db_table = 'universities_specialization'
        verbose_name = _('التخصص الأكاديمي الجامعي')
        verbose_name_plural = _('التخصصات الأكاديمية الجامعية')
        constraints = [
            models.UniqueConstraint(
                fields=['name_ar', 'fk_college', 'fk_section'],
                name='unique_name_ar_univ_specialization_no_deleted',
                condition=Q(is_deleted=False),
            ),
            models.UniqueConstraint(
                fields=['specialization_code', 'fk_college'],
                name='unique_spec_code_univ_specialization_no_deleted',
                condition=Q(is_deleted=False),
            ),
        ]

Specialization = UniversitySpecialization
