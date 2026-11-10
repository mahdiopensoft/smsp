"""
bubble_normalizer.py — Compatibility Layer for BubbleStandardizer
=================================================================
Maintains backward compatibility while delegating all standardization,
aspect-ratio padding, and adaptive CLAHE to the enterprise BubbleStandardizer.
"""

import numpy as np
from typing import List
from .bubble_standardizer import BubbleStandardizer, OUTPUT_SIZE


class BubbleNormalizer(BubbleStandardizer):
    """
    Backward-compatible BubbleNormalizer inheriting from BubbleStandardizer.
    Converts raw bubble crops into standardized 48x48 float32 grayscale tensors in [0, 1].
    """
    def __init__(self, output_size: int = OUTPUT_SIZE):
        super().__init__(output_size=output_size)


def normalize_bubble(crop: np.ndarray) -> np.ndarray:
    """Convenience function for single bubble normalization."""
    return BubbleStandardizer().standardize(crop)
