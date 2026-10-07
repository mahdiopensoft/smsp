from django.db import models
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class ExamDistribution(SoftDeleteModel):
    """
    نموذج توزيع وتصدير الاختبارات المجدول للمدارس والجامعات المستقلة
    """
    class TargetLevel(models.TextChoices):
        MINISTRY = 'ministry', _('الوزارة (شامل لكافة المدارس)')
        GOVERNORATE = 'governorate', _('محافظة / محافظات محددة')
        DIRECTORATE = 'directorate', _('مديرية / مديريات محددة')
        SCHOOL = 'school', _('مدارس محددة')
        UNIVERSITY = 'university', _('جامعة / كليات محددة')

    class TargetSystem(models.TextChoices):
        SCHOOL = 'school', _('نظام المدارس (SMS)')
        UNIVERSITY = 'university', _('نظام الجامعات (UMS)')

    class DeliveryMode(models.TextChoices):
        PRINTED_OMR = 'printed_omr', _('طباعة كراسات + أوراق إجابة OMR')
        CBT_ONLINE = 'cbt_online', _('اختبار إلكتروني عبر الشاشات')
        HYBRID = 'hybrid', _('مزدوج (ورقي وإلكتروني)')

    class Status(models.TextChoices):
        DRAFT = 'draft', _('مسودة')
        SCHEDULED = 'scheduled', _('مجدول')
        DISPATCHED = 'dispatched', _('تم الإرسال للأنظمة')
        ACCESSIBLE = 'accessible', _('متاح للطباعة بالمدارس')
        IN_PROGRESS = 'in_progress', _('الاختبار جاري حالياً')
        COMPLETED = 'completed', _('مكتمل ومنتهي')
        CANCELLED = 'cancelled', _('ملغي')

    exam = models.ForeignKey(
        'exams.Exam', 
        on_delete=models.CASCADE, 
        related_name='distributions', 
        verbose_name=_("الاختبار المعتمد")
    )
    title = models.CharField(max_length=255, verbose_name=_("عنوان مهمة التوزيع"))
    target_level = models.CharField(
        max_length=20, 
        choices=TargetLevel.choices, 
        default=TargetLevel.SCHOOL,
        verbose_name=_("مستوى الاستهداف الهرمي")
    )
    target_system = models.CharField(
        max_length=20, 
        choices=TargetSystem.choices, 
        default=TargetSystem.SCHOOL,
        verbose_name=_("النظام المستهدف")
    )
    delivery_mode = models.CharField(
        max_length=30,
        choices=DeliveryMode.choices,
        default=DeliveryMode.PRINTED_OMR,
        verbose_name=_("نمط التنفيذ والتسليم")
    )

    # المنظمات/المدارس المستهدفة في الشجرة الهرمية
    organizations = models.ManyToManyField(
        'common.Organization',
        blank=True,
        related_name='targeted_exam_distributions',
        verbose_name=_("المدارس / الكيانات المستهدفة")
    )

    # النوافذ الزمنية للجدولة
    dispatch_at = models.DateTimeField(verbose_name=_("وقت إرسال وتوفر الحزمة للأنظمة الفرعية"))
    accessible_from = models.DateTimeField(verbose_name=_("وقت إتاحة محتوى الأسئلة للطباعة بالمدرسة"))
    exam_start_at = models.DateTimeField(verbose_name=_("وقت بدء الامتحان الرسمي للطلاب"))
    exam_end_at = models.DateTimeField(verbose_name=_("وقت انتهاء الامتحان الرسمي وقفل التسليم"))

    # خيارات السرية والأمان ومنع التسريب
    is_encrypted = models.BooleanField(
        default=True, 
        verbose_name=_("تشفير محتوى الأسئلة حتى موعد الإتاحة لمنع التسريب")
    )
    auto_unlock = models.BooleanField(
        default=True, 
        verbose_name=_("فتح الأسئلة تلقائياً بمجرد حلول وقت الإتاحة")
    )
    encryption_key = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        verbose_name=_("مفتاح فك التشفير / كود الإفراج")
    )

    status = models.CharField(
        max_length=30, 
        choices=Status.choices, 
        default=Status.SCHEDULED, 
        verbose_name=_("حالة مهمة التوزيع")
    )
    notes = models.TextField(null=True, blank=True, verbose_name=_("ملاحظات وتعليمات للمدارس"))

    class Meta:
        verbose_name = _('توزيع اختبار مجدول')
        verbose_name_plural = _('توزيعات الاختبارات المجدولة')
        ordering = ['-dispatch_at']

    def __str__(self):
        return f"{self.title} - ({self.exam.title})"
