# Task: Histogram Extraction

## Task Overview

**Task ID**: sprint-2-t02
**Task Name**: Histogram Extraction
**Sprint**: 2
**Priority**: High
**Estimated Time**: 3 hours

---

## 1. Objective

Extract RGB channel histograms and a luminance histogram from an image, returning normalized values (0.0-1.0) suitable for analysis and AI prompt context.

## 2. Why This Matters

**Business Value**:
- Histograms reveal the tonal distribution — critical for understanding if an image needs exposure/contrast corrections
- Feeds directly into the AI prompt so Gemini can make informed adjustment decisions

**Technical Value**:
- Foundation for exposure detection and brightness/contrast scoring
- Industry-standard image analysis technique

## 3. Dependencies

**Prerequisites**:
- [ ] t01-analyzer-service (provides the orchestrator)

**Blocking**:
- [ ] t06-exposure-detection (uses histogram data)

## 4. Acceptance Criteria

**Definition of Done**:
- [ ] R, G, B channel histograms extracted (256 bins each)
- [ ] Luminance histogram calculated
- [ ] All values normalized to 0.0-1.0
- [ ] Output uses `HistogramData` Pydantic schema
- [ ] Unit tests with known input → expected output

## 5. Technical Implementation

### Approach
- Use `cv2.calcHist()` for per-channel histogram extraction
- Convert to grayscale for luminance histogram
- Normalize using `cv2.normalize()` or divide by pixel count
- Return as lists of 256 float values

### Key Algorithm
```python
def extract_histograms(image: np.ndarray) -> HistogramData:
    for channel in [0, 1, 2]:  # B, G, R in OpenCV
        hist = cv2.calcHist([image], [channel], None, [256], [0, 256])
        normalized = hist.flatten() / hist.sum()
    # Luminance: convert BGR → Gray, then calcHist
```

## 6. Testing Strategy

- Test with solid-color image (histogram should peak at one bin)
- Test with gradient image (histogram should be roughly uniform)
- Verify normalization sums to ~1.0
- Test with small and large images

---

**Task Status**: Not Started
**Last Updated**: 2024-02-27
