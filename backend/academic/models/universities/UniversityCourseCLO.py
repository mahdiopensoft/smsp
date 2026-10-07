from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class UniversityCourseCLO(BaseSyncModel):
    class DomainChoices(models.TextChoices):
        KNOWLEDGE = 'معرفة وفهم', _('معرفة وفهم (Knowledge & Understanding)')
        INTELLECTUAL = 'مهارات ذهنية', _('مهارات ذهنية (Intellectual Skills)')
        PRACTICAL = 'مهارات مهنية وعملية', _('مهارات مهنية وعملية (Professional & Practical Skills)')
        TRANSFERABLE = 'مهارات عامة وانتقالية', _('مهارات عامة وانتقالية (General & Transferable Skills)')

    course = models.ForeignKey(
        'academic.UniversityCourse', 
        on_delete=models.CASCADE, 
        related_name='clos', 
        verbose_name=_("المقرر الجامعي")
    )
    topic = models.ForeignKey(
        'academic.UniversityCourseTopic', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='clos', 
        verbose_name=_("موضوع المقرر")
    )
    clo_code = models.CharField(max_length=50, verbose_name=_("رمز مخرج التعلم الأكاديمي (مثل CLO-1)"))
    description = models.TextField(verbose_name=_("نص مخرج التعلم (CLO Description)"))
    domain = models.CharField(
        max_length=50, 
        choices=DomainChoices.choices, 
        default=DomainChoices.KNOWLEDGE, 
        verbose_name=_("مجال التعلم ومعايير الاعتماد")
    )
    order = models.IntegerField(default=1, verbose_name=_("الترتيب"))
    is_active = models.BooleanField(default=True, verbose_name=_("مفعل"))

    class Meta:
        db_table = 'universities_course_clo'
        ordering = ['order', 'id']
        verbose_name = _('مخرج تعلم مقرر جامعي (CLO)')
        verbose_name_plural = _('مخرجات تعلم المقررات الجامعية (CLOs)')

    def __str__(self):
        return f"{self.course.course_code} - {self.clo_code}"

CourseCLO = UniversityCourseCLO
