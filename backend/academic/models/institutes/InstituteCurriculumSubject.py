from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel
from academic.choices.institute_choices import InstituteSubjectEntityChoices

class InstituteCurriculumSubject(BaseSyncModel):
    curriculum = models.ForeignKey(
        'academic.InstituteCurriculum',
        on_delete=models.CASCADE,
        related_name='curriculum_subjects',
        verbose_name=_("الخطة الدراسية")
    )
    subject = models.ForeignKey(
        'academic.InstituteSubject',
        on_delete=models.PROTECT,
        related_name='curriculum_subjects',
        verbose_name=_("المادة الدراسية")
    )
    level = models.ForeignKey(
        'academic.InstituteLevel',
        on_delete=models.PROTECT,
        related_name='curriculum_subjects',
        verbose_name=_("المستوى الدراسي")
    )
    semester = models.ForeignKey(
        'academic.InstituteSemester',
        on_delete=models.PROTECT,
        related_name='curriculum_subjects',
        verbose_name=_("الفصل الدراسي")
    )
    is_ministerial_exam = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name=_("خاضعة للاختبار الوزاري النهائي")
    )
    exam_entity = models.CharField(
        max_length=30,
        choices=InstituteSubjectEntityChoices.choices,
        default=InstituteSubjectEntityChoices.INSTITUTIONAL,
        verbose_name=_("جهة عقد الاختبار (وزاري / مؤسسي)")
    )
    max_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=100.0,
        verbose_name=_("الدرجة العظمى")
    )
    min_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=50.0,
        verbose_name=_("درجة النجاح (الصغرى)")
    )
    added_to_total = models.BooleanField(
        default=True,
        verbose_name=_("تدخل في احتساب المجموع والمعدل")
    )
    order = models.PositiveSmallIntegerField(
        default=1,
        verbose_name=_("ترتيب المادة في الخطة")
    )
    note = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("ملاحظات")
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name=_("نشط")
    )

    class Meta:
        db_table = 'institutes_curriculum_subject'
        verbose_name = _("مقرر الخطة الدراسية للمعهد")
        verbose_name_plural = _("مقررات الخطط الدراسية للمعاهد")
        ordering = ['curriculum_id', 'level__order', 'semester__order', 'order']
        constraints = [
            models.UniqueConstraint(
                fields=['curriculum', 'subject', 'level', 'semester'],
                name='unique_institute_curriculum_subject'
            )
        ]

    def __str__(self):
        c_name = self.curriculum.name_ar if self.curriculum else ""
        s_name = self.subject.name_ar if self.subject else ""
        return f"{c_name} - {s_name}"
