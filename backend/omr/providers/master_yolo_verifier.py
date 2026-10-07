"""
master_yolo_verifier.py — Master Unified OMR YOLOv8 Verifier with Full Tracing
=============================================================================
Production-grade OMR bubble verification using the Master Unified YOLOv8 Model.
Includes Debug & Tracing mode to save cropped bubbles, visual predictions, and JSON logs.
"""

import os
import json
import logging
import time
import cv2
import numpy as np
from typing import Dict, List, Optional
import tempfile

logger = logging.getLogger("omr.ai.yolo")

DEFAULT_YOLO_PATH = os.path.join(os.path.dirname(__file__), "master_omr_yolo.pt")
DEBUG_TRACER_DIR  = os.path.join(os.path.dirname(os.path.dirname(__file__)), "debug_tracer")

class MasterYOLOVerifier:
    """
    High-Precision OMR Verifier wrapping Master Unified YOLOv8 with full tracing.
    """
    def __init__(
        self,
        model_path: str = DEFAULT_YOLO_PATH,
        conf: float = 0.35,
        iou: float = 0.35,
        enable_tracing: bool = True
    ):
        self.model_path = model_path
        self.conf = conf
        self.iou = iou
        self.enable_tracing = enable_tracing
        self.model = None
        self.tracer_dir = DEBUG_TRACER_DIR
        self._load_model()
        
        if self.enable_tracing:
            os.makedirs(os.path.join(self.tracer_dir, "crops"), exist_ok=True)
            os.makedirs(os.path.join(self.tracer_dir, "annotated"), exist_ok=True)

    def _load_model(self):
        if not os.path.exists(self.model_path):
            logger.warning(f"Master YOLO model file not found at: {self.model_path}")
            return
        
        try:
            from ultralytics import YOLO
            self.model = YOLO(self.model_path)
            logger.info(f"Loaded Master Unified OMR YOLO model from {self.model_path}")
            print(f"✅ [MasterYOLO] Loaded model: {self.model_path}")
        except Exception as e:
            logger.error(f"Failed to load YOLO model: {e}")
            self.model = None

    def _prepare_crop(self, crop: np.ndarray) -> np.ndarray:
        """Add context padding if crop is small (single bubble crop)."""
        if crop is None or crop.size == 0:
            return crop
        
        if len(crop.shape) == 2:
            crop_bgr = cv2.cvtColor(crop, cv2.COLOR_GRAY2BGR)
        else:
            crop_bgr = crop.copy()
            
        h, w = crop_bgr.shape[:2]
        if max(h, w) <= 500:
            pad = int(max(h, w) * 0.45)
            padded = cv2.copyMakeBorder(
                crop_bgr, pad, pad, pad, pad,
                cv2.BORDER_CONSTANT, value=(210, 210, 210)
            )
            return padded
        return crop_bgr

    def predict(self, crop: np.ndarray) -> Dict:
        """Classify a single bubble crop."""
        results = self.predict_batch([crop])
        return results[0] if results else {
            "label": "empty",
            "confidence": 0.5,
            "distribution": {"empty": 0.5, "filled": 0.25, "crossed": 0.25},
            "needs_review": True
        }

    def predict_batch(self, crops: List[np.ndarray]) -> List[Dict]:
        """Classify a list of bubble crops with full debug tracing."""
        if not crops:
            return []
            
        if self.model is None:
            return [{
                "label": "empty",
                "confidence": 0.5,
                "distribution": {"empty": 1.0, "filled": 0.0, "crossed": 0.0},
                "needs_review": True
            } for _ in crops]

        outputs = []
        timestamp = int(time.time())
        trace_data = []
        
        tmp_dir = tempfile.mkdtemp(prefix="omr_yolo_crops_")
        tmp_paths = []
        
        for idx, crop in enumerate(crops):
            padded = self._prepare_crop(crop)
            tmp_p = os.path.join(tmp_dir, f"crop_{idx:04d}.jpg")
            cv2.imwrite(tmp_p, padded)
            tmp_paths.append(tmp_p)
            
            # Trace: Save raw crop image
            if self.enable_tracing:
                raw_crop_path = os.path.join(self.tracer_dir, "crops", f"crop_{timestamp}_{idx:03d}.jpg")
                cv2.imwrite(raw_crop_path, crop)

        try:
            preds = self.model.predict(tmp_paths, conf=self.conf, iou=self.iou, verbose=False)
            
            for idx, (crop_img, res) in enumerate(zip(crops, preds)):
                boxes = res.boxes
                
                if len(boxes) == 0:
                    res_retry = self.model.predict(tmp_paths[idx], conf=0.10, iou=self.iou, verbose=False)[0]
                    boxes = res_retry.boxes
                
                # Copy for drawing annotated visual trace
                annotated_img = self._prepare_crop(crop_img).copy()

                
                if len(boxes) > 0:
                    best_box = max(boxes, key=lambda b: float(b.conf[0]))
                    cls_id = int(best_box.cls[0])
                    conf = float(best_box.conf[0])
                    raw_label = res.names.get(cls_id, "empty")
                    
                    if raw_label == "filled":
                        label = "filled"
                        color = (0, 200, 0)     # Green
                    elif raw_label == "crossed":
                        label = "crossed"
                        color = (0, 0, 220)     # Red
                    else:
                        label = "empty"
                        color = (220, 120, 0)   # Cyan/Orange
                        
                    dist = {
                        "empty": conf if label == "empty" else (1.0 - conf) / 2,
                        "filled": conf if label == "filled" else (1.0 - conf) / 2,
                        "crossed": conf if label == "crossed" else (1.0 - conf) / 2,
                    }
                    
                    # Draw box on annotated image
                    xyxy = best_box.xyxy[0].cpu().numpy().astype(int)
                    cv2.rectangle(annotated_img, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), color, 2)
                    cv2.putText(
                        annotated_img, f"{label} {conf*100:.0f}%",
                        (xyxy[0], max(xyxy[1]-5, 15)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2
                    )
                    
                    out_dict = {
                        "crop_index": idx,
                        "label": label,
                        "confidence": round(conf, 4),
                        "distribution": dist,
                        "needs_review": conf < 0.75
                    }
                else:
                    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY) if len(crop_img.shape) == 3 else crop_img
                    darkness = np.mean(gray < 120)
                    
                    lbl = "filled" if darkness > 0.45 else "empty"
                    c = 0.80 if lbl == "filled" else 0.95
                    
                    cv2.putText(
                        annotated_img, f"{lbl} {c*100:.0f}% (fallback)",
                        (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 2
                    )
                    
                    out_dict = {
                        "crop_index": idx,
                        "label": lbl,
                        "confidence": c,
                        "distribution": {lbl: c},
                        "needs_review": c < 0.75
                    }
                
                outputs.append(out_dict)
                trace_data.append(out_dict)
                
                # Trace: Save annotated visual image
                if self.enable_tracing:
                    annotated_path = os.path.join(
                        self.tracer_dir, "annotated",
                        f"pred_{timestamp}_{idx:03d}_{out_dict['label']}_{int(out_dict['confidence']*100)}.jpg"
                    )
                    cv2.imwrite(annotated_path, annotated_img)
                    
                    # Console trace log
                    print(
                        f" 🔍 [TRACER] Crop #{idx+1:02d}: Label='{out_dict['label']}' "
                        f"| Conf={out_dict['confidence']:.1%} | Image: {os.path.basename(annotated_path)}"
                    )

            # Trace: Save session JSON report
            if self.enable_tracing:
                json_log_path = os.path.join(self.tracer_dir, f"trace_log_{timestamp}.json")
                with open(json_log_path, "w") as f:
                    json.dump({
                        "timestamp": timestamp,
                        "total_crops": len(crops),
                        "results": trace_data
                    }, f, indent=2)
                print(f" 📑 [TRACER] Saved full session log: {json_log_path}")

        finally:
            for p in tmp_paths:
                if os.path.exists(p):
                    os.remove(p)
            if os.path.exists(tmp_dir):
                os.rmdir(tmp_dir)

        return outputs
