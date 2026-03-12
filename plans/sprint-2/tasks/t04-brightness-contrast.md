# Task: Brightness & Contrast Measurement

## Task Overview

**Task ID**: sprint-2-t04
**Task Name**: Brightness & Contrast Measurement
**Sprint**: 2
**Priority**: High
**Estimated Time**: 2 hours

---

## 1. Objective

Calculate normalized brightness and contrast scores (0.0-1.0) from an image. Brightness is derived from mean luminance; contrast is derived from the standard deviation of luminance.

## 2. Why This Matters

**Business Value**:
- Brightness and contrast scores directly inform how much exposure/contrast adjustment the AI should recommend
- Maps to the `contrast_score` field in the `ImageAnalysis` schema

**Technical Value**:
- Simple, well-understood metrics
- Reuses luminance computation for efficiency

## 3. Dependencies

**Prerequisites**:
- [ ] t01-analyzer-service
- [ ] t03-luminance-calculation (shares luminance computation)

## 4. Acceptance Criteria

**Definition of Done**:
- [ ] Brightness score: normalized 0.0-1.0
- [ ] Contrast score: normalized 0.0-1.0
- [ ] Values are meaningful (low contrast image → low score, etc.)
- [ ] Unit tests with synthetic images

## 5. Technical Implementation

### Approach
- Brightness = mean luminance (already 0-1)
- Contrast = standard deviation of luminance, scaled to 0-1
  - Max possible std dev for luminance ~ 0.5 (half black / half white image)
  - Normalize by dividing by 0.5 and clamping to 1.0

### Key Algorithm
```python
def calculate_brightness_contrast(image: np.ndarray) -> BrightnessContrastResult:
    luminance = compute_luminance_map(image)
    brightness = float(np.mean(luminance))
    contrast = min(float(np.std(luminance)) / 0.5, 1.0)
    return BrightnessContrastResult(brightness=brightness, contrast=contrast)
```

## 6. Testing Strategy

- Solid gray image → brightness ≈ 0.5, contrast ≈ 0.0
- Half black / half white → brightness ≈ 0.5, contrast → high
- All white → brightness ≈ 1.0, contrast ≈ 0.0

---

**Task Status**: Not Started
**Last Updated**: 2024-02-27
