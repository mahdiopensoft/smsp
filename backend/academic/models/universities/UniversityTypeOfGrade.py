from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class UniversityTypeOfGrade(BaseSyncModel):
    fk_branch = models.ForeignKey(
        'academic.Organization', 
        on_delete=models.CASCADE, 
        verbose_name=_("الفرع"), 
        null=True, 
        blank=True
    )
    name_ar = models.CharField(max_length=100, verbose_name=_('Name (Arabic)'))
    name_en = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Name (English)'))
    description = models.TextField(max_length=250, null=True, blank=True, verbose_name=_('Description'))

    def __str__(self):
        return self.name_ar

    class Meta:
        db_table = 'universities_type_of_grade'
        verbose_name = _('نوع الدرجة الجامعية')
        verbose_name_plural = _('أنواع الدرجات الجامعية')
        constraints = [
            models.UniqueConstraint(
                fields=['fk_branch', 'name_ar'],
                name='unique_name_ar_univ_type_of_grade_no_deleted',
                condition=Q(is_deleted=False),
            ),
            models.UniqueConstraint(
                fields=['fk_branch', 'name_en'],
                name='unique_name_en_univ_type_of_grade_no_deleted',
                condition=Q(is_deleted=False) & Q(name_en__gt=''),
            )
        ]

TypeOfGrade = UniversityTypeOfGrade
