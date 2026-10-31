import pytest
import hashlib
from decimal import Decimal
from django.utils import timezone
from academic.models.common.AcademicYear import AcademicYear
from academic.models.common.Subject import Subject
from exams.models.Exam import Exam
from exams.models.ExamVersion import ExamVersion
from exams.models.StudentExamRegistration import StudentExamRegistration
from submissions.models.Submission import Submission
from omr.models.OMRSheetResult import OMRSheetResult
from omr.models.OMRProcessingJob import OMRProcessingJob
from omr.tasks import process_omr_sheet_task
from OpenSoftCoreV41.usermanager.models.UserType import UserType
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db(databases=['default', 'screen', 'log'])
class TestDeterministicReprocessingAndIdempotency:

    def test_gate9_deterministic_fingerprint_and_idempotency_guard(self):
        """
        Gate 9: Deterministic Reprocessing & Idempotency
        1. Calculate composite SHA-256 fingerprint for identical sheet + exam version.
        2. First run registers completed job and submission.
        3. Second run with identical fingerprint MUST skip redundant processing,
           set status to SKIPPED_IDEMPOTENT, return the existing submission, and produce
           100.0% reproducible byte-level results.
        """
        user_type, _ = UserType.objects.get_or_create(id=2, defaults={'name_ar': 'طالب', 'name_en': 'Student'})
        student = User.objects.create(username="idemp_student_1", first_name="Ali", fk_user_type=user_type)

        year = AcademicYear.objects.create(hijri_year="1448", gregorian_year="2026", is_current=True)
        subject = Subject.objects.create(name_ar="فيزياء", subject_code="PHYS-101")
        exam = Exam.objects.create(title="اختبار الحتمية والتكرار", uniqueCode="EXAM-IDEMP-01", year=year, subject=subject)
        version = ExamVersion.objects.create(exam=exam, versionCode="A")
        reg = StudentExamRegistration.objects.create(student=student, examVersion=version, seatNumber="777001")

        raw_sheet_bytes = b"FAKE_SYNTHETIC_OMR_IMAGE_DATA_FOR_IDEMPOTENCY_VERIFICATION"
        source_hash = hashlib.sha256(raw_sheet_bytes).hexdigest()

        fingerprint = OMRProcessingJob.calculate_fingerprint(
            source_file_hash=source_hash,
            version_id=str(version.id),
            pipeline_ver="3.0",
            model_ver="1.0"
        )

        # 1. First execution: Job completes
        sub1 = Submission.objects.create(
            exam=exam,
            exam_version=version,
            registration=reg,
            status=Submission.Status.COMPLETED,
            mcq_score=Decimal("18.0"),
            total_score=Decimal("18.0"),
            overall_confidence=0.99
        )

        job1 = OMRProcessingJob.objects.create(
            source_file_hash=source_hash,
            processing_fingerprint=fingerprint,
            status=OMRProcessingJob.Status.COMPLETED,
            submission=sub1,
            result_summary={"score": 18.0, "confidence": 0.99, "status": "completed"},
            started_at=timezone.now(),
            completed_at=timezone.now(),
            worker_id="worker_alpha"
        )

        # 2. Second execution attempt with identical payload
        job2 = OMRProcessingJob.objects.create(
            source_file_hash=source_hash,
            processing_fingerprint=fingerprint,
            status=OMRProcessingJob.Status.PENDING
        )

        # Run task
        res = process_omr_sheet_task(
            file_bytes_hex=raw_sheet_bytes.hex(),
            exam_id=exam.id,
            version_id=version.id,
            job_id=str(job2.job_id)
        )

        # Verify idempotency
        assert res["status"] == "idempotent_skipped"
        assert res["submission_id"] == sub1.id

        job2.refresh_from_db()
        assert job2.status == OMRProcessingJob.Status.SKIPPED_IDEMPOTENT
        assert job2.submission_id == sub1.id
        assert job2.result_summary == job1.result_summary

        # Verify no duplicate submission was created in the database
        assert Submission.objects.filter(exam=exam).count() == 1
