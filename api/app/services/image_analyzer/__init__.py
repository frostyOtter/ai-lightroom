"""Image analyzer service.

Exposes the public API for image analysis:

    from app.services.image_analyzer import ImageAnalyzer

    analyzer = ImageAnalyzer()
    result = analyzer.analyze(raw_bytes)
"""

from app.services.image_analyzer.analyzer import ImageAnalyzer
from app.services.image_analyzer.exceptions import (
    AnalysisProcessingError,
    ImageAnalysisError,
    InvalidImageError,
)

__all__ = [
    "AnalysisProcessingError",
    "ImageAnalysisError",
    "ImageAnalyzer",
    "InvalidImageError",
]
