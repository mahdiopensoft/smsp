"""
bubble_standardizer.py — Enterprise OMR Bubble Standardization Pipeline
=======================================================================
Replaces legacy BubbleNormalizer with a robust, mathematically sound
pre-conditioning pipeline:
  1. Aspect-Ratio Preserving Symmetric Padding (Zero Distortion Centering).
  2. Adaptive CLAHE Grid Sizing (Eliminates mosaic noise on low DPI).
  3. Image Quality Assessment (IQA: Blur, Low Texture, Contrast).
"""

import cv2
import numpy as np
from typing import Optional, List, Tuple, Dict, Any


OUTPUT_SIZE = 48


class BubbleStandardizer:
    """
    Standardizes raw bubble crops into invariant 48x48 float32 tensors in [0, 1].
    Preserves perfect circular aspect ratios via symmetric canvas padding.
    """

    def __init__(self, output_size: int = OUTPUT_SIZE, clahe_clip: float = 2.0):
        self.output_size = output_size
        self.clahe_clip = clahe_clip

    def standardize(self, crop: np.ndarray) -> np.ndarray:
        """Main entry point: converts any raw crop to standardized 48x48 float32."""
        if crop is None or crop.size == 0:
            return np.ones((self.output_size, self.output_size), dtype=np.float32)

        gray = self._to_gray(crop)
        enhanced = self._apply_adaptive_clahe(gray)
        centered_square = self._center_with_symmetric_padding(enhanced)

        resized = cv2.resize(
            centered_square,
            (self.output_size, self.output_size),
            interpolation=cv2.INTER_AREA
        )
        normalized = resized.astype(np.float32) / 255.0
        return np.clip(normalized, 0.0, 1.0)

    # Backward compatibility alias
    def normalize(self, crop: np.ndarray) -> np.ndarray:
        return self.standardize(crop)

    def standardize_batch(self, crops: List[np.ndarray]) -> np.ndarray:
        """Batch standardization returning stacked (N, 48, 48) array."""
        if not crops:
            return np.empty((0, self.output_size, self.output_size), dtype=np.float32)
        return np.stack([self.standardize(c) for c in crops], axis=0)

    def normalize_batch(self, crops: List[np.ndarray]) -> np.ndarray:
        return self.standardize_batch(crops)

    @staticmethod
    def _to_gray(img: np.ndarray) -> np.ndarray:
        if img.ndim == 3:
            return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img.copy()

    def _apply_adaptive_clahe(self, gray: np.ndarray) -> np.ndarray:
        """Dynamically sizes CLAHE tiles to avoid mosaic artifacts on small crops."""
        h, w = gray.shape
        min_dim = min(h, w)
        if min_dim < 16:
            # Too small for tiling: apply standard contrast stretch
            norm = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
            return norm

        # Tile size between (2, 2) and (8, 8)
        grid_dim = max(2, min(8, min_dim // 6))
        clahe = cv2.createCLAHE(clipLimit=self.clahe_clip, tileGridSize=(grid_dim, grid_dim))
        return clahe.apply(gray)

    def _center_with_symmetric_padding(self, gray: np.ndarray) -> np.ndarray:
        """
        Locates circle center and extracts a strictly square crop.
        If the circle touches borders, pads symmetrically to avoid aspect distortion.
        """
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

        # Stage 2: Heavy ink contour moment centroid
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

        # Stage 3: Geometric center fallback
        if center_x is None:
            center_x, center_y = w // 2, h // 2
            radius = min_dim // 2

        # Desired square side = 2 * margin
        margin = max(int(radius * 1.30), min_dim // 2)

        # Compute required padding to keep (center_x, center_y) at the center of the square
        pad_top = max(0, margin - center_y)
        pad_bottom = max(0, (center_y + margin) - h)
        pad_left = max(0, margin - center_x)
        pad_right = max(0, (center_x + margin) - w)

        if pad_top > 0 or pad_bottom > 0 or pad_left > 0 or pad_right > 0:
            # Pad canvas with border reflection to preserve natural image texture
            padded = cv2.copyMakeBorder(
                gray, pad_top, pad_bottom, pad_left, pad_right,
                borderType=cv2.BORDER_REFLECT_101
            )
            # Adjusted center in padded coordinates
            adj_x = center_x + pad_left
            adj_y = center_y + pad_top
            square = padded[adj_y - margin:adj_y + margin, adj_x - margin:adj_x + margin]
        else:
            square = gray[center_y - margin:center_y + margin, center_x - margin:center_x + margin]

        return square if square.size > 0 else gray

    @staticmethod
    def assess_quality(crop: np.ndarray) -> Dict[str, Any]:
        """Fast Image Quality Assessment (IQA) for blur and low contrast."""
        if crop is None or crop.size == 0:
            return {"is_valid": False, "reason": "EMPTY_CROP", "blur_variance": 0.0}

        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY) if crop.ndim == 3 else crop
        std = float(np.std(gray))
        if std < 10.0:
            return {"is_valid": False, "reason": "LOW_TEXTURE_SOLID", "std_dev": round(std, 2)}

        blur_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        is_blurry = blur_var < 15.0
        return {
            "is_valid": not is_blurry,
            "reason": "MOTION_BLUR" if is_blurry else "OK",
            "blur_variance": round(blur_var, 2),
            "std_dev": round(std, 2)
        }
