import pytest
from omr.providers.decision_matrix import evaluate_question_bubbles

def test_clean_unanswered_question():
    states = {"A": "empty", "B": "empty", "C": "empty", "D": "empty"}
    res = evaluate_question_bubbles(states)
    assert res.candidate_choice is None
    assert res.final_marked_choice is None
    assert res.bubble_state == "empty"
    assert res.needs_review is False
    assert res.decision_confidence == 1.0
    assert res.review_priority == "NONE"

def test_single_filled_choice_auto_grades():
    states = {"A": "empty", "B": "filled", "C": "empty", "D": "empty"}
    confs = {"A": 0.99, "B": 0.95, "C": 0.99, "D": 0.99}
    res = evaluate_question_bubbles(states, vision_confidences=confs)
    assert res.candidate_choice == "B"
    assert res.final_marked_choice == "B"
    assert res.bubble_state == "filled"
    assert res.needs_review is False
    assert res.decision_confidence == 1.0
    assert res.review_priority == "NONE"

def test_single_half_filled_requires_review_without_silent_grading():
    states = {"A": "empty", "B": "half_filled", "C": "empty", "D": "empty"}
    res = evaluate_question_bubbles(states)
    assert res.candidate_choice == "B"
    assert res.final_marked_choice is None  # Must NOT be auto-graded!
    assert res.bubble_state == "half_filled"
    assert res.needs_review is True
    assert res.review_priority == "MEDIUM"
    assert res.reason_code == "HALF_FILLED_ACCEPTED"

def test_single_crossed_choice_never_auto_marked():
    states = {"A": "empty", "B": "crossed", "C": "empty", "D": "empty"}
    res = evaluate_question_bubbles(states)
    assert res.candidate_choice == "B"
    assert res.final_marked_choice is None  # NEVER auto-marked!
    assert res.bubble_state == "crossed"
    assert res.needs_review is True
    assert res.review_priority == "CRITICAL"
    assert res.reason_code == "CROSSED_INTENT_CLEAR"

def test_crossed_plus_filled_flags_for_review_with_filled_candidate():
    states = {"A": "crossed", "B": "filled", "C": "empty", "D": "empty"}
    res = evaluate_question_bubbles(states)
    assert res.candidate_choice == "B"
    assert res.final_marked_choice is None  # Must wait for human confirmation
    assert res.bubble_state == "ambiguous"
    assert res.needs_review is True
    assert res.review_priority == "HIGH"
    assert res.reason_code == "CROSSED_INTENT_CLEAR"

def test_multiple_filled_bubbles():
    states = {"A": "filled", "B": "filled", "C": "empty", "D": "empty"}
    res = evaluate_question_bubbles(states)
    assert res.candidate_choice is None
    assert res.final_marked_choice is None
    assert res.bubble_state == "multiple"
    assert res.needs_review is True
    assert res.review_priority == "CRITICAL"
    assert res.reason_code == "MULTIPLE_RESOLVED"

def test_filled_plus_half_filled():
    states = {"A": "half_filled", "B": "filled", "C": "empty", "D": "empty"}
    res = evaluate_question_bubbles(states)
    assert res.candidate_choice == "B"
    assert res.final_marked_choice is None
    assert res.bubble_state == "ambiguous"
    assert res.needs_review is True
    assert res.review_priority == "HIGH"

def test_vision_uncertain_on_invalid_roi():
    states = {"A": "empty", "B": "empty", "C": "empty", "D": "empty"}
    res = evaluate_question_bubbles(states, roi_valid=False)
    assert res.bubble_state == "vision_uncertain"
    assert res.needs_review is True
    assert res.review_priority == "CRITICAL"
    assert res.reason_code == "VISION_ERROR"

def test_vision_uncertain_on_collapsed_classifier_confidence():
    states = {"A": "empty", "B": "filled", "C": "empty", "D": "empty"}
    confs = {"A": 0.99, "B": 0.15, "C": 0.99, "D": 0.99}  # B is 0.15 < 0.30
    res = evaluate_question_bubbles(states, vision_confidences=confs)
    assert res.bubble_state == "vision_uncertain"
    assert res.needs_review is True
    assert res.review_priority == "CRITICAL"
    assert res.reason_code == "VISION_ERROR"
