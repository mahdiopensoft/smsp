from django.db import models
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class ExamSchoolDispatchStatus(SoftDeleteModel):
    """
    سجل متابعة وصول وحالة تنفيذ الاختبار في كل مدرسة مستهدفة
    """
    distribution = models.ForeignKey(
        'exams.ExamDistribution',
        on_delete=models.CASCADE,
        related_name='school_statuses',
        verbose_name=_("مهمة التوزيع")
    )
    school = models.ForeignKey(
        'common.Organization',
        on_delete=models.CASCADE,
        related_name='exam_dispatch_statuses',
        verbose_name=_("المدرسة المستهدفة")
    )

    # حالة الاستلام في نظام المدرسة الفرعي (SMS)
    is_received = models.BooleanField(default=False, verbose_name=_("تم الاستلام في نظام المدرسة"))
    received_at = models.DateTimeField(null=True, blank=True, verbose_name=_("تاريخ ووقت الاستلام"))

    # حالة فك التشفير والإتاحة للطباعة
    is_accessible = models.BooleanField(default=False, verbose_name=_("أصبحت الأسئلة متاحة للطباعة"))
    accessible_at = models.DateTimeField(null=True, blank=True, verbose_name=_("وقت إتاحة الأسئلة"))

    # إحصائيات الطباعة والتنفيذ الميداني بالمدرسة
    printed_booklets_count = models.PositiveIntegerField(default=0, verbose_name=_("عدد كراسات الأسئلة المطبوعة"))
    printed_sheets_count = models.PositiveIntegerField(default=0, verbose_name=_("عدد أوراق إجابة OMR المطبوعة"))
    students_attended_count = models.PositiveIntegerField(default=0, verbose_name=_("عدد الطلاب الذين أدوا الاختبار"))

    # إعادة رفع النتائج للبنك المركزي
    results_synced_back = models.BooleanField(default=False, verbose_name=_("تمت إعادة رفع النتائج للبنك المركزي"))
    synced_back_at = models.DateTimeField(null=True, blank=True, verbose_name=_("تاريخ ووقت رفع النتائج"))
    
    error_message = models.TextField(null=True, blank=True, verbose_name=_("رسالة خطأ في المزامنة إن وجدت"))

    class Meta:
        verbose_name = _('حالة تسليم الاختبار للمدرسة')
        verbose_name_plural = _('حالات تسليم الاختبارات للمدارس')
        unique_together = [('distribution', 'school')]
        ordering = ['school__name_ar']

    def __str__(self):
        status_txt = "مستلم" if self.is_received else "بانتظار المزامنة"
        return f"{self.school.name_ar} - {self.distribution.title} [{status_txt}]"
