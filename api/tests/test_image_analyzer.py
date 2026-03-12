"""Unit tests for the image analyzer service and all sub-modules.

Uses synthetic images (solid colors, gradients, half-split) with
known properties so expected analysis results can be asserted precisely.
"""

import cv2
import numpy as np
import pytest

from app.services.image_analyzer import (
    ImageAnalyzer,
    InvalidImageError,
)
from app.services.image_analyzer.brightness_contrast import (
    calculate_brightness_contrast,
)
from app.services.image_analyzer.colors import _bgr_to_hex, detect_dominant_colors
from app.services.image_analyzer.exposure import analyze_exposure
from app.services.image_analyzer.histogram import extract_histograms
from app.services.image_analyzer.luminance import (
    calculate_luminance,
    compute_luminance_map,
)

# ─── Helpers ──────────────────────────────────────────────────────


def _encode(image: np.ndarray, fmt: str = ".png") -> bytes:
    """Encode a NumPy BGR image to bytes."""
    ok, buf = cv2.imencode(fmt, image)
    assert ok
    return buf.tobytes()


def _solid(color_bgr: tuple[int, int, int], size: int = 100) -> np.ndarray:
    """Create a solid-color BGR image."""
    img = np.zeros((size, size, 3), dtype=np.uint8)
    img[:, :] = color_bgr
    return img


def _half_split(
    left_bgr: tuple[int, int, int],
    right_bgr: tuple[int, int, int],
    size: int = 100,
) -> np.ndarray:
    """Create an image split vertically: left half one color, right half another."""
    img = np.zeros((size, size * 2, 3), dtype=np.uint8)
    img[:, :size] = left_bgr
    img[:, size:] = right_bgr
    return img


# ─── Histogram Tests ──────────────────────────────────────────────


class TestHistogramExtraction:
    """Tests for histogram.py."""

    def test_solid_red_histogram(self) -> None:
        img = _solid((0, 0, 255))  # BGR red
        h = extract_histograms(img)

        # Red channel should peak at bin 255
        assert h.red[255] == pytest.approx(1.0)
        assert sum(h.red) == pytest.approx(1.0)

        # Green and Blue channels should peak at bin 0
        assert h.green[0] == pytest.approx(1.0)
        assert h.blue[0] == pytest.approx(1.0)

    def test_solid_white_luminance(self) -> None:
        img = _solid((255, 255, 255))
        h = extract_histograms(img)
        assert h.luminance[255] == pytest.approx(1.0)

    def test_histogram_normalization_sums_to_one(self) -> None:
        img = np.random.randint(0, 256, (50, 50, 3), dtype=np.uint8)
        h = extract_histograms(img)
        assert sum(h.red) == pytest.approx(1.0, abs=1e-6)
        assert sum(h.green) == pytest.approx(1.0, abs=1e-6)
        assert sum(h.blue) == pytest.approx(1.0, abs=1e-6)
        assert sum(h.luminance) == pytest.approx(1.0, abs=1e-6)

    def test_histogram_length(self) -> None:
        img = _solid((128, 128, 128))
        h = extract_histograms(img)
        assert len(h.red) == 256
        assert len(h.green) == 256
        assert len(h.blue) == 256
        assert len(h.luminance) == 256


# ─── Luminance Tests ──────────────────────────────────────────────


class TestLuminanceCalculation:
    """Tests for luminance.py."""

    def test_black_image_luminance(self) -> None:
        img = _solid((0, 0, 0))
        lum = calculate_luminance(img)
        assert lum.mean == pytest.approx(0.0, abs=1e-4)
        assert lum.std == pytest.approx(0.0, abs=1e-4)

    def test_white_image_luminance(self) -> None:
        img = _solid((255, 255, 255))
        lum = calculate_luminance(img)
        assert lum.mean == pytest.approx(1.0, abs=1e-3)
        assert lum.std == pytest.approx(0.0, abs=1e-4)

    def test_mid_gray_luminance(self) -> None:
        img = _solid((128, 128, 128))
        lum = calculate_luminance(img)
        expected = 128.0 / 255.0  # ~0.502
        assert lum.mean == pytest.approx(expected, abs=1e-2)

    def test_pure_green_luminance(self) -> None:
        """Pure green should have luminance ≈ 0.7152 (BT.709 G weight)."""
        img = _solid((0, 255, 0))  # BGR: G=255
        lum = calculate_luminance(img)
        assert lum.mean == pytest.approx(0.7152, abs=1e-3)

    def test_pure_red_luminance(self) -> None:
        """Pure red should have luminance ≈ 0.2126 (BT.709 R weight)."""
        img = _solid((0, 0, 255))  # BGR: R=255
        lum = calculate_luminance(img)
        assert lum.mean == pytest.approx(0.2126, abs=1e-3)

    def test_pure_blue_luminance(self) -> None:
        """Pure blue should have luminance ≈ 0.0722 (BT.709 B weight)."""
        img = _solid((255, 0, 0))  # BGR: B=255
        lum = calculate_luminance(img)
        assert lum.mean == pytest.approx(0.0722, abs=1e-3)

    def test_luminance_map_shape(self) -> None:
        img = _solid((100, 150, 200), size=50)
        lum_map = compute_luminance_map(img)
        assert lum_map.shape == (50, 50)
        assert lum_map.dtype == np.float32

    def test_luminance_min_max(self) -> None:
        img = _half_split((0, 0, 0), (255, 255, 255))
        lum = calculate_luminance(img)
        assert lum.min == pytest.approx(0.0, abs=1e-4)
        assert lum.max == pytest.approx(1.0, abs=1e-3)


