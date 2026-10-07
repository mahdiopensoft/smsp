from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class Question(SoftDeleteModel):
    class DifficultyChoices(models.IntegerChoices):
        EASY = 1, _('سهل')
        MEDIUM = 2, _('متوسط')
        HARD = 3, _('صعب')

    class BloomChoices(models.TextChoices):
        REMEMBER = 'تذكر', _('تذكر')
        UNDERSTAND = 'فهم', _('فهم')
        APPLY = 'تطبيق', _('تطبيق')
        ANALYZE = 'تحليل', _('تحليل')
        EVALUATE = 'تقييم', _('تقييم')
        CREATE = 'ابتكار', _('ابتكار')

    class TypeChoices(models.TextChoices):
        SINGLE_CHOICE = 'Single Choice', _('اختيار واحد')
        MULTIPLE_CHOICE = 'Multiple Choice', _('اختيار من متعدد')
        TRUE_FALSE = 'True/False', _('صح وخطأ')
        ESSAY = 'Essay', _('مقالي')
        FILL_BLANK = 'Fill in the Blanks', _('إكمال الفراغ')
        MATCHING = 'Matching', _('مطابقة')
        ORDERING = 'Ordering', _('ترتيب')
        CASE_STUDY = 'Case Study', _('دراسة حالة')

    class StatusChoices(models.TextChoices):
        IMPORTED = 'مستورد', _('مستورد')
        DRAFT = 'مسودة', _('مسودة')
        PENDING = 'قيد المراجعة', _('قيد المراجعة')
        DEPT_HEAD_REVIEW = 'قيد مراجعة رئيس القسم', _('قيد مراجعة رئيس القسم')
        APPROVED = 'معتمد', _('معتمد')
        REJECTED = 'مرفوض', _('مرفوض')
        ARCHIVED = 'مؤرشف', _('مؤرشف')
        DISABLED = 'معطل', _('معطل')

    content = models.TextField(verbose_name=_("نص السؤال (HTML)"))
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("وصف/فكرة السؤال"))
    lesson = models.ForeignKey(
        'academic.Lesson', 
        on_delete=models.CASCADE, 
        related_name='questions', 
        verbose_name=_("الدرس"), 
        null=True, 
        blank=True
    )
    import_session = models.ForeignKey(
        'bank.ImportSession', 
        on_delete=models.CASCADE, 
        related_name='questions', 
        verbose_name=_("جلسة الاستيراد"), 
        null=True, 
        blank=True
    )
    learningOutcome = models.ForeignKey(
        'academic.LearningOutcome', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='questions', 
        verbose_name=_("مخرج التعلم")
    )
    
    difficulty = models.IntegerField(choices=DifficultyChoices.choices, default=DifficultyChoices.EASY, verbose_name=_("مستوى الصعوبة"))
    bloomLevel = models.CharField(max_length=50, choices=BloomChoices.choices, default=BloomChoices.REMEMBER, verbose_name=_("مستوى بلوم"))
    questionType = models.CharField(max_length=50, choices=TypeChoices.choices, default=TypeChoices.SINGLE_CHOICE, verbose_name=_("نوع السؤال"))
    
    isTrue = models.BooleanField(null=True, blank=True, verbose_name=_("حالة سؤال الصح والخطأ"))
    answerText = models.TextField(null=True, blank=True, verbose_name=_("النص المرجعي للإجابة"))
    
    status = models.CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.DRAFT, verbose_name=_("حالة السؤال"))
    rejectionReason = models.TextField(null=True, blank=True, verbose_name=_("سبب الرفض"))
    defaultMark = models.FloatField(default=1.0, verbose_name=_("الدرجة الافتراضية"))
    expected_time_minutes = models.IntegerField(default=1, verbose_name=_("الزمن المتوقع للحل (بالدقائق)"))
    image = models.ImageField(upload_to='questions_images/', null=True, blank=True, verbose_name=_("صورة توضيحية"))
    
    version_number = models.PositiveIntegerField(default=1, verbose_name=_("رقم الإصدار"))
    parent_version = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='versions', 
        verbose_name=_("الإصدار الأب")
    )
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name=_("تاريخ الاعتماد"))
    institution_type = models.CharField(
        max_length=20, 
        choices=[
            ('school', 'مدرسة'),
            ('university', 'جامعة'),
            ('institute', 'معهد / تدريب مهني')
        ], 
        default='school', 
        verbose_name=_("نوع المؤسسة (مدرسي / جامعي / معهد)")
    )
    assessment_type = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("نوع التقييم (جامعات)"))

    createdBy = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='created_questions', 
        verbose_name=_("منشئ السؤال")
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='reviewed_questions', 
        verbose_name=_("المراجع")
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('سؤال')
        verbose_name_plural = _('الأسئلة')

    def __str__(self):
        import re
        clean_text = re.sub('<[^<]+?>', '', self.content) if self.content else ''
        return clean_text[:50] + ('...' if len(clean_text) > 50 else '')
