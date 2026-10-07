from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class UniversitySpecializationBranch(BaseSyncModel):
    fk_branch = models.ForeignKey(
        'academic.Organization', 
        on_delete=models.CASCADE, 
        verbose_name=_('Branch')
    )
    fk_specialization = models.ForeignKey(
        'academic.UniversitySpecialization', 
        related_name='branches', 
        on_delete=models.CASCADE, 
        verbose_name=_('التخصص')
    )
    capacity = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_('Capacity'))
    state = models.BooleanField(default=True, verbose_name=_('الحالة'))

    def __str__(self):
        return f'{self.fk_branch.name_ar} - {self.fk_specialization.name_ar}'

    class Meta:
        db_table = 'universities_specialization_branch'
        verbose_name = _('فرع التخصص الجامعي')
        verbose_name_plural = _('فروع التخصصات الجامعية')
        constraints = [
            models.UniqueConstraint(
                fields=['fk_branch', 'fk_specialization'],
                name='unique_fk_spec_fk_branch_univ_no_deleted',
                condition=Q(is_deleted=False),
            )
        ]

SpecializationBranch = UniversitySpecializationBranch
