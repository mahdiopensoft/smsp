from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class UniversitySemesterSubject(BaseSyncModel):
    fk_specialization = models.ForeignKey(
        'academic.UniversitySpecialization',
        related_name="semester_subjects",
        on_delete=models.CASCADE,
        verbose_name=_("التخصص / البرنامج الأكاديمي"),
        null=True,
        blank=True
    )
    fk_subject = models.ForeignKey(
        'academic.Subject', 
        related_name="semester_subjects", 
        on_delete=models.PROTECT, 
        verbose_name=_("المادة / المقرر (تاريخي)"),
        null=True, 
        blank=True
    )
    course = models.ForeignKey(
        'academic.UniversityCourse',
        related_name="semester_subjects",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("المقرر الجامعي")
    )
    level = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name=_("المستوى الدراسي")
    )
    semester = models.ForeignKey(
        'academic.UniversitySemester',
        related_name="semester_subjects",
        on_delete=models.PROTECT,
        verbose_name=_("الفصل الدراسي"),
        null=True,
        blank=True
    )
    fk_grading_system_june = models.ForeignKey(
        'academic.UniversityGradingSystem', 
        related_name='semestersubject_june', 
        on_delete=models.SET_NULL, 
        verbose_name=_('لنظام الدرجات للملتحقين بنظام العام'),
        null=True, 
        blank=True
    )
    fk_grading_system_october = models.ForeignKey(
        'academic.UniversityGradingSystem', 
        related_name='semestersubject_october', 
        on_delete=models.SET_NULL, 
        verbose_name=_('لنظام الدرجات للملتحقين بدور اكتوبر'),
        null=True, 
        blank=True
    )
    fk_grading_system_exempted = models.ForeignKey(
        'academic.UniversityGradingSystem',
        related_name='semestersubject_exempted',
        on_delete=models.SET_NULL,
        verbose_name=_('نظام درجات المعفيين'),
        null=True,
        blank=True
    )
    fk_grading_system_withdrawn = models.ForeignKey(
        'academic.UniversityGradingSystem',
        related_name='semestersubject_withdrawn',
        on_delete=models.SET_NULL,
        verbose_name=_('نظام درجات المنسحبين'),
        null=True,
        blank=True
    )
    number_of_hours = models.PositiveSmallIntegerField(
        default=3,
        null=True,
        blank=True,
        verbose_name=_("عدد الساعات")
    )
    is_failed = models.BooleanField(
        default=False,
        verbose_name=_("حالة الرسوب")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("نشط")
    )
    is_core_subject = models.BooleanField(
        default=True,
        verbose_name=_("مادة أساسية")
    )
    is_ministry_curriculum = models.BooleanField(
        default=False,
        verbose_name=_("منهج وزاري")
    )
    compatible_with_ministry_plan = models.BooleanField(
        default=False,
        verbose_name=_("متوافق مع الخطة الوزارية")
    )

    # Backward compatibility properties
    @property
    def added_to_total(self):
        return True

    @property
    def optional(self):
        return not self.is_core_subject

    @property
    def note(self):
        return ""

    class Meta:
        db_table = 'universities_semester_subject'
        verbose_name = _("مادة الفصل الأكاديمية الجامعية")
        verbose_name_plural = _("مواد الفصول الأكاديمية الجامعية")
        ordering = ['fk_specialization', 'level', 'semester']

    def __str__(self):
        c_name = self.course.name_ar if self.course else (self.fk_subject.name_ar if self.fk_subject else "")
        spec_name = self.fk_specialization.name_ar if self.fk_specialization else ""
        return f"{spec_name} - {c_name} (L{self.level})"

SemesterSubject = UniversitySemesterSubject
