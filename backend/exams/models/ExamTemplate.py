from django.db import models
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class ExamTemplate(SoftDeleteModel):
    """
    قالب اختبار قابل لإعادة الاستخدام
    يخزن كل إعدادات الاختبار بما في ذلك المصفوفة ومجموعات النماذج والاستهداف الجغرافي
    """
    name = models.CharField(
        max_length=255,
        verbose_name=_("اسم القالب")
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("وصف القالب")
    )
    institution_type = models.CharField(
        max_length=20,
        choices=[
            ('school', _('مدرسي')),
            ('university', _('جامعي')),
            ('institute', _('معاهد وتدريب مهني'))
        ],
        default='school',
        verbose_name=_("نوع المؤسسة")
    )
    config_json = models.JSONField(
        verbose_name=_("إعدادات القالب"),
        help_text=_("يحفظ كل إعدادات الاختبار والمصفوفة ومجموعات النماذج بصيغة JSON")
    )

    class Meta:
        verbose_name = _('قالب اختبار')
        verbose_name_plural = _('قوالب الاختبارات')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_institution_type_display()})"
