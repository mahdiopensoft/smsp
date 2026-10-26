import logging
from decimal import Decimal
from typing import Dict, Any, List
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from submissions.models.Submission import Submission
from submissions.models.SubmissionPage import SubmissionPage
from omr.models.OMRSheetResult import OMRSheetResult
from omr.models.OMRQuestionResult import OMRQuestionResult

logger = logging.getLogger(__name__)

class SubmissionAggregationService:
    """
    Deterministic multi-page submission aggregation service.
    Aggregates page-level results into a unified submission result,
    guaranteeing zero silent overwrites, question collision detection,
    and complete page integrity verification.
    """

    @classmethod
    @transaction.atomic
    def register_page(
        cls,
        submission: Submission,
        page_number: int,
        sheet_result: OMRSheetResult,
        source_file_hash: str = "",
        processing_fingerprint: str = "",
        image=None,
        aligned_image=None,
        layout_result: Dict[str, Any] = None,
        omr_result: List[Dict[str, Any]] = None,
    ) -> SubmissionPage:
        """
        Registers or updates a page for a submission and triggers deterministic aggregation.
        """
        page, _ = SubmissionPage.objects.update_or_create(
            submission=submission,
            page_number=page_number,
            is_deleted=False,
            defaults={
                "sheet_result": sheet_result,
                "source_file_hash": source_file_hash,
                "processing_fingerprint": processing_fingerprint,
                "page_score": sheet_result.mcq_score if sheet_result else Decimal("0.0"),
                "status": "completed" if (sheet_result and sheet_result.status == "verified") else "needs_review",
                "layout_result": layout_result or {},
                "omr_result": omr_result or [],
            }
        )
        if image:
            page.image = image
        if aligned_image:
            page.aligned_image = aligned_image
        page.save()

        # Aggregate full submission
        cls.aggregate_submission(submission)
        return page

    @classmethod
    @transaction.atomic
    def aggregate_submission(cls, submission: Submission) -> Submission:
        """
        Aggregates all pages for a submission, verifies completeness,
        checks for question collisions, and sets the final verified score and status.
        """
        pages = submission.pages.filter(is_deleted=False).order_by('page_number')
        page_count = pages.count()

        # 1. Verification of page count
        has_missing_pages = page_count < submission.expected_pages

        seen_questions = set()
        duplicate_questions = set()
        total_score = Decimal("0.0")
        max_possible_score = Decimal("0.0")
        total_questions = 0
        total_correct = 0
        total_wrong = 0
        total_unanswered = 0
        total_ambiguous = 0
        confidences = []
        has_page_review = False
        all_question_data = []

        for page in pages:
            if page.sheet_result:
                sr = page.sheet_result
                if sr.confidence is not None:
                    confidences.append(float(sr.confidence))
                if sr.status != "verified":
                    has_page_review = True

                for q in sr.questions.all().order_by('question_number'):
                    q_num = q.question_number
                    if q_num in seen_questions:
                        duplicate_questions.add(q_num)
                    else:
                        seen_questions.add(q_num)

                    weight = Decimal(str(q.assigned_weight or 1.0))
                    max_possible_score += weight
                    total_questions += 1

                    if q.is_correct:
                        total_score += weight
                        total_correct += 1
                    elif q.final_marked_choice is not None:
                        total_wrong += 1
                    else:
                        total_unanswered += 1

                    if q.needs_review:
                        total_ambiguous += 1
                        has_page_review = True

                    all_question_data.append({
                        "question_number": q_num,
                        "candidate_choice": q.candidate_choice,
                        "final_marked_choice": q.final_marked_choice,
                        "is_correct": q.is_correct,
                        "assigned_weight": float(weight),
                        "page_number": page.page_number,
                    })

        # Calculate average confidence
        avg_confidence = sum(confidences) / len(confidences) if confidences else 1.0

        # Determine submission status
        error_messages = []
        if has_missing_pages:
            error_messages.append(
                f"MISSING_PAGES: تم استلام {page_count} من أصل {submission.expected_pages} صفحة."
            )
        if duplicate_questions:
            sorted_dups = sorted(list(duplicate_questions))
            error_messages.append(
                f"QUESTION_COLLISION: تضارب في أرقام الأسئلة بين الصفحات: {sorted_dups}"
            )
        if submission.error_message and not submission.error_message.startswith("MISSING_PAGES"):
            error_messages.append(submission.error_message)

        if error_messages or has_page_review or has_missing_pages or duplicate_questions:
            submission.status = Submission.Status.NEEDS_REVIEW
        else:
            submission.status = Submission.Status.COMPLETED

        submission.mcq_score = total_score
        submission.total_score = total_score
        submission.overall_confidence = avg_confidence
        submission.omr_result = all_question_data
        submission.error_message = " | ".join(error_messages) if error_messages else ""

        submission.save(update_fields=[
            'status', 'mcq_score', 'total_score', 'overall_confidence',
            'omr_result', 'error_message'
        ])
        return submission
