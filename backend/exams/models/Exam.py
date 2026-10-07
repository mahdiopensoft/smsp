from django.db import models
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class Exam(SoftDeleteModel):
    examGenerationSetting = models.ForeignKey(
        'exams.ExamGenerationSetting', 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name=_("إعدادات التوليد")
    )
    uniqueCode = models.CharField(max_length=100, unique=True, verbose_name=_("رمز الاختبار (كود سري)"))
    title = models.CharField(max_length=255, verbose_name=_("عنوان الاختبار"))
    institution_type = models.CharField(
        max_length=20,
        choices=[('school', _('مدرسي')), ('university', _('جامعي')), ('institute', _('معاهد وتدريب مهني'))],
        default='school',
        verbose_name=_("نوع المؤسسة")
    )
    year = models.ForeignKey(
        'academic.AcademicYear', 
        on_delete=models.CASCADE, 
        verbose_name=_("السنة الدراسية")
    )
    subject = models.ForeignKey(
        'academic.Subject', 
        on_delete=models.CASCADE, 
        verbose_name=_("المادة")
    )
    examSchedule = models.ForeignKey(
        'exams.ExamSchedule', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name=_("جدول الاختبار")
    )
    country = models.ForeignKey(
        'common.Country',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("الدولة")
    )
    governorate = models.ForeignKey(
        'common.Governorate',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("المحافظة")
    )
    directorate = models.ForeignKey(
        'common.Directorate',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("المديرية")
    )
    region = models.ForeignKey(
        'common.Region',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("المنطقة")
    )

    # Advanced Generation Options
    bloom_enabled = models.BooleanField(
        default=True,
        verbose_name=_("تفعيل مستويات بلوم"),
        help_text=_("إذا كان معطلاً يتم تجاهل بلوم عند توليد الاختبار")
    )
    models_mode = models.CharField(
        max_length=20,
        choices=[
            ('uniform', _('موحّد - نفس الأسئلة')),
            ('advanced', _('متقدم - مجموعات بصعوبة مختلفة'))
        ],
        default='uniform',
        verbose_name=_("وضع النماذج")
    )
    model_groups_config = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_("إعدادات مجموعات النماذج"),
        help_text=_("يخزن مجموعات النماذج مع توزيع الصعوبة لكل مجموعة")
    )
    target_scope_level = models.CharField(
        max_length=20,
        choices=[
            ('all', _('الكل')),
            ('governorate', _('محافظات محددة')),
            ('directorate', _('مديريات محددة')),
            ('region', _('مناطق محددة')),
            ('school', _('مدارس محددة'))
        ],
        default='all',
        verbose_name=_("مستوى الاستهداف الجغرافي")
    )
    exclude_previously_used = models.BooleanField(
        default=False,
        verbose_name=_("استبعاد الأسئلة المكررة"),
        help_text=_("استبعاد الأسئلة المستخدمة في اختبارات سابقة لنفس المادة والسنة")
    )

    class Meta:
        verbose_name = _('اختبار')
        verbose_name_plural = _('الاختبارات')

    def __str__(self):
        return f"{self.title} ({self.uniqueCode})"
