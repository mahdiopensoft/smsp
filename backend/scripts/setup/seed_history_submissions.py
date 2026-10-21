import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from exams.models.Exam import Exam
from exams.models.StudentExamRegistration import StudentExamRegistration
from submissions.models.Submission import Submission
from bank.models.Answer import Answer

def run():
    exam = Exam.objects.filter(uniqueCode="YE-SANAA-G9-HIST-1446").first()
    if not exam:
        print("Exam not found!")
        return

    regs = list(StudentExamRegistration.objects.filter(examVersion__exam=exam).select_related('examVersion', 'student_profile').order_by('id'))
    print(f"Found {len(regs)} registrations for exam {exam.id}")

    Submission.objects.filter(exam=exam).delete()

    created_subs = 0
    # 38 students have submissions, 2 be absent
    for idx, reg in enumerate(regs):
        if idx >= 38:
            print(f"Leaving student {reg.seatNumber} ({reg.student_profile.name_ar}) as absent")
            continue

        version = reg.examVersion
        qos = version.question_orders.select_related('question').order_by('orderIndex')
        
        # Decide student ability
        if idx < 15:
            target_accuracy = random.uniform(0.88, 0.98)
        elif idx < 28:
            target_accuracy = random.uniform(0.72, 0.86)
        elif idx < 35:
            target_accuracy = random.uniform(0.55, 0.70)
        else:
            target_accuracy = random.uniform(0.40, 0.52)

        questions_result = []
        earned_score = 0.0

        for qo in qos:
            q = qo.question
            q_idx = qo.orderIndex
            is_tf = (q.questionType == 'true_false')

            if is_tf:
                choices = ['صح', 'خطأ']
                correct_c = 'صح' if (q.isTrue is True) else 'خطأ'
            else:
                choices = ['أ', 'ب', 'ج', 'د']
                all_ans = list(Answer.objects.filter(question=q).order_by('id'))
                correct_c = 'أ'
                for a_idx, ans in enumerate(all_ans):
                    if ans.isTrue:
                        correct_c = ['أ', 'ب', 'ج', 'د'][min(a_idx, 3)]
                        break

            # Does student answer correctly?
            is_correct = (random.random() < target_accuracy)
            if is_correct:
                marked_c = correct_c
            else:
                wrong_choices = [c for c in choices if c != correct_c]
                marked_c = random.choice(wrong_choices) if wrong_choices else correct_c

            mark = 2.0 if is_correct else 0.0
            earned_score += mark

            questions_result.append({
                "question_id": q_idx,
                "question_text": q.content[:80] if q.content else f"سؤال رقم {q_idx}",
                "choices": choices,
                "correct_choice": correct_c,
                "marked_choice": marked_c,
                "is_correct": is_correct,
                "bubble_state": "filled",
                "marks_awarded": mark,
                "max_mark": 2.0,
                "final_confidence": round(random.uniform(0.92, 0.99), 2),
                "ai_results": {marked_c: "filled"},
                "ai_confidence": {marked_c: {"label": "filled", "confidence": round(random.uniform(0.91, 0.99), 2), "needs_review": False}},
            })

        sub_status = Submission.Status.COMPLETED
        if idx in [10, 22]: # Two sheets marked as needs_review for review demo
            sub_status = Submission.Status.NEEDS_REVIEW
            questions_result[5]["bubble_state"] = "ambiguous"
            questions_result[5]["final_confidence"] = 0.58

        sub = Submission.objects.create(
            exam=exam,
            exam_version=version,
            registration=reg,
            status=sub_status,
            mcq_score=earned_score,
            total_score=earned_score,
            overall_confidence=round(random.uniform(0.94, 0.99), 2),
            omr_result=questions_result,
            layout_result={
                "seat_number": reg.seatNumber,
                "secret_number": reg.secretNumber,
                "student_name": reg.student_profile.name_ar,
                "version_code": version.versionCode,
                "total_questions": 50,
                "total_correct": int(earned_score / 2),
                "score_percent": round((earned_score / 100.0) * 100, 1),
                "dispatched_to_control": False,
            }
        )
        created_subs += 1

    print(f"Successfully created {created_subs} submissions for exam {exam.id} ({exam.title})")

if __name__ == '__main__':
    run()
