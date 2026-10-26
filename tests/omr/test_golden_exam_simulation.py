import pytest
import io
import csv
from decimal import Decimal
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
from omr.apis.ExamGradebookMVS import ExamGradebookMVS
from OpenSoftCoreV41.usermanager.models.UserType import UserType

User = get_user_model()

@pytest.mark.django_db(databases=['default', 'screen', 'log'])
class TestGoldenExamSimulation:

    def test_gate8_end_to_end_golden_exam_and_full_control_export(self):
        """
        Gate 8: Complete Golden Exam Simulation
        1. 25 registered students (well exceeding the 10-student pagination limit).
        2. Frozen exam version key with cryptographic SHA-256 integrity.
        3. Custom weighted questions.
        4. Submissions processed and verified.
        5. Full control sheet export bypassing 10-student pagination to export 100% of students.
        """
        user_type, _ = UserType.objects.get_or_create(id=2, defaults={'name_ar': 'طالب', 'name_en': 'Student'})
        staff_type, _ = UserType.objects.get_or_create(id=3, defaults={'name_ar': 'موظف', 'name_en': 'Staff'})

        officer = User.objects.create(
            username="golden_officer",
            first_name="Control",
            last_name="Director",
            is_staff=True,
            fk_user_type=staff_type
        )

        year = AcademicYear.objects.create(hijri_year="1448", gregorian_year="2026", is_current=True)
        subject = Subject.objects.create(name_ar="رياضيات متقدمة", subject_code="GOLD-MATH-01")
        exam = Exam.objects.create(
            title="اختبار الكنترول الذهبي النهائي",
            uniqueCode="EXAM-GOLDEN-2026",
            year=year,
            subject=subject,
        )

        version = ExamVersion.objects.create(
            exam=exam,
            versionCode="A"
        )

        # Freeze key with 5 questions and specific assigned weights (total = 20.0)
        snapshot = {
            "exam_id": exam.id,
            "version_id": version.id,
            "version_code": "A",
            "total_questions": 5,
            "questions": {
                "1": {"question_id": 101, "correct_choice": "A", "assigned_weight": 4.0},
                "2": {"question_id": 102, "correct_choice": "B", "assigned_weight": 4.0},
                "3": {"question_id": 103, "correct_choice": "C", "assigned_weight": 4.0},
                "4": {"question_id": 104, "correct_choice": "D", "assigned_weight": 4.0},
                "5": {"question_id": 105, "correct_choice": "A", "assigned_weight": 4.0},
            }
        }
        version.freeze_key(user=officer, custom_snapshot=snapshot)
        assert version.key_status == ExamVersion.KeyStatus.FROZEN
        assert version.verify_key_integrity() is True

        # Register 25 students (exceeding standard 10-student pagination)
        total_students_count = 25
        students = []
        registrations = []

        for i in range(1, total_students_count + 1):
            s = User.objects.create(
                username=f"golden_student_{i:03d}",
                first_name=f"طالب_{i}",
                last_name="الذهبي",
                fk_user_type=user_type
            )
            reg = StudentExamRegistration.objects.create(
                student=s,
                examVersion=version,
                seatNumber=f"100{i:02d}"
            )
            students.append(s)
            registrations.append(reg)

            # Process submission for students 1..20 (students 21..25 absent)
            if i <= 20:
                is_full_mark = (i % 2 == 1)
                score = Decimal("20.0") if is_full_mark else Decimal("12.0")

                sub = Submission.objects.create(
                    exam=exam,
                    exam_version=version,
                    registration=reg,
                    status=Submission.Status.COMPLETED,
                    mcq_score=score,
                    total_score=score,
                    overall_confidence=0.98,
                    layout_result={
                        "seat_number": reg.seatNumber,
                        "student_name": f"{s.first_name} {s.last_name}",
                        "version_code": "A",
                        "total_correct": 5 if is_full_mark else 3,
                        "dispatched_to_control": True
                    }
                )

                sheet_res = OMRSheetResult.objects.create(
                    submission=sub,
                    status="verified",
                    confidence=0.98,
                    total_questions=5,
                    correct_answers=5 if is_full_mark else 3,
                    wrong_answers=0 if is_full_mark else 2,
                    mcq_score=score,
                    mcq_max_score=Decimal("20.0"),
                    pipeline_version="3.0",
                    opencv_engine_version="3.0",
                    decision_matrix_version="3.0"
                )

        assert StudentExamRegistration.objects.filter(examVersion__exam=exam).count() == 25
        assert Submission.objects.filter(exam=exam).count() == 20

        # Export control sheet
        factory = APIRequestFactory()
        request = factory.get(f"/api/omr/gradebook/{exam.id}/export-control-sheet/")
        force_authenticate(request, user=officer)

        view = ExamGradebookMVS.as_view({'get': 'export_control_sheet'})
        response = view(request, pk=exam.id)

        assert response.status_code == 200
        assert "text/csv" in response["Content-Type"]

        # Parse CSV content
        content = response.content.decode("utf-8-sig")
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)

        # Header rows + Column titles + Data rows
        data_rows = [r for r in rows if len(r) >= 14 and r[0].isdigit()]

        # GATE 8 PASS CRITERIA: Exactly 25 students exported, 0 truncation!
        assert len(data_rows) == 25, f"Expected 25 exported students, but got {len(data_rows)} (pagination trap was not bypassed!)"

        # Verify first student has seatNumber 10001 and score 20
        first_row = data_rows[0]
        assert first_row[1] == "10001"
        assert float(first_row[8]) == 20.0
        assert first_row[13] == "مرحل رسمياً"

        # Verify absent student (e.g. student #25 with seat 10025)
        last_row = data_rows[24]
        assert last_row[1] == "10025"
        assert last_row[8] == "غائب"
