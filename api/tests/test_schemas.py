"""Unit tests for image analysis Pydantic schemas."""

import pytest
from pydantic import ValidationError

from app.schemas.image_analysis import (
    BrightnessContrastResult,
    DominantColor,
    ExposureResult,
    HistogramData,
    ImageAnalysis,
    LuminanceResult,
)


class TestDominantColor:
    """Tests for the DominantColor schema."""

    def test_valid_color(self) -> None:
        color = DominantColor(hex="#FF0000", percentage=50.0)
        assert color.hex == "#FF0000"
        assert color.percentage == 50.0

    def test_lowercase_hex_accepted(self) -> None:
        color = DominantColor(hex="#ff00aa", percentage=25.0)
        assert color.hex == "#ff00aa"

    def test_invalid_hex_rejected(self) -> None:
        with pytest.raises(ValidationError):
            DominantColor(hex="FF0000", percentage=50.0)  # missing #

    def test_short_hex_rejected(self) -> None:
        with pytest.raises(ValidationError):
            DominantColor(hex="#FFF", percentage=50.0)  # 3-digit hex

    def test_percentage_bounds(self) -> None:
        DominantColor(hex="#000000", percentage=0.0)
        DominantColor(hex="#000000", percentage=100.0)

        with pytest.raises(ValidationError):
            DominantColor(hex="#000000", percentage=-1.0)

        with pytest.raises(ValidationError):
            DominantColor(hex="#000000", percentage=101.0)


class TestLuminanceResult:
    """Tests for the LuminanceResult schema."""

    def test_valid_result(self) -> None:
        lr = LuminanceResult(mean=0.5, std=0.1, min=0.0, max=1.0)
        assert lr.mean == 0.5
        assert lr.std == 0.1

    def test_boundary_values(self) -> None:
        lr = LuminanceResult(mean=0.0, std=0.0, min=0.0, max=0.0)
        assert lr.mean == 0.0

        lr = LuminanceResult(mean=1.0, std=1.0, min=1.0, max=1.0)
        assert lr.max == 1.0

    def test_out_of_range_rejected(self) -> None:
        with pytest.raises(ValidationError):
            LuminanceResult(mean=1.5, std=0.0, min=0.0, max=1.0)

        with pytest.raises(ValidationError):
            LuminanceResult(mean=-0.1, std=0.0, min=0.0, max=1.0)


class TestBrightnessContrastResult:
    """Tests for the BrightnessContrastResult schema."""

    def test_valid_result(self) -> None:
        bc = BrightnessContrastResult(brightness=0.5, contrast=0.3)
        assert bc.brightness == 0.5
        assert bc.contrast == 0.3

    def test_out_of_range_rejected(self) -> None:
        with pytest.raises(ValidationError):
            BrightnessContrastResult(brightness=1.1, contrast=0.5)


class TestExposureResult:
    """Tests for the ExposureResult schema."""

    def test_valid_result(self) -> None:
        er = ExposureResult(
            exposure_score=0.5,
            highlight_clipping=0.01,
            shadow_clipping=0.02,
            dynamic_range=0.8,
        )
        assert er.exposure_score == 0.5
        assert er.dynamic_range == 0.8

    def test_out_of_range_rejected(self) -> None:
        with pytest.raises(ValidationError):
            ExposureResult(
                exposure_score=1.5,
                highlight_clipping=0.0,
                shadow_clipping=0.0,
                dynamic_range=0.5,
            )


class TestHistogramData:
    """Tests for the HistogramData schema."""

    def test_valid_histogram(self) -> None:
        bins = [0.0] * 256
        h = HistogramData(red=bins, green=bins, blue=bins, luminance=bins)
        assert len(h.red) == 256

    def test_wrong_length_rejected(self) -> None:
        short = [0.0] * 100
        full = [0.0] * 256
        with pytest.raises(ValidationError):
            HistogramData(red=short, green=full, blue=full, luminance=full)


class TestImageAnalysis:
    """Tests for the top-level ImageAnalysis schema."""

    def _make_valid_analysis(self) -> ImageAnalysis:
        bins = [0.0] * 256
        return ImageAnalysis(
            histogram=HistogramData(red=bins, green=bins, blue=bins, luminance=bins),
            luminance=LuminanceResult(mean=0.5, std=0.1, min=0.0, max=1.0),
            brightness_contrast=BrightnessContrastResult(brightness=0.5, contrast=0.3),
            dominant_colors=[
                DominantColor(hex="#FF0000", percentage=60.0),
                DominantColor(hex="#00FF00", percentage=40.0),
            ],
            exposure=ExposureResult(
                exposure_score=0.5,
                highlight_clipping=0.01,
                shadow_clipping=0.02,
                dynamic_range=0.8,
            ),
            image_width=1920,
            image_height=1080,
        )

    def test_valid_analysis(self) -> None:
        analysis = self._make_valid_analysis()
        assert analysis.image_width == 1920
        assert len(analysis.dominant_colors) == 2

    def test_empty_dominant_colors_rejected(self) -> None:
        bins = [0.0] * 256
        with pytest.raises(ValidationError):
            ImageAnalysis(
                histogram=HistogramData(
                    red=bins, green=bins, blue=bins, luminance=bins
                ),
                luminance=LuminanceResult(mean=0.5, std=0.1, min=0.0, max=1.0),
                brightness_contrast=BrightnessContrastResult(
                    brightness=0.5, contrast=0.3
                ),
                dominant_colors=[],  # min_length=1
                exposure=ExposureResult(
                    exposure_score=0.5,
                    highlight_clipping=0.0,
                    shadow_clipping=0.0,
                    dynamic_range=0.5,
                ),
                image_width=100,
                image_height=100,
            )

    def test_zero_dimension_rejected(self) -> None:
        bins = [0.0] * 256
        with pytest.raises(ValidationError):
            ImageAnalysis(
                histogram=HistogramData(
                    red=bins, green=bins, blue=bins, luminance=bins
                ),
                luminance=LuminanceResult(mean=0.5, std=0.1, min=0.0, max=1.0),
                brightness_contrast=BrightnessContrastResult(
                    brightness=0.5, contrast=0.3
                ),
                dominant_colors=[DominantColor(hex="#FF0000", percentage=100.0)],
                exposure=ExposureResult(
                    exposure_score=0.5,
                    highlight_clipping=0.0,
                    shadow_clipping=0.0,
                    dynamic_range=0.5,
                ),
                image_width=0,  # gt=0 violated
                image_height=100,
            )

    def test_serialization_round_trip(self) -> None:
        analysis = self._make_valid_analysis()
        json_str = analysis.model_dump_json()
        restored = ImageAnalysis.model_validate_json(json_str)
        assert restored.image_width == analysis.image_width
        assert len(restored.dominant_colors) == len(analysis.dominant_colors)
