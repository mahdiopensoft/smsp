import os
import hashlib
import logging
from celery import shared_task
from django.utils import timezone
from django.db import transaction
from omr.models.OMRProcessingJob import OMRProcessingJob
from submissions.models.Submission import Submission

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def process_omr_sheet_task(
    self,
    file_bytes_hex: str,
    exam_id: int,
    version_id: int = None,
    batch_id: int = None,
    job_id: str = None,
    pipeline_version: str = "3.0",
    model_version: str = "1.0",
):
    """
    Celery worker task for deterministic, asynchronous, idempotent OMR sheet processing.
    Guarantees no duplicate execution for the same composite fingerprint.
    """
    file_bytes = bytes.fromhex(file_bytes_hex)
    source_file_hash = hashlib.sha256(file_bytes).hexdigest()
    v_str = str(version_id) if version_id else "auto"
    fingerprint = OMRProcessingJob.calculate_fingerprint(
        source_file_hash=source_file_hash,
        version_id=v_str,
        pipeline_ver=pipeline_version,
        model_ver=model_version
    )

    job = None
    if job_id:
        job = OMRProcessingJob.objects.filter(job_id=job_id).first()

    # 1. Idempotency Check (Gate 9)
    existing_job = OMRProcessingJob.objects.filter(
        processing_fingerprint=fingerprint,
        status=OMRProcessingJob.Status.COMPLETED,
        is_deleted=False
    ).select_related('submission').first()

    if existing_job and existing_job.submission:
        logger.info(f"Idempotent hit for fingerprint {fingerprint}. Reusing submission {existing_job.submission_id}")
        if job:
            job.status = OMRProcessingJob.Status.SKIPPED_IDEMPOTENT
            job.submission = existing_job.submission
            job.result_summary = existing_job.result_summary
            job.completed_at = timezone.now()
            job.save(update_fields=['status', 'submission', 'result_summary', 'completed_at'])
        return {
            "status": "idempotent_skipped",
            "submission_id": existing_job.submission_id,
            "result_summary": existing_job.result_summary
        }

    if not job:
        job = OMRProcessingJob.objects.create(
            batch_id=batch_id,
            source_file_hash=source_file_hash,
            processing_fingerprint=fingerprint,
            status=OMRProcessingJob.Status.PROCESSING,
            started_at=timezone.now(),
            worker_id=getattr(self.request, 'hostname', 'local_worker')
        )
    else:
        job.status = OMRProcessingJob.Status.PROCESSING
        job.started_at = timezone.now()
        job.worker_id = getattr(self.request, 'hostname', 'local_worker')
        job.save(update_fields=['status', 'started_at', 'worker_id'])

    try:
        from omr.providers.opencv_omr import OpenCVOMREngine
        from exams.models.Exam import Exam
        from exams.models.ExamVersion import ExamVersion

        exam_obj = Exam.objects.get(id=exam_id)
        version_obj = ExamVersion.objects.filter(id=version_id).first() if version_id else None

        engine = OpenCVOMREngine()
        # Verify frozen answer key
        if version_obj:
            if not version_obj.verify_key_integrity():
                raise ValueError("CRITICAL_INTEGRITY_VIOLATION: مفتاح الإجابة غير مطابق للبصمة المشفرة")

        # Process sheet
        raw_result = engine.process_omr(file_bytes, filename="async_sheet.jpg")

        with transaction.atomic():
            sub = Submission.objects.create(
                exam=exam_obj,
                exam_version=version_obj,
                batch_id=batch_id,
                status=Submission.Status.COMPLETED if raw_result.get("overall_confidence", 0) > 0.8 else Submission.Status.NEEDS_REVIEW,
                overall_confidence=raw_result.get("overall_confidence", 0.95),
                omr_result=raw_result.get("questions", []),
                layout_result=raw_result
            )
            job.submission = sub
            job.status = OMRProcessingJob.Status.COMPLETED
            job.completed_at = timezone.now()
            job.result_summary = {
                "score": float(sub.mcq_score or 0.0),
                "confidence": float(sub.overall_confidence or 0.0),
                "status": sub.status
            }
            job.save(update_fields=['submission', 'status', 'completed_at', 'result_summary'])

        return {
            "status": "success",
            "submission_id": sub.id,
            "job_id": str(job.job_id)
        }

    except Exception as exc:
        logger.exception(f"OMR processing failed for job {job.job_id}: {exc}")
        job.status = OMRProcessingJob.Status.FAILED
        job.error_details = str(exc)
        job.completed_at = timezone.now()
        job.retry_count += 1
        job.save(update_fields=['status', 'error_details', 'completed_at', 'retry_count'])
        if self.request.retries < self.max_retries:
            raise self.retry(exc=exc, countdown=2 ** self.request.retries)
        raise exc