# ─── Brightness / Contrast Tests ─────────────────────────────────


class TestBrightnessContrast:
    """Tests for brightness_contrast.py."""

    def test_mid_gray_brightness(self) -> None:
        img = _solid((128, 128, 128))
        bc = calculate_brightness_contrast(img)
        assert bc.brightness == pytest.approx(0.5, abs=0.02)

    def test_solid_image_zero_contrast(self) -> None:
        img = _solid((100, 100, 100))
        bc = calculate_brightness_contrast(img)
        assert bc.contrast == pytest.approx(0.0, abs=1e-4)

    def test_half_bw_high_contrast(self) -> None:
        img = _half_split((0, 0, 0), (255, 255, 255))
        bc = calculate_brightness_contrast(img)
        assert bc.contrast > 0.9

    def test_black_image_low_brightness(self) -> None:
        img = _solid((0, 0, 0))
        bc = calculate_brightness_contrast(img)
        assert bc.brightness == pytest.approx(0.0, abs=1e-4)

    def test_white_image_high_brightness(self) -> None:
        img = _solid((255, 255, 255))
        bc = calculate_brightness_contrast(img)
        assert bc.brightness == pytest.approx(1.0, abs=1e-3)

    def test_contrast_clamped_to_one(self) -> None:
        """Contrast should never exceed 1.0."""
        img = _half_split((0, 0, 0), (255, 255, 255))
        bc = calculate_brightness_contrast(img)
        assert bc.contrast <= 1.0


# ─── Dominant Color Tests ─────────────────────────────────────────


class TestDominantColors:
    """Tests for colors.py."""

    def test_solid_red_single_color(self) -> None:
        img = _solid((0, 0, 255))  # BGR red
        colors = detect_dominant_colors(img, k=5)
        assert len(colors) == 1  # Only one unique color
        assert colors[0].hex == "#FF0000"
        assert colors[0].percentage == pytest.approx(100.0)

    def test_two_color_split(self) -> None:
        img = _half_split((0, 0, 0), (255, 255, 255))
        colors = detect_dominant_colors(img, k=2)
        assert len(colors) == 2
        total = sum(c.percentage for c in colors)
        assert total == pytest.approx(100.0, abs=0.1)

    def test_hex_format(self) -> None:
        img = _solid((0, 128, 255))  # BGR → R=255, G=128, B=0
        colors = detect_dominant_colors(img, k=1)
        assert colors[0].hex.startswith("#")
        assert len(colors[0].hex) == 7

    def test_sorted_by_percentage_desc(self) -> None:
        # Create an image with 75% blue, 25% red
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[:75, :] = [255, 0, 0]  # BGR blue
        img[75:, :] = [0, 0, 255]  # BGR red
        colors = detect_dominant_colors(img, k=2)
        assert colors[0].percentage >= colors[1].percentage

    def test_bgr_to_hex_conversion(self) -> None:
        assert _bgr_to_hex(np.array([0, 0, 255])) == "#FF0000"
        assert _bgr_to_hex(np.array([0, 255, 0])) == "#00FF00"
        assert _bgr_to_hex(np.array([255, 0, 0])) == "#0000FF"
        assert _bgr_to_hex(np.array([255, 255, 255])) == "#FFFFFF"
        assert _bgr_to_hex(np.array([0, 0, 0])) == "#000000"

    def test_k_greater_than_unique_colors(self) -> None:
        """If k > unique colors, should return fewer results without crashing."""
        img = _solid((100, 200, 50))
        colors = detect_dominant_colors(img, k=10)
        assert len(colors) >= 1


# ─── Exposure Detection Tests ─────────────────────────────────────


