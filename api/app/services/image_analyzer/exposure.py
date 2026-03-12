"""Exposure analysis: score, clipping detection, and dynamic range.

Analyzes image exposure by examining the grayscale intensity
distribution to detect over/under-exposure and information loss.
"""

import cv2
import numpy as np

from app.schemas.image_analysis import ExposureResult

# Pixel thresholds for clipping detection
_HIGHLIGHT_THRESHOLD = 250  # Pixels above this are "clipped" highlights
_SHADOW_THRESHOLD = 5  # Pixels below this are "clipped" shadows

# Percentiles used for dynamic range calculation
_DR_LOW_PERCENTILE = 5
_DR_HIGH_PERCENTILE = 95


def analyze_exposure(image: np.ndarray) -> ExposureResult:
    """Analyze image exposure characteristics.

    Args:
        image: BGR image as a NumPy array (H, W, 3), uint8.

    Returns:
        ExposureResult with exposure_score, highlight/shadow clipping
        fractions, and dynamic_range score (all 0.0-1.0).
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    total_pixels = float(gray.size)

    # Exposure score: mean brightness normalized to 0-1
    exposure_score = float(np.mean(gray)) / 255.0

    # Clipping detection
    highlight_clipping = float(np.sum(gray > _HIGHLIGHT_THRESHOLD)) / total_pixels
    shadow_clipping = float(np.sum(gray < _SHADOW_THRESHOLD)) / total_pixels

    # Dynamic range: spread between 5th and 95th percentiles
    p_low, p_high = np.percentile(gray, [_DR_LOW_PERCENTILE, _DR_HIGH_PERCENTILE])
    dynamic_range = float(p_high - p_low) / 255.0

    return ExposureResult(
        exposure_score=round(exposure_score, 6),
        highlight_clipping=round(highlight_clipping, 6),
        shadow_clipping=round(shadow_clipping, 6),
        dynamic_range=round(dynamic_range, 6),
    )
