# Sprint 2 Walkthrough: Image Analysis Engine

**Sprint**: 2 — Image Analysis Engine
**Status**: Complete
**Tests**: 73 passing (94% coverage, 0.56s)

---

## What Was Built

Sprint 2 delivers a complete **image analysis engine** that extracts visual metadata from uploaded images. This service will feed into the Gemini AI prompt in Sprint 3, giving the AI the information it needs to generate intelligent Lightroom presets.

### New Files Created

```
api/app/
├── schemas/
│   ├── __init__.py              # Re-exports all schemas
│   └── image_analysis.py        # 7 Pydantic models for analysis output
│
└── services/
    ├── __init__.py              # Re-exports ImageAnalyzer
    └── image_analyzer/
        ├── __init__.py          # Package exports
        ├── analyzer.py          # Orchestrator class (main entry point)
        ├── histogram.py         # RGB + luminance histogram extraction
        ├── luminance.py         # BT.709 perceptual luminance calculation
        ├── brightness_contrast.py  # Brightness & contrast scoring
        ├── colors.py            # KMeans dominant color detection
        ├── exposure.py          # Exposure score, clipping, dynamic range
        └── exceptions.py        # Custom exception hierarchy

api/tests/
├── test_image_analyzer.py       # 39 tests for all analysis modules
└── test_schemas.py              # 18 tests for Pydantic schemas

plans/sprint-2/tasks/
├── t01-analyzer-service.md
├── t02-histogram-extraction.md
├── t03-luminance-calculation.md
├── t04-brightness-contrast.md
├── t05-dominant-colors.md
├── t06-exposure-detection.md
├── t07-error-handling.md
└── t08-performance-opt.md
```

---

## Architecture

### How It Works

```
Raw Image Bytes (JPEG/PNG/WebP)
        │
        ▼
┌───────────────────┐
│   ImageAnalyzer   │  ← Single entry point
│    .analyze()     │
└───────┬───────────┘
        │  decode → resize if > 1920px
        │
        ├──► histogram.py      → HistogramData (4×256 normalized bins)
        ├──► luminance.py      → LuminanceResult (mean/std/min/max)
        ├──► brightness_contrast.py → BrightnessContrastResult (0-1 scores)
        ├──► colors.py         → List[DominantColor] (hex + %)
        └──► exposure.py       → ExposureResult (score/clipping/DR)
                │
                ▼
        ImageAnalysis (Pydantic model)
```

### Usage

```python
from app.services.image_analyzer import ImageAnalyzer

analyzer = ImageAnalyzer()
result = analyzer.analyze(image_bytes)

# Access results
print(result.luminance.mean)           # 0.52
print(result.brightness_contrast.brightness)  # 0.52
print(result.brightness_contrast.contrast)    # 0.34
print(result.exposure.exposure_score)         # 0.51
print(result.exposure.dynamic_range)          # 0.78
print(result.dominant_colors[0].hex)          # "#3A5F8C"
print(result.dominant_colors[0].percentage)   # 42.5
print(result.image_width, result.image_height)  # 4000 3000
```

---

## Module Details

### 1. Schemas (`schemas/image_analysis.py`)

Seven Pydantic models with full validation:

