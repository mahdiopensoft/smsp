"""
master_yolo_verifier.py — Master Unified OMR YOLOv8 Verifier (Enterprise Certified)
==================================================================================
Production-grade OMR bubble verification using the Master Unified YOLOv8 Model.

Key Architectural Guarantees:
  1. In-Memory Batch Inference: Direct RAM tensors, eliminating disk I/O, file collisions, and tempfile leaks.
  2. Genuine Multi-Class Detection Evidence: Uses real detector scores per class, completely eliminating
     synthetic/fake distribution heuristics (e.g. dividing (1-conf)/2).
  3. No Blind Dark-Pixel Guessing: If YOLO detects 0 boxes, explicitly flags DETECTION_FAILED, sets
     confidence to 0.0, and marks needs_review=True instead of pretending high confidence.
  4. Honest Model-Unavailable State: Returns unclassified/0.0 confidence when model is None with no false labels.
  5. Multi-Box Conflict Resolution: Detects and flags competing bounding boxes across different classes.
  6. Thread-Safe Concurrency: Protected with threading.Lock for multi-threaded Django/Celery execution.
  7. Strict Schema Verification: Enforces {0: 'filled', 1: 'empty', 2: 'crossed'} on weight load.
  8. Risk-Calibrated Quality Gate: Per-class minimum acceptance thresholds (filled: 0.80, crossed: 0.80, empty: 0.65).
"""

import os
import json
import logging
import time
import uuid
import threading
import cv2
import numpy as np
from typing import Dict, List, Optional, Any, Tuple

logger = logging.getLogger("omr.ai.yolo")

DEFAULT_YOLO_PATH = os.path.join(os.path.dirname(__file__), "master_omr_yolo.pt")
DEBUG_TRACER_DIR  = os.path.join(os.path.dirname(os.path.dirname(__file__)), "debug_tracer")

EXPECTED_YOLO_CLASSES = {
    0: "filled",
    1: "empty",
    2: "crossed"
}

DEFAULT_PER_CLASS_THRESHOLDS = {
    "filled":  0.80,   # High-risk: changes student grade
    "crossed": 0.80,   # High-risk: represents canceled answer
    "empty":   0.65,   # Standard: default blank state
}


def format_unified_prediction(
    label: str,
    confidence: float,
    distribution: Dict[str, float],
    raw_label: str,
    raw_conf: float,
    decision_reason: str,
    status: str = "success",
    model_name: str = "YOLOv8_Master",
    model_version: str = "4.1_inmemory",
    crop_index: Optional[int] = None,
    extra_review_reasons: Optional[List[str]] = None,
    per_class_thresholds: Optional[Dict[str, float]] = None,
    detection_succeeded: bool = True
) -> Dict[str, Any]:
    """Standardized prediction dictionary contract across all vision models."""
    thresholds = per_class_thresholds or DEFAULT_PER_CLASS_THRESHOLDS
    req_threshold = thresholds.get(label, 0.75)

    probs = np.array(list(distribution.values()), dtype=np.float64)
    probs_sum = float(probs.sum())
    if probs_sum > 1e-9:
        normalized_probs = probs / probs_sum
        normalized_probs = np.clip(normalized_probs, 1e-9, 1.0)
        entropy = float(-np.sum(normalized_probs * np.log2(normalized_probs)))
        norm_entropy = float(entropy / np.log2(len(distribution))) if len(distribution) > 1 else 0.0
    else:
        entropy = 0.0
        norm_entropy = 0.0

    review_reasons = list(extra_review_reasons or [])
    if detection_succeeded and confidence < req_threshold:
        review_reasons.append(f"LOW_CONFIDENCE_{label.upper()}: {confidence:.2%} < {req_threshold:.2%}")
    if norm_entropy > 0.65:
        review_reasons.append(f"HIGH_ENTROPY_AMBIGUITY: {norm_entropy:.2f}")
    if not detection_succeeded:
        review_reasons.append("DETECTION_FAILED")

    needs_review = len(review_reasons) > 0

    res = {
        "status":              status,
        "detection_succeeded": detection_succeeded,
        "label":               label,
        "confidence":          round(float(confidence), 4),
        "distribution":        {k: round(float(v), 4) for k, v in distribution.items()},
        "entropy":             round(entropy, 4),
        "normalized_entropy":  round(norm_entropy, 4),
        "raw_prediction":      raw_label,
        "raw_confidence":      round(float(raw_conf), 4),
        "decision_reason":     decision_reason,
        "needs_review":        needs_review,
        "review_reasons":      review_reasons,
        "model_name":          model_name,
        "model_version":       model_version,
    }
    if crop_index is not None:
        res["crop_index"] = crop_index
    return res


