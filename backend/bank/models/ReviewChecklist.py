from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class ReviewChecklist(SoftDeleteModel):
    question = models.ForeignKey(
        'bank.Question', 
        on_delete=models.CASCADE, 
        related_name='review_checklists', 
        verbose_name=_("السؤال")
    )
    linguistic_check = models.BooleanField(default=False, verbose_name=_("سلامة اللغة والإملاء والتشكيل"))
    scientific_check = models.BooleanField(default=False, verbose_name=_("صحة المعلومة والمفهوم العلمي"))
    image_check = models.BooleanField(default=True, verbose_name=_("وضوح وجودة الصور والمرفقات"))
    answer_check = models.BooleanField(default=False, verbose_name=_("دقة تحديد الإجابة وخلو البدائل من التمويه الخاطئ"))
    curriculum_check = models.BooleanField(default=False, verbose_name=_("توافق السؤال مع الدرس والوحدة"))
    learning_outcome_check = models.BooleanField(default=True, verbose_name=_("توافق السؤال مع مخرج التعلم"))
    bloom_check = models.BooleanField(default=False, verbose_name=_("صحة تصنيف مستوى بلوم المعرفي"))
    
    notes = models.TextField(null=True, blank=True, verbose_name=_("ملاحظات المراجع"))
    decision = models.CharField(max_length=50, default='Approved', verbose_name=_("قرار المراجعة"))
    
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='completed_review_checklists', 
        verbose_name=_("المراجع")
    )

    class Meta:
        verbose_name = _('قائمة فحص المراجعة')
        verbose_name_plural = _('قوائم فحص المراجعة')

    def is_all_passed(self):
        return all([
            self.linguistic_check,
            self.scientific_check,
            self.image_check,
            self.answer_check,
            self.curriculum_check,
            self.learning_outcome_check,
            self.bloom_check
        ])
