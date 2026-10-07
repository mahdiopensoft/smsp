from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class UniversityGradeDistribution(BaseSyncModel):
    fk_grading_system = models.ForeignKey(
        'academic.UniversityGradingSystem', 
        related_name='type_of_grade', 
        on_delete=models.CASCADE, 
        verbose_name=_('Grading System')
    )
    fk_type_of_grade = models.ForeignKey(
        'academic.UniversityTypeOfGrade', 
        related_name='grading_system', 
        on_delete=models.CASCADE, 
        verbose_name=_('Type Of Grade')
    )
    grade = models.PositiveSmallIntegerField(verbose_name=_('Grade'))
    is_mandatory = models.BooleanField(verbose_name=_('Mandatory To Success'), default=False)
    success_percentage = models.DecimalField(
        verbose_name=_('نسبة النجاح في التوزيع'),
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        help_text=_('النسبة المئوية المطلوبة للنجاح في هذا التوزيع (مثال: 50 تعني 50%). تُستخدم فقط عند تفعيل خيار الإلزامية.')
    )
    for_attendance_grades = models.BooleanField(verbose_name=_('درجه الحضور'), default=False)
    for_attendance = models.BooleanField(verbose_name=_('اعتماد حالة الحضور والغياب'), default=False)

    def __str__(self):
        return f'{self.fk_grading_system.name_ar} - {self.fk_type_of_grade.name_ar}'

    class Meta:
        db_table = 'universities_grade_distribution'
        verbose_name = _('توزيع الدرجات الجامعي')
        verbose_name_plural = _('توزيعات الدرجات الجامعية')
        constraints = [
            models.UniqueConstraint(
                fields=['fk_type_of_grade', 'fk_grading_system'],
                name='unique_type_of_grade_grading_sys_univ_no_deleted',
                condition=Q(is_deleted=False),
            ),
        ]

GradeDistribution = UniversityGradeDistribution
