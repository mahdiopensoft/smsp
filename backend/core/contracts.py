"""
Data Contracts — Pydantic models for inter-engine communication.

Each engine in the pipeline communicates through these standardized
data contracts. This ensures type safety, validation, and serialization
across the entire pipeline.

These contracts match the JSON structures defined in the project
specification document (1.md sections 5.1–5.8).
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, field_validator
import uuid


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    NEEDS_REVIEW = "needs_review"
    REVIEWED = "reviewed"


class ConfidenceDecision(str, Enum):
    AUTO_ACCEPT = "automatic_accept"
    QUICK_REVIEW = "quick_review"
    FULL_REVIEW = "full_review"
    REJECT = "reject"


class BubbleState(str, Enum):
    """Classification of a bubble mark state by OMR engine."""
    EMPTY = "empty"
    FILLED = "filled"
    ERASED = "erased"
    CROSSED = "crossed"
    AMBIGUOUS = "ambiguous"


# ---------------------------------------------------------------------------
# Template Contracts
# ---------------------------------------------------------------------------

class RegionContract(BaseModel):
    """Bounding box for a region, in mm, relative to the fiducial coordinate system."""
    dx_mm: float
    dy_mm: float
    width_mm: float
    height_mm: float
    reference_frame: str = "fiducial_space"


class FiducialMark(BaseModel):
    """A single fiducial anchor point on the paper (Absolute or Reference mm)."""
    id: str  # e.g., "TL", "TR", "BL", "BR"
    x_mm: float
    y_mm: float
    width_mm: float
    height_mm: float
    type: str = "square"  # e.g., "nested_square", "timing_mark"


class MCQChoice(BaseModel):
    """A single bubble choice with geometric safe zones."""
    bubble_id: str  # e.g., "Q1_A"
    choice: str  # "A", "B", "C", "D"
    bubble_region: RegionContract
    safe_region: RegionContract
    expanded_region: RegionContract


class MCQQuestion(BaseModel):
    """MCQ question definition with bubble regions."""
    question_id: int
    choices: List[MCQChoice]


class EssayRegion(BaseModel):
    """Handwriting region for an essay question."""
    question_id: int
    region: RegionContract


class TemplateContract(BaseModel):
    """
    Complete template manifest for an exam paper.
    Coordinates are relative to fiducial marks, NOT page edges.
    """
    template_id: str
    template_hash: Optional[str] = None
    version: str = "1.0"
    expected_scan_dpi: int = 300
    paper_size: str = "A4"
    alignment_strategy: str = "homography"
    
    fiducial_marks: List[FiducialMark]
    barcode_region: Optional[RegionContract] = None
    mcq_questions: List[MCQQuestion] = Field(default_factory=list)
    essay_regions: List[EssayRegion] = Field(default_factory=list)

    @field_validator("fiducial_marks")
    @classmethod
    def validate_fiducials(cls, v):
        if len(v) < 3:
            raise ValueError("Template must have at least 3 fiducial marks for alignment")
        return v


# ---------------------------------------------------------------------------
# Alignment Engine Contract
# ---------------------------------------------------------------------------

class AlignmentResult(BaseModel):
    """Output from the Alignment Engine."""
    status: str = "success"
    confidence: float = 0.0
    homography_matrix: Optional[List[List[float]]] = None
    transformed_image_path: Optional[str] = None
    rotation_angle: float = 0.0
    fiducials_detected: int = 0


# ---------------------------------------------------------------------------
# Layout Engine Contract
# ---------------------------------------------------------------------------

class DetectedRegion(BaseModel):
    """A region detected by the Layout Engine."""
    region_type: str  # "barcode", "mcq_area", "essay_area", "header"
    region: RegionContract
    confidence: float = 0.0


class LayoutResult(BaseModel):
    """Output from the Layout Engine."""
    status: str = "success"
    confidence: float = 0.0
    barcode_value: Optional[str] = None
    template_id: Optional[str] = None
    student_id: Optional[str] = None
    detected_regions: List[DetectedRegion] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# OMR Engine Contract
# ---------------------------------------------------------------------------

class OMRQuestionResult(BaseModel):
    """OMR result for a single MCQ question."""
    question_id: int
    marked_choice: Optional[str] = None  # "A", "B", "C", "D" or None
    bubble_state: BubbleState = BubbleState.EMPTY
    choice_confidences: Dict[str, float] = Field(default_factory=dict)
    final_confidence: float = 0.0
    method_used: str = ""


class OMRResult(BaseModel):
    """Output from the OMR Engine for all MCQ questions."""
    status: str = "success"
    confidence: float = 0.0
    questions: List[OMRQuestionResult] = Field(default_factory=list)
    total_questions: int = 0
    answered_questions: int = 0
    provider_used: str = ""


# ---------------------------------------------------------------------------
# HTR Engine Contract
# ---------------------------------------------------------------------------

class WordConfidence(BaseModel):
    """Confidence for a single recognized word."""
    word: str
    confidence: float


class HTRQuestionResult(BaseModel):
    """HTR result for a single essay question."""
    question_id: int
    extracted_text: str = ""
    word_confidences: List[WordConfidence] = Field(default_factory=list)
    overall_confidence: float = 0.0
    model_used: str = ""
    language_detected: str = ""


class HTRResult(BaseModel):
    """Output from the HTR Engine for all essay questions."""
    status: str = "success"
    confidence: float = 0.0
    questions: List[HTRQuestionResult] = Field(default_factory=list)
    provider_used: str = ""


# ---------------------------------------------------------------------------
# Rubric Contract
# ---------------------------------------------------------------------------

class RubricCriterion(BaseModel):
    """A single grading criterion within a rubric."""
    name: str  # e.g., "definition", "reason", "example"
    description: str
    points: float


class RubricContract(BaseModel):
    """Rubric for evaluating an essay question."""
    question_id: int
    max_score: float
    criteria: List[RubricCriterion]


# ---------------------------------------------------------------------------
# LLM Judge Contract
# ---------------------------------------------------------------------------

class JudgeResult(BaseModel):
    """Output from the LLM Judge for a single essay question."""
    question_id: int
    score: float
    max_score: float
    criteria_scores: Dict[str, float] = Field(default_factory=dict)
    reasoning: str = ""
    confidence: float = 0.0
    model_used: str = ""


class JudgeFullResult(BaseModel):
    """Output from the LLM Judge for all essay questions."""
    status: str = "success"
    confidence: float = 0.0
    questions: List[JudgeResult] = Field(default_factory=list)
    provider_used: str = ""


# ---------------------------------------------------------------------------
# Confidence Engine Contract
# ---------------------------------------------------------------------------

class ConfidenceBreakdown(BaseModel):
    """Breakdown of confidence scores from each engine."""
    alignment: float = 0.0
    omr: float = 0.0
    htr: float = 0.0
    judge: float = 0.0


class ConfidenceResult(BaseModel):
    """Output from the Confidence Engine."""
    overall_confidence: float = 0.0
    decision: ConfidenceDecision = ConfidenceDecision.FULL_REVIEW
    breakdown: ConfidenceBreakdown = Field(default_factory=ConfidenceBreakdown)
    flags: List[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Audit Contract
# ---------------------------------------------------------------------------

class AuditPayload(BaseModel):
    """Complete audit record for a single submission."""
    audit_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    submission_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    original_image_url: Optional[str] = None
    aligned_image_url: Optional[str] = None
    alignment_result: Optional[dict] = None
    omr_result: Optional[dict] = None
    htr_result: Optional[dict] = None
    judge_result: Optional[dict] = None
    confidence_result: Optional[dict] = None
    final_grade: Optional[float] = None
    reviewer_id: Optional[str] = None
    human_changes: Optional[dict] = None
    processing_time_ms: float = 0.0


# ---------------------------------------------------------------------------
# Final Grade Contract
# ---------------------------------------------------------------------------

class FinalGradeResult(BaseModel):
    """Aggregated final grade for a submission."""
    submission_id: str
    student_id: str
    exam_id: str
    mcq_score: float = 0.0
    mcq_max: float = 0.0
    essay_score: float = 0.0
    essay_max: float = 0.0
    total_score: float = 0.0
    total_max: float = 0.0
    percentage: float = 0.0
    confidence: float = 0.0
    decision: ConfidenceDecision = ConfidenceDecision.FULL_REVIEW
    needs_review: bool = False
