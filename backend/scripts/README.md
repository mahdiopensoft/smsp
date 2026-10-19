# دليل السكربتات المساعدة والتأسيس (Backend Utility Scripts)

يحتوي هذا المجلد على كافة سكربتات التهيئة الأولية وبذر البيانات والصيانة والاختبار، منظمة بحسب وظيفتها ليبقى جذر المشروع نظيفاً ومهنياً.

---

## هيكلية المجلد:

### 1. `seeds/` (سكربتات بذر البيانات الأولية)
- `seed_students.py`: بذر طلاب تجريبيين مع أرقام الجلوس وربطهم بالاختبارات.
- `seed_institutes_data.py`: بذر بيانات المعاهد والتعليم الفني والتدريب المهني.
- `seed_higher_education_orgs.py`: بذر مؤسسات وكليات وتخصصات التعليم العالي.
- `seed_study_systems.py`: بذر أنظمة التعليم والترميز.
- `seed_yemen_educational_hierarchy.py`: بذر الهيكلية التعليمية اليمنية (المراحل، الصفوف، المسارات، المواد).

### 2. `setup/` (سكربتات تسجيل وتهيئة الشاشات)
- `setup_omr_screens.py`: تسجيل شاشات التصحيح الضوئي في جدول الشاشات.
- `apply_common_setup_screen.py`: تهيئة شاشات الإعداد المشترك.
- `register_curriculum_exclusions_screen.py`: تسجيل شاشة الحذف من المنهج.
- `register_exam_dispatch_screen.py`: تسجيل شاشة ترحيل وإرسال الاختبارات.
- `register_separated_screens.py`: تسجيل الشاشات المستقلة.
- `setup_school_and_university_sidebar.py`: ترتيب عناصر القائمة الجانبية.
- `update_academic_screens.py`: تحديث بيانات شاشات القطاع الأكاديمي.
- `cleanup_learning_outcomes_screen.py` & `cleanup_unneeded_institute_screens.py`: تنظيف الشاشات الملغاة.
- `fix_academic_screens_fields.py` & `fix_students_screen.py`: تصحيح حقول شاشات معينة.
- `organize_frontend_academic_screens.py`: تنظيم ربط شاشات الواجهة الأمامية.

### 3. `maintenance/` (سكربتات الصيانة والترحيل)
- `fix_schema.py`: تصحيحات على بنية ومخطط الجداول.
- `delete_migrations.py`: تنظيف ملفات الهجرة أثناء إعادة البناء.
- `reset_db_sequences.py`: إعادة ضبط وتصفير تسلسل مفاتيح الجداول (Sequences).
- `backup_data.py`: عمل نسخة احتياطية من البيانات.
- `migrate_schools_and_universities.py`: ترحيل ومطابقة بيانات المدارس والجامعات.
- `folders_commit.py` & `allow_folders.txt`: أدوات تثبيت وتنظيم المجلدات.

### 4. `tests/` (سكربتات الاختبار والفحص)
- `test_multipage_and_control.py`: فحص التصحيح الجماعي المتعدد (PDF/ADF) وسجل الكنترول.
- `test_omr_grading.py`: فحص واختبار دقة محرك قراءة الفقاعات وتصحيحها.
- `verify_exam_dispatch_pipeline.py`: اختبار تدفق إرسال وتوزيع الاختبارات.

---

## كيفية تشغيل أي سكربت:
من داخل مجلد `backend/`:
```bash
# مثال لتشغيل سكربت بذر الطلاب:
PYTHONPATH=. python scripts/seeds/seed_students.py

# مثال لتشغيل سكربت اختبار التصحيح:
PYTHONPATH=. python scripts/tests/test_omr_grading.py
```