class TestExposureDetection:
    """Tests for exposure.py."""

    def test_black_image_exposure(self) -> None:
        img = _solid((0, 0, 0))
        exp = analyze_exposure(img)
        assert exp.exposure_score == pytest.approx(0.0, abs=1e-4)
        assert exp.shadow_clipping == pytest.approx(1.0, abs=1e-4)
        assert exp.highlight_clipping == pytest.approx(0.0, abs=1e-4)

    def test_white_image_exposure(self) -> None:
        img = _solid((255, 255, 255))
        exp = analyze_exposure(img)
        assert exp.exposure_score == pytest.approx(1.0, abs=1e-4)
        assert exp.highlight_clipping == pytest.approx(1.0, abs=1e-4)
        assert exp.shadow_clipping == pytest.approx(0.0, abs=1e-4)

    def test_mid_gray_well_exposed(self) -> None:
        img = _solid((128, 128, 128))
        exp = analyze_exposure(img)
        assert 0.4 < exp.exposure_score < 0.6
        assert exp.highlight_clipping == pytest.approx(0.0, abs=1e-4)
        assert exp.shadow_clipping == pytest.approx(0.0, abs=1e-4)

    def test_high_dynamic_range(self) -> None:
        img = _half_split((0, 0, 0), (255, 255, 255))
        exp = analyze_exposure(img)
        assert exp.dynamic_range > 0.9

    def test_low_dynamic_range(self) -> None:
        img = _solid((128, 128, 128))
        exp = analyze_exposure(img)
        assert exp.dynamic_range == pytest.approx(0.0, abs=0.01)

    def test_exposure_values_in_range(self) -> None:
        img = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        exp = analyze_exposure(img)
        assert 0.0 <= exp.exposure_score <= 1.0
        assert 0.0 <= exp.highlight_clipping <= 1.0
        assert 0.0 <= exp.shadow_clipping <= 1.0
        assert 0.0 <= exp.dynamic_range <= 1.0


# ─── ImageAnalyzer Integration Tests ─────────────────────────────


class TestImageAnalyzer:
    """Integration tests for the ImageAnalyzer orchestrator."""

    def setup_method(self) -> None:
        self.analyzer = ImageAnalyzer()

    def test_analyze_solid_image(self) -> None:
        img = _solid((128, 128, 128))
        result = self.analyzer.analyze(_encode(img))
        assert result.image_width == 100
        assert result.image_height == 100
        assert 0.4 < result.luminance.mean < 0.6

    def test_analyze_returns_all_fields(self) -> None:
        img = _solid((50, 100, 200))
        result = self.analyzer.analyze(_encode(img))
        assert result.histogram is not None
        assert result.luminance is not None
        assert result.brightness_contrast is not None
        assert len(result.dominant_colors) >= 1
        assert result.exposure is not None

    def test_analyze_invalid_bytes_raises(self) -> None:
        with pytest.raises(InvalidImageError):
            self.analyzer.analyze(b"not a valid image")

    def test_analyze_empty_bytes_raises(self) -> None:
        with pytest.raises(InvalidImageError):
            self.analyzer.analyze(b"")

    def test_analyze_large_image_preserves_original_dimensions(self) -> None:
        img = np.random.randint(0, 256, (3000, 4000, 3), dtype=np.uint8)
        result = self.analyzer.analyze(_encode(img, ".jpg"))
        assert result.image_width == 4000
        assert result.image_height == 3000

    def test_analyze_jpeg_format(self) -> None:
        img = _solid((100, 150, 200))
        result = self.analyzer.analyze(_encode(img, ".jpg"))
        assert result.image_width == 100

    def test_analyze_small_image_no_resize(self) -> None:
        img = np.zeros((10, 10, 3), dtype=np.uint8)
        img[:, :] = [100, 100, 100]
        result = self.analyzer.analyze(_encode(img))
        assert result.image_width == 10
        assert result.image_height == 10

    def test_analyze_gradient_image(self) -> None:
        """A horizontal gradient should have moderate contrast."""
        gradient = np.zeros((100, 256, 3), dtype=np.uint8)
        for i in range(256):
            gradient[:, i] = [i, i, i]
        result = self.analyzer.analyze(_encode(gradient))
        assert result.brightness_contrast.contrast > 0.3
        assert 0.3 < result.luminance.mean < 0.7

    def test_analyze_single_pixel_image(self) -> None:
        """Smallest possible image should still work."""
        img = np.array([[[128, 128, 128]]], dtype=np.uint8)
        result = self.analyzer.analyze(_encode(img))
        assert result.image_width == 1
        assert result.image_height == 1
