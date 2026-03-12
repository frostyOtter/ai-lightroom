"""Luminance calculation using ITU-R BT.709 coefficients.

Computes perceptual luminance from an image using the standard
weighting: L = 0.2126*R + 0.7152*G + 0.0722*B.
"""

import cv2
import numpy as np

from app.schemas.image_analysis import LuminanceResult

# ITU-R BT.709 luminance coefficients
_WEIGHT_R = 0.2126
_WEIGHT_G = 0.7152
_WEIGHT_B = 0.0722


def compute_luminance_map(image: np.ndarray) -> np.ndarray:
    """Compute a per-pixel luminance map from a BGR image.

    Args:
        image: BGR image as a NumPy array (H, W, 3), uint8.

    Returns:
        2D float32 array (H, W) with luminance values in [0.0, 1.0].
    """
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    luminance: np.ndarray = (
        _WEIGHT_R * rgb[:, :, 0] + _WEIGHT_G * rgb[:, :, 1] + _WEIGHT_B * rgb[:, :, 2]
    )
    return luminance


def calculate_luminance(image: np.ndarray) -> LuminanceResult:
    """Calculate luminance statistics for a BGR image.

    Args:
        image: BGR image as a NumPy array (H, W, 3), uint8.

    Returns:
        LuminanceResult with mean, std, min, max luminance (all 0.0-1.0).
    """
    luminance = compute_luminance_map(image)
    return LuminanceResult(
        mean=float(np.mean(luminance)),
        std=float(np.std(luminance)),
        min=float(np.min(luminance)),
        max=float(np.max(luminance)),
    )
