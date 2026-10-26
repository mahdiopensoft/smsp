"""
Standalone Bubble Decision Matrix for OMR Exam Grading.
Pure-function rule engine decoupled from Computer Vision / OpenCV code.
Strictly enforces the Zero Silent Scoring Errors principle.
"""

from typing import Dict, Any, List, Optional

class DecisionMatrixResult:
    def __init__(
        self,
        candidate_choice: Optional[str],
        final_marked_choice: Optional[str],
        bubble_state: str,
        vision_confidence: float,
        decision_confidence: float,
        needs_review: bool,
        review_priority: str,
        reason_code: Optional[str] = None
    ):
        self.candidate_choice = candidate_choice
        self.final_marked_choice = final_marked_choice
        self.bubble_state = bubble_state
        self.vision_confidence = vision_confidence
        self.decision_confidence = decision_confidence
        self.needs_review = needs_review
        self.review_priority = review_priority
        self.reason_code = reason_code

    def to_dict(self) -> Dict[str, Any]:
        return {
            "candidate_choice": self.candidate_choice,
            "final_marked_choice": self.final_marked_choice,
            "bubble_state": self.bubble_state,
            "vision_confidence": round(self.vision_confidence, 4),
            "decision_confidence": round(self.decision_confidence, 4),
            "needs_review": self.needs_review,
            "review_priority": self.review_priority,
            "reason_code": self.reason_code,
        }

