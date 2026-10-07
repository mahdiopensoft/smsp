from django.db import models
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class QuestionMetrics(SoftDeleteModel):
    question = models.OneToOneField(
        'bank.Question', 
        on_delete=models.CASCADE, 
        related_name='metrics', 
        verbose_name=_("السؤال")
    )
    usage_count = models.IntegerField(default=0, verbose_name=_("عدد مرات الاستخدام"))
    last_used_at = models.DateTimeField(null=True, blank=True, verbose_name=_("تاريخ آخر استخدام"))
    
    total_correct_answers = models.IntegerField(default=0, verbose_name=_("إجمالي الإجابات الصحيحة التراكمي"))
    total_respondents = models.IntegerField(default=0, verbose_name=_("إجمالي الطلاب المجيبين"))
    
    actual_difficulty = models.FloatField(null=True, blank=True, verbose_name=_("معامل الصعوبة الفعلي (p-value)"))
    discrimination_index = models.FloatField(null=True, blank=True, verbose_name=_("معامل التمييز (D)"))
    point_biserial = models.FloatField(null=True, blank=True, verbose_name=_("معامل الارتباط النقطي (rpb)"))
    
    avg_answer_time = models.FloatField(null=True, blank=True, verbose_name=_("متوسط زمن الحل (ثواني)"))
    total_answer_time = models.FloatField(default=0.0, verbose_name=_("مجموع أزمنة الإجابة التراكمي"))
    total_timed_responses = models.IntegerField(default=0, verbose_name=_("عدد الاستجابات المؤقتة"))
    
    rejection_count = models.IntegerField(default=0, verbose_name=_("عدد مرات الرفض"))
    edit_count = models.IntegerField(default=0, verbose_name=_("عدد مرات التعديل"))
    exclusion_rate = models.FloatField(default=0.0, verbose_name=_("معدل الاستبعاد القانوني"))
    
    last_calculated_at = models.DateTimeField(null=True, blank=True, verbose_name=_("تاريخ آخر عملية حسابية"))

    class Meta:
        verbose_name = _('مؤشرات القياس النفسي للسؤال')
        verbose_name_plural = _('مؤشرات القياس النفسي للأسئلة')

    def __str__(self):
        return f"Metrics for Question #{self.question_id} (p={self.actual_difficulty}, D={self.discrimination_index})"

    def recalculate_p_value(self):
        if self.total_respondents > 0:
            self.actual_difficulty = round(self.total_correct_answers / self.total_respondents, 3)
        return self.actual_difficulty
