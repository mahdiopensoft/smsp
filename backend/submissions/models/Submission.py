from django.db import models
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class Submission(SoftDeleteModel):
    class Status(models.TextChoices):
        PENDING = "pending", _("قيد الانتظار")
        ALIGNING = "aligning", _("جاري المحاذاة")
        OMR_PROCESSING = "omr_processing", _("جاري قراءة الدوائر")
        HTR_PROCESSING = "htr_processing", _("جاري استخراج النص")
        JUDGING = "judging", _("جاري التقييم")
        NEEDS_REVIEW = "needs_review", _("يحتاج مراجعة")
        REVIEWED = "reviewed", _("تمت المراجعة")
        COMPLETED = "completed", _("مكتمل")
        FAILED = "failed", _("فشل")

    batch = models.ForeignKey(
        'submissions.SubmissionBatch', 
        on_delete=models.CASCADE, 
        related_name="submissions", 
        null=True, 
        blank=True,
        verbose_name=_("الدفعة")
    )
    exam = models.ForeignKey(
        "exams.Exam", 
        on_delete=models.CASCADE, 
        related_name="submissions",
        verbose_name=_("الاختبار")
    )
    exam_version = models.ForeignKey(
        "exams.ExamVersion", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="submissions", 
        verbose_name=_("نموذج الاختبار")
    )
    registration = models.OneToOneField(
        "exams.StudentExamRegistration", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="submission", 
        verbose_name=_("تسجيل الطالب")
    )

    original_image = models.ImageField(upload_to="uploads/original/%Y/%m/", verbose_name=_("الصورة الأصلية"))
    aligned_image = models.ImageField(upload_to="uploads/aligned/%Y/%m/", blank=True, verbose_name=_("الصورة المحاذاة"))

    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING, db_index=True, verbose_name=_("الحالة"))
    current_engine = models.CharField(max_length=50, blank=True, verbose_name=_("المحرك الحالي"))

    alignment_result = models.JSONField(null=True, blank=True)
    layout_result = models.JSONField(null=True, blank=True)
    omr_result = models.JSONField(null=True, blank=True)
    htr_result = models.JSONField(null=True, blank=True)
    verification_result = models.JSONField(null=True, blank=True)
    judge_result = models.JSONField(null=True, blank=True)
    confidence_result = models.JSONField(null=True, blank=True)

    mcq_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name=_("درجة الخيارات"))
    essay_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name=_("درجة المقالي"))
    total_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name=_("الدرجة الكلية"))
    overall_confidence = models.FloatField(null=True, blank=True, verbose_name=_("نسبة الثقة الكلية"))

    processing_started_at = models.DateTimeField(null=True, blank=True)
    processing_completed_at = models.DateTimeField(null=True, blank=True)
    processing_time_ms = models.FloatField(null=True, blank=True)
    error_message = models.TextField(blank=True, verbose_name=_("رسالة الخطأ"))

    class Meta:
        db_table = "submissions"
        verbose_name = _("ورقة اختبار")
        verbose_name_plural = _("أوراق الاختبارات")
        indexes = [
            models.Index(fields=["exam", "status"]),
            models.Index(fields=["registration", "exam"]),
        ]

    def __str__(self):
        student_name = self.registration.student.name if self.registration and hasattr(self.registration, 'student') and self.registration.student else "Unknown"
        return f"Submission: {student_name} — {self.exam.title} [{self.status}]"
