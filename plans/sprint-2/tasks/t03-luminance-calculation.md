# Task: Luminance Calculation

## Task Overview

**Task ID**: sprint-2-t03
**Task Name**: Luminance Calculation
**Sprint**: 2
**Priority**: High
**Estimated Time**: 2 hours

---

## 1. Objective

Calculate overall average luminance and luminance distribution statistics from an image, using standard ITU-R BT.709 coefficients.

## 2. Why This Matters

**Business Value**:
- Luminance is the primary measure of perceived brightness — essential for exposure correction recommendations
- Provides the `exposure_score` field required by the `ImageAnalysis` schema

**Technical Value**:
- Uses standard weighting (0.2126R + 0.7152G + 0.0722B) for perceptually accurate results
- Forms the basis of brightness scoring

## 3. Dependencies

**Prerequisites**:
- [ ] t01-analyzer-service

## 4. Acceptance Criteria

**Definition of Done**:
- [ ] Average luminance calculated (0.0-1.0 normalized)
- [ ] Luminance distribution computed (std dev, min, max)
- [ ] Edge cases handled (all-black, all-white, single-pixel images)
- [ ] Unit tests passing

## 5. Technical Implementation

### Approach
- Convert image from BGR to RGB
- Apply BT.709 luminance weights: `L = 0.2126*R + 0.7152*G + 0.0722*B`
- Normalize pixel values to 0.0-1.0 range
- Compute mean, std, min, max

### Key Algorithm
```python
def calculate_luminance(image: np.ndarray) -> LuminanceResult:
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    luminance = 0.2126 * rgb[:,:,0] + 0.7152 * rgb[:,:,1] + 0.0722 * rgb[:,:,2]
    return LuminanceResult(
        mean=float(np.mean(luminance)),
        std=float(np.std(luminance)),
        min=float(np.min(luminance)),
        max=float(np.max(luminance)),
    )
```

## 6. Testing Strategy

- Black image → luminance ≈ 0.0
- White image → luminance ≈ 1.0
- 50% gray image → luminance ≈ 0.5
- Pure red/green/blue images → verify weighted calculation

---

**Task Status**: Not Started
**Last Updated**: 2024-02-27
