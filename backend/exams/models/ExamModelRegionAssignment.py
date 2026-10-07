from django.db import models
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class ExamModelRegionAssignment(SoftDeleteModel):
    """
    ربط مجموعة نماذج بمنطقة جغرافية
    يحدد أي محافظة / مديرية تأخذ أي مجموعة نماذج (صعب / سهل / متوسط)
    """
    exam = models.ForeignKey(
        'exams.Exam',
        on_delete=models.CASCADE,
        related_name='model_region_assignments',
        verbose_name=_("الاختبار")
    )

    # مجموعة النماذج
    model_group_index = models.IntegerField(
        verbose_name=_("رقم مجموعة النماذج"),
        help_text=_("ترتيب المجموعة في قائمة مجموعات النماذج (0-indexed)")
    )
    difficulty_profile = models.CharField(
        max_length=20,
        choices=[
            ('easy', _('سهل')),
            ('medium', _('متوسط')),
            ('hard', _('صعب')),
            ('mixed', _('مختلط'))
        ],
        default='mixed',
        verbose_name=_("ملف الصعوبة")
    )

    # الربط الجغرافي
    scope_level = models.CharField(
        max_length=20,
        choices=[
            ('governorate', _('محافظة')),
            ('directorate', _('مديرية')),
            ('region', _('منطقة')),
            ('school', _('مدرسة / مؤسسة'))
        ],
        default='governorate',
        verbose_name=_("مستوى الاستهداف")
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
        verbose_name = _('تعيين نماذج لمنطقة')
        verbose_name_plural = _('تعيينات نماذج للمناطق')
        ordering = ['model_group_index', 'scope_level']

    def __str__(self):
        target = self.governorate or self.directorate or self.region or self.organization
        return f"مجموعة {self.model_group_index + 1} ({self.get_difficulty_profile_display()}) → {target or '—'}"
