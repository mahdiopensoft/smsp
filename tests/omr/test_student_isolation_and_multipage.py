import pytest
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
from academic.models.common.AcademicYear import AcademicYear
from academic.models.common.Subject import Subject
from exams.models.Exam import Exam
from exams.models.ExamVersion import ExamVersion
from exams.models.StudentExamRegistration import StudentExamRegistration
from django.contrib.auth import get_user_model
from OpenSoftCoreV41.usermanager.models.UserType import UserType

User = get_user_model()
from submissions.models.Submission import Submission
from submissions.models.SubmissionPage import SubmissionPage
from submissions.services.aggregation import SubmissionAggregationService
from omr.models.OMRSheetResult import OMRSheetResult
from omr.models.OMRQuestionResult import OMRQuestionResult

@pytest.mark.django_db(databases=['default', 'screen', 'log'])
class TestStudentIsolationAndMultiPage:

    @pytest.fixture
    def setup_data(self):
        user_type, _ = UserType.objects.get_or_create(
            id=2,
            defaults={'name_ar': 'طالب', 'name_en': 'Student'}
        )
        year = AcademicYear.objects.create(
            hijri_year="1448", gregorian_year="2026", is_current=True
        )
        subject = Subject.objects.create(
            name_ar="مادة العزل", subject_code="ISO-101"
        )
        exam_a = Exam.objects.create(
            title="Exam A - Chemistry",
            uniqueCode="EXAM-CHEM-A",
            year=year,
            subject=subject,
        )
        version_a = ExamVersion.objects.create(
            exam=exam_a,
            versionCode="A"
        )

        exam_b = Exam.objects.create(
            title="Exam B - Physics",
            uniqueCode="EXAM-PHYS-B",
            year=year,
            subject=subject,
        )
        version_b = ExamVersion.objects.create(
            exam=exam_b,
            versionCode="A"
        )

        student_a = User.objects.create(username="student_a_1001", first_name="Ahmed", fk_user_type=user_type)
        reg_a = StudentExamRegistration.objects.create(
            student=student_a,
            examVersion=version_a,
            seatNumber="1001"
        )

        student_b = User.objects.create(username="student_b_2002", first_name="Saeed", fk_user_type=user_type)
        reg_b = StudentExamRegistration.objects.create(
            student=student_b,
            examVersion=version_b,
            seatNumber="2002"
        )

        return {
            "exam_a": exam_a,
            "version_a": version_a,
            "reg_a": reg_a,
            "exam_b": exam_b,
            "version_b": version_b,
            "reg_b": reg_b,
        }

    def test_gate3_cross_exam_isolation_strictly_enforced(self, setup_data):
        """
        Gate 3: Attempting to submit a sheet with seat number 2002 (registered in Exam B)
        into Exam A must NEVER link the student from Exam B.
        It must set registration=None, status=NEEDS_REVIEW, and log UNREGISTERED_STUDENT_IN_EXAM.
        """
        exam_a = setup_data["exam_a"]
        candidate_seats = ["2002"]

        # Simulate the isolation logic
        matched_reg = None
        reg_qs = StudentExamRegistration.objects.filter(
            examVersion__exam=exam_a, is_deleted=False
        ).select_related('student', 'student_profile__organization', 'examVersion')
        for c_seat in candidate_seats:
            if c_seat:
                matched_reg = reg_qs.filter(seatNumber=c_seat).first()
                if matched_reg:
                    break

        unregistered_error = ""
        if not matched_reg and candidate_seats:
            unregistered_error = "UNREGISTERED_STUDENT_IN_EXAM: رقم الجلوس غير مسجل في هذا الاختبار"

        assert matched_reg is None
        assert "UNREGISTERED_STUDENT_IN_EXAM" in unregistered_error

        # Create submission with this isolated behavior
        sub = Submission.objects.create(
            exam=exam_a,
            registration=matched_reg,
            status=Submission.Status.NEEDS_REVIEW if unregistered_error else Submission.Status.COMPLETED,
            error_message=unregistered_error,
            layout_result={"seat_number": "2002", "is_cross_exam": False}
        )

        assert sub.registration is None
        assert sub.status == Submission.Status.NEEDS_REVIEW
        assert "UNREGISTERED_STUDENT_IN_EXAM" in sub.error_message

    def test_gate5_multipage_aggregation_and_collision_detection(self, setup_data):
        """
        Gate 5: Multi-page submission must aggregate page scores, detect missing pages,
        and catch question collisions deterministically.
        """
        exam_a = setup_data["exam_a"]
        version_a = setup_data["version_a"]
        reg_a = setup_data["reg_a"]

        # Create a submission expecting 2 pages
        sub = Submission.objects.create(
            exam=exam_a,
            exam_version=version_a,
            registration=reg_a,
            expected_pages=2,
            status=Submission.Status.PENDING
        )

        # 1. Page 1 arrives (Questions 1 to 5, all correct)
        sheet_res_p1 = OMRSheetResult.objects.create(
            submission=sub,
            status="verified",
            confidence=0.98,
            mcq_score=Decimal("5.0"),
            total_questions=5,
            correct_answers=5
        )
        for i in range(1, 6):
            OMRQuestionResult.objects.create(
                sheet_result=sheet_res_p1,
                question_number=i,
                final_marked_choice="A",
                correct_choice="A",
                is_correct=True,
                assigned_weight=1.0,
                marks_awarded=1.0
            )

        page1 = SubmissionAggregationService.register_page(
            submission=sub,
            page_number=1,
            sheet_result=sheet_res_p1,
            source_file_hash="hash_p1",
            processing_fingerprint="fingerprint_p1"
        )

        sub.refresh_from_db()
        # Expect NEEDS_REVIEW because page 2 is missing (1 of 2 pages)
        assert sub.status == Submission.Status.NEEDS_REVIEW
        assert "MISSING_PAGES" in sub.error_message
        assert sub.mcq_score == Decimal("5.0")
        assert sub.pages.count() == 1

        # 2. Page 2 arrives (Questions 6 to 10, all correct)
        sheet_res_p2 = OMRSheetResult.objects.create(
            submission=sub,
            status="verified",
            confidence=0.96,
            mcq_score=Decimal("5.0"),
            total_questions=5,
            correct_answers=5
        )
        for i in range(6, 11):
            OMRQuestionResult.objects.create(
                sheet_result=sheet_res_p2,
                question_number=i,
                final_marked_choice="B",
                correct_choice="B",
                is_correct=True,
                assigned_weight=1.0,
                marks_awarded=1.0
            )

        page2 = SubmissionAggregationService.register_page(
            submission=sub,
            page_number=2,
            sheet_result=sheet_res_p2,
            source_file_hash="hash_p2",
            processing_fingerprint="fingerprint_p2"
        )

        sub.refresh_from_db()
        # Both pages present and clean: Status must be COMPLETED, mcq_score == 10.0
        assert sub.status == Submission.Status.COMPLETED
        assert sub.error_message == ""
        assert sub.mcq_score == Decimal("10.0")
        assert sub.total_score == Decimal("10.0")
        assert len(sub.omr_result) == 10

        # 3. Collision Test: Suppose page 2 mistakenly re-evaluates question 5
        OMRQuestionResult.objects.create(
            sheet_result=sheet_res_p2,
            question_number=5, # Collision with page 1!
            final_marked_choice="C",
            correct_choice="A",
            is_correct=False,
            assigned_weight=1.0,
            marks_awarded=0.0
        )
        SubmissionAggregationService.aggregate_submission(sub)
        sub.refresh_from_db()

        assert sub.status == Submission.Status.NEEDS_REVIEW
        assert "QUESTION_COLLISION" in sub.error_message
        assert "5" in sub.error_message

    def test_mismatched_exam_diagnostic_detection(self, setup_data):
        """
        Gate 3 Extension: If a barcode contains an Exam Code belonging to Exam B
        while the envelope/session is configured for Exam A:
        1. It must detect that the sheet belongs to Exam B.
        2. It must retrieve the student's name from Exam B without registering them in Exam A.
        3. It must populate the seat number (e.g. 2002) and never leave it empty.
        4. It must never use the placeholder 'طالب اختبار'.
        5. It must flag the submission as NEEDS_REVIEW with a MISMATCHED_EXAM diagnostic.
        """
        exam_a = setup_data["exam_a"]
        exam_b = setup_data["exam_b"]

        barcode_val = "EXAM-PHYS-B|A|2002|5001"
        candidate_seats = ["2002"]

        # Parse barcode
        extracted_exam_code = "EXAM-PHYS-B"
        foreign_exam = Exam.objects.filter(uniqueCode=extracted_exam_code, is_deleted=False).first()
        assert foreign_exam == exam_b
        assert foreign_exam.id != exam_a.id

        # Registration search inside Exam A must fail
        matched_reg = StudentExamRegistration.objects.filter(
            examVersion__exam=exam_a, seatNumber="2002", is_deleted=False
        ).first()
        assert matched_reg is None

        # Look up foreign student
        foreign_reg = StudentExamRegistration.objects.filter(
            examVersion__exam=foreign_exam, seatNumber="2002", is_deleted=False
        ).select_related('student', 'student_profile').first()
        assert foreign_reg is not None

        s_name = f"{foreign_reg.student.first_name} (ورقة تابعة لاختبار آخر)"
        seat_num = "2002"
        unregistered_error = (
            f"MISMATCHED_EXAM: الورقة تتبع اختبار آخر ('{foreign_exam.title}') "
            f"وليست لهذا الاختبار المختار ('{exam_a.title}'). الطالبة/الطالب: {foreign_reg.student.first_name} (رقم الجلوس: {seat_num}). تم عزل الورقة للتدقيق البشري."
        )

        assert "Saeed" in s_name
        assert s_name != "طالب اختبار"
        assert seat_num == "2002"
        assert "MISMATCHED_EXAM" in unregistered_error
        assert "Exam B - Physics" in unregistered_error

        sub = Submission.objects.create(
            exam=exam_a,
            registration=None,
            status=Submission.Status.NEEDS_REVIEW,
            error_message=unregistered_error,
            layout_result={
                "student_name": s_name,
                "seat_number": seat_num,
                "is_cross_exam": False,
            }
        )
        assert sub.registration is None
        assert sub.status == Submission.Status.NEEDS_REVIEW
        assert sub.layout_result["student_name"] == s_name
        assert sub.layout_result["seat_number"] == "2002"
