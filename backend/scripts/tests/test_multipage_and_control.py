"""
test_multipage_and_control.py
==============================
اختبار شامل ودقيق لنظام التصحيح المتعدد للصفحات (PDF / ADF Scan)
وحق الكنترول المركزي (Control Locking & Ledger)
للتأكد التام من الجاهزية للواقع العملي بنسبة 100%.
"""

import os
import sys
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

import cv2
import numpy as np
import fitz  # PyMuPDF
from django.test import RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from templates_engine.models.ExamTemplate import ExamTemplate
from exams.models.Exam import Exam
from exams.models.ExamVersion import ExamVersion
from exams.models.StudentExamRegistration import StudentExamRegistration
from submissions.models.Submission import Submission
from submissions.models.SubmissionBatch import SubmissionBatch
from omr.models.OMRSheetResult import OMRSheetResult
from omr.models.OMRQuestionResult import OMRQuestionResult
from omr.api import grade_sheet, batch_scan_api
from omr.apis.OMRHumanReviewMVS import OMRHumanReviewMVS
from omr.apis.ExamGradebookMVS import ExamGradebookMVS
from submissions.apis.SubmissionMVS import SubmissionMVS

def create_synthetic_sheet_image(template_data, marked_answers):
    """رسم ورقة إجابة A5 قياسية بالدوائر والعلامات الزاوية"""
    scale = 300.0 / 25.4
    paper_w = int(210.0 * scale)  # 2480 px
    paper_h = int(148.5 * scale)  # 1754 px
    img = np.ones((paper_h, paper_w, 3), dtype=np.uint8) * 255

    # 1. رسم علامات المحاذاة الأربع (Fiducials)
    f_sz = int(5.5 * scale)
    fiducials = [
        (int(6.0 * scale), int(6.0 * scale)),
        (int(198.5 * scale), int(6.0 * scale)),
        (int(6.0 * scale), int(137.0 * scale)),
        (int(198.5 * scale), int(137.0 * scale)),
    ]
    for fx, fy in fiducials:
        cv2.rectangle(img, (fx, fy), (fx + f_sz, fy + f_sz), (0, 0, 0), -1)

    # 2. رسم فقاعات الأسئلة وتظليل الإجابات المحددة
    for q in template_data.get('mcq_questions', []):
        q_num = q.get('q_num') or q.get('question_number')
        user_choice = marked_answers.get(q_num)
        for choice, coords in q.get('bubbles', {}).items():
            cx = int(coords['x'] * scale)
            cy = int(coords['y'] * scale)
            r = int((coords.get('r') or (coords.get('width', 4.5) / 2.0)) * scale)
            cv2.circle(img, (cx, cy), r, (50, 50, 50), 2)
            if user_choice == choice:
                cv2.circle(img, (cx, cy), r - 3, (15, 15, 15), -1)

    return img

