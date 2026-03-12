"""Image analysis orchestrator.

The ImageAnalyzer class is the single entry point for all image
analysis operations.  It decodes raw image bytes, optionally resizes
for performance, runs every analysis sub-module, and returns a
comprehensive ImageAnalysis result.
"""

import logging

import cv2
import numpy as np

from app.schemas.image_analysis import ImageAnalysis
from app.services.image_analyzer.brightness_contrast import (
    calculate_brightness_contrast,
)
from app.services.image_analyzer.colors import detect_dominant_colors
from app.services.image_analyzer.exceptions import (
    AnalysisProcessingError,
    InvalidImageError,
)
from app.services.image_analyzer.exposure import analyze_exposure
from app.services.image_analyzer.histogram import extract_histograms
from app.services.image_analyzer.luminance import calculate_luminance

logger = logging.getLogger(__name__)

# Images larger than this (on their longest side) will be resized
# before analysis to keep processing fast and memory reasonable.
_MAX_DIMENSION = 1920


def _decode_image(image_bytes: bytes) -> np.ndarray:
    """Decode raw bytes into a BGR NumPy array.

    Args:
        image_bytes: Raw image file bytes (JPEG, PNG, WebP, etc.).

    Returns:
        BGR image as a NumPy array.

    Raises:
        InvalidImageError: If the bytes cannot be decoded.
    """
    if not image_bytes:
        raise InvalidImageError("Empty image bytes provided")

    buf = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(buf, cv2.IMREAD_COLOR)
    if image is None:
        raise InvalidImageError(
            "Could not decode image bytes — invalid or corrupt file"
        )
    return image


def _resize_if_needed(image: np.ndarray) -> np.ndarray:
    """Down-scale an image if its longest side exceeds _MAX_DIMENSION.

    Preserves aspect ratio.  Returns the original array unchanged if
    the image is already within limits.

    Args:
        image: BGR image.

    Returns:
        Possibly resized BGR image.
    """
    h, w = image.shape[:2]
    longest = max(h, w)
    if longest <= _MAX_DIMENSION:
        return image

    scale = _MAX_DIMENSION / longest
    new_w = max(int(w * scale), 1)
    new_h = max(int(h * scale), 1)
    resized: np.ndarray = cv2.resize(
        image, (new_w, new_h), interpolation=cv2.INTER_AREA
    )
    logger.debug("Resized image from %dx%d to %dx%d", w, h, new_w, new_h)
    return resized


class ImageAnalyzer:
    """Orchestrates comprehensive image analysis.

    Usage::

        analyzer = ImageAnalyzer()
        result = analyzer.analyze(image_bytes)
        print(result.luminance.mean)

    All public methods accept raw image bytes and handle decoding
    internally, so callers never need to touch OpenCV directly.
    """

    def analyze(self, image_bytes: bytes) -> ImageAnalysis:
        """Run the full analysis pipeline on an image.

        Args:
            image_bytes: Raw image file bytes.

        Returns:
            ImageAnalysis containing histogram, luminance, brightness/
            contrast, dominant colors, and exposure data.

        Raises:
            InvalidImageError: If bytes cannot be decoded.
            AnalysisProcessingError: If any analysis step fails.
        """
        image = _decode_image(image_bytes)
        original_h, original_w = image.shape[:2]

        # Resize for faster processing (analysis results are
        # independent of resolution for the metrics we compute).
        image = _resize_if_needed(image)

        try:
            histogram = extract_histograms(image)
            lum = calculate_luminance(image)
            bc = calculate_brightness_contrast(image)
            colors = detect_dominant_colors(image)
            exposure = analyze_exposure(image)
        except Exception as exc:
            logger.error("Image analysis failed: %s", exc, exc_info=True)
            raise AnalysisProcessingError(
                f"Analysis computation failed: {exc}"
            ) from exc

        return ImageAnalysis(
            histogram=histogram,
            luminance=lum,
            brightness_contrast=bc,
            dominant_colors=colors,
            exposure=exposure,
            image_width=original_w,
            image_height=original_h,
        )
