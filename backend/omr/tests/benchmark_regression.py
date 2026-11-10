"""
benchmark_regression.py — Baseline Regression Benchmark for OMR Engine
======================================================================
Ensures zero-regression: any changes to normalization, models, or grading
must pass this benchmark before being considered production-ready.
"""

import os
import sys

# Ensure Django environment is initialized
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

from omr.api import _detect_template_from_sheet, _grade_with_template

KIBSI_IMG = "/home/mahdi/.gemini/antigravity/brain/6285f380-24a5-4c5a-8a8a-81e6fff5ded8/.user_uploaded/media_1794151684155_b50a3877.png"
ASEEL_IMG = "/home/mahdi/Desktop/m/NewQuestionBankV4/NewQuestionBank/backend/media/uploads/original/2026/11/قالب_اختبار_مادة_التاريخ_-_الشهادة_الأساسية_الصف_التاسع_-_أمانة_2wXs5px.png"


def run_benchmark():
    print("=" * 60)
    print("OMR REGRESSION BENCHMARK SUITE")
    print("=" * 60)

    # ── Test 1: Ahmad Al-Kibsi Sheet ──
    print("\n[1/2] Testing Ahmad Al-Kibsi Sheet (Seat: 94101)...")
    assert os.path.exists(KIBSI_IMG), f"Missing test image: {KIBSI_IMG}"
    
    detect_res = _detect_template_from_sheet(KIBSI_IMG)
    tpl_obj, model_code, q_count = detect_res
    barcode = getattr(detect_res, 'barcode', '')
    qr = getattr(detect_res, 'qr', '')
    
    print(f"  -> Detected Barcode: {barcode}")
    print(f"  -> Detected QR:      {qr}")
    print(f"  -> Template ID:     {tpl_obj.id if tpl_obj else 'None'}")
    print(f"  -> Model Code:      {model_code}")
    print(f"  -> Expected Qs:     {q_count}")
    
    assert barcode == "94101", f"Expected barcode '94101', got '{barcode}'"
    assert tpl_obj is not None, "Failed to resolve template for Kibsi sheet"
    assert q_count == 50, f"Expected 50 questions, got {q_count}"

    grade_res = _grade_with_template(KIBSI_IMG, str(tpl_obj.id), {}, 108)
    qs = grade_res.get("questions", [])
    print(f"  -> Graded Questions: {len(qs)}")
    assert len(qs) == 50, f"Expected 50 graded questions, got {len(qs)}"
    print("  ✅ [PASS] Kibsi Sheet benchmark passed!")

    # ── Test 2: Aseel Al-Haj Sheet ──
    print("\n[2/2] Testing Aseel Al-Haj Sheet (Seat: 418485)...")
    assert os.path.exists(ASEEL_IMG), f"Missing test image: {ASEEL_IMG}"
    
    detect_res_aseel = _detect_template_from_sheet(ASEEL_IMG)
    tpl_aseel, model_aseel, q_aseel = detect_res_aseel
    bc_aseel = getattr(detect_res_aseel, 'barcode', '')
    
    print(f"  -> Detected Barcode: {bc_aseel}")
    print(f"  -> Template ID:     {tpl_aseel.id if tpl_aseel else 'None'}")
    print(f"  -> Model Code:      {model_aseel}")
    print(f"  -> Expected Qs:     {q_aseel}")
    
    assert tpl_aseel is not None, "Failed to resolve template for Aseel sheet"
    assert q_aseel == 50, f"Expected 50 questions, got {q_aseel}"

    grade_res_aseel = _grade_with_template(ASEEL_IMG, str(tpl_aseel.id), {}, 108)
    qs_aseel = grade_res_aseel.get("questions", [])
    print(f"  -> Graded Questions: {len(qs_aseel)}")
    assert len(qs_aseel) == 50, f"Expected 50 graded questions, got {len(qs_aseel)}"
    print("  ✅ [PASS] Aseel Sheet benchmark passed!")

    print("\n" + "=" * 60)
    print("🎉 ALL REGRESSION BENCHMARKS PASSED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    run_benchmark()
