"""
config.py — Enterprise OMR & Vision Configuration Contract
==========================================================
Clean, typed, modular configuration dataclasses for Vision, Models,
Physical Ink Density, and Academic Scoring Policies.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional


@dataclass
class VisionConfig:
    """Settings for image standardization, enhancement, and quality guards."""
    bubble_target_size: int = 48
    enable_clahe: bool = True
    clahe_clip_limit: float = 2.0
    adaptive_clahe_tile: bool = True       # Dynamic grid based on crop pixel size
    padding_fill_mode: str = "reflect"      # Prevents ellipse squashing on border crops
    min_bubble_variance: float = 12.0      # Discards pure white or solid artifact crops
    blur_threshold: float = 20.0           # Laplacian variance threshold for blur detection


@dataclass
class ModelConfig:
    """Inference thresholds and fallback policy for YOLOv8 and ResNet CNN."""
    yolo_conf: float = 0.35
    yolo_iou: float = 0.35
    cnn_conf: float = 0.75
    enable_cnn_fallback: bool = True       # Automatically invoke CNN when YOLO finds 0 boxes


@dataclass
class InkConfig:
    """Physical ink density thresholds (Ground Truth Anchor)."""
    filled_threshold: float = 0.22         # Ink area >= 22% considered filled
    empty_threshold: float = 0.08          # Ink area <= 8% considered clean empty
    margin_delta: float = 0.06             # Minimum separation between top candidates


@dataclass
class ScoringPolicyConfig:
    """
    Academic Scoring and Grading Rules.
    Governs how marks are mathematically computed for all regular and edge cases.
    """
    # ── 1. Negative Marking (عقوبة الإجابة الخاطئة) ──
    # Deduction ratio for wrong answers (0.0 = none, 0.25 = 1/4 mark, 0.33 = 1/3 mark, etc.)
    wrong_answer_penalty: float = 0.0

    # Score floor mode:
    # "ALLOW_NEGATIVE"    -> Net negative score allowed to deduct from total exam mark (standard negative marking)
    # "PER_QUESTION_ZERO" -> Question score never drops below 0.0 (safeguard)
    score_floor_mode: str = "ALLOW_NEGATIVE"

    # ── 2. Multiple Marked Choices (تظليل خيارين أو أكثر في سؤال مفرد) ──
    # A) When student marks multiple choices and ONE OF THEM IS CORRECT:
    # "ZERO"          -> Strict disqualification: 0 marks (Official Yemen Ministry standard)
    # "PARTIAL_50"     -> 50% partial credit awarded
    # "SPLIT_PENALTY"  -> Full mark minus penalty for the wrong choice
    # "FLAG_REVIEW"    -> Freeze grade and escalate to Control human review
    multi_choice_policy: str = "ZERO"
    multi_one_correct_policy: Optional[str] = None

    # B) When student marks multiple choices and BOTH ARE WRONG:
    # "ZERO"           -> 0 marks (Standard)
    # "APPLY_PENALTY"  -> Apply wrong answer penalty once (-penalty * mark)
    # "DOUBLE_PENALTY" -> Double penalty for hedging/guessing (-penalty * 2 * mark)
    # "FLAG_REVIEW"    -> Flag for review to inspect potential exam malpractice
    multi_both_wrong_policy: str = "ZERO"

    # ── 3. Crossed-out Choices (الشطب بالقلم وتظليل بديل) ──
    # When student crossed out one choice (X/Slash) and filled another:
    # "ACCEPT_FILLED"  -> Auto-accept filled choice and ignore crossed
    # "FLAG_REVIEW"    -> Escalate to Control to verify student intent
    # "DISQUALIFY"     -> Treat as multiple fill (0 marks)
    crossed_choice_policy: str = "ACCEPT_FILLED"

    # ── 4. Erased Choices (المسح بالممحاة) ──
    # When student erased an earlier choice and marked a new one:
    # "ACCEPT_FILLED"  -> Auto-accept newly filled choice and ignore eraser ghost
    # "FLAG_REVIEW"    -> Escalate to human review if eraser residue is dark
    erased_choice_policy: str = "ACCEPT_FILLED"

    # ── 5. Blank / Unanswered Questions (الأسئلة المتروكة فارغة) ──
    # Penalty for leaving question blank (normally 0.0, unless competitive exam penalty applies)
    blank_answer_penalty: float = 0.0

    # ── 6. Faint / Hesitant Marks (التظليل الباهت أو النصف ممتلئ) ──
    # "FLAG_REVIEW"    -> Escalate to human review so student is not penalized for faint pencil
    # "REJECT_EMPTY"   -> Treat as empty (0 marks)
    half_filled_policy: str = "FLAG_REVIEW"


@dataclass
class OMRConfig:
    """Master Unified Configuration object."""
    vision: VisionConfig = field(default_factory=VisionConfig)
    model: ModelConfig = field(default_factory=ModelConfig)
    ink: InkConfig = field(default_factory=InkConfig)
    scoring: ScoringPolicyConfig = field(default_factory=ScoringPolicyConfig)

    @classmethod
    def from_template(cls, template_data: Optional[Dict[str, Any]] = None) -> "OMRConfig":
        """Builds configuration with template-specific overrides if provided."""
        config = cls()
        if not template_data or not isinstance(template_data, dict):
            return config

        overrides = template_data.get("omr_config", {})
        if not isinstance(overrides, dict):
            return config

        # Apply Vision overrides
        for k, v in overrides.get("vision", {}).items():
            if hasattr(config.vision, k):
                setattr(config.vision, k, v)

        # Apply Model overrides
        for k, v in overrides.get("model", {}).items():
            if hasattr(config.model, k):
                setattr(config.model, k, v)

        # Apply Ink overrides
        for k, v in overrides.get("ink", {}).items():
            if hasattr(config.ink, k):
                setattr(config.ink, k, v)

        # Apply Scoring overrides
        for k, v in overrides.get("scoring", {}).items():
            if hasattr(config.scoring, k):
                setattr(config.scoring, k, v)

        return config

    def to_dict(self) -> Dict[str, Any]:
        """Serialize configuration to a nested dictionary."""
        return asdict(self)
