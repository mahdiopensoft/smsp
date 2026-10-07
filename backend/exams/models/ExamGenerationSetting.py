from django.db import models
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class ExamGenerationSetting(SoftDeleteModel):
    name = models.CharField(max_length=255, verbose_name=_("اسم الإعداد"))
    easyPercentage = models.IntegerField(default=30)
    mediumPercentage = models.IntegerField(default=50)
    hardPercentage = models.IntegerField(default=20)
    rememberPercentage = models.IntegerField(default=20)
    understandPercentage = models.IntegerField(default=30)
    applyPercentage = models.IntegerField(default=30)
    analyzePercentage = models.IntegerField(default=10)
    evaluatePercentage = models.IntegerField(default=5)
    createPercentage = models.IntegerField(default=5)

    class Meta:
        verbose_name = _('إعداد توليد اختبار')
        verbose_name_plural = _('إعدادات توليد الاختبارات')

    def __str__(self):
        return self.name
