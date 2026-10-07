from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class QuestionVersion(SoftDeleteModel):
    original_question = models.ForeignKey(
        'bank.Question', 
        on_delete=models.CASCADE, 
        related_name='version_records', 
        verbose_name=_("السؤال الأصلي")
    )
    version_question = models.ForeignKey(
        'bank.Question', 
        on_delete=models.CASCADE, 
        related_name='forked_from_versions', 
        verbose_name=_("السؤال النسخة")
    )
    version_number = models.PositiveIntegerField(verbose_name=_("رقم الإصدار"))
    diff_summary = models.JSONField(null=True, blank=True, verbose_name=_("ملخص الفروقات"))
    change_reason = models.TextField(null=True, blank=True, verbose_name=_("سبب التعديل أو الإصدار"))
    
    createdBy = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='created_question_versions', 
        verbose_name=_("منشئ الإصدار")
    )

    class Meta:
        verbose_name = _('إصدار سؤال')
        verbose_name_plural = _('إصدارات الأسئلة')
        ordering = ['-version_number']

    def __str__(self):
        return f"Question #{self.original_question_id} v{self.version_number}"
