import os

files = [
    '01_introduction_and_system_architecture.md',
    '02_users_roles_and_access_control.md',
    '03_common_and_academic_hierarchy.md',
    '04_question_bank_and_authoring.md',
    '05_review_workflow_and_quality.md',
    '06_exam_generation_tos_and_models.md',
    '07_exam_distribution_and_dispatch.md',
    '08_omr_scanning_and_evaluation.md',
    '09_reports_analytics_and_psychometrics.md',
    '10_audit_logs_and_security.md',
    '11_cross_cutting_and_non_functional.md'
]

master_path = os.path.join(os.path.dirname(__file__), 'SYSTEM_REQUIREMENTS_SPECIFICATION.md')
base_dir = os.path.dirname(__file__)

header = """# وثيقة متطلبات النظام الرسمية (System Requirements Specification - SRS)
## نظام بنك الأسئلة المركزي، التوليد، والتصحيح الآلي المتقدم (NewQuestionBank)
### الإصدار: 4.0 الإنتاجي (Production Baseline)
### المرجع الأساسي لفريق ضبط الجودة والاختبار (QA & Testing Reference)

---

## 📌 ديباجة وتوجيهات لفريق الاختبار (QA & Testing Guide)
1. **المرجعية الصارمة**: هذه الوثيقة تم استخراجها والتحقق منها مباشرة من الكود البرمجي الفعلي للنظام (Frontend & Backend Models, Views, Serializers, Workflows, APIs, Permissions, and Validations).
2. **صيغة الاختبار والتحقق**: كل متطلب في هذه الوثيقة مصاغ بإحدى الصيغ الثلاث الإلزامية:
   - `يجب أن يتيح النظام...` (Functional Capability to Test).
   - `يجب أن يمنع النظام...` (Negative Constraint / Security Boundary to Test).
   - `يجب أن يتحقق النظام من...` (Validation Rule / Business Integrity to Test).
3. **معرفات المتطلبات الفريدة**: كل متطلب يحمل معرّفاً ثابتاً وفريداً يسهل الربط به في تقارير الاختبار (مثل `REQ-SYS-...`, `REQ-ROLE-...`, `REQ-AUTH-...`, `REQ-QB-...`, `REQ-REV-...`, `REQ-EXAM-...`, `REQ-DISP-...`, `REQ-OMR-...`, `REQ-RPT-...`, `REQ-AUD-...`, `REQ-NFR-...`).

---

## 📑 فهرس محتويات الوثيقة الشاملة
1. [الباب الأول: مقدمة النظام، الهيكل العام، والمصطلحات الديناميكية](01_introduction_and_system_architecture.md)
2. [الباب الثاني: المستخدمون، الأدوار، المصادقة، والتحكم بالوصول](02_users_roles_and_access_control.md)
3. [الباب الثالث: الهيكل الجغرافي والمؤسسي، والترتيب الأكاديمي للقطاعات الثلاثة](03_common_and_academic_hierarchy.md)
4. [الباب الرابع: بنك الأسئلة المركزي، محرك التأليف، والاستيراد الجماعي](04_question_bank_and_authoring.md)
5. [الباب الخامس: مسار المراجعة والتحكيم الأكاديمي، فحص الجودة، وتتبع الإصدارات](05_review_workflow_and_quality.md)
6. [الباب السادس: جدول المواصفات، بناء وتوليد الاختبارات، النماذج، وسجلات الممتحنين](06_exam_generation_tos_and_models.md)
7. [الباب السابع: نظام توزيع وتصدير الاختبارات المجدول وحماية التسريب](07_exam_distribution_and_dispatch.md)
8. [الباب الثامن: نظام التصحيح الآلي (OMR)، قوالب التظليل، والتدقيق البشري](08_omr_scanning_and_evaluation.md)
9. [الباب التاسع: التقارير، التحليلات الأكاديمية، ومحرك القياس السيكومتري](09_reports_analytics_and_psychometrics.md)
10. [الباب العاشر: سجلات التدقيق الجنائي، الرقابة، وإدارة السجلات](10_audit_logs_and_security.md)
11. [الباب الحادي عشر: مصفوفة العلاقات، دورات الحياة، الملفات، والإشعارات، والمتطلبات غير الوظيفية](11_cross_cutting_and_non_functional.md)

---

"""

with open(master_path, 'w', encoding='utf-8') as out_f:
    out_f.write(header)
    for fname in files:
        fpath = os.path.join(base_dir, fname)
        if os.path.exists(fpath):
            with open(fpath, 'r', encoding='utf-8') as in_f:
                content = in_f.read()
                out_f.write('\n\n' + '=' * 80 + '\n\n')
                out_f.write(content)
        else:
            print(f'Warning: {fpath} does not exist!')

print(f'Master SRS compiled successfully. Size: {os.path.getsize(master_path)} bytes.')
