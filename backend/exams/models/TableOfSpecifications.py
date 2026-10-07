from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class TableOfSpecifications(SoftDeleteModel):
    name = models.CharField(max_length=255, verbose_name=_("عنوان جدول المواصفات"))
    institution_type = models.CharField(
        max_length=20,
        choices=[('school', _('مدرسي')), ('university', _('جامعي')), ('institute', _('معاهد وتدريب مهني'))],
        default='school',
        verbose_name=_("نوع المؤسسة")
    )
    subject = models.ForeignKey(
        'academic.Subject',
        on_delete=models.CASCADE,
        related_name='specification_tables',
        verbose_name=_("المادة الدراسية")
    )
    level = models.ForeignKey(
        'academic.SchoolLevel',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='specification_tables',
        verbose_name=_("الصف / المستوى")
    )
    matrix_data = models.JSONField(
        default=list,
        verbose_name=_("مصفوفة الأوزان النسبية (الوحدات مقابل بلوم)")
    )
    total_questions_count = models.PositiveIntegerField(default=30, verbose_name=_("إجمالي عدد الأسئلة المستهدف"))
    total_marks = models.FloatField(default=100.0, verbose_name=_("إجمالي درجات الاختبار"))
    is_active = models.BooleanField(default=True, verbose_name=_("نشط"))
    
    createdBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_tos_tables',
        verbose_name=_("منشئ الجدول")
    )

    class Meta:
        verbose_name = _('جدول المواصفات')
        verbose_name_plural = _('جداول المواصفات')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - ({self.subject.name_ar if hasattr(self.subject, 'name_ar') else self.subject_id})"