| Model | Purpose | Key Fields |
|-------|---------|------------|
| `HistogramData` | 4 channel histograms | `red`, `green`, `blue`, `luminance` (256 bins each) |
| `DominantColor` | Single color entry | `hex` (#RRGGBB validated), `percentage` (0-100) |
| `LuminanceResult` | Luminance statistics | `mean`, `std`, `min`, `max` (all 0.0-1.0) |
| `BrightnessContrastResult` | Brightness/contrast scores | `brightness`, `contrast` (0.0-1.0) |
| `ExposureResult` | Exposure analysis | `exposure_score`, `highlight_clipping`, `shadow_clipping`, `dynamic_range` |
| `ImageAnalysis` | Top-level aggregate | All of the above + `image_width`, `image_height` |

### 2. Histogram Extraction (`histogram.py`)

- Uses `cv2.calcHist()` for per-channel RGB histograms (256 bins each)
- Computes luminance histogram from grayscale conversion
- All histograms normalized so values sum to 1.0
- Handles edge case of zero-pixel-count channels

### 3. Luminance Calculation (`luminance.py`)

- Implements **ITU-R BT.709** perceptual luminance:
  `L = 0.2126×R + 0.7152×G + 0.0722×B`
- Provides both:
  - `compute_luminance_map()` → 2D float32 array (shared by other modules)
  - `calculate_luminance()` → `LuminanceResult` with statistics

### 4. Brightness & Contrast (`brightness_contrast.py`)

- **Brightness** = mean luminance (directly 0-1)
- **Contrast** = standard deviation of luminance / 0.5, clamped to 1.0
  - Max std dev ≈ 0.5 occurs with a 50/50 black-white split
- Reuses `compute_luminance_map()` from the luminance module

### 5. Dominant Colors (`colors.py`)

- Downsamples image to ~100px for speed
- Uses **OpenCV KMeans** clustering (not sklearn — avoids extra dependency)
- Fast path: single-color images skip KMeans entirely
- Handles `k > unique_colors` gracefully
- Returns colors sorted by percentage descending

### 6. Exposure Detection (`exposure.py`)

| Metric | Calculation |
|--------|-------------|
| `exposure_score` | `mean(grayscale) / 255` — 0.0 = black, 0.5 = ideal, 1.0 = white |
| `highlight_clipping` | Fraction of pixels > 250 |
| `shadow_clipping` | Fraction of pixels < 5 |
| `dynamic_range` | `(P95 - P5) / 255` — percentile-based spread |

### 7. Error Handling (`exceptions.py`)

Three-level exception hierarchy:
```
ImageAnalysisError (base)
├── InvalidImageError    — bytes can't be decoded
└── AnalysisProcessingError — computation failure
```

### 8. Performance Optimizations

| Optimization | Impact |
|-------------|--------|
| Resize images > 1920px | Prevents OOM on 20MP+ photos |
| Downsample to ~100px for KMeans | Color detection < 50ms |
| NumPy vectorization throughout | No Python loops on pixel data |
| Float32 precision | Half memory of float64 |
| Shared luminance map | Computed once, reused by brightness/contrast |

---

## Test Coverage

```
73 tests, 94% coverage, runs in 0.56 seconds
```

| Test Class | Tests | What It Covers |
|-----------|-------|----------------|
| `TestHistogramExtraction` | 4 | Solid colors, normalization, bin lengths |
| `TestLuminanceCalculation` | 8 | Black/white/gray, pure RGB channels, BT.709 weights, luminance map shape |
| `TestBrightnessContrast` | 6 | Mid-gray, zero contrast, high contrast, boundary values, clamping |
| `TestDominantColors` | 6 | Single/multi colors, hex format, sorting, edge cases |
| `TestExposureDetection` | 6 | Black/white/gray, dynamic range, value bounds |
| `TestImageAnalyzer` | 9 | Integration: solid/gradient/single-pixel, JPEG, large images, invalid bytes |
| `TestDominantColor` (schema) | 5 | Hex validation, percentage bounds |
| `TestLuminanceResult` (schema) | 3 | Valid results, boundaries, out-of-range rejection |
| `TestBrightnessContrastResult` (schema) | 2 | Valid/invalid values |
| `TestExposureResult` (schema) | 2 | Valid/invalid values |
| `TestHistogramData` (schema) | 2 | Correct/wrong bin lengths |
| `TestImageAnalysis` (schema) | 4 | Full validation, empty colors, zero dimensions, JSON round-trip |

All tests use **synthetic images** (solid colors, gradients, half-splits) with mathematically known properties — no test fixtures or external files needed.

---

## How This Feeds Into Sprint 3

The `ImageAnalysis` result will be serialized and included in the Gemini AI prompt. For example:

```
The image has:
- Average luminance: 0.42 (slightly underexposed)
- Contrast: 0.28 (low contrast)
- Dominant colors: #3A5F8C (42%), #8B6E4A (28%), #C4A882 (15%)
- Dynamic range: 0.65 (good, but not full)
- Shadow clipping: 2.1% (minor)

Given the user wants a "warm cinematic" look, generate Lightroom adjustments...
```

This gives Gemini concrete data about the image instead of relying purely on vision analysis, leading to more accurate and targeted preset generation.

---

**Sprint Completed**: All 8 tasks done
**Last Updated**: 2025-03-09
