from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class UniversityDepartment(BaseSyncModel):
    fk_college = models.ForeignKey(
        'academic.UniversityCollege', 
        related_name='sections', 
        on_delete=models.CASCADE, 
        verbose_name=_('College')
    )
    name_ar = models.CharField(max_length=100, verbose_name=_('Name (Arabic)'))
    name_en = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Name (English)'))
    section_code = models.CharField(verbose_name=_("رمز القسم"), max_length=10)
    is_active = models.BooleanField(default=True, verbose_name=_('حالة التفعيل'))

    def __str__(self):
        return f"{self.fk_college.name_ar} - {self.name_ar}"

    class Meta:
        db_table = 'universities_department'
        verbose_name = _('القسم الأكاديمي الجامعي')
        verbose_name_plural = _('الأقسام الأكاديمية الجامعية')
        constraints = [
            models.UniqueConstraint(
                fields=['fk_college', 'name_ar'],
                name='unique_name_ar_univ_dept_no_deleted',
                condition=Q(is_deleted=False),
            ),
            models.UniqueConstraint(
                fields=['fk_college', 'name_en'],
                name='unique_name_en_univ_dept_no_deleted',
                condition=Q(is_deleted=False) & Q(name_en__gt=''),
            )
        ]

Department = UniversityDepartment
