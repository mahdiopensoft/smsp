from django.db import models
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class ExamQuestionOrder(SoftDeleteModel):
    examVersion = models.ForeignKey(
        'exams.ExamVersion', 
        on_delete=models.CASCADE, 
        related_name='question_orders'
    )
    question = models.ForeignKey(
        'bank.Question', 
        on_delete=models.CASCADE, 
        related_name='exam_appearances'
    )
    orderIndex = models.IntegerField(verbose_name=_("ترتيب السؤال في النموذج"))

    class Meta:
        unique_together = ('examVersion', 'question')
        ordering = ['orderIndex']
        verbose_name = _('ترتيب سؤال الاختبار')
        verbose_name_plural = _('ترتيبات أسئلة الاختبار')

    def __str__(self):
        return f"Q{self.orderIndex} in {self.examVersion}"
