from django.utils.translation import gettext_lazy as _
from .common_choices import BaseIntegerChoices, BaseTextChoices

class SchoolStageChoice(BaseIntegerChoices):
    PRIMARY = 1, _('المرحلة الابتدائية')
    INTERMEDIATE = 2, _('المرحلة الإعدادية / المتوسطة')
    SECONDARY = 3, _('المرحلة الثانوية')

class SchoolTermChoice(BaseIntegerChoices):
    FIRST_TERM = 1, _('الفصل الدراسي الأول')
    SECOND_TERM = 2, _('الفصل الدراسي الثاني')
    SUMMER_TERM = 3, _('الفصل الصيفي')

class SchoolSectionGenderChoice(BaseIntegerChoices):
    BOYS = 1, _('بنين')
    GIRLS = 2, _('بنات')
    MIXED = 3, _('مختلط')
