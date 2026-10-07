from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class TemplateVersion(SoftDeleteModel):
    template = models.ForeignKey(
        'templates_engine.ExamTemplate', 
        on_delete=models.CASCADE, 
        related_name="versions",
        verbose_name=_("القالب")
    )
    version = models.CharField(max_length=20, verbose_name=_("الإصدار"))
    template_data_snapshot = models.JSONField(default=dict)
    change_notes = models.TextField(blank=True, verbose_name=_("ملاحظات التغيير"))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        verbose_name=_("المنشئ")
    )

    class Meta:
        db_table = "template_versions"
        verbose_name = _("نسخة قالب")
        verbose_name_plural = _("نسخ القوالب")

    def __str__(self):
        return f"{self.template.name} — v{self.version}"
