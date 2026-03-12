# Task: Dominant Color Detection

## Task Overview

**Task ID**: sprint-2-t05
**Task Name**: Dominant Color Detection
**Sprint**: 2
**Priority**: High
**Estimated Time**: 3 hours

---

## 1. Objective

Extract the top 5 dominant colors from an image using KMeans clustering, returning hex color codes and percentage coverage.

## 2. Why This Matters

**Business Value**:
- Dominant colors inform the AI about the image's palette, enabling more targeted HSL adjustments
- Maps to the `dominant_colors` array in the `ImageAnalysis` schema

**Technical Value**:
- KMeans is efficient and well-suited for color quantization
- Downsampling keeps processing time under 1 second

## 3. Dependencies

**Prerequisites**:
- [ ] t01-analyzer-service

## 4. Acceptance Criteria

**Definition of Done**:
- [ ] Top 5 dominant colors extracted
- [ ] Each color has hex value (#RRGGBB format)
- [ ] Each color has percentage (sum ≈ 100%)
- [ ] Colors sorted by percentage descending
- [ ] Performance < 1 second for typical photos

## 5. Technical Implementation

### Approach
- Resize image to max ~100x100 for performance
- Reshape to (N, 3) pixel array
- Apply KMeans clustering with K=5
- Count cluster membership for percentages
- Convert BGR cluster centers to hex

### Key Algorithm
```python
def detect_dominant_colors(image: np.ndarray, k: int = 5) -> list[DominantColor]:
    small = cv2.resize(image, (100, 100))
    pixels = small.reshape(-1, 3).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 3, cv2.KMEANS_PP_CENTERS)
    # Count labels for percentages, convert centers BGR→hex
```

### Why OpenCV KMeans over sklearn
- Already a dependency (no extra import)
- Faster for this specific use case (float32 pixel data)
- Avoids pulling in all of sklearn

## 6. Testing Strategy

- Solid red image → single dominant color ≈ #FF0000 at ~100%
- Two-color image (50/50 split) → two colors at ~50% each
- Verify hex format matches `^#[0-9A-Fa-f]{6}$`
- Verify percentages sum to ~100%

---

**Task Status**: Not Started
**Last Updated**: 2024-02-27
