from django.db import models
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class OMRPrintOrder(SoftDeleteModel):
    class Status(models.TextChoices):
        PENDING = 'pending', _('قيد المراجعة والاعتماد')
        SCHEDULED = 'scheduled', _('بانتظار الموعد')
        READY = 'ready', _('جاهز للتنفيذ')
        PRINTING = 'printing', _('قيد الطباعة')
        COMPLETED = 'completed', _('مكتمل')
        FAILED = 'failed', _('فشل أو يحتاج معالجة')
        CANCELLED = 'cancelled', _('ملغى')

    order_number = models.CharField(max_length=100, unique=True, verbose_name=_("رقم أمر الطباعة"))
    exam = models.OneToOneField(
        'exams.Exam',
        on_delete=models.CASCADE,
        related_name='omr_print_order',
        verbose_name=_("الاختبار المعتمد")
    )
    scheduled_print_date = models.DateField(null=True, blank=True, verbose_name=_("تاريخ الطباعة المعتمد"))
    press_name = models.CharField(
        max_length=255, 
        default='المطبعة السرية المركزية (ديوان الوزارة)', 
        verbose_name=_("المطبعة المنفذة")
    )
    status = models.CharField(
        max_length=30, 
        choices=Status.choices, 
        default=Status.PENDING, 
        verbose_name=_("حالة الطلب")
    )
    
    return_reason = models.TextField(null=True, blank=True, verbose_name=_("سبب الإرجاع"))
    return_notes = models.TextField(null=True, blank=True, verbose_name=_("ملاحظات الإرجاع"))
    
    advance_reason = models.TextField(null=True, blank=True, verbose_name=_("سبب تقديم الموعد"))
    advance_auth_doc = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("رقم وثيقة التفويض"))

    batch_id = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("رقم دفعة الطباعة المنفذة"))
    printed_at = models.DateTimeField(null=True, blank=True, verbose_name=_("تاريخ ووقت اكتمال الطباعة"))
    reprinted_count = models.PositiveIntegerField(default=0, verbose_name=_("عدد الأوراق المعاد طباعتها"))
    responsible_officer = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("الموظف المسؤول"))

    class Meta:
        verbose_name = _('أمر طباعة OMR')
        verbose_name_plural = _('أوامر طباعة OMR')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order_number} - {self.exam.title} ({self.status})"
