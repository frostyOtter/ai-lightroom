"""Custom exceptions for image analysis."""


class ImageAnalysisError(Exception):
    """Base exception for image analysis errors."""


class InvalidImageError(ImageAnalysisError):
    """Raised when image bytes cannot be decoded."""


class AnalysisProcessingError(ImageAnalysisError):
    """Raised when an analysis computation fails."""
