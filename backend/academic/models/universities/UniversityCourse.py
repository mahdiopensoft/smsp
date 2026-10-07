from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class UniversityCourse(BaseSyncModel):
    class CourseTypeChoices(models.TextChoices):
        UNIV_REQ = 'متطلب جامعة', _('متطلب جامعة')
        COLLEGE_REQ = 'متطلب كلية', _('متطلب كلية')
        DEPT_REQ = 'متطلب قسم', _('متطلب قسم')
        MAJOR_CORE = 'تخصص إجباري', _('تخصص إجباري')
        MAJOR_ELECTIVE = 'تخصص اختياري', _('تخصص اختياري')
        FREE_ELECTIVE = 'اختياري حر', _('اختياري حر')

    name_ar = models.CharField(max_length=200, verbose_name=_("اسم المقرر (عربي)"))
    name_en = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("اسم المقرر (إنجليزي)"))
    course_code = models.CharField(max_length=50, unique=True, db_index=True, verbose_name=_("كود المقرر الأكاديمي"))
    credit_hours = models.PositiveSmallIntegerField(
        default=3, 
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name=_("الساعات المعتمدة")
    )
    lecture_hours = models.PositiveSmallIntegerField(default=2, verbose_name=_("ساعات المحاضرة (نظري)"))
    lab_hours = models.PositiveSmallIntegerField(default=0, verbose_name=_("ساعات المعمل/العملي"))
    
    college = models.ForeignKey(
        'academic.UniversityCollege', 
        on_delete=models.CASCADE, 
        related_name='courses', 
        null=True, 
        blank=True, 
        verbose_name=_("الكلية")
    )
    department = models.ForeignKey(
        'academic.UniversityDepartment', 
        on_delete=models.SET_NULL, 
        related_name='courses', 
        null=True, 
        blank=True, 
        verbose_name=_("القسم الأكاديمي")
    )
    prerequisite_course = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='dependent_courses', 
        verbose_name=_("المتطلب السابق")
    )
    course_type = models.CharField(
        max_length=50, 
        choices=CourseTypeChoices.choices, 
        default=CourseTypeChoices.MAJOR_CORE, 
        verbose_name=_("نوع المتطلب")
    )
    description = models.TextField(null=True, blank=True, verbose_name=_("التوصيف الأكاديمي ومفردات المقرر"))
    is_active = models.BooleanField(default=True, verbose_name=_("مفعل"))

    class Meta:
        db_table = 'universities_course'
        verbose_name = _('مقرر جامعي')
        verbose_name_plural = _('المقررات الجامعية')
        ordering = ['course_code', 'id']

    def __str__(self):
        code = f"{self.course_code} - " if self.course_code else ""
        return f"{code}{self.name_ar}"
