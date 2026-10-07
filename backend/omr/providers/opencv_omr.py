"""
OpenCV OMR Provider — Classical bubble detection using pixel density analysis.
Upgraded to support rigorous geometric coordinates (dx_mm, dy_mm) and confidence zones (safe_region, expanded_region).

Pipeline (per the pl.md specification):
  Aligned Image (from Alignment Engine)
       ↓
  Load Template (bubble regions with coordinates)
       ↓
  For each MCQ question:
     → Crop each bubble region (A, B, C, D)
     → Convert to grayscale → threshold
     → Calculate darkness percentage (black pixels / total pixels)
     → If darkness > 60% → FILLED
     → If 40%-60% → AMBIGUOUS (needs review)
     → If < 40% → EMPTY
       ↓
  Select the darkest bubble as the answer
       ↓
  Calculate confidence score per question
       ↓
  Match against answer key → score

This is the classical approach (Pattern 1 from pl.md):
  OpenCV + Adaptive Threshold + OMR

For Pattern 3 (OpenCV + OMR + AI Verification),
the AI verification layer runs after this via the Verification Engine.
"""

import logging
import os
import cv2
import numpy as np

from core.base_engine import BaseEngine, EngineResult

logger = logging.getLogger("omr")

# Calibrated thresholds from measuring actual printed OMR sheets at 300 DPI:
# - Blank bubble ring (printed outline):  fill_ratio ≈ 0.20-0.25
# - Fully filled bubble:                  fill_ratio ≈ 0.60-0.85
# - Crossed / partially filled:           fill_ratio ≈ 0.30-0.55
# - Erased (smudge):                      fill_ratio ≈ 0.28-0.42
EMPTY_THRESHOLD  = 0.28   # below = only printed ring = EMPTY
FILLED_THRESHOLD = 0.55   # above = solid dark fill    = FILLED
INK_DARK_THR     = 0.25   # darkness in safe region distinguishing crossed vs erased
MM_TO_INCH       = 25.4
DEFAULT_FILLED_THRESHOLD = FILLED_THRESHOLD  # backward compat alias
DEFAULT_AMBIGUOUS_LOW    = EMPTY_THRESHOLD

