"""
BubbleNormalizer — Hybrid Centering Pipeline (Production Certified)
===================================================================
Converts raw bubble crops into standardized 48x48 float32 grayscale in [0, 1].
Solves HoughCircles failure on solid black ink and heavy crosses via Moment Centroid fallback.
"""

import cv2
import numpy as np
from typing import Optional, List, Tuple

OUTPUT_SIZE = 48
CLAHE_CLIP = 2.0
CLAHE_TILE = (8, 8)

class BubbleNormalizer:
    def __init__(self, output_size: int = OUTPUT_SIZE):
        self.output_size = output_size
        self._clahe = cv2.createCLAHE(
            clipLimit=CLAHE_CLIP,
            tileGridSize=CLAHE_TILE,
        )

    def normalize(self, crop: np.ndarray) -> np.ndarray:
        if crop is None or crop.size == 0:
            return np.ones((self.output_size, self.output_size), dtype=np.float32)
        gray = self._to_gray(crop)
        enhanced = self._clahe.apply(gray)
        centered = self._hybrid_center_crop(enhanced)
        resized = cv2.resize(
            centered,
            (self.output_size, self.output_size),
            interpolation=cv2.INTER_AREA
        )
        normalized = resized.astype(np.float32) / 255.0
        return np.clip(normalized, 0.0, 1.0)

    def normalize_batch(self, crops: List[np.ndarray]) -> np.ndarray:
        if not crops:
            return np.empty((0, self.output_size, self.output_size), dtype=np.float32)
        return np.stack([self.normalize(c) for c in crops], axis=0)

    @staticmethod
    def _to_gray(img: np.ndarray) -> np.ndarray:
        if img.ndim == 3:
            return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img.copy()

    def _hybrid_center_crop(self, gray: np.ndarray) -> np.ndarray:
        h, w = gray.shape
        min_dim = min(h, w)
        if min_dim < 12:
            return gray

        center_x, center_y, radius = None, None, None

        # Stage 1: HoughCircles
        blurred = cv2.GaussianBlur(gray, (5, 5), 1.2)
        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=min_dim * 0.5,
            param1=80,
            param2=25,
            minRadius=int(min_dim * 0.20),
            maxRadius=int(min_dim * 0.55),
        )

        if circles is not None and len(circles) > 0:
            cx, cy, r = np.round(circles[0, 0]).astype(int)
            if 0 <= cx < w and 0 <= cy < h and r > 3:
                center_x, center_y, radius = cx, cy, r

        # Stage 2: Heavy Ink Contour Moment Centroid (when Hough fails on solid ink/crosses)
        if center_x is None:
            mean_val = float(np.mean(gray))
            thresh_val = max(30, int(mean_val * 0.75))
            _, binary = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY_INV)

            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                c = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(c)
                if area > (h * w * 0.05):
                    M = cv2.moments(c)
                    if M["m00"] > 0:
                        center_x = int(M["m10"] / M["m00"])
                        center_y = int(M["m01"] / M["m00"])
                        radius = int(np.sqrt(area / np.pi))

        # Stage 3: Geometric Center Fallback
        if center_x is None:
            center_x, center_y = w // 2, h // 2
            radius = min_dim // 2

        margin = int(radius * 1.30)
        margin = max(margin, min_dim // 2)
        x1 = max(0, center_x - margin)
        y1 = max(0, center_y - margin)
        x2 = min(w, center_x + margin)
        y2 = min(h, center_y + margin)

        crop = gray[y1:y2, x1:x2]
        return crop if crop.size > 0 else gray

def normalize_bubble(crop: np.ndarray) -> np.ndarray:
    return BubbleNormalizer().normalize(crop)
