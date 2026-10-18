import os
import sys
import django
import json
import cv2
import numpy as np

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from templates_engine.models.ExamTemplate import ExamTemplate
from omr.providers.opencv_omr import OpenCVOMREngine, normalize_choice
from templates_engine.builder import TemplateBuilderService

def run_test():
    print("================================================================")
    print("🧪 اختبار نظام التصحيح الآلي (OMR Grading Engine Test)")
    print("================================================================")

    template_obj = ExamTemplate.objects.filter(id=28).first()
    if not template_obj:
        template_obj = ExamTemplate.objects.filter(name__icontains="50").first()
    
    td = template_obj.template_data
    builder = TemplateBuilderService()
    template_contract = builder.build_from_designer_config(td)
    td_dict = template_contract.model_dump()

    dpi = 300
    scale = dpi / 25.4
    paper_size = td_dict.get("paper_size", "A5")
    pw_mm = 210.0 if "A5" in paper_size.upper() else 210.0
    ph_mm = 148.5 if "A5" in paper_size.upper() else 297.0
    
    img_w = int(round(pw_mm * scale))
    img_h = int(round(ph_mm * scale))
    sheet_img = np.ones((img_h, img_w, 3), dtype=np.uint8) * 255

    # رسم علامات الزوايا (Fiducials)
    for fid in td_dict.get("fiducial_marks", []):
        fx = int(round(fid["x_mm"] * scale))
        fy = int(round(fid["y_mm"] * scale))
        fw = int(round(fid["width_mm"] * scale))
        fh = int(round(fid["height_mm"] * scale))
        cv2.rectangle(sheet_img, (fx, fy), (fx + fw, fy + fh), (0, 0, 0), -1)

    mcqs = td_dict.get("mcq_questions", [])
    print(f"📊 عدد الأسئلة في القالب: {len(mcqs)}")
    
    # محاكاة إجابات الطالب ومفتاح الحل:
    # Q1 (صح/خطأ): صحيحة ('صح' -> 'A')
    # Q2 (صح/خطأ): صحيحة ('خطأ' -> 'B')
    # Q3 (صح/خطأ): خاطئة (الطالب اختار 'صح' والمفتاح 'B')
    # Q4 (صح/خطأ): ملتبسة (ظلل 'صح' و 'خطأ' معاً)
    # Q5 (صح/خطأ): فارغة (لم يجب)
    # Q21 (اختيار من متعدد 1,2,3,4): صحيحة (المفتاح 'A', ظلل '1')
    # Q22 (اختيار من متعدد 1,2,3,4): صحيحة (المفتاح 'B', ظلل '2')
    # Q23 (اختيار من متعدد 1,2,3,4): خاطئة (المفتاح 'D', ظلل '1')
    # باقي الأسئلة: صحيحة
    
    simulated_answers = {}
    answer_key = {}
    
    for idx, q in enumerate(mcqs, 1):
        choices = [c["choice"] for c in q["choices"]]
        
        if idx == 1:
            answer_key[str(idx)] = "A"
            simulated_answers[idx] = ["صح"]
        elif idx == 2:
            answer_key[str(idx)] = "B"
            simulated_answers[idx] = ["خطأ"]
        elif idx == 3:
            answer_key[str(idx)] = "B"
            simulated_answers[idx] = ["صح"] # خاطئة
        elif idx == 4:
            answer_key[str(idx)] = "A"
            simulated_answers[idx] = ["صح", "خطأ"] # ملتبسة
        elif idx == 5:
            answer_key[str(idx)] = "A"
            simulated_answers[idx] = [] # فارغة
        elif idx == 21:
            answer_key[str(idx)] = "A"
            simulated_answers[idx] = ["1"] # صحيحة
        elif idx == 22:
            answer_key[str(idx)] = "B"
            simulated_answers[idx] = ["2"] # صحيحة
        elif idx == 23:
            answer_key[str(idx)] = "D"
            simulated_answers[idx] = ["1"] # خاطئة
        else:
            # افتراضياً: الإجابة هي الخيار الأول ومفتاح الحل هو الأول
            first_c = choices[0]
            answer_key[str(idx)] = normalize_choice(first_c)
            simulated_answers[idx] = [first_c]

    # رسم كافة الدوائر على الورقة
    for q in mcqs:
        qid = q["question_id"]
        to_fill = simulated_answers.get(qid, [])
        for ch in q["choices"]:
            choice_lbl = ch["choice"]
            bubble = ch["bubble_region"]
            cx = int(round((bubble["dx_mm"] + bubble["width_mm"] / 2.0) * scale))
            cy = int(round((bubble["dy_mm"] + bubble["height_mm"] / 2.0) * scale))
            r = int(round((bubble["width_mm"] / 2.0) * scale))

            # رسم حلقة الدائرة المطبوعة
            cv2.circle(sheet_img, (cx, cy), r, (100, 100, 100), 2)

            # تظليل الدائرة بالكامل إذا كان الخيار مجاباً
            if choice_lbl in to_fill:
                cv2.circle(sheet_img, (cx, cy), int(r * 0.85), (20, 20, 20), -1)

    test_img_path = "/tmp/test_omr_sheet_filled.png"
    cv2.imwrite(test_img_path, sheet_img)
    print(f"💾 تم حفظ صورة ورقة الاختبار التجريبية المظللة في: {test_img_path}")

    # تشغيل محرك التصحيح
    print("\n--- [تشغيل المحرك: OpenCVOMREngine] ---")
    engine = OpenCVOMREngine()
    res = engine._process(
        input_data={"image_path": test_img_path},
        context={
            "template": template_contract,
            "dpi": dpi,
            "answer_key": {
                "mcq_answers": answer_key,
                "mcq_marks_per_question": 1.0,
            }
        }
    )

    data = res.data or {}
    print(f"الحالة: {res.status}, معدل الثقة: {res.confidence}")
    print(f"الدرجة المحتسبة: {data.get('total_score')} من {data.get('max_score')}")
    print(f"الدوائر الملتبسة: {data.get('ambiguous_bubbles')}")

    q_dict = {q["question_id"]: q for q in data.get("questions", [])}
    
    print("\nتفحص الحالات المختارة بدقة:")
    for check_id in [1, 2, 3, 4, 5, 21, 22, 23]:
        qinfo = q_dict.get(check_id, {})
        print(f"Q{check_id:02d}: المظلل={qinfo.get('marked_choice')!r:8} | المفتاح={qinfo.get('correct_choice')!r:5} | صح={str(qinfo.get('is_correct')):5} | الحالة={qinfo.get('bubble_state')!r:10} | الدرجة={qinfo.get('marks_awarded')} | الثقة={qinfo.get('final_confidence')}")

if __name__ == '__main__':
    run_test()
