from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class OMRReviewAuditLog(SoftDeleteModel):
    class ReasonCode(models.TextChoices):
        CROSSED_BUT_STUDENT_INTENT_CLEAR = "CROSSED_INTENT_CLEAR", _("شطب صريح مع وضوح نية الطالب")
        HALF_FILLED_ACCEPTED = "HALF_FILLED_ACCEPTED", _("قبول تظليل نصفي/باهت كإجابة مقصودة")
        MULTIPLE_MARKS_RESOLVED = "MULTIPLE_RESOLVED", _("حسم تظليل متعدد وفق محضر الكنترول")
        VISION_ERROR_CORRECTED = "VISION_ERROR", _("تصحيح خطأ قراءة بصرية أو تشوه بالورقة")
        ORIENTATION_OR_SKEW_RESOLVED = "ORIENTATION_RESOLVED", _("تصحيح خطأ دوران أو ميلان")
        BLANK_CONFIRMED = "BLANK_CONFIRMED", _("تأكيد ترك السؤال فارغاً بدون إجابة")
        OTHER = "OTHER", _("سبب آخر موثق بالملاحظات")

    sheet_result = models.ForeignKey(
        'omr.OMRSheetResult',
        on_delete=models.CASCADE,
        related_name='review_audits',
        verbose_name=_("نتيجة الورقة")
    )
    question_result = models.ForeignKey(
        'omr.OMRQuestionResult',
        on_delete=models.CASCADE,
        related_name='review_audits',
        verbose_name=_("نتيجة السؤال")
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("المراجع")
    )
    reason_code = models.CharField(
        max_length=35,
        choices=ReasonCode.choices,
        default=ReasonCode.OTHER,
        verbose_name=_("كود السبب")
    )
    reason_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("تفاصيل إضافية")
    )
    before_snapshot = models.JSONField(
        default=dict,
        verbose_name=_("لقطة السؤال قبل التعديل")
    )
    after_snapshot = models.JSONField(
        default=dict,
        verbose_name=_("لقطة السؤال بعد التعديل")
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_("عنوان IP")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("تاريخ ووقت التعديل")
    )

    class Meta:
        db_table = "omr_review_audit_logs"
        verbose_name = _("سجل تدقيق مراجعة OMR")
        verbose_name_plural = _("سجلات تدقيق مراجعة OMR")
        ordering = ['-created_at']

    def __str__(self):
        return f"Audit #{self.id} for Q#{self.question_result.question_number if self.question_result else '?'} by {self.reviewer}"
