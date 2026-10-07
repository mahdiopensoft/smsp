from django.db import models
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class OMRQuestionResult(SoftDeleteModel):
    class BubbleState(models.TextChoices):
        EMPTY = "empty", _("فارغ")
        FILLED = "filled", _("مظلل")
        ERASED = "erased", _("ممسوح")
        CROSSED = "crossed", _("مشطوب")
        AMBIGUOUS = "ambiguous", _("ملتبس")
        MULTIPLE = "multiple", _("تظليل متعدد")

    sheet_result = models.ForeignKey(
        'omr.OMRSheetResult',
        on_delete=models.CASCADE,
        related_name="questions"
    )

    question_number = models.PositiveIntegerField(verbose_name=_("رقم السؤال"))
    marked_choice = models.CharField(max_length=5, blank=True, null=True, verbose_name=_("الخيار المظلل"))
    correct_choice = models.CharField(max_length=5, blank=True, null=True, verbose_name=_("الخيار الصحيح"))
    is_correct = models.BooleanField(null=True, verbose_name=_("هل هو صحيح؟"))
    bubble_state = models.CharField(
        max_length=20,
        choices=BubbleState.choices,
        default=BubbleState.EMPTY,
        verbose_name=_("حالة الدائرة")
    )

    choice_confidences = models.JSONField(
        default=dict,
        help_text='{"A": 0.05, "B": 0.10, "C": 0.82, "D": 0.03}'
    )
    final_confidence = models.FloatField(default=0.0)

    region_coordinates = models.JSONField(
        null=True, blank=True,
        help_text='{"x": 100, "y": 200, "width": 30, "height": 30}'
    )

    darkness_values = models.JSONField(
        null=True, blank=True,
        help_text='{"A": 0.05, "B": 0.08, "C": 0.82, "D": 0.06}'
    )

    marks_awarded = models.DecimalField(max_digits=4, decimal_places=2, default=0, verbose_name=_("الدرجة الممنوحة"))

    class Meta:
        db_table = "omr_question_results"
        verbose_name = _("نتيجة سؤال OMR")
        verbose_name_plural = _("نتائج أسئلة OMR")
        ordering = ["question_number"]
        unique_together = [("sheet_result", "question_number")]

    def __str__(self):
        return f"Q{self.question_number}: {self.marked_choice or '—'} (conf={self.final_confidence:.2f})"
