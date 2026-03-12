# Task: Analyzer Service

## Task Overview

**Task ID**: sprint-2-t01
**Task Name**: Image Analyzer Service
**Sprint**: 2
**Priority**: High
**Estimated Time**: 2 hours

---

## 1. Objective

Create the main `ImageAnalyzer` class that orchestrates all image analysis operations (histogram, luminance, brightness/contrast, dominant colors, exposure) and returns a comprehensive `ImageAnalysis` result.

## 2. Why This Matters

**Business Value**:
- Single entry point for all image analysis — simplifies the API layer
- Provides the image metadata that feeds into the Gemini AI prompt for intelligent preset generation

**Technical Value**:
- Establishes the service architecture pattern for all future services
- Decouples analysis sub-modules so they can be developed/tested independently

**Risks of Not Doing**:
- Without orchestration, each analysis step would need to be called individually from routes
- Inconsistent error handling across analysis steps

## 3. Dependencies

**Prerequisites**:
- [x] Sprint 0 complete (project infrastructure)
- [x] OpenCV, NumPy, Pillow installed (in requirements.txt)

**Blocking**:
- [ ] t02-histogram-extraction
- [ ] t03-luminance-calculation
- [ ] t04-brightness-contrast
- [ ] t05-dominant-colors
- [ ] t06-exposure-detection

## 4. Acceptance Criteria

**Definition of Done**:
- [ ] `ImageAnalyzer` class created in `api/app/services/image_analyzer/analyzer.py`
- [ ] `analyze(image_bytes)` method returns `ImageAnalysis` schema
- [ ] Proper `__init__.py` exports
- [ ] Error handling for invalid images
- [ ] Unit tests written and passing

## 5. Technical Implementation

### Approach
- Create `ImageAnalyzer` class that accepts raw image bytes
- Convert bytes to NumPy array using OpenCV
- Optionally resize large images for performance
- Call each sub-module and aggregate results into `ImageAnalysis` Pydantic model

### Code Structure

```
api/app/services/image_analyzer/
├── __init__.py          # Exports ImageAnalyzer
├── analyzer.py          # Main orchestrator class
├── histogram.py         # Histogram extraction
├── luminance.py         # Luminance calculation
├── colors.py            # Dominant color detection
└── exposure.py          # Exposure analysis
```

## 6. Testing Strategy

- Test with synthetic images (solid color, gradient, etc.)
- Test error handling with invalid/corrupt bytes
- Test with various image sizes

---

**Task Status**: Not Started
**Last Updated**: 2024-02-27
