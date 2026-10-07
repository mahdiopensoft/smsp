from django.db import models
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class DistractorAnalysis(SoftDeleteModel):
    answer = models.OneToOneField(
        'bank.Answer', 
        on_delete=models.CASCADE, 
        related_name='distractor_analysis', 
        verbose_name=_("الخيار / البديل")
    )
    question = models.ForeignKey(
        'bank.Question', 
        on_delete=models.CASCADE, 
        related_name='distractor_analyses', 
        verbose_name=_("السؤال")
    )
    selection_count = models.IntegerField(default=0, verbose_name=_("عدد مرات اختيار هذا البديل"))
    selection_rate = models.FloatField(default=0.0, verbose_name=_("نسبة الاختيار العامة"))
    upper_group_rate = models.FloatField(default=0.0, verbose_name=_("نسبة اختيار الفئة المتفوقة (أعلى 27%)"))
    lower_group_rate = models.FloatField(default=0.0, verbose_name=_("نسبة اختيار الفئة الضعيفة (أدنى 27%)"))
    last_calculated_at = models.DateTimeField(null=True, blank=True, verbose_name=_("تاريخ آخر حساب"))

    class Meta:
        verbose_name = _('تحليل المشتت / البديل')
        verbose_name_plural = _('تحليلات المشتتات والبدائل')

    def __str__(self):
        return f"Distractor #{self.answer_id} (Rate: {self.selection_rate:.1%})"
