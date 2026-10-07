from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class InstituteShortCourse(BaseSyncModel):
    name_ar = models.CharField(max_length=200, verbose_name=_("اسم الدورة التدريبية (عربي)"))
    name_en = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("اسم الدورة التدريبية (إنجليزي)"))
    course_code = models.CharField(max_length=50, unique=True, verbose_name=_("رمز / كود الدورة"))
    field = models.ForeignKey(
        'academic.InstituteField',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='short_courses',
        verbose_name=_("المجال المهني / التقني")
    )
    organization = models.ForeignKey(
        'academic.Organization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='institute_short_courses',
        verbose_name=_("المعهد / المركز المنظم")
    )
    duration_weeks = models.PositiveSmallIntegerField(default=4, verbose_name=_("مدة الدورة (بالأسابيع)"))
    total_hours = models.PositiveSmallIntegerField(default=40, verbose_name=_("إجمالي عدد الساعات التدريبية"))
    training_content = models.TextField(null=True, blank=True, verbose_name=_("المحتوى والمنهج التدريبي"))
    target_audience = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("الفئة المستهدفة"))
    assessment_method = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("آلية التقييم والاجتياز"))
    certificate_type = models.CharField(max_length=150, null=True, blank=True, verbose_name=_("نوع الشهادة الممنوحة"))
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name=_("رسوم الدورة"))
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_("نشط"))

    class Meta:
        db_table = 'institutes_short_course'
        verbose_name = _("دورة تدريبية قصيرة")
        verbose_name_plural = _("الدورات التدريبية القصيرة للمعاهد")
        ordering = ['field_id', 'name_ar']

    def __str__(self):
        return f"{self.name_ar} ({self.total_hours} ساعة)"
