"""
BubbleNormalizer
================
Converts any raw bubble crop (any size, scanner or phone photo) into a
standardized 48×48 grayscale image ready for the AI classifier.

Pipeline:
  raw crop  →  CLAHE  →  circle-centered crop  →  resize 48×48  →  [0,1] float32

This makes the AI completely independent of:
  - Sheet size / DPI
  - Scanner brightness / phone camera exposure
  - Template layout (works with ANY template)
"""

import cv2
import numpy as np
from typing import Optional, Tuple


# ─── Constants ────────────────────────────────────────────────────────────────
OUTPUT_SIZE  = 48        # pixels — input size for the CNN
CLAHE_CLIP   = 2.0       # contrast limit for CLAHE
CLAHE_TILE   = (8, 8)    # tile grid size for CLAHE


class BubbleNormalizer:
    """
    Takes a raw (H×W grayscale or BGR) bubble crop and returns a
    normalized 48×48 float32 numpy array in [0, 1].
    """

    def __init__(self, output_size: int = OUTPUT_SIZE):
        self.output_size = output_size
        self._clahe = cv2.createCLAHE(
            clipLimit=CLAHE_CLIP,
            tileGridSize=CLAHE_TILE,
        )

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def normalize(self, crop: np.ndarray) -> np.ndarray:
        """
        Parameters
        ----------
        crop : np.ndarray
            Raw bubble crop (BGR or grayscale, any size).

        Returns
        -------
        np.ndarray  shape (48, 48)  dtype float32  range [0, 1]
        """
        gray     = self._to_gray(crop)
        enhanced = self._clahe.apply(gray)
        centered = self._center_on_circle(enhanced)
        resized  = cv2.resize(centered, (self.output_size, self.output_size),
                              interpolation=cv2.INTER_AREA)
        # Normalize to [0,1]: 0=black, 1=white
        # Filled bubble = mostly dark pixels (low values)
        # Empty bubble  = mostly white pixels (high values)
        normalized = resized.astype(np.float32) / 255.0
        return normalized

    def normalize_batch(self, crops: list) -> np.ndarray:
        """
        Normalize a list of crops and return a (N, H, W) float32 array.
        """
        return np.stack([self.normalize(c) for c in crops], axis=0)

    # ------------------------------------------------------------------ #
    #  Internal helpers                                                    #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _to_gray(img: np.ndarray) -> np.ndarray:
        if img.ndim == 3:
            return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img.copy()

    def _center_on_circle(self, gray: np.ndarray) -> np.ndarray:
        """
        Attempt to find the printed circle's center using HoughCircles.
        If found, crop a square region around that center.
        If not found, fall back to the full crop.
        """
        h, w = gray.shape
        min_dim = min(h, w)

        # Blur slightly before Hough to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 1.2)

        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=min_dim * 0.5,          # only one circle expected
            param1=80,
            param2=25,
            minRadius=int(min_dim * 0.25),
            maxRadius=int(min_dim * 0.55),
        )

        if circles is not None:
            x, y, r = np.round(circles[0, 0]).astype(int)
            # Expand the radius slightly so we capture the full ring
            margin = int(r * 1.25)
            x1 = max(0, x - margin)
            y1 = max(0, y - margin)
            x2 = min(w, x + margin)
            y2 = min(h, y + margin)
            crop = gray[y1:y2, x1:x2]
            if crop.size > 0:
                return crop

        # Fallback: return original crop (already good enough for most cases)
        return gray

    # ------------------------------------------------------------------ #
    #  Debug / visualization                                               #
    # ------------------------------------------------------------------ #

    def debug_grid(self, crops: list, labels: Optional[list] = None,
                   cols: int = 10) -> np.ndarray:
        """
        Returns a visual grid of normalized bubble crops for debugging.
        """
        normalized = [self.normalize(c) for c in crops]
        rows_needed = (len(normalized) + cols - 1) // cols
        cell = self.output_size + 4
        canvas = np.ones((rows_needed * cell, cols * cell), dtype=np.float32)

        for idx, img in enumerate(normalized):
            r = idx // cols
            c = idx % cols
            y, x = r * cell + 2, c * cell + 2
            canvas[y:y + self.output_size, x:x + self.output_size] = img

        out = (canvas * 255).astype(np.uint8)
        if labels:
            out = cv2.cvtColor(out, cv2.COLOR_GRAY2BGR)
            for idx, lbl in enumerate(labels):
                r = idx // cols
                c = idx % cols
                py = r * cell + self.output_size
                px = c * cell
                cv2.putText(out, str(lbl)[:4],
                            (px, py + 3),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (0, 200, 100), 1)
        return out


# ─── Standalone helper function ───────────────────────────────────────────────

_default_normalizer = BubbleNormalizer()


def normalize_bubble(crop: np.ndarray) -> np.ndarray:
    """
    Convenience function: normalize a single bubble crop.
    Returns float32 array of shape (48, 48).
    """
    return _default_normalizer.normalize(crop)
