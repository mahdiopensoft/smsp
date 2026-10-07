from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class UniversityCourseTopic(BaseSyncModel):
    course = models.ForeignKey(
        'academic.UniversityCourse', 
        on_delete=models.CASCADE, 
        related_name='topics', 
        verbose_name=_("المقرر الجامعي")
    )
    semester_subject = models.ForeignKey(
        'academic.UniversitySemesterSubject', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='course_topics', 
        verbose_name=_("مقرر الفصل والتخصص")
    )
    name_ar = models.CharField(max_length=255, verbose_name=_("عنوان الموضوع / الوحدة (عربي)"))
    name_en = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("عنوان الموضوع / الوحدة (إنجليزي)"))
    week_number = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_("الأسبوع الدراسي في الخطة"))
    order = models.IntegerField(default=1, verbose_name=_("الترتيب"))
    description = models.TextField(null=True, blank=True, verbose_name=_("المفردات والتفاصيل الأكاديمية"))
    is_active = models.BooleanField(default=True, verbose_name=_("مفعل"))

    class Meta:
        db_table = 'universities_course_topic'
        ordering = ['week_number', 'order', 'id']
        verbose_name = _('موضوع/مفردة مقرر جامعي')
        verbose_name_plural = _('موضوعات ومفردات المقررات الجامعية')

    def __str__(self):
        return f"{self.course.course_code} - {self.name_ar}"

CourseTopic = UniversityCourseTopic