def run_tests():
    print("=" * 70)
    print("🚀 بدء الاختبارات الشاملة للمسح المتعدد للصفحات وحق الكنترول المركزي...")
    print("=" * 70)

    # 1. جلب قالب نشط (مثل القالب 28)
    tpl = ExamTemplate.objects.filter(id=28, is_active=True).first()
    if not tpl:
        tpl = ExamTemplate.objects.filter(is_active=True).first()
    assert tpl is not None, "يجب وجود قالب نشط في قاعدة البيانات"
    print(f"✅ القالب المستخدم: {tpl.name} (id={tpl.id})")

    # 2. إنشاء اختبار ونموذج وتسجيلات طلاب
    exam = Exam.objects.filter(is_deleted=False).first()
    assert exam is not None, "يجب وجود اختبار في قاعدة البيانات"
    version, _ = ExamVersion.objects.get_or_create(exam=exam, versionCode="A")
    
    reg_student1, _ = StudentExamRegistration.objects.get_or_create(
        examVersion=version, seatNumber="77001", defaults={"isPresent": True}
    )
    reg_student2, _ = StudentExamRegistration.objects.get_or_create(
        examVersion=version, seatNumber="77002", defaults={"isPresent": True}
    )
    print(f"✅ تم تجهيز الاختبار والطلاب: {reg_student1.seatNumber}, {reg_student2.seatNumber}")

    # 3. رسم صفحتين: الطالب 1 والطالب 2
    answers_s1 = {1: 'A', 2: 'B', 3: 'A', 4: 'A', 5: 'B'}
    answers_s2 = {1: 'B', 2: 'A', 3: 'B', 4: 'B', 5: 'A'}

    img_s1 = create_synthetic_sheet_image(tpl.template_data, answers_s1)
    img_s2 = create_synthetic_sheet_image(tpl.template_data, answers_s2)

    # تحويل الصورتين إلى صفحات في ملف PDF واحد متعدد الصفحات
    pdf_doc = fitz.open()
    for img_arr in [img_s1, img_s2]:
        _, enc = cv2.imencode('.png', img_arr)
        img_bytes = enc.tobytes()
        rect = fitz.Rect(0, 0, img_arr.shape[1], img_arr.shape[0])
        pdf_page = pdf_doc.new_page(width=rect.width, height=rect.height)
        pdf_page.insert_image(rect, stream=img_bytes)
    
    pdf_bytes = pdf_doc.tobytes()
    pdf_doc.close()
    print(f"✅ تم توليد ملف PDF متعدد الصفحات بنجاح (حجم: {len(pdf_bytes)} بايت، صفحتين)")

    # ═════════════════════════════════════════════════════════════════
    # اختبار 1: رفع وتصحيح PDF متعدد الصفحات عبر grade_sheet
    # ═════════════════════════════════════════════════════════════════
    print("\n[اختبار 1]: تجربة رفع ملف PDF متعدد الصفحات إلى /api/omr/grade/ ...")
    rf = RequestFactory()
    uploaded_pdf = SimpleUploadedFile("multipage_sheets.pdf", pdf_bytes, content_type="application/pdf")
    req = rf.post('/api/omr/grade/', {
        'sheet_image': uploaded_pdf,
        'template_id': str(tpl.id),
        'exam_id': str(exam.id),
        'version_id': str(version.id),
        'dpi': '300',
    })
    
    res = grade_sheet(req)
    assert res.status_code == 200, f"فشل تصحيح الـ PDF متعدد الصفحات: {res.data}"
    data = res.data
    assert data.get("is_batch") is True, "يجب أن يعيد الرد is_batch: True"
    assert data.get("total_pages") == 2, f"يجب أن يكون عدد الصفحات 2، المستلم: {data.get('total_pages')}"
    assert len(data.get("pages")) == 2, "يجب أن يحتوي الرد على مصفوفة الصفحات المفحوصة"
    print(f"🎉 نجح اختبار الـ PDF متعدد الصفحات: تم مسح {data['total_pages']} صفحات، النتيجة الأولى: {data['pages'][0]['score']}, النتيجة الثانية: {data['pages'][1]['score']}")

    # ═════════════════════════════════════════════════════════════════
    # اختبار 2: تجربة endpoint المباشر batch_scan_api
    # ═════════════════════════════════════════════════════════════════
    print("\n[اختبار 2]: تجربة المسح الجماعي المباشر /api/omr/batch-scan/ ...")
    uploaded_pdf2 = SimpleUploadedFile("batch_test.pdf", pdf_bytes, content_type="application/pdf")
    req_batch = rf.post('/api/omr/batch-scan/', {
        'files': [uploaded_pdf2],
        'template_id': str(tpl.id),
        'exam_id': str(exam.id),
        'dpi': '300',
    })
    res_batch = batch_scan_api(req_batch)
    assert res_batch.status_code == 200, f"فشل endpoint المسح الجماعي: {res_batch.data}"
    batch_data = res_batch.data
    assert batch_data.get("success") is True
    assert batch_data.get("total_papers") == 2
    print(f"🎉 نجح endpoint المسح الجماعي: تم معالجة {batch_data['total_papers']} أوراق بالدفعة #{batch_data['batch_id']}.")

    # ═════════════════════════════════════════════════════════════════
    # اختبار 3: ترحيل الدرجات إلى الكنترول المركزي وقفل السجلات (Ledger & Lock)
    # ═════════════════════════════════════════════════════════════════
    print("\n[اختبار 3]: ترحيل درجات الاختبار إلى نظام الكنترول المركزي وتوليد الإيصال...")
    gb_view = ExamGradebookMVS.as_view({'post': 'dispatch_to_control'})
    req_dispatch = rf.post(f'/api/omr/gradebook/{exam.id}/dispatch-to-control/', {})
    res_dispatch = gb_view(req_dispatch, pk=str(exam.id))
    assert res_dispatch.status_code == 200, f"فشل الترحيل للكنترول: {res_dispatch.data}"
    disp_data = res_dispatch.data
    assert disp_data.get("success") is True
    receipt_code = disp_data.get("control_receipt_code")
    assert receipt_code and receipt_code.startswith("CTL-"), f"رقم الإيصال غير مطابق للمعيار: {receipt_code}"
    print(f"🔒 تم قفل وترحيل الدرجات بنجاح! رقم إيصال الكنترول الرقمي: {receipt_code}")

    # جلب أحد التسليمات المفحوصة والمقفلة
    locked_submission = Submission.objects.filter(exam=exam, is_deleted=False).first()
    assert locked_submission is not None
    assert locked_submission.layout_result.get("dispatched_to_control") is True
    assert locked_submission.layout_result.get("control_receipt_code") == receipt_code
    print(f"✅ تحقق من السجل #{locked_submission.id}: مقفل بختم رقمي: {locked_submission.layout_result.get('tamper_seal')}")

    # ═════════════════════════════════════════════════════════════════
    # اختبار 4: التحقق الصارم من منع التعديل أو التلاعب بعد قفل الكنترول (403 Forbidden)
    # ═════════════════════════════════════════════════════════════════
    print("\n[اختبار 4]: محاولة تعديل الورقة المقفلة عبر المراجعة البشرية override_question ...")
    hr_override = OMRHumanReviewMVS.as_view({'post': 'override_question'})
    sheet_res = OMRSheetResult.objects.filter(submission=locked_submission).first()
    assert sheet_res is not None

    req_override = rf.post(f'/api/omr/human-review/{sheet_res.id}/override-question/', {
        'question_number': 1,
        'new_choice': 'C',
    })
    res_override = hr_override(req_override, pk=str(sheet_res.id))
    assert res_override.status_code == 403, f"كان يجب رفض التعديل بـ 403 Forbidden لكن الرد كان: {res_override.status_code}"
    print(f"🛡️ نجح قفل الكنترول! تم رفض التعديل: {res_override.data.get('message')}")

    print("\n[اختبار 5]: محاولة اعتماد المراجعة approve_review لورقة مقفلة بالكنترول ...")
    hr_approve = OMRHumanReviewMVS.as_view({'post': 'approve_review'})
    req_approve = rf.post(f'/api/omr/human-review/{sheet_res.id}/approve-review/', {})
    res_approve = hr_approve(req_approve, pk=str(sheet_res.id))
    assert res_approve.status_code == 403, f"كان يجب رفض الاعتماد بـ 403 لكن الرد كان: {res_approve.status_code}"
    print(f"🛡️ نجح قفل الكنترول! تم رفض الاعتماد: {res_approve.data.get('message')}")

    print("\n[اختبار 6]: محاولة إعادة المعالجة والتصحيح reprocess لورقة مقفلة بالكنترول ...")
    sub_reprocess = SubmissionMVS.as_view({'post': 'reprocess'})
    req_reprocess = rf.post(f'/api/submissions/submissions/{locked_submission.id}/reprocess/', {})
    res_reprocess = sub_reprocess(req_reprocess, pk=str(locked_submission.id))
    assert res_reprocess.status_code == 403, f"كان يجب رفض إعادة المعالجة بـ 403 لكن الرد كان: {res_reprocess.status_code}"
    print(f"🛡️ نجح قفل الكنترول! تم رفض إعادة المعالجة: {res_reprocess.data.get('message')}")

    print("\n[اختبار 7]: محاولة التعديل اليدوي update_review لورقة مقفلة بالكنترول ...")
    sub_update_rev = SubmissionMVS.as_view({'post': 'update_review'})
    req_up_rev = rf.post(f'/api/submissions/submissions/{locked_submission.id}/update_review/', {'total_score': 99.0})
    res_up_rev = sub_update_rev(req_up_rev, pk=str(locked_submission.id))
    assert res_up_rev.status_code == 403, f"كان يجب رفض التعديل اليدوي بـ 403 لكن الرد كان: {res_up_rev.status_code}"
    print(f"🛡️ نجح قفل الكنترول! تم رفض التعديل اليدوي: {res_up_rev.data.get('message')}")

    print("\n[اختبار 8]: محاولة حذف الورقة delete لورقة مقفلة بالكنترول ...")
    sub_destroy = SubmissionMVS.as_view({'delete': 'destroy'})
    req_del = rf.delete(f'/api/submissions/submissions/{locked_submission.id}/')
    res_del = sub_destroy(req_del, pk=str(locked_submission.id))
    assert res_del.status_code == 403, f"كان يجب منع الحذف بـ 403 لكن الرد كان: {res_del.status_code}"
    print(f"🛡️ نجح قفل الكنترول! تم منع حذف الورقة: {res_del.data.get('message')}")

    # ═════════════════════════════════════════════════════════════════
    # اختبار 9: إلغاء الترحيل وإعادة الفتح للتدقيق (Rollback Dispatch)
    # ═════════════════════════════════════════════════════════════════
    print("\n[اختبار 9]: تجربة إلغاء الترحيل بطلب رسمي من إدارة الكنترول (Rollback Dispatch) ...")
    gb_rollback = ExamGradebookMVS.as_view({'post': 'rollback_dispatch'})
    req_rollback = rf.post(f'/api/omr/gradebook/{exam.id}/rollback-dispatch/', {})
    res_rollback = gb_rollback(req_rollback, pk=str(exam.id))
    assert res_rollback.status_code == 200
    print(f"🔓 تم إلغاء الترحيل وفتح السجلات للتدقيق بنجاح: {res_rollback.data.get('message')}")

    # التأكد من إمكانية التعديل الآن بعد إلغاء الترحيل
    req_override_after = rf.post(f'/api/omr/human-review/{sheet_res.id}/override-question/', {
        'question_number': 1,
        'new_choice': 'C',
    })
    res_override_after = hr_override(req_override_after, pk=str(sheet_res.id))
    assert res_override_after.status_code == 200, f"يجب السماح بالتعديل بعد إلغاء الترحيل: {res_override_after.data}"
    print(f"✅ بعد إلغاء الترحيل تم قبول التعديل بنجاح: النتيجة الجديدة = {res_override_after.data.get('score')}")

    print("\n" + "=" * 70)
    print("🏆 اكتملت جميع الاختبارات بنجاح بنسبة 100%! النظام جاهز للواقع الميداني بلا أي أخطاء.")
    print("=" * 70)

if __name__ == '__main__':
    run_tests()
