from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class UniversityStudySystem(BaseSyncModel):
    name_ar = models.CharField(max_length=100, verbose_name=_("اسم النظام الدراسي (عربي)"))
    name_en = models.CharField(max_length=100, verbose_name=_("اسم النظام الدراسي (إنجليزي)"))
    unified_code = models.CharField(max_length=50, verbose_name=_("الكود الموحد"))
    banner_color = models.CharField(max_length=7, default='#1976D2', verbose_name=_("لون البانر"))
    is_active = models.BooleanField(default=True, verbose_name=_('حالة التفعيل'))

    class Meta:
        db_table = 'universities_study_system'
        verbose_name = _("النظام الدراسي الجامعي")
        verbose_name_plural = _("الأنظمة الدراسية الجامعية")
        constraints = [
            models.UniqueConstraint(
                fields=['name_ar'],
                name='unique_name_ar_univ_study_system_no_deleted',
                condition=Q(is_deleted=False),
            ),
            models.UniqueConstraint(
                fields=['unified_code'],
                name='unique_unified_code_univ_study_system_no_deleted',
                condition=Q(is_deleted=False),
            ),
        ]

    def __str__(self):
        return f"{self.name_ar} ({self.unified_code})"

StudeySystem = UniversityStudySystem
StudySystem = UniversityStudySystem