class OpenCVOMREngine(BaseEngine):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Lazy-load AI verifier to avoid startup delay when not needed
        self._ai_verifier = None

    @property
    def ai_verifier(self):
        if self._ai_verifier is None:
            from omr.providers.ai_verification import AIBubbleVerifier
            self._ai_verifier = AIBubbleVerifier()
        return self._ai_verifier

    @property
    def engine_name(self) -> str:
        return "omr"

    def _mm_to_px(self, mm: float, dpi: int) -> int:
        return int(mm * (dpi / MM_TO_INCH))

    def _align_image(self, image: np.ndarray, template: dict, scan_dpi: int) -> np.ndarray:
        """
        Automatic optical alignment using 4 corner fiducial marks.
        If fiducials are detected, corrects rotation and perspective skew.
        """
        try:
            h, w = image.shape[:2]
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image

            thresholds_to_try = []
            try:
                _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
                thresholds_to_try.append(otsu)
            except Exception:
                pass
            for th_val in [70, 100, 130, 160]:
                _, th = cv2.threshold(gray, th_val, 255, cv2.THRESH_BINARY_INV)
                thresholds_to_try.append(th)

            paper_size = str(template.get("paper_size", "A5")).upper()
            if "A4" in paper_size:
                pw_mm = 297.0 if w >= h else 210.0
                ph_mm = 210.0 if w >= h else 297.0
            else:
                pw_mm = 210.0 if w >= h else 148.5
                ph_mm = 148.5 if w >= h else 210.0

            # Scale of current input image in px/mm
            curr_scale = max(w / pw_mm, h / ph_mm)
            expected_size_px = 5.5 * curr_scale
            min_sz = max(4.0, expected_size_px * 0.35)
            max_sz = max(expected_size_px * 2.2, 12.0)

            quads = {
                "TL": (0, 0, w // 4, h // 4),
                "TR": (3 * w // 4, 0, w, h // 4),
                "BL": (0, 3 * h // 4, w // 4, h),
                "BR": (3 * w // 4, 3 * h // 4, w, h),
            }

            detected_centers = {}
            for thresh_img in thresholds_to_try:
                for q_id, (qx1, qy1, qx2, qy2) in quads.items():
                    if q_id in detected_centers:
                        continue
                    roi = thresh_img[qy1:qy2, qx1:qx2]
                    cnts, _ = cv2.findContours(roi, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                    candidates = []
                    for c in cnts:
                        bx, by, bw, bh = cv2.boundingRect(c)
                        if min_sz <= bw <= max_sz and min_sz <= bh <= max_sz:
                            ratio = bw / float(bh)
                            if 0.55 <= ratio <= 1.80:
                                c_roi = roi[by:by+bh, bx:bx+bw]
                                fill = cv2.countNonZero(c_roi) / (bw * bh)
                                if fill > 0.50:
                                    center = (float(qx1 + bx + bw / 2.0), float(qy1 + by + bh / 2.0))
                                    candidates.append((center, fill, abs(bw - expected_size_px)))
                    if candidates:
                        candidates.sort(key=lambda item: (item[2], -item[1]))
                        detected_centers[q_id] = candidates[0][0]
                if len(detected_centers) == 4:
                    break

            # 3-corner parallelogram recovery: TL + BR = TR + BL
            if len(detected_centers) == 3:
                if "TL" not in detected_centers and all(k in detected_centers for k in ("TR", "BL", "BR")):
                    detected_centers["TL"] = (
                        detected_centers["TR"][0] + detected_centers["BL"][0] - detected_centers["BR"][0],
                        detected_centers["TR"][1] + detected_centers["BL"][1] - detected_centers["BR"][1]
                    )
                elif "TR" not in detected_centers and all(k in detected_centers for k in ("TL", "BL", "BR")):
                    detected_centers["TR"] = (
                        detected_centers["TL"][0] + detected_centers["BR"][0] - detected_centers["BL"][0],
                        detected_centers["TL"][1] + detected_centers["BR"][1] - detected_centers["BL"][1]
                    )
                elif "BL" not in detected_centers and all(k in detected_centers for k in ("TL", "TR", "BR")):
                    detected_centers["BL"] = (
                        detected_centers["TL"][0] + detected_centers["BR"][0] - detected_centers["TR"][0],
                        detected_centers["TL"][1] + detected_centers["BR"][1] - detected_centers["TR"][1]
                    )
                elif "BR" not in detected_centers and all(k in detected_centers for k in ("TL", "TR", "BL")):
                    detected_centers["BR"] = (
                        detected_centers["TR"][0] + detected_centers["BL"][0] - detected_centers["TL"][0],
                        detected_centers["TR"][1] + detected_centers["BL"][1] - detected_centers["TL"][1]
                    )

            if len(detected_centers) == 4:
                fid_map = {f.get("id"): f for f in template.get("fiducial_marks", [])}
                if all(k in fid_map for k in ("TL", "TR", "BL", "BR")):
                    scale = scan_dpi / MM_TO_INCH
                    dst_pts = np.float32([
                        [(fid_map["TL"]["x_mm"] + fid_map["TL"]["width_mm"] / 2.0) * scale,
                         (fid_map["TL"]["y_mm"] + fid_map["TL"]["height_mm"] / 2.0) * scale],
                        [(fid_map["TR"]["x_mm"] + fid_map["TR"]["width_mm"] / 2.0) * scale,
                         (fid_map["TR"]["y_mm"] + fid_map["TR"]["height_mm"] / 2.0) * scale],
                        [(fid_map["BL"]["x_mm"] + fid_map["BL"]["width_mm"] / 2.0) * scale,
                         (fid_map["BL"]["y_mm"] + fid_map["BL"]["height_mm"] / 2.0) * scale],
                        [(fid_map["BR"]["x_mm"] + fid_map["BR"]["width_mm"] / 2.0) * scale,
                         (fid_map["BR"]["y_mm"] + fid_map["BR"]["height_mm"] / 2.0) * scale],
                    ])
                    src_pts = np.float32([
                        detected_centers["TL"],
                        detected_centers["TR"],
                        detected_centers["BL"],
                        detected_centers["BR"],
                    ])

                    target_w = int(round(pw_mm * scale))
                    target_h = int(round(ph_mm * scale))

                    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
                    aligned = cv2.warpPerspective(image, M, (target_w, target_h), borderValue=(255, 255, 255))
                    logger.info(f"Aligned sheet using fiducials (target: {target_w}x{target_h} @ {scan_dpi} DPI)")
                    return aligned
        except Exception as e:
            logger.warning(f"Fiducial alignment skipped: {e}")

        return image

    def _process(self, input_data: dict, context: dict = None) -> EngineResult:
        image_path = input_data.get("image_path")
        if not image_path or not os.path.exists(image_path):
            return EngineResult(engine_name=self.engine_name, status="error", errors=[f"Image not found: {image_path}"])

        template_raw = (context or {}).get("template", {})
        if hasattr(template_raw, "model_dump"):
            template = template_raw.model_dump()
        elif isinstance(template_raw, dict):
            template = template_raw
        else:
            template = {}

        answer_key = (context or {}).get("answer_key", {})
        mcq_questions = template.get("mcq_questions", [])

        if not mcq_questions:
            return EngineResult(engine_name=self.engine_name, status="skipped", confidence=1.0, data={"message": "No MCQ"})

        image = cv2.imread(image_path)
        if image is None:
            return EngineResult(engine_name=self.engine_name, status="error", errors=["Failed to load aligned image"])

        img_h, img_w = image.shape[:2]
        paper_size = str(template.get("paper_size", "A5")).upper()
        if "A4" in paper_size:
            pw_mm = 297.0 if img_w >= img_h else 210.0
        else:
            pw_mm = 210.0 if img_w >= img_h else 148.5

        calc_dpi = int(round(img_w / (pw_mm / MM_TO_INCH)))
        ctx_dpi = (context or {}).get("dpi")
        if ctx_dpi and abs(ctx_dpi - calc_dpi) < 0.15 * calc_dpi:
            scan_dpi = ctx_dpi
        elif 72 <= calc_dpi <= 2400:
            scan_dpi = calc_dpi
        else:
            scan_dpi = template.get("expected_scan_dpi", 300)

        # Optical fiducial alignment
        image = self._align_image(image, template, scan_dpi)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image.copy()
        
        # Calculate block size dynamically based on DPI to avoid hollowing out solid bubble centers
        # The block size must be significantly larger than the bubble size (which is ~53px at 300 DPI)
        block_size = int(scan_dpi / 2)
        if block_size % 2 == 0:
            block_size += 1
        block_size = max(block_size, 31)
        
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, block_size, 8)

        mcq_answers = answer_key.get("mcq_answers", {})
        marks_per_q = float(answer_key.get("mcq_marks_per_question", 1))

        # Dynamic detection & AI thresholds from template config
        detection_cfg = template.get("detection") or template.get("template_data", {}).get("detection", {}) or {}
        thresholds_cfg = detection_cfg.get("thresholds", {}) or {}
        filled_threshold = float(thresholds_cfg.get("filled_min", FILLED_THRESHOLD * 100)) / 100.0 if thresholds_cfg.get("filled_min") else FILLED_THRESHOLD
        empty_threshold = float(thresholds_cfg.get("empty_max", EMPTY_THRESHOLD * 100)) / 100.0 if thresholds_cfg.get("empty_max") else EMPTY_THRESHOLD
        enable_ai_verification = detection_cfg.get("ai_verification", True)

        question_results = []
        total_correct = 0
        total_answered = 0
        total_ambiguous = 0
        confidences = []

        for q in mcq_questions:
            q_id = q["question_id"]
            choices = q.get("choices", [])
            q_result = self._process_question(
                binary, gray, q_id, choices, mcq_answers, marks_per_q, scan_dpi,
                filled_threshold=filled_threshold,
                empty_threshold=empty_threshold,
                enable_ai_verification=enable_ai_verification
            )
            question_results.append(q_result)

            if q_result["is_correct"]: total_correct += 1
            if q_result["marked_choice"]: total_answered += 1
            if q_result["bubble_state"] == "ambiguous": total_ambiguous += 1
            confidences.append(q_result["final_confidence"])

        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        if total_ambiguous > 0:
            avg_confidence = max(avg_confidence - min(total_ambiguous * 0.05, 0.3), 0.0)

        total_score = total_correct * marks_per_q
        max_score = len(mcq_questions) * marks_per_q
        return EngineResult(
            engine_name=self.engine_name, 
            status="success", 
            confidence=round(avg_confidence, 4),
            data={
                "answers": {q["question_id"]: q["marked_choice"] for q in question_results},
                "ambiguous_bubbles": [q["question_id"] for q in question_results if q["bubble_state"] == "ambiguous"],
                "questions": question_results, 
                "total_questions": len(mcq_questions),
                "total_score": total_score,
                "max_score": max_score,
                "ambiguous_count": total_ambiguous,
                "detected_dpi": scan_dpi,
                "aligned_image": image,
            }, 
            provider_used="opencv"
        )

    def _process_question(
        self, binary_image: np.ndarray, gray_image: np.ndarray,
        question_id: int, choices: list, answer_key: dict, marks_per_q: float, dpi: int,
        filled_threshold: float = FILLED_THRESHOLD,
        empty_threshold: float = EMPTY_THRESHOLD,
        enable_ai_verification: bool = True
    ) -> dict:
        darkness_values   = {}
        classical_results = {}   # raw OpenCV classification per choice
        bubble_crops      = {}   # raw gray crops per choice (for UI & AI)

        actual_centers = {}
        for choice_data in choices:
            choice_label = choice_data["choice"]
            safe = choice_data.get("safe_region", choice_data.get("region", {}))
            bubble = choice_data.get("bubble_region", choice_data.get("region", {}))

            bx = self._mm_to_px(bubble.get("dx_mm", 0), dpi)
            by = self._mm_to_px(bubble.get("dy_mm", 0), dpi)
            bw = self._mm_to_px(bubble.get("width_mm", 0), dpi)
            bh = self._mm_to_px(bubble.get("height_mm", 0), dpi)

            expected_cx = bx + bw // 2
            expected_cy = by + bh // 2

            # ── Dynamic Local Bubble Snapping ─────────────────────────
            # Search in a local window around expected position for the true printed circle
            win_pad_x = max(int(bw * 1.2), int(self._mm_to_px(3.5, dpi)))
            win_pad_y = max(int(bh * 1.0), int(self._mm_to_px(2.5, dpi)))
            img_h, img_w = binary_image.shape[:2]

            wx1 = max(0, expected_cx - win_pad_x)
            wx2 = min(img_w, expected_cx + win_pad_x)
            wy1 = max(0, expected_cy - win_pad_y)
            wy2 = min(img_h, expected_cy + win_pad_y)

            best_cx, best_cy = expected_cx, expected_cy
            if wx2 > wx1 and wy2 > wy1:
                win_roi = binary_image[wy1:wy2, wx1:wx2]
                k_sz = max(3, int(self._mm_to_px(0.4, dpi)) | 1)
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k_sz, k_sz))
                closed_roi = cv2.morphologyEx(win_roi, cv2.MORPH_CLOSE, kernel)
                cnts, _ = cv2.findContours(closed_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                best_dist = float('inf')
                for c in cnts:
                    rx, ry, rw, rh = cv2.boundingRect(c)
                    if int(bw * 0.60) <= rw <= int(bw * 1.50) and int(bh * 0.60) <= rh <= int(bh * 1.50):
                        ratio = rw / float(max(1, rh))
                        if 0.70 <= ratio <= 1.40:
                            c_cand_x = wx1 + rx + rw // 2
                            c_cand_y = wy1 + ry + rh // 2
                            dist = (c_cand_x - expected_cx) ** 2 + (c_cand_y - expected_cy) ** 2
                            if dist < best_dist:
                                best_dist = dist
                                best_cx, best_cy = c_cand_x, c_cand_y

            actual_centers[choice_label] = (best_cx, best_cy)

            # Refined bubble and safe regions centered on the snapped physical circle
            sw = self._mm_to_px(safe.get("width_mm", 0), dpi)
            sh = self._mm_to_px(safe.get("height_mm", 0), dpi)

            refined_bx = max(0, min(best_cx - bw // 2, img_w - bw))
            refined_by = max(0, min(best_cy - bh // 2, img_h - bh))
            refined_sx = max(0, min(best_cx - sw // 2, img_w - sw))
            refined_sy = max(0, min(best_cy - sh // 2, img_h - sh))

            # 1. First Pass: Pixel Density in Refined Safe Region
            best_darkness = 0.0
            for shift_x in (-2, 0, 2):
                for shift_y in (-2, 0, 2):
                    cur_x = max(0, min(refined_sx + shift_x, img_w - sw))
                    cur_y = max(0, min(refined_sy + shift_y, img_h - sh))
                    safe_roi = binary_image[cur_y:cur_y+sh, cur_x:cur_x+sw]
                    if safe_roi.size > 0:
                        cur_darkness = cv2.countNonZero(safe_roi) / safe_roi.size
                        if cur_darkness > best_darkness:
                            best_darkness = cur_darkness

            darkness = best_darkness
            darkness_values[choice_label] = round(darkness, 4)

            # Extract bubble crop centered directly on the physical bubble
            bubble_gray_roi = gray_image[refined_by:refined_by+bh, refined_bx:refined_bx+bw]
            if bubble_gray_roi.size > 0:
                bubble_crops[choice_label] = bubble_gray_roi

            # 2. Otsu fill-ratio on the full bubble bounding box
            if darkness > 0.06 and bubble_gray_roi.size > 0:
                _, bubble_otsu = cv2.threshold(
                    bubble_gray_roi, 0, 255,
                    cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
                fill_ratio = cv2.countNonZero(bubble_otsu) / bubble_otsu.size

                if fill_ratio > filled_threshold:
                    classical_results[choice_label] = "filled"
                elif fill_ratio < empty_threshold:
                    classical_results[choice_label] = "empty"
                else:
                    # Ambiguous zone — use safe-region darkness to distinguish
                    if darkness > INK_DARK_THR:
                        classical_results[choice_label] = "crossed"
                    else:
                        classical_results[choice_label] = "erased"
            else:
                classical_results[choice_label] = "empty"

        # ── Pass 2: AI verification on crops with markings ──────────────────
        ai_results   = dict(classical_results)  # start from classical
        ai_conf_data = {}  # store confidence per choice

        # Only send candidates with potential ink to AI verifier to ensure fast processing
        crops_for_ai = {
            k: v for k, v in bubble_crops.items()
            if darkness_values.get(k, 0) > 0.06 or classical_results.get(k) != "empty"
        }

        if enable_ai_verification and crops_for_ai:
            crop_keys   = list(crops_for_ai.keys())
            crop_imgs   = [crops_for_ai[k] for k in crop_keys]
            predictions = self.ai_verifier.predict_batch(crop_imgs)

            for key, pred in zip(crop_keys, predictions):
                ai_results[key]   = pred["label"]
                ai_conf_data[key] = pred
                classical_lbl     = classical_results[key]
                if pred["label"] != classical_lbl:
                    logger.debug(
                        f"  [AI] Q{question_id} {key}: "
                        f"{classical_lbl} → {pred['label']} "
                        f"({pred['confidence']:.0%})"
                    )

        # ── Classify question state from AI results ─────────────────────────
        filled_choices  = [lbl for lbl, st in ai_results.items() if st == "filled"]
        crossed_choices = [lbl for lbl, st in ai_results.items() if st == "crossed"]
        erased_choices  = [lbl for lbl, st in ai_results.items() if st == "erased"]
        half_choices    = [lbl for lbl, st in ai_results.items() if st == "half_filled"]

        # Compute question-level confidence from AI data
        question_confidence = 1.0
        for key, pred in ai_conf_data.items():
            if pred.get("needs_review", False):
                question_confidence = min(question_confidence, pred["confidence"])


        if len(filled_choices) == 1:
            marked_choice   = filled_choices[0]
            bubble_state    = "filled"
            final_confidence = question_confidence
            if crossed_choices or half_choices:
                final_confidence = min(final_confidence, 0.85)
        elif len(filled_choices) > 1:
            marked_choice   = None
            bubble_state    = "ambiguous"
            final_confidence = 0.20
        else:
            marked_choice = None
            if crossed_choices:
                bubble_state    = "crossed"
                final_confidence = question_confidence
            elif erased_choices:
                bubble_state    = "erased"
                final_confidence = question_confidence
            elif half_choices:
                bubble_state    = "half_filled"
                final_confidence = min(question_confidence, 0.60)
            else:
                bubble_state    = "empty"
                final_confidence = 1.0

        correct_choice = answer_key.get(str(question_id))
        is_correct = (marked_choice == correct_choice) if marked_choice and correct_choice else None

        # Convert crops to base64 data URLs for visual proof in UI
        import base64
        choice_crops_b64 = {}
        for ch_key, crop_img in bubble_crops.items():
            if crop_img is not None and crop_img.size > 0:
                _, buf = cv2.imencode('.png', crop_img)
                choice_crops_b64[ch_key] = "data:image/png;base64," + base64.b64encode(buf).decode()

        return {
            "question_id":       question_id,
            "choices":           [c["choice"] for c in choices],
            "marked_choice":     marked_choice,
            "correct_choice":    correct_choice,
            "is_correct":        is_correct,
            "bubble_state":      bubble_state,
            "choice_confidences": darkness_values,
            "ai_results":        ai_results,
            "ai_confidence":     ai_conf_data,     # per-choice confidence data
            "choice_crops":      choice_crops_b64, # real crop images in base64
            "actual_centers":    actual_centers,   # physical bubble centers (px)
            "final_confidence":  round(final_confidence, 4),
        }
