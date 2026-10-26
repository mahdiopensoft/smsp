from django.db import models
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class SubmissionPage(SoftDeleteModel):
    submission = models.ForeignKey(
        'submissions.Submission',
        on_delete=models.CASCADE,
        related_name='pages',
        verbose_name=_("التسليم الأساسي")
    )
    page_number = models.PositiveSmallIntegerField(default=1, verbose_name=_("رقم الصفحة"))
    source_file_hash = models.CharField(max_length=64, db_index=True, blank=True, verbose_name=_("بصمة الملف الأصلي"))
    processing_fingerprint = models.CharField(max_length=64, db_index=True, blank=True, verbose_name=_("بصمة المعالجة المركبة"))
    image = models.ImageField(upload_to="uploads/pages/%Y/%m/", blank=True, verbose_name=_("صورة الصفحة"))
    aligned_image = models.ImageField(upload_to="uploads/pages_aligned/%Y/%m/", blank=True, verbose_name=_("الصورة المحاذاة"))
    page_score = models.DecimalField(max_digits=6, decimal_places=2, default=0.0, verbose_name=_("درجة الصفحة"))
    sheet_result = models.OneToOneField(
        'omr.OMRSheetResult',
        on_delete=models.SET_NULL,
        related_name='page_detail',
        null=True,
        blank=True,
        verbose_name=_("نتيجة التصحيح التفصيلية")
    )
    status = models.CharField(max_length=30, default='pending', verbose_name=_("حالة الصفحة"))
    layout_result = models.JSONField(null=True, blank=True, verbose_name=_("بيانات التخطيط"))
    omr_result = models.JSONField(null=True, blank=True, verbose_name=_("نتائج الدوائر"))

    class Meta:
        db_table = "submission_pages"
        verbose_name = _("صفحة ورقة الاختبار")
        verbose_name_plural = _("صفحات أوراق الاختبارات")
        constraints = [
            models.UniqueConstraint(
                fields=['submission', 'page_number'],
                condition=models.Q(is_deleted=False),
                name='unique_submission_page_number'
            ),
            models.CheckConstraint(
                condition=models.Q(page_number__gte=1),
                name='chk_page_number_positive'
            )
        ]

    def __str__(self):
        return f"SubmissionPage #{self.page_number} for Submission {self.submission_id}"
