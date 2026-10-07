from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class UniversityCollegeBranch(BaseSyncModel):
    fk_branch = models.ForeignKey(
        'academic.Organization', 
        on_delete=models.CASCADE, 
        verbose_name=_('Branch')
    )
    fk_college = models.ForeignKey(
        'academic.UniversityCollege', 
        related_name='branches', 
        on_delete=models.CASCADE, 
        verbose_name=_('الكلية')
    )

    def __str__(self):
        return f'{self.fk_branch.name_ar} - {self.fk_college.name_ar}'

    class Meta:
        db_table = 'universities_college_branch'
        verbose_name = _('فرع الكلية الجامعية')
        verbose_name_plural = _('فروع الكليات الجامعية')
        constraints = [
            models.UniqueConstraint(
                fields=['fk_branch', 'fk_college'],
                name='unique_fk_branch_fk_univ_college_no_deleted',
                condition=Q(is_deleted=False),
            )
        ]

CollegeBranch = UniversityCollegeBranch