_GLOBAL_MASTER_YOLO: Optional["MasterYOLOVerifier"] = None
_GLOBAL_YOLO_LOCK = threading.Lock()

def get_master_yolo_verifier(
    model_path: str = DEFAULT_YOLO_PATH,
    conf: float = 0.12,
    iou: float = 0.35,
    enable_tracing: bool = False,
    per_class_thresholds: Optional[Dict[str, float]] = None
) -> "MasterYOLOVerifier":
    """Returns a process-wide pre-warmed singleton of MasterYOLOVerifier."""
    global _GLOBAL_MASTER_YOLO
    if _GLOBAL_MASTER_YOLO is None:
        with _GLOBAL_YOLO_LOCK:
            if _GLOBAL_MASTER_YOLO is None:
                _GLOBAL_MASTER_YOLO = MasterYOLOVerifier(
                    model_path=model_path,
                    conf=conf,
                    iou=iou,
                    enable_tracing=enable_tracing,
                    per_class_thresholds=per_class_thresholds
                )
    return _GLOBAL_MASTER_YOLO


class MasterYOLOVerifier:
    """
    High-Precision, Thread-Safe OMR Verifier wrapping Master Unified YOLOv8
    with In-Memory Batch Inference and Zero-Disk Latency.
    """
    def __init__(
        self,
        model_path: str = DEFAULT_YOLO_PATH,
        conf: float = 0.12,
        iou: float = 0.35,
        enable_tracing: bool = False,
        per_class_thresholds: Optional[Dict[str, float]] = None
    ):
        self.model_path = model_path
        self.conf = conf
        self.iou = iou
        self.enable_tracing = enable_tracing
        self.per_class_thresholds = per_class_thresholds or DEFAULT_PER_CLASS_THRESHOLDS
        self.model = None
        self._lock = threading.Lock()
        self.tracer_dir = DEBUG_TRACER_DIR
        self._load_model()
        
        if self.enable_tracing:
            os.makedirs(os.path.join(self.tracer_dir, "crops"), mode=0o700, exist_ok=True)
            os.makedirs(os.path.join(self.tracer_dir, "annotated"), mode=0o700, exist_ok=True)

    @classmethod
    def cleanup_tracer(cls, max_age_hours: int = 24):
        """Removes tracing files older than max_age_hours to prevent disk overflow."""
        if not os.path.exists(DEBUG_TRACER_DIR):
            return
        now = time.time()
        for root, dirs, files in os.walk(DEBUG_TRACER_DIR):
            for f in files:
                f_path = os.path.join(root, f)
                try:
                    if os.stat(f_path).st_mtime < now - (max_age_hours * 3600):
                        os.remove(f_path)
                except Exception as ex:
                    logger.warning(f"Failed to remove stale tracer file {f_path}: {ex}")

    def _load_model(self):
        """Loads and validates YOLO model weights with strict schema contracts."""
        if not os.path.exists(self.model_path):
            logger.warning(f"Master YOLO model file not found at: {self.model_path}")
            return
        
        try:
            from ultralytics import YOLO
            self.model = YOLO(self.model_path)
            
            # Schema Contract Verification
            if hasattr(self.model, "names") and isinstance(self.model.names, dict):
                model_classes = self.model.names
                if len(model_classes) != len(EXPECTED_YOLO_CLASSES):
                    raise ValueError(
                        f"YOLO Architecture Mismatch: expected {len(EXPECTED_YOLO_CLASSES)} classes, "
                        f"found {len(model_classes)}: {model_classes}"
                    )
                for idx, exp_name in EXPECTED_YOLO_CLASSES.items():
                    if model_classes.get(idx) != exp_name:
                        raise ValueError(
                            f"YOLO Class Alignment Mismatch at index {idx}: expected '{exp_name}', "
                            f"got '{model_classes.get(idx)}'. Model mapping: {model_classes}"
                        )
                logger.info(f"MasterYOLO Class Schema Contract Verified: {model_classes}")
            else:
                logger.warning("YOLO model missing 'names' dictionary attribute.")

            logger.info(f"Loaded Master Unified OMR YOLO model from {self.model_path}")
            import torch
            if torch.cuda.is_available():
                self.model.to('cuda:0')
                self.device = 'cuda:0'
                logger.info(f"Master YOLO model pinned directly to GPU: {torch.cuda.get_device_name(0)}")
            else:
                self.device = 'cpu'
                logger.info("Master YOLO model running on CPU")
        except Exception as e:
            logger.error(f"Failed to load/verify YOLO model: {e}", exc_info=True)
            self.model = None

    def _validate_crop_input(self, crop: Any) -> Tuple[bool, Optional[np.ndarray], Optional[str]]:
        """
        Validates crop array integrity, dimensions, and color space.
        Returns (is_valid, bgr_crop, error_reason).
        """
        if crop is None or not isinstance(crop, np.ndarray):
            return False, None, "INVALID_OR_NONE_INPUT"
        if crop.size == 0:
            return False, None, "EMPTY_CROP_ARRAY"
        if crop.ndim not in (2, 3):
            return False, None, f"INVALID_NDIM_{crop.ndim}"
        h, w = crop.shape[:2]
        if h < 8 or w < 8:
            return False, None, f"CROP_TOO_SMALL_{w}x{h}"

        if crop.ndim == 2:
            bgr_crop = cv2.cvtColor(crop, cv2.COLOR_GRAY2BGR)
        elif crop.shape[2] == 1:
            bgr_crop = cv2.cvtColor(crop[:, :, 0], cv2.COLOR_GRAY2BGR)
        elif crop.shape[2] == 4:
            bgr_crop = cv2.cvtColor(crop, cv2.COLOR_BGRA2BGR)
        else:
            bgr_crop = crop.copy()

        return True, bgr_crop, None

    def _prepare_crop(self, crop_bgr: np.ndarray) -> np.ndarray:
        """Add context padding if crop is small (single bubble crop) for standard YOLO receptive field."""
        h, w = crop_bgr.shape[:2]
        if max(h, w) <= 500:
            pad = int(max(h, w) * 0.45)
            padded = cv2.copyMakeBorder(
                crop_bgr, pad, pad, pad, pad,
                cv2.BORDER_CONSTANT, value=(210, 210, 210)
            )
            return padded
        return crop_bgr

    def _check_ood_and_geometry(self, crop: np.ndarray, box_xyxy: Optional[np.ndarray] = None) -> List[str]:
        """
        Out-of-Distribution & Geometric Anomaly Guard.
        Flags non-bubble artifacts, uniform blocks, or distorted aspect ratios.
        """
        anomalies = []
        if crop is None or crop.size == 0:
            return ["EMPTY_IMAGE_DATA"]

        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY) if len(crop.shape) == 3 else crop
        std_dev = float(np.std(gray))
        if std_dev < 12.0:
            anomalies.append(f"LOW_TEXTURE_VARIANCE_OOD: std={std_dev:.1f} (solid/blank patch)")

        if box_xyxy is not None:
            bw = max(1, box_xyxy[2] - box_xyxy[0])
            bh = max(1, box_xyxy[3] - box_xyxy[1])
            aspect_ratio = float(bw) / float(bh)
            if aspect_ratio < 0.60 or aspect_ratio > 1.65:
                anomalies.append(f"ANOMALOUS_ASPECT_RATIO: {aspect_ratio:.2f} (expected ~1.0 for circular bubble)")

        return anomalies

    def predict(self, crop: np.ndarray) -> Dict[str, Any]:
        """Classify a single bubble crop under unified contract."""
        results = self.predict_batch([crop])
        return results[0] if results else format_unified_prediction(
            label="unclassified",
            confidence=0.0,
            distribution={"empty": 0.0, "filled": 0.0, "crossed": 0.0},
            raw_label="NO_DATA",
            raw_conf=0.0,
            decision_reason="EMPTY_CROP_INPUT",
            status="error",
            detection_succeeded=False,
            extra_review_reasons=["NO_IMAGE_DATA"]
        )

    def predict_batch(self, crops: List[np.ndarray]) -> List[Dict[str, Any]]:
        """
        Classify a batch of bubble crops using In-Memory Inference.
        Guarantees thread-safety, zero disk I/O, genuine confidence scores,
        and explicit failure handling without blind heuristics.
        """
        if not crops:
            return []

        # Point 3: Clean, honest model-unavailable response with no fake predictions
        if self.model is None:
            return [format_unified_prediction(
                label="unclassified",
                confidence=0.0,
                distribution={"empty": 0.0, "filled": 0.0, "crossed": 0.0},
                raw_label="MODEL_UNAVAILABLE",
                raw_conf=0.0,
                decision_reason="YOLO_MODEL_NOT_INITIALIZED_OR_UNAVAILABLE",
                status="model_unavailable",
                detection_succeeded=False,
                crop_index=idx,
                extra_review_reasons=["MODEL_UNAVAILABLE"]
            ) for idx in range(len(crops))]

        # Validate inputs and prepare in-memory batch
        valid_indices = []
        batch_inputs = []
        pre_results = [None] * len(crops)

        for idx, crop in enumerate(crops):
            is_valid, bgr_crop, err_reason = self._validate_crop_input(crop)
            if not is_valid:
                pre_results[idx] = format_unified_prediction(
                    label="unclassified",
                    confidence=0.0,
                    distribution={"empty": 0.0, "filled": 0.0, "crossed": 0.0},
                    raw_label="INVALID_CROP",
                    raw_conf=0.0,
                    decision_reason=f"INPUT_VALIDATION_FAILED: {err_reason}",
                    status="error",
                    detection_succeeded=False,
                    crop_index=idx,
                    extra_review_reasons=[f"INVALID_INPUT: {err_reason}"]
                )
            else:
                valid_indices.append(idx)
                batch_inputs.append(self._prepare_crop(bgr_crop))

        if not batch_inputs:
            return pre_results

        # Point 6: Thread-safe, direct in-memory batch prediction (Zero Disk I/O)
        with self._lock:
            try:
                preds = self.model.predict(
                    batch_inputs,
                    conf=self.conf,
                    iou=self.iou,
                    device=getattr(self, 'device', 'cpu'),
                    verbose=False
                )
            except Exception as e:
                logger.error(f"YOLO in-memory inference exception: {e}", exc_info=True)
                for orig_idx in valid_indices:
                    pre_results[orig_idx] = format_unified_prediction(
                        label="unclassified",
                        confidence=0.0,
                        distribution={"empty": 0.0, "filled": 0.0, "crossed": 0.0},
                        raw_label="INFERENCE_EXCEPTION",
                        raw_conf=0.0,
                        decision_reason=f"YOLO_EXCEPTION: {str(e)}",
                        status="error",
                        detection_succeeded=False,
                        crop_index=orig_idx,
                        extra_review_reasons=["INFERENCE_CRASH"]
                    )
                return pre_results

        session_id = uuid.uuid4().hex[:12] if self.enable_tracing else None
        timestamp = int(time.time())

        # Process each prediction (Zero-redundant, single-batch inference)
        for batch_i, orig_idx in enumerate(valid_indices):
            res = preds[batch_i]
            crop_img = crops[orig_idx]
            boxes = res.boxes

            if len(boxes) > 0:
                # Point 1: Extract genuine detection scores for all candidate classes
                class_scores = {"empty": 0.0, "filled": 0.0, "crossed": 0.0}
                boxes_by_class = {"empty": [], "filled": [], "crossed": []}

                for b in boxes:
                    c_id = int(b.cls[0])
                    c_name = res.names.get(c_id, "empty")
                    c_conf = float(b.conf[0])
                    if c_name in class_scores:
                        if c_conf > class_scores[c_name]:
                            class_scores[c_name] = c_conf
                        boxes_by_class[c_name].append(b)

                # Find dominant box
                best_box = max(boxes, key=lambda b: float(b.conf[0]))
                best_cls_id = int(best_box.cls[0])
                conf = float(best_box.conf[0])
                raw_label = res.names.get(best_cls_id, "empty")
                xyxy = best_box.xyxy[0].cpu().numpy().astype(int)

                # Point 5: Multi-box conflict resolution
                extra_reasons = []
                competing_classes = [c for c, score in class_scores.items() if score >= 0.40]
                if len(competing_classes) > 1:
                    extra_reasons.append(f"MULTI_BOX_CLASS_CONFLICT: {competing_classes} with scores {class_scores}")

                # Point 4: Out-of-distribution & Geometry Check
                ood_flags = self._check_ood_and_geometry(crop_img, box_xyxy=xyxy)
                extra_reasons.extend(ood_flags)

                # Point 1: True mathematical distribution from genuine class scores
                score_sum = sum(class_scores.values())
                if score_sum > 1e-9:
                    dist = {k: score / score_sum for k, score in class_scores.items()}
                else:
                    dist = {k: (1.0 if k == raw_label else 0.0) for k in class_scores}

                label = raw_label
                out_dict = format_unified_prediction(
                    label=label,
                    confidence=conf,
                    distribution=dist,
                    raw_label=raw_label,
                    raw_conf=conf,
                    decision_reason="YOLO_OBJECT_DETECTION",
                    status="success",
                    crop_index=orig_idx,
                    per_class_thresholds=self.per_class_thresholds,
                    extra_review_reasons=extra_reasons,
                    detection_succeeded=True
                )
            else:
                # Point 2: No blind guessing. Zero boxes = DETECTION_FAILED.
                # Do not assign fake filled/empty or static 95% confidence!
                ood_flags = self._check_ood_and_geometry(crop_img)
                review_reasons = ["NO_OBJECT_DETECTED_BY_YOLO", "HUMAN_AUDIT_REQUIRED"] + ood_flags

                out_dict = format_unified_prediction(
                    label="unknown",
                    confidence=0.0,
                    distribution={"empty": 0.0, "filled": 0.0, "crossed": 0.0},
                    raw_label="NO_BOX_DETECTED",
                    raw_conf=0.0,
                    decision_reason="YOLO_FOUND_ZERO_BOUNDING_BOXES",
                    status="DETECTION_FAILED",
                    crop_index=orig_idx,
                    per_class_thresholds=self.per_class_thresholds,
                    extra_review_reasons=review_reasons,
                    detection_succeeded=False
                )

            pre_results[orig_idx] = out_dict

            # Optional Debug Tracing (strictly isolated and non-blocking)
            if self.enable_tracing and session_id:
                try:
                    annotated_img = batch_inputs[batch_i].copy()
                    color = (0, 200, 0) if out_dict["label"] == "filled" else ((0, 0, 220) if out_dict["label"] == "crossed" else (220, 120, 0))
                    cv2.putText(
                        annotated_img, f"{out_dict['label']} {out_dict['confidence']*100:.0f}%",
                        (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2
                    )
                    annotated_path = os.path.join(
                        self.tracer_dir, "annotated",
                        f"pred_{timestamp}_{session_id}_{orig_idx:04d}_{out_dict['label']}.jpg"
                    )
                    cv2.imwrite(annotated_path, annotated_img)
                except Exception as ex:
                    logger.warning(f"Tracer dump failed: {ex}")

        return pre_results
