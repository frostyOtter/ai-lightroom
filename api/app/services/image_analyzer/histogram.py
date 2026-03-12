"""Histogram extraction from images using OpenCV.

Extracts per-channel RGB histograms and a luminance histogram,
each with 256 bins normalized so the values sum to 1.0.
"""

import cv2
import numpy as np

from app.schemas.image_analysis import HistogramData


def extract_histograms(image: np.ndarray) -> HistogramData:
    """Extract RGB and luminance histograms from a BGR image.

    Args:
        image: BGR image as a NumPy array (H, W, 3).

    Returns:
        HistogramData with normalized 256-bin histograms for R, G, B,
        and luminance channels.
    """
    channels: dict[str, list[float]] = {}

    # OpenCV uses BGR ordering — map to our schema names
    channel_map = {0: "blue", 1: "green", 2: "red"}

    for idx, name in channel_map.items():
        hist = cv2.calcHist([image], [idx], None, [256], [0, 256])
        total = float(hist.sum())
        if total > 0:
            normalized = (hist.flatten() / total).tolist()
        else:
            normalized = [0.0] * 256
        channels[name] = normalized

    # Luminance histogram from grayscale conversion
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lum_hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    lum_total = float(lum_hist.sum())
    if lum_total > 0:
        lum_normalized = (lum_hist.flatten() / lum_total).tolist()
    else:
        lum_normalized = [0.0] * 256

    return HistogramData(
        red=channels["red"],
        green=channels["green"],
        blue=channels["blue"],
        luminance=lum_normalized,
    )
