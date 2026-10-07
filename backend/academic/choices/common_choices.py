from django.db import models
from django.utils.translation import gettext_lazy as _

class BaseIntegerChoices(models.IntegerChoices):
    @classmethod
    def get_value(cls, label):
        for item in cls.choices:
            if item[1] == label:
                return item[0]
        return None

class BaseTextChoices(models.TextChoices):
    @classmethod
    def get_value(cls, label):
        for item in cls.choices:
            if item[1] == label:
                return item[0]
        return None

class InstitutionTypeChoice(BaseTextChoices):
    SCHOOL = 'school', _('مدرسة / تعليم عام')
    UNIVERSITY = 'university', _('جامعة / تعليم أكاديمي')
    INSTITUTE = 'institute', _('معهد / تدريب مهني وفني')

class GenderChoice(BaseIntegerChoices):
    MALE = 1, _('ذكر')
    FEMALE = 2, _('أنثى')
    COED = 3, _('مختلط')

class ActiveStatusChoice(BaseIntegerChoices):
    INACTIVE = 0, _('غير نشط')
    ACTIVE = 1, _('نشط')
