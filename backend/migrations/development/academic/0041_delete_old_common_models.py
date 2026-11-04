# Generated manually for safe modular academic refactoring

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0040_universityexamperiod_universitylesson_universityunit_and_more'),
        ('bank', '0010_alter_question_lesson'),
        ('exams', '0015_alter_curriculumexclusion_lesson_and_more'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AlterField(
                    model_name='schoolclasssubject',
                    name='subject',
                    field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='class_subjects', to='academic.universitysubject', verbose_name='المادة (تاريخي)'),
                ),
                migrations.AlterField(
                    model_name='universitysemestersubject',
                    name='fk_subject',
                    field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='semester_subjects', to='academic.universitysubject', verbose_name='المادة / المقرر (تاريخي)'),
                ),
                migrations.DeleteModel(
                    name='ExamPeriod',
                ),
                migrations.DeleteModel(
                    name='Lesson',
                ),
                migrations.DeleteModel(
                    name='Unit',
                ),
                migrations.DeleteModel(
                    name='Subject',
                ),
                migrations.AddConstraint(
                    model_name='universitysubject',
                    constraint=models.UniqueConstraint(condition=models.Q(('is_deleted', False)), fields=('name_ar',), name='unique_active_univ_subject_name_ar'),
                ),
                migrations.AddConstraint(
                    model_name='universitysubject',
                    constraint=models.UniqueConstraint(condition=models.Q(('is_deleted', False), models.Q(('name_en__isnull', True), _negated=True), models.Q(('name_en', ''), _negated=True)), fields=('name_en',), name='unique_active_univ_subject_name_en'),
                ),
                migrations.AddConstraint(
                    model_name='universitysubject',
                    constraint=models.UniqueConstraint(condition=models.Q(('is_deleted', False), models.Q(('subject_code__isnull', True), _negated=True), models.Q(('subject_code', ''), _negated=True)), fields=('subject_code',), name='unique_active_univ_subject_code'),
                ),
                migrations.AddConstraint(
                    model_name='universitysubject',
                    constraint=models.UniqueConstraint(condition=models.Q(('is_deleted', False)), fields=('subject_order',), name='unique_active_univ_subject_order'),
                ),
                migrations.AddConstraint(
                    model_name='universityunit',
                    constraint=models.UniqueConstraint(condition=models.Q(('is_deleted', False), ('semester__isnull', False), ('semester_subject__isnull', False)), fields=('semester_subject', 'semester', 'name_ar'), name='unique_univ_unit_sem_sub_sem_name_ar'),
                ),
                migrations.AddConstraint(
                    model_name='universityunit',
                    constraint=models.UniqueConstraint(condition=models.Q(('is_deleted', False), ('semester__isnull', False), ('semester_subject__isnull', False), models.Q(('name_en__isnull', True), _negated=True), models.Q(('name_en', ''), _negated=True)), fields=('semester_subject', 'semester', 'name_en'), name='unique_univ_unit_sem_sub_sem_name_en'),
                ),
                migrations.AddConstraint(
                    model_name='universityunit',
                    constraint=models.UniqueConstraint(condition=models.Q(('is_deleted', False), ('semester__isnull', False), ('semester_subject__isnull', False)), fields=('semester_subject', 'semester', 'order'), name='unique_univ_unit_sem_sub_sem_order'),
                ),
                migrations.AddConstraint(
                    model_name='universityunit',
                    constraint=models.UniqueConstraint(condition=models.Q(('is_deleted', False), ('semester__isnull', True), ('semester_subject__isnull', False)), fields=('semester_subject', 'name_ar'), name='unique_univ_unit_sem_sub_nullsem_name_ar'),
                ),
                migrations.AddConstraint(
                    model_name='universityunit',
                    constraint=models.UniqueConstraint(condition=models.Q(('is_deleted', False), ('semester__isnull', True), ('semester_subject__isnull', False), models.Q(('name_en__isnull', True), _negated=True), models.Q(('name_en', ''), _negated=True)), fields=('semester_subject', 'name_en'), name='unique_univ_unit_sem_sub_nullsem_name_en'),
                ),
                migrations.AddConstraint(
                    model_name='universityunit',
                    constraint=models.UniqueConstraint(condition=models.Q(('is_deleted', False), ('semester__isnull', True), ('semester_subject__isnull', False)), fields=('semester_subject', 'order'), name='unique_univ_unit_sem_sub_nullsem_order'),
                ),
            ]
        ),
    ]
