"""Pydantic schemas for image analysis results.

These schemas define the data structures returned by the ImageAnalyzer
service. All scores are normalized to 0.0-1.0 ranges for consistency.
"""

from pydantic import BaseModel, Field


class HistogramData(BaseModel):
    """RGB and luminance histogram data.

    Each channel contains 256 normalized values (0.0-1.0) representing
    the proportion of pixels at each intensity level.
    """

    red: list[float] = Field(
        ...,
        min_length=256,
        max_length=256,
        description="Red channel histogram (256 bins, normalized)",
    )
    green: list[float] = Field(
        ...,
        min_length=256,
        max_length=256,
        description="Green channel histogram (256 bins, normalized)",
    )
    blue: list[float] = Field(
        ...,
        min_length=256,
        max_length=256,
        description="Blue channel histogram (256 bins, normalized)",
    )
    luminance: list[float] = Field(
        ...,
        min_length=256,
        max_length=256,
        description="Luminance histogram (256 bins, normalized)",
    )


class DominantColor(BaseModel):
    """A single dominant color detected in an image.

    Attributes:
        hex: Color in #RRGGBB format.
        percentage: Percentage of image covered (0.0-100.0).
    """

    hex: str = Field(
        ...,
        pattern=r"^#[0-9A-Fa-f]{6}$",
        description="Hex color code (#RRGGBB)",
    )
    percentage: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Percentage of image covered by this color",
    )


class LuminanceResult(BaseModel):
    """Luminance statistics for an image.

    All values are normalized to the 0.0-1.0 range.

    Attributes:
        mean: Average luminance.
        std: Standard deviation of luminance.
        min: Minimum luminance value.
        max: Maximum luminance value.
    """

    mean: float = Field(..., ge=0.0, le=1.0, description="Average luminance")
    std: float = Field(..., ge=0.0, le=1.0, description="Luminance standard deviation")
    min: float = Field(..., ge=0.0, le=1.0, description="Minimum luminance")
    max: float = Field(..., ge=0.0, le=1.0, description="Maximum luminance")


class BrightnessContrastResult(BaseModel):
    """Brightness and contrast scores.

    Attributes:
        brightness: 0.0 (black) to 1.0 (white).
        contrast: 0.0 (flat/no contrast) to 1.0 (maximum contrast).
    """

    brightness: float = Field(
        ..., ge=0.0, le=1.0, description="Brightness score (0=dark, 1=bright)"
    )
    contrast: float = Field(
        ..., ge=0.0, le=1.0, description="Contrast score (0=flat, 1=high contrast)"
    )


class ExposureResult(BaseModel):
    """Exposure analysis results.

    Attributes:
        exposure_score: 0.0 (under-exposed) to 1.0 (over-exposed), 0.5 = ideal.
        highlight_clipping: Fraction of pixels clipped in highlights (0.0-1.0).
        shadow_clipping: Fraction of pixels clipped in shadows (0.0-1.0).
        dynamic_range: 0.0 (narrow) to 1.0 (full range).
    """

    exposure_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Exposure score (0=under, 0.5=ideal, 1=over)",
    )
    highlight_clipping: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Fraction of pixels clipped in highlights",
    )
    shadow_clipping: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Fraction of pixels clipped in shadows",
    )
    dynamic_range: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Dynamic range score (0=narrow, 1=full)",
    )


class ImageAnalysis(BaseModel):
    """Complete image analysis result.

    This is the top-level schema returned by the ImageAnalyzer service.
    It aggregates results from all analysis sub-modules.

    Attributes:
        histogram: RGB and luminance histograms.
        luminance: Luminance statistics.
        brightness_contrast: Brightness and contrast scores.
        dominant_colors: Top dominant colors with percentages.
        exposure: Exposure analysis results.
        image_width: Width of the analyzed image in pixels.
        image_height: Height of the analyzed image in pixels.
    """

    histogram: HistogramData = Field(..., description="RGB and luminance histograms")
    luminance: LuminanceResult = Field(..., description="Luminance statistics")
    brightness_contrast: BrightnessContrastResult = Field(
        ..., description="Brightness and contrast scores"
    )
    dominant_colors: list[DominantColor] = Field(
        ...,
        min_length=1,
        max_length=10,
        description="Dominant colors sorted by percentage descending",
    )
    exposure: ExposureResult = Field(..., description="Exposure analysis results")
    image_width: int = Field(..., gt=0, description="Image width in pixels")
    image_height: int = Field(..., gt=0, description="Image height in pixels")
