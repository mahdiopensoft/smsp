from django.utils.translation import gettext_lazy as _
from .common_choices import BaseIntegerChoices, BaseTextChoices

class InstituteEducationSystemTypeChoices(BaseTextChoices):
    VOCATIONAL_DIPLOMA_PREP = 'vocational_prep', _('دبلوم مهني بعد الإعدادية')
    VOCATIONAL_DIPLOMA_SEC = 'vocational_sec', _('دبلوم مهني بعد الثانوية')
    TECHNICAL_DIPLOMA_2Y = 'technical_2y', _('دبلوم تقني سنتين')
    TECHNICAL_DIPLOMA_3Y = 'technical_3y', _('دبلوم تقني 3 سنوات')
    COMPLEMENTARY_DIPLOMA = 'complementary', _('دبلوم تقني تكميلي')
    PROFESSIONAL_ACCREDITATION = 'accreditation', _('تحقيق المهنة')

class InstituteStudyNatureChoices(BaseTextChoices):
    PRACTICAL_VOCATIONAL = 'practical', _('مهني / عملي')
    TECHNICAL_THEORETICAL = 'technical', _('تقني / نظري')
    INTEGRATED = 'integrated', _('مشترك (نظري وعملي)')

class InstituteSubjectTypeChoices(BaseTextChoices):
    THEORETICAL = 'theoretical', _('مادة نظرية')
    PRACTICAL = 'practical', _('مادة عملية')
    MIXED = 'mixed', _('نظري وعملي')

class InstituteSubjectEntityChoices(BaseTextChoices):
    MINISTERIAL = 'ministerial', _('مادة وزارية')
    INSTITUTIONAL = 'institutional', _('مادة تابعة للمؤسسة / المعهد')

class InstituteSubjectAcademicCategoryChoices(BaseTextChoices):
    SPECIALIZED = 'specialized', _('مادة تخصصية')
    SUPPORTIVE = 'supportive', _('مادة مساعدة')
    GENERAL_CULTURAL = 'cultural', _('مادة ثقافية / عامة')

class InstituteSemesterNatureChoices(BaseTextChoices):
    REGULAR = 'regular', _('فصل دراسي اعتيادي')
    FINAL_MINISTERIAL = 'final_ministerial', _('فصل دراسي نهائي (وزاري)')

class InstituteGradingCalculationChoices(BaseTextChoices):
    CUMULATIVE_AND_MINISTERIAL = 'cumulative_ministerial', _('مجموع ومعدل تراكمي عام + وزاري خاص')
    GENERAL_TOTAL_AND_MINISTERIAL_GPA = 'general_total_ministerial', _('المجموع العام فقط + المعدل الوزاري الخاص')
    CERTIFICATE_OF_COMPETENCE = 'competence_only', _('شهادة كفاءة واجتياز فقط')
