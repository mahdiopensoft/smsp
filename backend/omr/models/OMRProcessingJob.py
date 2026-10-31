import uuid
import hashlib
from django.db import models
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class OMRProcessingJob(SoftDeleteModel):
    class Status(models.TextChoices):
        PENDING = "pending", _("قيد الانتظار")
        PROCESSING = "processing", _("جاري التنفيذ")
        COMPLETED = "completed", _("مكتمل بنجاح")
        FAILED = "failed", _("فشل التنفيذ")
        SKIPPED_IDEMPOTENT = "skipped_idempotent", _("تم التخطي (موجود مسبقاً)")

    job_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, verbose_name=_("معرف المهمة"))
    batch = models.ForeignKey(
        'submissions.SubmissionBatch',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='omr_jobs',
        verbose_name=_("الدفعة")
    )
    submission = models.ForeignKey(
        'submissions.Submission',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processing_jobs',
        verbose_name=_("التسليم المرتبط")
    )
    source_file_hash = models.CharField(max_length=64, db_index=True, verbose_name=_("بصمة الملف الأصلي"))
    processing_fingerprint = models.CharField(max_length=64, db_index=True, verbose_name=_("بصمة المعالجة المركبة"))
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING, db_index=True)
    retry_count = models.PositiveSmallIntegerField(default=0, verbose_name=_("عدد محاولات الإعادة"))
    worker_id = models.CharField(max_length=100, blank=True, verbose_name=_("معرف العامل"))
    result_summary = models.JSONField(default=dict, blank=True, verbose_name=_("ملخص النتيجة"))
    error_details = models.TextField(blank=True, verbose_name=_("تفاصيل الخطأ"))
    started_at = models.DateTimeField(null=True, blank=True, verbose_name=_("وقت البدء"))
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name=_("وقت الانتهاء"))

    class Meta:
        db_table = "omr_processing_jobs"
        verbose_name = _("مهمة معالجة OMR")
        verbose_name_plural = _("مهام معالجة OMR")
        indexes = [
            models.Index(fields=["processing_fingerprint", "status"]),
            models.Index(fields=["source_file_hash"]),
        ]

    @classmethod
    def calculate_fingerprint(cls, source_file_hash: str, version_id: str, pipeline_ver: str = "3.0", model_ver: str = "1.0") -> str:
        """
        Calculates cryptographic composite processing fingerprint:
        SHA-256(source_file_hash + version_id + pipeline_ver + model_ver)
        """
        raw = f"{source_file_hash}:{version_id}:{pipeline_ver}:{model_ver}"
        return hashlib.sha256(raw.encode('utf-8')).hexdigest()

    def __str__(self):
        return f"OMRJob [{self.status}] — {self.job_id}"
