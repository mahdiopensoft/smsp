"""
grading_policy.py — Academic Scoring Policy Engine
==================================================
Deterministic, mathematically sound calculation of question scores
based on academic policies (negative marking, multiple fills, crossed-out marks).
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from .config import ScoringPolicyConfig


@dataclass
class GradingDecision:
    """Result of grading a single question under the active policy."""
    marks_awarded: float
    is_correct: Optional[bool]
    status_code: str
    needs_review: bool
    explanation: str


def evaluate_question_score(
    marked_choice: Optional[str],
    all_marked_choices: List[str],
    bubble_state: str,
    correct_choice: Optional[str],
    max_mark: float,
    policy: Optional[ScoringPolicyConfig] = None
) -> GradingDecision:
    """
    Computes marks and evaluation status for a single question.
    """
    if policy is None:
        policy = ScoringPolicyConfig()

    max_mark = float(max_mark)

    # 1. Blank / Unanswered Question
    if not marked_choice and not all_marked_choices:
        penalty = float(policy.blank_answer_penalty) * max_mark
        marks = round(-penalty, 2) if penalty > 0 else 0.0
        return GradingDecision(
            marks_awarded=marks,
            is_correct=False,
            status_code="BLANK",
            needs_review=False,
            explanation="السؤال متروك فارغاً بدون تظليل."
        )

    # Normalize choices for safe comparison
    norm_correct = str(correct_choice).strip().upper() if correct_choice else None
    norm_marked = str(marked_choice).strip().upper() if marked_choice else None
    norm_all = [str(c).strip().upper() for c in all_marked_choices]

    # 2. Multiple Marked Bubbles (>= 2 choices filled)
    if len(norm_all) >= 2 or bubble_state == "multiple":
        is_correct_in_multi = (norm_correct in norm_all) if norm_correct else False

        one_correct_pol = policy.multi_one_correct_policy if policy.multi_one_correct_policy is not None else policy.multi_choice_policy
        both_wrong_pol = getattr(policy, "multi_both_wrong_policy", "ZERO") or "ZERO"

        if is_correct_in_multi:
            # ── Sub-case 2.1: One of the marked choices IS CORRECT ──
            if one_correct_pol == "PARTIAL_50":
                partial_mark = round(max_mark * 0.50, 2)
                return GradingDecision(
                    marks_awarded=partial_mark,
                    is_correct=True,
                    status_code="MULTI_PARTIAL_50",
                    needs_review=True,
                    explanation=f"تظليل خيارين أحدهما صحيح: مُنح نصف الدرجة ({partial_mark}/{max_mark})."
                )
            elif one_correct_pol == "FLAG_REVIEW":
                return GradingDecision(
                    marks_awarded=0.0,
                    is_correct=None,
                    status_code="MULTI_FLAGGED",
                    needs_review=True,
                    explanation="تظليل متعدد معلّق (أحدهما صحيح): بانتظار قرار المصحح البشري في الكنترول."
                )
            elif one_correct_pol == "SPLIT_PENALTY":
                penalty = float(policy.wrong_answer_penalty) * max_mark
                net_mark = max(0.0, round(max_mark - penalty, 2))
                return GradingDecision(
                    marks_awarded=net_mark,
                    is_correct=True,
                    status_code="MULTI_SPLIT_PENALTY",
                    needs_review=True,
                    explanation=f"تظليل متعدد مع خصم عقوبة الخطأ: {net_mark}/{max_mark}."
                )
            else:
                # Strict standard: ZERO (Default Yemen Ministry Rule)
                return GradingDecision(
                    marks_awarded=0.0,
                    is_correct=False,
                    status_code="MULTI_DISQUALIFIED",
                    needs_review=True,
                    explanation="تظليل خيارات متعددة (بينها إجابة صحيحة): إلغاء وتصفير السؤال وفق اللائحة الوزارية."
                )
        else:
            # ── Sub-case 2.2: BOTH marked choices ARE WRONG ──
            if both_wrong_pol == "APPLY_PENALTY":
                penalty = float(policy.wrong_answer_penalty) * max_mark
                marks = round(-penalty, 2) if penalty > 0 else 0.0
                if getattr(policy, "score_floor_mode", "ALLOW_NEGATIVE") == "PER_QUESTION_ZERO":
                    marks = max(0.0, marks)
                return GradingDecision(
                    marks_awarded=marks,
                    is_correct=False,
                    status_code="MULTI_BOTH_WRONG_PENALTY",
                    needs_review=False,
                    explanation=f"تظليل خيارين كلاهما خاطئ: تم تطبيق عقوبة الإجابة الخاطئة ({marks})."
                )
            elif both_wrong_pol == "DOUBLE_PENALTY":
                penalty = float(policy.wrong_answer_penalty) * 2 * max_mark
                marks = round(-penalty, 2) if penalty > 0 else 0.0
                if getattr(policy, "score_floor_mode", "ALLOW_NEGATIVE") == "PER_QUESTION_ZERO":
                    marks = max(0.0, marks)
                return GradingDecision(
                    marks_awarded=marks,
                    is_correct=False,
                    status_code="MULTI_DOUBLE_PENALTY",
                    needs_review=True,
                    explanation=f"تظليل خيارات متعددة خاطئة: تم تطبيق عقوبة مضاعفة ({marks}) لشبهة التحايل."
                )
            elif both_wrong_pol == "FLAG_REVIEW":
                return GradingDecision(
                    marks_awarded=0.0,
                    is_correct=False,
                    status_code="MULTI_BOTH_WRONG_FLAGGED",
                    needs_review=True,
                    explanation="تظليل خيارين كلاهما خاطئ: محال للمراجعة للتحقق من أسباب تكرار التظليل."
                )
            else:
                # Default ZERO
                return GradingDecision(
                    marks_awarded=0.0,
                    is_correct=False,
                    status_code="MULTI_BOTH_WRONG_ZERO",
                    needs_review=False,
                    explanation="تظليل خيارين كلاهما خاطئ: 0 درجات دون خصم إضافي."
                )

    # 3. Crossed out with alternative choice
    if bubble_state == "crossed":
        if policy.crossed_choice_policy == "ACCEPT_FILLED" and norm_marked:
            # Grade the alternative choice
            pass
        elif policy.crossed_choice_policy == "FLAG_REVIEW":
            return GradingDecision(
                marks_awarded=0.0,
                is_correct=None,
                status_code="CROSSED_FLAGGED",
                needs_review=True,
                explanation="إجابة مشطوبة: تتطلب تدقيقاً للتأكد من نية الطالب."
            )

    # 4. Single Marked Choice: Correct or Wrong
    if norm_correct and norm_marked == norm_correct:
        return GradingDecision(
            marks_awarded=max_mark,
            is_correct=True,
            status_code="CORRECT",
            needs_review=False,
            explanation=f"إجابة صحيحة ({norm_marked}): منحت الدرجة كاملة ({max_mark})."
        )
    else:
        penalty = float(policy.wrong_answer_penalty) * max_mark
        marks = round(-penalty, 2) if penalty > 0 else 0.0
        return GradingDecision(
            marks_awarded=marks,
            is_correct=False,
            status_code="WRONG",
            needs_review=False,
            explanation=f"إجابة خاطئة ({norm_marked or '—'} مقابل {norm_correct or '—'}): الدرجة {marks}."
        )
