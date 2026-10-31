import pytest
from decimal import Decimal
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, force_authenticate
from academic.models.common.AcademicYear import AcademicYear
from academic.models.common.Subject import Subject
from exams.models.Exam import Exam
from exams.models.ExamVersion import ExamVersion
from exams.models.StudentExamRegistration import StudentExamRegistration
from submissions.models.Submission import Submission
from omr.models.OMRSheetResult import OMRSheetResult
from omr.models.OMRQuestionResult import OMRQuestionResult
from omr.models.OMRReviewAuditLog import OMRReviewAuditLog
from omr.apis.OMRHumanReviewMVS import OMRHumanReviewMVS
from omr.apis.ExamGradebookMVS import ExamGradebookMVS
from config.views import protected_media_view
from OpenSoftCoreV41.usermanager.models.UserType import UserType

User = get_user_model()

@pytest.mark.django_db(databases=['default', 'screen', 'log'])
class TestHumanReviewAndSecurity:

    @pytest.fixture
    def setup_data(self):
        user_type, _ = UserType.objects.get_or_create(id=2, defaults={'name_ar': 'طالب', 'name_en': 'Student'})
        staff_type, _ = UserType.objects.get_or_create(id=3, defaults={'name_ar': 'موظف', 'name_en': 'Staff'})

        reviewer = User.objects.create(
            username="reviewer_officer",
            first_name="Control",
            last_name="Auditor",
            is_staff=True,
            fk_user_type=staff_type
        )
        student = User.objects.create(
            username="student_test_aud",
            first_name="Zaid",
            fk_user_type=user_type
        )

        year = AcademicYear.objects.create(hijri_year="1448", gregorian_year="2026", is_current=True)
        subject = Subject.objects.create(name_ar="مادة المراجعة", subject_code="AUD-101")
        exam = Exam.objects.create(title="اختبار التدقيق الأمني", uniqueCode="EXAM-AUDIT-01", year=year, subject=subject)
        version = ExamVersion.objects.create(exam=exam, versionCode="A")
        reg = StudentExamRegistration.objects.create(student=student, examVersion=version, seatNumber="998877")

        sub = Submission.objects.create(
            exam=exam,
            exam_version=version,
            registration=reg,
            status=Submission.Status.NEEDS_REVIEW
        )

        sheet = OMRSheetResult.objects.create(
            submission=sub,
            status="needs_review",
            confidence=0.75,
            total_questions=3,
            answered_questions=2,
            correct_answers=1,
            wrong_answers=1,
            unanswered=1,
            ambiguous_count=1,
            mcq_score=Decimal("2.0"),
            mcq_max_score=Decimal("10.0")
        )

        # Q1 has custom weight 3.5
        q1 = OMRQuestionResult.objects.create(
            sheet_result=sheet,
            question_number=1,
            marked_choice=None,
            candidate_choice="B",
            final_marked_choice=None,
            original_marked_choice="B",
            original_bubble_state="crossed",
            correct_choice="B",
            is_correct=False,
            assigned_weight=3.5,
            marks_awarded=0.0,
            needs_review=True,
            review_priority="CRITICAL",
            bubble_state="crossed"
        )

        return {
            "reviewer": reviewer,
            "student": student,
            "exam": exam,
            "sub": sub,
            "sheet": sheet,
            "q1": q1,
        }

    def test_human_override_retains_history_and_uses_exact_weight(self, setup_data):
        """
        Gate 6 & P0 Audit:
        Overriding question must create OMRReviewAuditLog, retain original_marked_choice,
        and award assigned_weight (3.5) rather than the average unit mark.
        """
        factory = APIRequestFactory()
        sheet = setup_data["sheet"]
        reviewer = setup_data["reviewer"]
        q1 = setup_data["q1"]

        request = factory.post(
            f"/api/omr/human-review/{sheet.id}/override-question/",
            {
                "question_number": 1,
                "marked_choice": "B",
                "reason_code": OMRReviewAuditLog.ReasonCode.CROSSED_BUT_STUDENT_INTENT_CLEAR,
                "reason_text": "تم التحقق من نية الطالب وفق المحضر"
            },
            format='json'
        )
        force_authenticate(request, user=reviewer)

        view = OMRHumanReviewMVS.as_view({'post': 'override_question'})
        response = view(request, pk=sheet.id)

        assert response.status_code == 200

        # Verify Q1 state
        q1.refresh_from_db()
        assert q1.final_marked_choice == "B"
        assert q1.original_marked_choice == "B"  # Must NOT be erased
        assert q1.original_bubble_state == "crossed"
        assert q1.is_correct is True
        assert q1.needs_review is False
        assert float(q1.marks_awarded) == 3.5  # Exactly assigned_weight, not 10/3!

        # Verify audit log
        audit = OMRReviewAuditLog.objects.filter(question_result=q1).first()
        assert audit is not None
        assert audit.reviewer == reviewer
        assert audit.reason_code == OMRReviewAuditLog.ReasonCode.CROSSED_BUT_STUDENT_INTENT_CLEAR
        assert audit.before_snapshot["final_marked_choice"] is None
        assert audit.after_snapshot["final_marked_choice"] == "B"
        assert audit.after_snapshot["marks_awarded"] == 3.5

    def test_security_exam_gradebook_and_protected_media(self, setup_data):
        """
        Gate 7 & P0 Security:
        1. Gradebook must reject unauthenticated requests.
        2. Protected media must deny anonymous access to student papers.
        """
        factory = APIRequestFactory()

        # 1. Gradebook authentication check
        anon_request = factory.get("/api/omr/gradebook/")
        gradebook_view = ExamGradebookMVS.as_view({'get': 'list'})
        resp = gradebook_view(anon_request)
        assert resp.status_code in [401, 403]

        # Authenticated staff access
        staff_request = factory.get("/api/omr/gradebook/")
        force_authenticate(staff_request, user=setup_data["reviewer"])
        resp_auth = gradebook_view(staff_request)
        assert resp_auth.status_code == 200

        # 2. Protected media check
        rf = RequestFactory()
        anon_media_req = rf.get("/media/uploads/original/2026/sheet.jpg")
        anon_media_req.user = None
        media_resp = protected_media_view(anon_media_req, "uploads/original/2026/sheet.jpg")
        assert media_resp.status_code == 403

        # Authenticated access to media
        auth_media_req = rf.get("/media/uploads/original/2026/sheet.jpg")
        auth_media_req.user = setup_data["reviewer"]
        media_resp_auth = protected_media_view(auth_media_req, "uploads/original/2026/sheet.jpg")
        # File doesn't exist on disk, so it should return 404 (NOT 403 Forbidden)
        assert media_resp_auth.status_code == 404
