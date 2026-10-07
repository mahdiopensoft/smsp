from django.db import models
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class Answer(SoftDeleteModel):
    question = models.ForeignKey(
        'bank.Question', 
        on_delete=models.CASCADE, 
        related_name='options', 
        verbose_name=_("السؤال")
    )
    text = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("نص الخيار"))
    image = models.ImageField(upload_to='answers_images/', null=True, blank=True, verbose_name=_("صورة الخيار"))
    latex = models.TextField(null=True, blank=True, verbose_name=_("معادلة رياضية (Latex)"))
    isTrue = models.BooleanField(default=False, verbose_name=_("هل هي الإجابة الصحيحة؟"))

    class Meta:
        verbose_name = _('إجابة')
        verbose_name_plural = _('الإجابات')

    def __str__(self):
        if self.text:
            return self.text
        elif self.image:
            return f"صورة: {self.image.name}"
        elif self.latex:
            return f"معادلة: {self.latex}"
        return f"خيار لـ {self.question_id}"
