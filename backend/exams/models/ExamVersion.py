from django.db import models
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class ExamVersion(SoftDeleteModel):
    exam = models.ForeignKey(
        'exams.Exam', 
        on_delete=models.CASCADE, 
        related_name='versions', 
        verbose_name=_("الاختبار الأساسي")
    )
    versionCode = models.CharField(max_length=50, verbose_name=_("رمز النموذج (A, B, C...)"))
    
    # Smart Model Difficulty Assignment
    model_group_index = models.IntegerField(
        default=0,
        verbose_name=_("رقم مجموعة النماذج"),
        help_text=_("ترتيب المجموعة التي ينتمي إليها هذا النموذج")
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
    difficulty_distribution = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_("توزيع الصعوبة التفصيلي"),
        help_text=_("مثال: {'easy': 60, 'medium': 30, 'hard': 10}")
    )

    class Meta:
        unique_together = ('exam', 'versionCode')
        verbose_name = _('نموذج اختبار')
        verbose_name_plural = _('نماذج الاختبارات')

    def __str__(self):
        return f"{self.exam.title} - {self.versionCode}"
