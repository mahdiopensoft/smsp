from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class StudentExamRegistration(SoftDeleteModel):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='exam_registrations',
        verbose_name=_("حساب الطالب")
    )
    student_profile = models.ForeignKey(
        'academic.Student', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='exam_registrations', 
        verbose_name=_("سجل الطالب الأكاديمي")
    )
    examVersion = models.ForeignKey(
        'exams.ExamVersion', 
        on_delete=models.CASCADE, 
        related_name='registered_students',
        verbose_name=_("نموذج الاختبار")
    )
    seatNumber = models.CharField(max_length=50, verbose_name=_("رقم الجلوس في هذا الاختبار"))
    secretNumber = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("الرقم السري"))
    isPresent = models.BooleanField(default=False, verbose_name=_("حاضر؟"))
    
    # ── Print Registry Tracking (سجل الطباعة) ──
    is_printed = models.BooleanField(default=False, verbose_name=_("تمت طباعة الورقة؟"))
    printed_at = models.DateTimeField(null=True, blank=True, verbose_name=_("تاريخ ووقت الطباعة"))
    print_batch = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("دفعة الطباعة"))

    class Meta:
        unique_together = ('student', 'examVersion')
        verbose_name = _('تسجيل طالب في اختبار')
        verbose_name_plural = _('تسجيلات الطلاب في الاختبارات')
        
    def __str__(self):
        return f"{self.student} - {self.examVersion} (Seat: {self.seatNumber})"
