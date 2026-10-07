from django.db import models
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class MatchingPair(SoftDeleteModel):
    question = models.ForeignKey(
        'bank.Question',
        on_delete=models.CASCADE,
        related_name='matching_pairs',
        verbose_name=_("السؤال")
    )
    left_text = models.CharField(max_length=500, verbose_name=_("عنصر العمود الأيمن"))
    left_image = models.ImageField(upload_to='matching_images/', null=True, blank=True, verbose_name=_("صورة العمود الأيمن"))
    right_text = models.CharField(max_length=500, verbose_name=_("عنصر العمود الأيسر (المطابق)"))
    right_image = models.ImageField(upload_to='matching_images/', null=True, blank=True, verbose_name=_("صورة العمود الأيسر"))
    order = models.PositiveIntegerField(default=1, verbose_name=_("الترتيب"))

    class Meta:
        verbose_name = _('زوج مطابقة')
        verbose_name_plural = _('أزواج المطابقة')
        ordering = ['order']

    def __str__(self):
        return f"{self.left_text} ➔ {self.right_text}"


class OrderingItem(SoftDeleteModel):
    question = models.ForeignKey(
        'bank.Question',
        on_delete=models.CASCADE,
        related_name='ordering_items',
        verbose_name=_("السؤال")
    )
    text = models.CharField(max_length=500, verbose_name=_("نص العنصر"))
    image = models.ImageField(upload_to='ordering_images/', null=True, blank=True, verbose_name=_("صورة العنصر"))
    correct_position = models.PositiveIntegerField(verbose_name=_("الموضع الصحيح في الترتيب"))

    class Meta:
        verbose_name = _('عنصر ترتيب')
        verbose_name_plural = _('عناصر الترتيب')
        ordering = ['correct_position']

    def __str__(self):
        return f"Pos {self.correct_position}: {self.text}"


class BlankAnswer(SoftDeleteModel):
    question = models.ForeignKey(
        'bank.Question',
        on_delete=models.CASCADE,
        related_name='blank_answers',
        verbose_name=_("السؤال")
    )
    blank_index = models.PositiveIntegerField(default=1, verbose_name=_("رقم الفراغ في النص"))
    accepted_answers = models.JSONField(default=list, verbose_name=_("قائمة الإجابات المقبولة"))
    is_case_sensitive = models.BooleanField(default=False, verbose_name=_("حساسية حالة الأحرف"))

    class Meta:
        verbose_name = _('إجابة فراغ')
        verbose_name_plural = _('إجابات الفراغات')
        ordering = ['blank_index']

    def __str__(self):
        return f"Blank #{self.blank_index}: {self.accepted_answers}"


class CaseStudySubQuestion(SoftDeleteModel):
    parent_question = models.ForeignKey(
        'bank.Question',
        on_delete=models.CASCADE,
        related_name='case_study_sub_questions',
        verbose_name=_("سؤال دراسة الحالة الرئيسي")
    )
    sub_question = models.ForeignKey(
        'bank.Question',
        on_delete=models.CASCADE,
        related_name='case_study_parent_link',
        verbose_name=_("السؤال الفرعي")
    )
    order = models.PositiveIntegerField(default=1, verbose_name=_("ترتيب السؤال الفرعي"))
    sub_mark = models.FloatField(default=1.0, verbose_name=_("درجة السؤال الفرعي"))

    class Meta:
        verbose_name = _('سؤال فرعي لدراسة الحالة')
        verbose_name_plural = _('أسئلة فرعية لدراسات الحالة')
        ordering = ['order']

    def __str__(self):
        return f"SubQuestion #{self.sub_question_id} for Case #{self.parent_question_id}"
