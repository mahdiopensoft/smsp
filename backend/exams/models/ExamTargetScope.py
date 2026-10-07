from django.db import models
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class ExamTargetScope(SoftDeleteModel):
    """
    نطاق استهداف الاختبار - يحدد المناطق الجغرافية والمؤسسات المستهدفة
    يسمح باختيار عدة محافظات / مديريات / مناطق / مدارس كأهداف للاختبار
    """
    class ScopeLevel(models.TextChoices):
        COUNTRY = 'country', _('دولة كاملة')
        GOVERNORATE = 'governorate', _('محافظة')
        DIRECTORATE = 'directorate', _('مديرية')
        REGION = 'region', _('منطقة')
        SCHOOL = 'school', _('مدرسة / مؤسسة')

    exam = models.ForeignKey(
        'exams.Exam',
        on_delete=models.CASCADE,
        related_name='target_scopes',
        verbose_name=_("الاختبار")
    )
    scope_level = models.CharField(
        max_length=20,
        choices=ScopeLevel.choices,
        verbose_name=_("مستوى الاستهداف")
    )

    # الربط الجغرافي (واحد فقط يكون معبأ حسب scope_level)
    country = models.ForeignKey(
        'common.Country',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("الدولة")
    )
    governorate = models.ForeignKey(
        'common.Governorate',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("المحافظة")
    )
    directorate = models.ForeignKey(
        'common.Directorate',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("المديرية")
    )
    region = models.ForeignKey(
        'common.Region',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("المنطقة")
    )
    organization = models.ForeignKey(
        'common.Organization',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("المدرسة / المؤسسة")
    )

    class Meta:
        verbose_name = _('نطاق استهداف اختبار')
        verbose_name_plural = _('نطاقات استهداف الاختبارات')
        ordering = ['scope_level']

    def __str__(self):
        level_names = {
            'country': self.country,
            'governorate': self.governorate,
            'directorate': self.directorate,
            'region': self.region,
            'school': self.organization,
        }
        target = level_names.get(self.scope_level)
        return f"{self.exam.title} → {self.get_scope_level_display()}: {target or '—'}"
