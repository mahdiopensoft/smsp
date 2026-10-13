from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class CurriculumExclusion(SoftDeleteModel):
    """
    نموذج المحذوفات من المنهج والمقررات الدراسية والتدريبية لكل عام دراسي.
    يحدد الدروس أو الوحدات التي يتم استبعادها بقرار وزاري أو أكاديمي
    بحيث لا تدخل في توليد ونماذج الاختبارات لذلك العام.
    """
    class InstitutionTypeChoices(models.TextChoices):
        SCHOOL = 'school', _('مدرسي')
        UNIVERSITY = 'university', _('جامعي')
        INSTITUTE = 'institute', _('معاهد وتدريب مهني')

    class ExclusionTypeChoices(models.TextChoices):
        UNIT = 'unit', _('وحدة كاملة')
        LESSON = 'lesson', _('درس محدد')

    academic_year = models.ForeignKey(
        'academic.AcademicYear',
        on_delete=models.CASCADE,
        related_name='curriculum_exclusions',
        verbose_name=_("العام الدراسي")
    )
    institution_type = models.CharField(
        max_length=20,
        choices=InstitutionTypeChoices.choices,
        default=InstitutionTypeChoices.SCHOOL,
        verbose_name=_("نوع المؤسسة التعليمية")
    )

    # 1. School Hierarchy Fields (المدارس)
    stage = models.ForeignKey(
        'academic.SchoolStage',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='curriculum_exclusions',
        verbose_name=_("المرحلة الدراسية")
    )
    class_track = models.ForeignKey(
        'academic.SchoolClassTrack',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='curriculum_exclusions',
        verbose_name=_("الصف الدراسي / المسار")
    )
    subject = models.ForeignKey(
        'academic.Subject',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='curriculum_exclusions',
        verbose_name=_("المادة الدراسية")
    )
    class_subject = models.ForeignKey(
        'academic.SchoolClassSubject',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='curriculum_exclusions',
        verbose_name=_("مادة مسار الصف")
    )

    # 2. University Hierarchy Fields (الجامعات)
    college = models.ForeignKey(
        'academic.UniversityCollege',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='curriculum_exclusions',
        verbose_name=_("الكلية")
    )
    department = models.ForeignKey(
        'academic.UniversityDepartment',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='curriculum_exclusions',
        verbose_name=_("القسم الأكاديمي")
    )
    specialization = models.ForeignKey(
        'academic.UniversitySpecialization',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='curriculum_exclusions',
        verbose_name=_("التخصص والبرنامج")
    )
    semester_subject = models.ForeignKey(
        'academic.UniversitySemesterSubject',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='curriculum_exclusions',
        verbose_name=_("مقرر الفصل الجامعي")
    )

    # 3. Institute Hierarchy Fields (المعاهد والتدريب المهني)
    institute_field = models.ForeignKey(
        'academic.InstituteField',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='curriculum_exclusions',
        verbose_name=_("المجال المهني")
    )
    institute_education_system = models.ForeignKey(
        'academic.InstituteEducationSystem',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='curriculum_exclusions',
        verbose_name=_("نظام التعليم التدريبي")
    )
    institute_specialization = models.ForeignKey(
        'academic.InstituteSpecialization',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='curriculum_exclusions',
        verbose_name=_("التخصص المهني")
    )
    institute_curriculum = models.ForeignKey(
        'academic.InstituteCurriculum',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='curriculum_exclusions',
        verbose_name=_("الخطة التدريبية")
    )
    institute_subject = models.ForeignKey(
        'academic.InstituteSubject',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='curriculum_exclusions',
        verbose_name=_("المادة التدريبية")
    )

    # Exclusion Target (نطاق الحذف)
    exclusion_type = models.CharField(
        max_length=20,
        choices=ExclusionTypeChoices.choices,
        default=ExclusionTypeChoices.LESSON,
        verbose_name=_("نطاق الحذف (وحدة / درس)")
    )
    unit = models.ForeignKey(
        'academic.Unit',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='curriculum_exclusions',
        verbose_name=_("الوحدة المستبعدة")
    )
    lesson = models.ForeignKey(
        'academic.Lesson',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='curriculum_exclusions',
        verbose_name=_("الدرس المستبعد")
    )

    # Reason & Decrees (قرار الحذف)
    reason = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name=_("مبرر / رقم قرار الحذف (تعميم وزاري)")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("مفعل")
    )

    createdBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_curriculum_exclusions',
        verbose_name=_("أنشئ بواسطة")
    )

    class Meta:
        verbose_name = _('محذوف من المنهج')
        verbose_name_plural = _('المحذوفات من المناهج')
        ordering = ['-created_at']

    def __str__(self):
        try:
            target = "غير محدد"
            if self.exclusion_type == 'unit' and self.unit:
                target = getattr(self.unit, 'name_ar', str(self.unit))
            elif self.lesson:
                target = getattr(self.lesson, 'name_ar', str(self.lesson))
            year_str = str(self.academic_year) if self.academic_year_id else ''
            disp = self.get_exclusion_type_display() if hasattr(self, 'get_exclusion_type_display') else (self.exclusion_type or '')
            return f"{disp}: {target} ({year_str})"
        except Exception:
            return f"CurriculumExclusion #{getattr(self, 'id', 'unknown')}"
