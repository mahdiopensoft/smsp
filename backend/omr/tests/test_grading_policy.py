"""
test_grading_policy.py — Unit Tests for Academic Scoring Policy Engine
======================================================================
Tests all real academic scenarios: negative marking, multi-mark partial credit,
disqualification, and crossed-out choices.
"""

from omr.config import ScoringPolicyConfig
from omr.grading_policy import evaluate_question_score


def test_standard_scoring():
    policy = ScoringPolicyConfig(wrong_answer_penalty=0.0)

    # 1. Correct answer
    res = evaluate_question_score("A", ["A"], "filled", "A", 2.0, policy)
    assert res.is_correct is True
    assert res.marks_awarded == 2.0
    assert res.status_code == "CORRECT"

    # 2. Wrong answer (no penalty)
    res = evaluate_question_score("B", ["B"], "filled", "A", 2.0, policy)
    assert res.is_correct is False
    assert res.marks_awarded == 0.0
    assert res.status_code == "WRONG"

    # 3. Blank
    res = evaluate_question_score(None, [], "empty", "A", 2.0, policy)
    assert res.is_correct is False
    assert res.marks_awarded == 0.0
    assert res.status_code == "BLANK"
    print("  ✅ Standard scoring passed!")


def test_negative_marking():
    # 25% deduction for wrong answer
    policy = ScoringPolicyConfig(wrong_answer_penalty=0.25)

    # Wrong answer on a 4.0 mark question -> deduction of 1.0 mark
    res = evaluate_question_score("B", ["B"], "filled", "A", 4.0, policy)
    assert res.is_correct is False
    assert res.marks_awarded == -1.0
    assert res.status_code == "WRONG"
    print("  ✅ Negative marking passed!")


def test_multiple_choices_policies():
    # Scenario A: Strict Disqualification (ZERO)
    policy_strict = ScoringPolicyConfig(multi_choice_policy="ZERO")
    res = evaluate_question_score(None, ["A", "B"], "multiple", "A", 2.0, policy_strict)
    assert res.marks_awarded == 0.0
    assert res.status_code == "MULTI_DISQUALIFIED"
    assert res.needs_review is True

    # Scenario B: Partial Credit (50% if correct is among choices)
    policy_partial = ScoringPolicyConfig(multi_choice_policy="PARTIAL_50")
    res_partial = evaluate_question_score(None, ["A", "B"], "multiple", "A", 2.0, policy_partial)
    assert res_partial.marks_awarded == 1.0
    assert res_partial.status_code == "MULTI_PARTIAL_50"
    assert res_partial.needs_review is True

    # Partial credit when correct is NOT among choices -> 0.0
    res_no_correct = evaluate_question_score(None, ["B", "C"], "multiple", "A", 2.0, policy_partial)
    assert res_no_correct.marks_awarded == 0.0
    assert res_no_correct.status_code in ("MULTI_DISQUALIFIED", "MULTI_BOTH_WRONG_ZERO")

    # Scenario D: Both marked choices are WRONG with negative penalty
    policy_penalty = ScoringPolicyConfig(
        wrong_answer_penalty=0.25,
        multi_both_wrong_policy="APPLY_PENALTY"
    )
    res_both_wrong = evaluate_question_score(None, ["B", "C"], "multiple", "A", 4.0, policy_penalty)
    assert res_both_wrong.marks_awarded == -1.0
    assert res_both_wrong.status_code == "MULTI_BOTH_WRONG_PENALTY"

    # Scenario E: Both marked choices are WRONG with double penalty (anti-cheating)
    policy_double = ScoringPolicyConfig(
        wrong_answer_penalty=0.25,
        multi_both_wrong_policy="DOUBLE_PENALTY"
    )
    res_double = evaluate_question_score(None, ["B", "C"], "multiple", "A", 4.0, policy_double)
    assert res_double.marks_awarded == -2.0
    assert res_double.status_code == "MULTI_DOUBLE_PENALTY"

    # Scenario F: Split penalty when one is correct and one is wrong
    policy_split = ScoringPolicyConfig(
        wrong_answer_penalty=0.25,
        multi_one_correct_policy="SPLIT_PENALTY"
    )
    res_split = evaluate_question_score(None, ["A", "B"], "multiple", "A", 4.0, policy_split)
    assert res_split.marks_awarded == 3.0  # 4.0 - (0.25 * 4.0) = 3.0
    assert res_split.status_code == "MULTI_SPLIT_PENALTY"

    # Scenario C: Flag for Human Review
    policy_flag = ScoringPolicyConfig(multi_choice_policy="FLAG_REVIEW")
    res_flag = evaluate_question_score(None, ["A", "B"], "multiple", "A", 2.0, policy_flag)
    assert res_flag.is_correct is None
    assert res_flag.status_code == "MULTI_FLAGGED"
    assert res_flag.needs_review is True
    print("  ✅ Multiple choices policies passed!")


def test_crossed_out_policy():
    policy_accept = ScoringPolicyConfig(crossed_choice_policy="ACCEPT_FILLED")
    # Crossed choice "B", filled alternative "A", correct is "A"
    res = evaluate_question_score("A", ["A"], "crossed", "A", 2.0, policy_accept)
    assert res.is_correct is True
    assert res.marks_awarded == 2.0
    print("  ✅ Crossed out policy passed!")


if __name__ == "__main__":
    print("Running Academic Scoring Engine Tests...")
    test_standard_scoring()
    test_negative_marking()
    test_multiple_choices_policies()
    test_crossed_out_policy()
    print("🎉 ALL SCORING ENGINE TESTS PASSED!")
