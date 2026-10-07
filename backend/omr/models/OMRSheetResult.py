from django.db import models
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class OMRSheetResult(SoftDeleteModel):
    submission = models.OneToOneField(
        "submissions.Submission",
        on_delete=models.CASCADE,
        related_name="omr_detail",
        verbose_name=_("التسليم")
    )
    status = models.CharField(max_length=20, default="success", verbose_name=_("الحالة"))
    confidence = models.FloatField(default=0.0, verbose_name=_("نسبة الثقة"))

    total_questions = models.PositiveIntegerField(default=0, verbose_name=_("إجمالي الأسئلة"))
    answered_questions = models.PositiveIntegerField(default=0, verbose_name=_("الأسئلة المجاب عليها"))
    correct_answers = models.PositiveIntegerField(default=0, verbose_name=_("الإجابات الصحيحة"))
    wrong_answers = models.PositiveIntegerField(default=0, verbose_name=_("الإجابات الخاطئة"))
    unanswered = models.PositiveIntegerField(default=0, verbose_name=_("غير المجاب عليها"))
    ambiguous_count = models.PositiveIntegerField(default=0, verbose_name=_("الأسئلة الملتبسة"))

    mcq_score = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name=_("درجة الخيارات"))
    mcq_max_score = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name=_("الدرجة العظمى للخيارات"))

    provider_used = models.CharField(max_length=50, default="opencv", verbose_name=_("مزود الخدمة"))
    processing_time_ms = models.FloatField(default=0.0, verbose_name=_("زمن المعالجة"))

    class Meta:
        db_table = "omr_sheet_results"
        verbose_name = _("نتيجة OMR")
        verbose_name_plural = _("نتائج OMR")

    def __str__(self):
        return f"OMR [{self.correct_answers}/{self.total_questions}] — {self.submission_id}"
