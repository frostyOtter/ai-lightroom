"""Brightness and contrast measurement.

Brightness is derived from mean luminance. Contrast is derived from
the standard deviation of luminance, normalized to a 0.0-1.0 scale.
"""

import numpy as np

from app.schemas.image_analysis import BrightnessContrastResult
from app.services.image_analyzer.luminance import compute_luminance_map

# Maximum possible std dev for luminance occurs with a 50/50 black/white
# image, which gives std ≈ 0.5.  We use this as the normalization factor.
_MAX_STD = 0.5


def calculate_brightness_contrast(
    image: np.ndarray,
) -> BrightnessContrastResult:
    """Calculate brightness and contrast scores for a BGR image.

    Args:
        image: BGR image as a NumPy array (H, W, 3), uint8.

    Returns:
        BrightnessContrastResult with brightness and contrast in [0.0, 1.0].
    """
    luminance = compute_luminance_map(image)

    brightness = float(np.mean(luminance))
    contrast = min(float(np.std(luminance)) / _MAX_STD, 1.0)

    return BrightnessContrastResult(
        brightness=brightness,
        contrast=contrast,
    )
