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

class Algorithms4BuildingAcademicNo(BaseIntegerChoices):
    YEAR = 1, _("السنة الدراسية")
    COLLEGE_CODE = 2, _("شفرة الكلية")
    BRANCH_CODE = 3, _("شفرة الفرع")
    SERIAL_NUMBER = 4, _("ارقم تسلسلية")
    BATCH_NUMBER = 5, _("رقم الدفعة")

class NumberingSystemChoice(BaseIntegerChoices):
    ACADEMIC_NO = 1, _("بالرقم الاكاديمي")
    NAME = 2, _("بالاسم")
    RANDOM = 3, _("عشوائي")

class LevelChoice(BaseIntegerChoices):
    LEVEL_1 = 1, _("المستوى الاول")
    LEVEL_2 = 2, _("المستوى الثاني")
    LEVEL_3 = 3, _("المستوى الثالث")
    LEVEL_4 = 4, _("المستوى الرابع")
    LEVEL_5 = 5, _("المستوى الخامس")
    LEVEL_6 = 6, _("المستوى السادس")
    LEVEL_7 = 7, _("المستوى السابع")

class SemesterChoice(BaseIntegerChoices):
    SEM_1 = 1, _("الفصل الأول")
    SEM_2 = 2, _("الفصل الثاني")
    SEM_3 = 3, _("الفصل الثالث")
    SEM_4 = 4, _("الفصل الرابع")
    SEM_5 = 5, _("الفصل الخامس")
    SEM_6 = 6, _("الفصل السادس")
    SEM_7 = 7, _("الفصل السابع")
    SEM_8 = 8, _("الفصل الثامن")
    SEM_9 = 9, _("الفصل التاسع")
    SEM_10 = 10, _("الفصل العاشر")
    SEM_11 = 11, _("الفصل الحادي عشر")
    SEM_12 = 12, _("الفصل الثاني عشر")

class GradeSystemTypeChoices(BaseIntegerChoices):
    JUNE = 1, _("يونيو")
    OCTOBER = 2, _("اكتوبر")
    EXEMPTED = 3, _("معفيين")
    WITHDRAWN = 4, _("المتنازلين")

class NumberOfSemesterEachLevelChoices(BaseIntegerChoices):
    ONE_SEMESTER = 1, _("فصل")
    TWO_SEMESTERS = 2, _("فصلين")
    THREE_SEMESTERS = 3, _("3 فصول")
    FOUR_SEMESTERS = 4, _("4 فصول")

class NumberOfLevelsChoices(BaseIntegerChoices):
    ONE_LEVEL = 1, _("مستوى واحد")
    TWO_LEVELS = 2, _("مستويين")
    THREE_LEVELS = 3, _("ثلاثة مستويات")
    FOUR_LEVELS = 4, _("أربعة مستويات")
    FIVE_LEVELS = 5, _("خمسة مستويات")
    SIX_LEVELS = 6, _("ستة مستويات")
    SEVEN_LEVELS = 7, _("سبعة مستويات")
    EIGHT_LEVELS = 8, _("ثمان مستويات")

class DegreeChoice(BaseIntegerChoices):
    BACHELOR = 1, _('بكالوريوس')
    MASTERS = 2, _('ماجستير')
    DOCTORATE = 3, _('دكتوراه')
    DIPLOMA = 4, _('دبلوم')

class EducationalLevelChoice(BaseIntegerChoices):
    SECONDARY = 1, _("الثانوية وما يعادلها")
    HIGHER_EDUCATION = 2, _("تعليم عالي")
    OTHER = 3, _("أخرى")

class StudyTypeChoice(BaseIntegerChoices):
    GENERAL = 1, _('النظام العام')
    PARALLEL = 2, _('النظام الموازي')
    PRIVATE_EXPENSE = 3, _('النفقة الخاصة')
    UNDEFINED = 4, _('غير محدد')
    POSTGRADUATE = 19, _('الدراسات العليا')
