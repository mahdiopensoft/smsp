from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class UniversityLevel(BaseSyncModel):
    name_ar = models.CharField(max_length=150, verbose_name=_('الاسم (عربي)'))
    name_en = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('الاسم (إنجليزي)'))
    is_active = models.BooleanField(default=True, verbose_name=_('حالة التفعيل'))

    def __str__(self):
        return f'{self.name_ar}'

    class Meta:
        db_table = 'universities_level'
        verbose_name = _('المستوى التعليمي / الدرجة الجامعية')
        verbose_name_plural = _('المستويات التعليمية / الدرجات الجامعية')
        constraints = [
            models.UniqueConstraint(
                fields=['name_ar'],
                name='unique_name_ar_univ_educational_no_deleted',
                condition=Q(is_deleted=False),
            ),
        ]

EducationalLevels = UniversityLevel
