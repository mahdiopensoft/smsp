import pytest
from django.utils import timezone
from bank.models.Question import Question
from bank.models.Answer import Answer
from exams.models.Exam import Exam
from exams.models.ExamVersion import ExamVersion
from exams.models.ExamQuestionOrder import ExamQuestionOrder
from academic.models.common.AcademicYear import AcademicYear
from academic.models.common.Subject import Subject

@pytest.mark.django_db(databases=['default', 'screen', 'log'])
def test_answer_key_freeze_and_cryptographic_verification():
    # 1. Create prerequisites
    year = AcademicYear.objects.create(hijri_year="1448", gregorian_year="2026", is_current=True)
    subject = Subject.objects.create(name_ar="رياضيات", subject_code="MATH-101")
    exam = Exam.objects.create(
        title="اختبار تجريبي للحتمية",
        uniqueCode="EXAM-DETERMINISM-001",
        year=year,
        subject=subject
    )
    version = ExamVersion.objects.create(exam=exam, versionCode="A")

    # 2. Create questions with options
    q1 = Question.objects.create(content="السؤال الأول", defaultMark=2.0)
    opt1_a = Answer.objects.create(question=q1, text="خيار أ", isTrue=False, order_index=0)
    opt1_b = Answer.objects.create(question=q1, text="خيار ب (صحيح)", isTrue=True, order_index=1)
    opt1_c = Answer.objects.create(question=q1, text="خيار ج", isTrue=False, order_index=2)

    q2 = Question.objects.create(content="السؤال الثاني", defaultMark=3.0)
    opt2_a = Answer.objects.create(question=q2, text="خيار أ (صحيح)", isTrue=True, order_index=0)
    opt2_b = Answer.objects.create(question=q2, text="خيار ب", isTrue=False, order_index=1)

    ExamQuestionOrder.objects.create(examVersion=version, question=q1, orderIndex=1)
    ExamQuestionOrder.objects.create(examVersion=version, question=q2, orderIndex=2)

    # 3. Freeze Key
    assert version.key_status == ExamVersion.KeyStatus.DRAFT
    snapshot = version.freeze_key()
    version.refresh_from_db()

    assert version.key_status == ExamVersion.KeyStatus.FROZEN
    assert version.answer_key_hash is not None
    assert len(version.answer_key_hash) == 64
    assert version.verify_key_integrity() is True

    # Verify snapshot content
    assert snapshot["total_questions"] == 2
    assert snapshot["questions"]["1"]["correct_choice"] == "B"
    assert snapshot["questions"]["2"]["correct_choice"] == "A"

    # 4. Tamper Test: Modify 1 byte in the snapshot
    tampered_snapshot = dict(version.answer_key_snapshot)
    tampered_snapshot["questions"]["1"]["correct_choice"] = "C"
    version.answer_key_snapshot = tampered_snapshot
    # Check that verify_key_integrity fails immediately
    assert version.verify_key_integrity() is False

    # 5. Immutability Test: Modifying Bank Question/Answer does NOT change frozen snapshot
    # Restore untampered snapshot
    version.freeze_key(force=True)
    assert version.verify_key_integrity() is True

    # Mutate bank option
    opt1_b.isTrue = False
    opt1_b.save()
    opt1_a.isTrue = True
    opt1_a.save()

    # The frozen key snapshot in ExamVersion must still say Q1 correct choice is B!
    version.refresh_from_db()
    assert version.answer_key_snapshot["questions"]["1"]["correct_choice"] == "B"
    assert version.verify_key_integrity() is True
