from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class InstituteSpecialTrack(BaseSyncModel):
    name_ar = models.CharField(max_length=200, verbose_name=_("اسم البرنامج / المسار الخاص (عربي)"))
    name_en = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("اسم البرنامج / المسار الخاص (إنجليزي)"))
    track_code = models.CharField(max_length=50, unique=True, verbose_name=_("رمز المسار"))
    field = models.ForeignKey(
        'academic.InstituteField',
        on_delete=models.CASCADE,
        related_name='special_tracks',
        verbose_name=_("المجال المهني / التقني")
    )
    education_system = models.ForeignKey(
        'academic.InstituteEducationSystem',
        on_delete=models.CASCADE,
        related_name='special_tracks',
        verbose_name=_("نظام التعليم (تحقيق المهنة / إثبات الكفاءة)")
    )
    target_profession = models.CharField(max_length=200, verbose_name=_("المهنة / التخصص المستهدف"))
    admission_prerequisites = models.TextField(null=True, blank=True, verbose_name=_("متطلبات وشروط المتقدمين والخبرات السابقة"))
    evaluation_mechanism = models.TextField(null=True, blank=True, verbose_name=_("آلية ومعايير الاختبار التقييمي"))
    has_theoretical_exam = models.BooleanField(default=True, verbose_name=_("يتضمن اختباراً نظرياً"))
    has_practical_exam = models.BooleanField(default=True, verbose_name=_("يتضمن اختباراً عملياً"))
    passing_score = models.DecimalField(max_digits=5, decimal_places=2, default=60.0, verbose_name=_("درجة الاجتياز"))
    certificate_name = models.CharField(
        max_length=200,
        default="شهادة تحقيق مهنة / إثبات كفاءة",
        verbose_name=_("مسمى الشهادة الممنوحة")
    )
    note = models.TextField(null=True, blank=True, verbose_name=_("ملاحظات إضافية"))
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_("نشط"))

    class Meta:
        db_table = 'institutes_special_track'
        verbose_name = _("مؤهل مسار خاص / تحقيق مهنة")
        verbose_name_plural = _("مؤهلات المسارات الخاصة وتحقيق المهنة")
        ordering = ['field_id', 'name_ar']

    def __str__(self):
        return f"{self.name_ar} ({self.target_profession})"