def evaluate_question_bubbles(
    choice_states: Dict[str, str],
    vision_confidences: Optional[Dict[str, float]] = None,
    darkness_values: Optional[Dict[str, float]] = None,
    roi_valid: bool = True,
    min_vision_threshold: float = 0.30
) -> DecisionMatrixResult:
    """
    Evaluates bubble markings for a single question based on official exam regulations.
    
    Args:
        choice_states: Mapping of label -> state ('empty', 'filled', 'half_filled', 'crossed', 'erased')
        vision_confidences: Mapping of label -> float [0.0 - 1.0] from CV/YOLO model
        darkness_values: Mapping of label -> float [0.0 - 1.0] physical darkness/fill ratio
        roi_valid: Whether the question's bounding boxes / ROIs passed geometric sanity check
        min_vision_threshold: Minimum allowable vision model confidence before triggering VISION_UNCERTAIN
        
    Returns:
        DecisionMatrixResult
    """
    if vision_confidences is None:
        vision_confidences = {}
    if darkness_values is None:
        darkness_values = {}

    # Calculate average vision confidence across choices
    if vision_confidences:
        avg_vision_conf = sum(vision_confidences.values()) / max(1, len(vision_confidences))
    else:
        avg_vision_conf = 1.0

    # ── Rule 1: Vision / Geometric Failure (Zero Silent Error Guard) ─────────────
    # If the ROI was torn, unaligned, or classifier confidence collapsed below threshold
    if not roi_valid:
        return DecisionMatrixResult(
            candidate_choice=None,
            final_marked_choice=None,
            bubble_state="vision_uncertain",
            vision_confidence=0.0,
            decision_confidence=0.0,
            needs_review=True,
            review_priority="CRITICAL",
            reason_code="VISION_ERROR"
        )

    # Check for severe classifier uncertainty on non-empty candidates
    for choice, state in choice_states.items():
        if state not in ("empty", "erased"):
            c_conf = vision_confidences.get(choice, 1.0)
            if c_conf < min_vision_threshold:
                return DecisionMatrixResult(
                    candidate_choice=choice,
                    final_marked_choice=None,
                    bubble_state="vision_uncertain",
                    vision_confidence=c_conf,
                    decision_confidence=0.0,
                    needs_review=True,
                    review_priority="CRITICAL",
                    reason_code="VISION_ERROR"
                )

    # Segregate markings
    filled_choices  = [lbl for lbl, st in choice_states.items() if st == "filled"]
    half_choices    = [lbl for lbl, st in choice_states.items() if st == "half_filled"]
    crossed_choices = [lbl for lbl, st in choice_states.items() if st == "crossed"]
    erased_choices  = [lbl for lbl, st in choice_states.items() if st == "erased"]

    # ── Rule 2: Clean Unanswered Question ─────────────────────────────────────────
    if not filled_choices and not half_choices and not crossed_choices:
        return DecisionMatrixResult(
            candidate_choice=None,
            final_marked_choice=None,
            bubble_state="erased" if erased_choices else "empty",
            vision_confidence=avg_vision_conf,
            decision_confidence=1.0,
            needs_review=False,
            review_priority="NONE"
        )

    # ── Rule 3: Single Clean Filled Bubble (Unambiguous auto-grade) ───────────────
    if len(filled_choices) == 1 and not half_choices and not crossed_choices:
        choice = filled_choices[0]
        v_conf = vision_confidences.get(choice, 1.0)
        return DecisionMatrixResult(
            candidate_choice=choice,
            final_marked_choice=choice,
            bubble_state="filled",
            vision_confidence=v_conf,
            decision_confidence=1.0,
            needs_review=False,
            review_priority="NONE"
        )

    # ── Rule 4: Single Half Filled Bubble (Faint or incomplete shading) ───────────
    if len(half_choices) == 1 and not filled_choices and not crossed_choices:
        choice = half_choices[0]
        v_conf = vision_confidences.get(choice, 0.70)
        return DecisionMatrixResult(
            candidate_choice=choice,
            final_marked_choice=None,  # Forbidden to auto-grade faint bubbles!
            bubble_state="half_filled",
            vision_confidence=v_conf,
            decision_confidence=0.50,
            needs_review=True,
            review_priority="MEDIUM",
            reason_code="HALF_FILLED_ACCEPTED"
        )

    # ── Rule 5: Single Crossed Bubble (Crossed out without replacement) ───────────
    if len(crossed_choices) == 1 and not filled_choices and not half_choices:
        choice = crossed_choices[0]
        v_conf = vision_confidences.get(choice, 0.85)
        return DecisionMatrixResult(
            candidate_choice=choice,
            final_marked_choice=None,  # NEVER auto-mark a crossed bubble!
            bubble_state="crossed",
            vision_confidence=v_conf,
            decision_confidence=0.20,
            needs_review=True,
            review_priority="CRITICAL",
            reason_code="CROSSED_INTENT_CLEAR"
        )

    # ── Rule 6: Crossed + Filled (Student crossed one choice and filled another) ───
    if len(crossed_choices) >= 1 and len(filled_choices) == 1:
        filled_choice = filled_choices[0]
        v_conf = vision_confidences.get(filled_choice, 0.85)
        return DecisionMatrixResult(
            candidate_choice=filled_choice,
            final_marked_choice=None,  # Human review must confirm student's intent
            bubble_state="ambiguous",
            vision_confidence=v_conf,
            decision_confidence=0.40,
            needs_review=True,
            review_priority="HIGH",
            reason_code="CROSSED_INTENT_CLEAR"
        )

    # ── Rule 7: Crossed + Half Filled ─────────────────────────────────────────────
    if len(crossed_choices) >= 1 and len(half_choices) >= 1 and not filled_choices:
        half_choice = half_choices[0]
        v_conf = vision_confidences.get(half_choice, 0.60)
        return DecisionMatrixResult(
            candidate_choice=half_choice,
            final_marked_choice=None,
            bubble_state="ambiguous",
            vision_confidence=v_conf,
            decision_confidence=0.20,
            needs_review=True,
            review_priority="CRITICAL",
            reason_code="MULTIPLE_RESOLVED"
        )

    # ── Rule 8: Multiple Filled Bubbles (>= 2 Filled) ─────────────────────────────
    if len(filled_choices) >= 2:
        return DecisionMatrixResult(
            candidate_choice=None,
            final_marked_choice=None,
            bubble_state="multiple",
            vision_confidence=avg_vision_conf,
            decision_confidence=0.0,
            needs_review=True,
            review_priority="CRITICAL",
            reason_code="MULTIPLE_RESOLVED"
        )

    # ── Rule 9: Filled + Half Filled (Correction attempt or smudged duplicate) ────
    if len(filled_choices) == 1 and len(half_choices) >= 1:
        filled_choice = filled_choices[0]
        v_conf = vision_confidences.get(filled_choice, 0.85)
        return DecisionMatrixResult(
            candidate_choice=filled_choice,
            final_marked_choice=None,
            bubble_state="ambiguous",
            vision_confidence=v_conf,
            decision_confidence=0.40,
            needs_review=True,
            review_priority="HIGH",
            reason_code="MULTIPLE_RESOLVED"
        )

    # ── Rule 10: Multiple Crossed / Ambiguous Fallback ────────────────────────────
    return DecisionMatrixResult(
        candidate_choice=None,
        final_marked_choice=None,
        bubble_state="multiple" if len(crossed_choices) >= 2 else "ambiguous",
        vision_confidence=avg_vision_conf,
        decision_confidence=0.0,
        needs_review=True,
        review_priority="CRITICAL",
        reason_code="MULTIPLE_RESOLVED"
    )
