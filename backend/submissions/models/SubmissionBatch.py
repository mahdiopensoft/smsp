from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class SubmissionBatch(SoftDeleteModel):
    class Status(models.TextChoices):
        PENDING = "pending", _("قيد الانتظار")
        PROCESSING = "processing", _("جاري المعالجة")
        COMPLETED = "completed", _("مكتمل")
        PARTIALLY_COMPLETED = "partially_completed", _("مكتمل جزئياً")
        FAILED = "failed", _("فشل")

    name = models.CharField(max_length=255, verbose_name=_("اسم الدفعة"))
    exam = models.ForeignKey(
        "exams.Exam", 
        on_delete=models.CASCADE, 
        related_name="batches",
        verbose_name=_("الاختبار")
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,
        null=True, 
        related_name="uploaded_batches",
        verbose_name=_("تم الرفع بواسطة")
    )
    total_papers = models.PositiveIntegerField(default=0, verbose_name=_("إجمالي الأوراق"))
    processed_papers = models.PositiveIntegerField(default=0, verbose_name=_("الأوراق المعالجة"))
    failed_papers = models.PositiveIntegerField(default=0, verbose_name=_("الأوراق الفاشلة"))

    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING, verbose_name=_("الحالة"))
    notes = models.TextField(blank=True, verbose_name=_("ملاحظات"))

    class Meta:
        db_table = "submission_batches"
        verbose_name = _("دفعة أوراق")
        verbose_name_plural = _("دفعات الأوراق")

    def __str__(self):
        return f"Batch: {self.name} ({self.total_papers} papers)"
