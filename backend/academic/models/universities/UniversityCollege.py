from django.db import models
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class UniversityCollege(BaseSyncModel):
    name_ar = models.CharField(max_length=100, verbose_name=_('Name (Arabic)'))
    name_en = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Name (English)'))
    college_no = models.PositiveSmallIntegerField(
        verbose_name=_('College Number'), 
        validators=[MinValueValidator(1), MaxValueValidator(99)]
    )
    highest_level = models.PositiveSmallIntegerField(
        verbose_name=_('اعلى مستوى في الكلية'), 
        blank=True, 
        null=True, 
        validators=[MinValueValidator(1), MaxValueValidator(99)]
    )
    first_year = models.IntegerField(
        verbose_name=_('عام البداية'), 
        default=2000
    )
    is_active = models.BooleanField(verbose_name=_('تمكين العمل على الكلية'), default=True)
    has_general_specialization = models.BooleanField(verbose_name=_('يملك تخصص عام'), default=False)
    fee = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        verbose_name=_('Fee'), 
        validators=[MinValueValidator(1), MaxValueValidator(9999999999)]
    )

    def __str__(self):
        return self.name_ar

    class Meta:
        db_table = 'universities_college'
        verbose_name = _('الكلية الجامعية')
        verbose_name_plural = _('الكليات الجامعية')
        constraints = [
            models.UniqueConstraint(
                fields=['name_ar'],
                name='unique_name_ar_univ_college_no_deleted',
                condition=Q(is_deleted=False),
            ),
            models.UniqueConstraint(
                fields=['college_no'],
                name='unique_univ_college_no_no_deleted',
                condition=Q(is_deleted=False),
            )
        ]

College = UniversityCollege
