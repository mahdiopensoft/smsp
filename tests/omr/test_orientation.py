import numpy as np
import cv2
import pytest
from omr.providers.opencv_omr import OpenCVOMREngine

def test_180_degree_inversion_detection_and_auto_rotation():
    engine = OpenCVOMREngine()

    # Create a synthetic A5-proportioned image (1000h x 700w)
    h, w = 1000, 700
    sheet = np.full((h, w, 3), 255, dtype=np.uint8)

    # Draw header text/graphics in top 15% (Upright sheet)
    cv2.rectangle(sheet, (50, 30), (w - 50, 150), (0, 0, 0), -1)
    cv2.putText(sheet, "MINISTRY OF EDUCATION - OFFICIAL EXAM", (70, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # 1. When upright, _validate_and_orient_aligned_sheet should keep it upright
    upright_res, meta_upright = engine._validate_and_orient_aligned_sheet(sheet, {})
    assert meta_upright["rotated_180"] is False

    # 2. Rotate the sheet 180° (Simulating inverted scanner feed)
    inverted_sheet = cv2.rotate(sheet, cv2.ROTATE_180)

    # 3. _validate_and_orient_aligned_sheet should detect inversion and rotate it back 180°
    corrected_sheet, meta_inverted = engine._validate_and_orient_aligned_sheet(inverted_sheet, {})
    assert meta_inverted["rotated_180"] is True

    # 4. Verify that in corrected_sheet, the dark header is back at the top!
    gray_corrected = cv2.cvtColor(corrected_sheet, cv2.COLOR_BGR2GRAY)
    _, binary_corrected = cv2.threshold(gray_corrected, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    top_ink = cv2.countNonZero(binary_corrected[0:180, :])
    bottom_ink = cv2.countNonZero(binary_corrected[820:1000, :])

    assert top_ink > bottom_ink * 2.0  # Header is restored to the top!
