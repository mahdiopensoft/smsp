from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class UniversityCollegeSettings(BaseSyncModel):
    fk_college = models.ForeignKey(
        'academic.UniversityCollege', 
        related_name='college_settings', 
        on_delete=models.CASCADE, 
        verbose_name=_('College Settings')
    )
    use_grade_improvement = models.BooleanField(default=False, verbose_name=_("استخدام تحسين التقدير"))
    use_pass_improvement = models.BooleanField(default=False, verbose_name=_("استخدام تحسين التنجيح"))
    include_grade_improvement_in_gpa = models.BooleanField(default=False, verbose_name=_("احتساب تحسين التقدير في المعدل"))
    include_pass_improvement_in_gpa = models.BooleanField(default=False, verbose_name=_("احتساب تحسين التنجيح في المعدل"))
    use_postgraduate_grade_improvement = models.BooleanField(default=False, verbose_name=_("استخدام تحسين التقدير للدراسات العليا"))
    use_postgraduate_pass_improvement = models.BooleanField(default=False, verbose_name=_("استخدام تحسين التقدير للدراسات العليا"))
    include_postgraduate_grade_improvement_in_gpa = models.BooleanField(default=False, verbose_name=_("احتساب تحسين التقدير في المعدل للدراسات العليا"))
    include_postgraduate_pass_improvement_in_gpa = models.BooleanField(default=False, verbose_name=_("احتساب تحسين التنجيح في المعدل للدراسات العليا"))
    show_student_photo = models.BooleanField(default=False, verbose_name=_("اظهار صورة الطالب في صفحات النظام"))
    allow_repeat_students_to_improve_grade = models.BooleanField(default=False, verbose_name=_("السماح للطلاب الباقيين للاعادة باعادة مواد المقبول لتحسين التقدير"))
    use_block_system = models.BooleanField(default=False, verbose_name=_("استخدام نظام البلك"))
    allow_move_to_other_block_with_fail = models.BooleanField(default=False, verbose_name=_("الانتقال لبلك اخر مع مادة رسوب"))
    allow_move_to_upper_level_with_block_fail = models.BooleanField(default=False, verbose_name=_("انتقال الطالب لمستوى اعلى مع بلك رسوب"))
    allow_individual_repeat_assignment = models.BooleanField(default=False, verbose_name=_("السماح بتعيين الاعادة من ملف الطالب بشكل فردي"))
    show_subject_parts_in_student_portal = models.BooleanField(default=False, verbose_name=_("عرض اجزاء المواد في بوابة الطلاب"))
    enable_student_to_select_next_track = models.BooleanField(default=False, verbose_name=_("في حالة وجود مسار - تمكين الطالب من اختيار مسار التخصص التالي في البوابة"))
    is_current_year = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_("العام الجامعي الحالي"))
    record_of_page = models.PositiveSmallIntegerField(default=10, verbose_name=_("عدد سجلات الصفحة"))
    email_of_service_in_university = models.EmailField(blank=True, null=True, verbose_name=_("ايميل الخدمة في الجامعة"))
    copy_of_emails_to = models.EmailField(blank=True, null=True, verbose_name=_("نسخة من الإيميلات إالى"))
    excused_mark = models.FloatField(default=0, verbose_name=_("درجة المستاذن"))
    absent_mark = models.FloatField(default=0, verbose_name=_("درجة الغائب"))
    exempt_mark = models.FloatField(default=0, verbose_name=_("درجة المعفي في الحضور"))
    announcement_of_final_exam_results = models.BooleanField(default=False, verbose_name=_("اعلان نتائج الاختبارات"))

    def __str__(self):
        return f"{self.fk_college.name_ar}"

    class Meta:
        db_table = 'universities_college_settings'
        verbose_name = _('إعدادات الكلية الجامعية')
        verbose_name_plural = _('إعدادات الكليات الجامعية')

CollegeSettings = UniversityCollegeSettings
