from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class ExamTemplate(SoftDeleteModel):
    name = models.CharField(max_length=255, verbose_name=_("اسم القالب"))
    version = models.CharField(max_length=20, default="1.0", verbose_name=_("الإصدار"))
    description = models.TextField(blank=True, verbose_name=_("الوصف"))

    template_data = models.JSONField(
        default=dict,
        help_text=_("Complete template JSON: fiducials, MCQ regions, essay regions, barcode")
    )

    paper_width_mm = models.FloatField(default=210, verbose_name=_("عرض الورقة (مم)"))  # A4 width
    paper_height_mm = models.FloatField(default=297, verbose_name=_("طول الورقة (مم)"))  # A4 height
    dpi = models.PositiveIntegerField(default=300, verbose_name=_("دقة الطباعة (DPI)"))

    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_("نشط"))
    is_validated = models.BooleanField(default=False, verbose_name=_("تم التحقق"))

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True, 
        related_name="created_templates",
        verbose_name=_("المنشئ")
    )

    class Meta:
        db_table = "exam_templates"
        verbose_name = _("قالب اختبار")
        verbose_name_plural = _("قوالب الاختبارات")
        unique_together = [("name", "version")]

    def __str__(self):
        return f"{self.name} v{self.version}"

    @property
    def fiducial_marks(self):
        return self.template_data.get("fiducial_marks", [])

    @property
    def mcq_questions(self):
        return self.template_data.get("mcq_questions", [])

    @property
    def essay_regions(self):
        return self.template_data.get("essay_regions", [])

    @property
    def barcode_region(self):
        return self.template_data.get("barcode_region")

    @property
    def total_mcq_count(self):
        return len(self.mcq_questions)

    @property
    def total_essay_count(self):
        return len(self.essay_regions)
