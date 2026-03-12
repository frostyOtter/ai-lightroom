# Task: Exposure Detection

## Task Overview

**Task ID**: sprint-2-t06
**Task Name**: Exposure Detection
**Sprint**: 2
**Priority**: High
**Estimated Time**: 2 hours

---

## 1. Objective

Analyze image exposure to detect over/under-exposure, calculate an exposure score (0.0-1.0), measure dynamic range, and detect highlight/shadow clipping.

## 2. Why This Matters

**Business Value**:
- Exposure analysis directly informs the AI how to adjust highlights, shadows, whites, blacks
- Maps to `exposure_score` and `dynamic_range_score` in the `ImageAnalysis` schema

**Technical Value**:
- Clipping detection catches information loss that manual inspection might miss
- Dynamic range score helps the AI decide how aggressively to apply tone curve adjustments

## 3. Dependencies

**Prerequisites**:
- [ ] t01-analyzer-service
- [ ] t02-histogram-extraction (uses histogram data for clipping detection)

## 4. Acceptance Criteria

**Definition of Done**:
- [ ] Exposure score: 0.0 (severely under) to 1.0 (severely over), 0.5 = well-exposed
- [ ] Highlight clipping percentage (pixels > 250)
- [ ] Shadow clipping percentage (pixels < 5)
- [ ] Dynamic range score: 0.0-1.0
- [ ] Unit tests with known-exposure images

## 5. Technical Implementation

### Approach
- Exposure score: based on mean luminance distance from ideal (0.5)
  - `score = mean_luminance` (0.0 = pure black, 1.0 = pure white, 0.5 = ideal)
- Clipping: percentage of pixels at extremes
  - Highlight: pixel value > 250 (out of 255)
  - Shadow: pixel value < 5
- Dynamic range: spread of the luminance histogram
  - Based on percentile range (5th to 95th)

### Key Algorithm
```python
def analyze_exposure(image: np.ndarray) -> ExposureResult:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    exposure_score = float(np.mean(gray)) / 255.0
    highlight_clipping = float(np.sum(gray > 250)) / gray.size
    shadow_clipping = float(np.sum(gray < 5)) / gray.size
    p5, p95 = np.percentile(gray, [5, 95])
    dynamic_range = (p95 - p5) / 255.0
    return ExposureResult(...)
```

## 6. Testing Strategy

- Black image → exposure ≈ 0.0, shadow clipping ≈ 100%
- White image → exposure ≈ 1.0, highlight clipping ≈ 100%
- Mid-gray → exposure ≈ 0.5, no clipping
- High dynamic range image → dynamic_range close to 1.0
- Low dynamic range (flat) → dynamic_range close to 0.0

---

**Task Status**: Not Started
**Last Updated**: 2024-02-27
