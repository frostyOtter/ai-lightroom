"""Dominant color detection using OpenCV KMeans clustering.

Extracts the top-K dominant colors from an image by clustering pixel
colors and ranking clusters by membership count.
"""

import cv2
import numpy as np

from app.schemas.image_analysis import DominantColor

# Target size for downsampling before KMeans (keeps it fast)
_KMEANS_SIZE = 100


def _bgr_to_hex(bgr: np.ndarray) -> str:
    """Convert a BGR color array to a hex string (#RRGGBB).

    Args:
        bgr: Array of shape (3,) with B, G, R values (0-255).

    Returns:
        Hex color string, e.g. '#FF8800'.
    """
    b, g, r = int(bgr[0]), int(bgr[1]), int(bgr[2])
    return f"#{r:02X}{g:02X}{b:02X}"


def detect_dominant_colors(image: np.ndarray, k: int = 5) -> list[DominantColor]:
    """Detect the top-K dominant colors in a BGR image.

    The image is downsampled to a small size for performance, then
    OpenCV KMeans clustering is applied to group similar pixel colors.

    Args:
        image: BGR image as a NumPy array (H, W, 3), uint8.
        k: Number of dominant colors to extract (default 5).

    Returns:
        List of DominantColor sorted by percentage descending.
    """
    # Downsample for speed
    h, w = image.shape[:2]
    scale = min(_KMEANS_SIZE / max(h, w), 1.0)
    if scale < 1.0:
        new_w = max(int(w * scale), 1)
        new_h = max(int(h * scale), 1)
        small = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    else:
        small = image

    # Reshape to (N, 3) pixel array
    pixels = small.reshape(-1, 3).astype(np.float32)

    # Ensure k doesn't exceed unique pixel count
    unique_pixels = np.unique(pixels, axis=0)
    unique_count = len(unique_pixels)
    k = min(k, unique_count)

    # Fast path: if there's only one unique color, skip KMeans
    if unique_count == 1:
        hex_color = _bgr_to_hex(unique_pixels[0])
        return [DominantColor(hex=hex_color, percentage=100.0)]

    # KMeans clustering
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 3, cv2.KMEANS_PP_CENTERS)

    # Count membership per cluster
    labels_flat = labels.flatten()
    total_pixels = len(labels_flat)

    # Build results sorted by percentage descending
    results: list[DominantColor] = []
    for i in range(k):
        count = int(np.sum(labels_flat == i))
        percentage = (count / total_pixels) * 100.0
        hex_color = _bgr_to_hex(centers[i])
        results.append(DominantColor(hex=hex_color, percentage=round(percentage, 2)))

    results.sort(key=lambda c: c.percentage, reverse=True)
    return results
