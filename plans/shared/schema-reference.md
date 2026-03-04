# ColorPreset Schema Reference

Complete reference for the ColorPreset JSON schema used throughout the project.

## Overview

The ColorPreset schema defines a complete color adjustment preset with comprehensive metadata, image analysis, and multiple export profiles. This schema is based on `example-schema.json` and serves as the contract between the backend API and frontend applications.

## Schema Structure

```typescript
interface ColorPreset {
  schema_version: string;
  preset_id: string;
  preset_name: string;
  created_at: string;
  source: SourceInfo;
  user_preferences: UserPreferences;
  image_analysis: ImageAnalysis;
  adjustments: Adjustments;
  export_profiles: ExportProfiles;
}

interface SourceInfo {
  generated_by: 'user' | 'ai' | 'hybrid';
  model: string;
  app_version: string;
}

interface UserPreferences {
  style: 'professional' | 'cinematic' | 'soft' | 'dramatic';
  intensity: number;           // 0.0 to 1.0
  skin_tone_priority: boolean;
  background_separation: number; // 0.0 to 1.0
  color_temperature_bias: 'neutral' | 'warm' | 'cool';
}

interface ImageAnalysis {
  enabled: boolean;
  exposure_score: number;      // 0.0 to 1.0
  contrast_score: number;      // 0.0 to 1.0
  dominant_colors: Array<{hex: string; percentage: number}>;
  face_detected: boolean;
  dynamic_range_score: number; // 0.0 to 1.0
}

interface Adjustments {
  global: GlobalAdjustments;
  tone_curve: ToneCurve;
  color: ColorAdjustments;
  hsl: HSLAdjustments;
  detail: DetailAdjustments;
  effects: Effects;
}

interface GlobalAdjustments {
  exposure: number;    // -1.0 to 1.0
  contrast: number;    // -1.0 to 1.0
  highlights: number;  // -1.0 to 1.0
  shadows: number;     // -1.0 to 1.0
  whites: number;      // -1.0 to 1.0
  blacks: number;      // -1.0 to 1.0
}

interface ToneCurve {
  highlights: number; // -1.0 to 1.0
  lights: number;     // -1.0 to 1.0
  darks: number;      // -1.0 to 1.0
  shadows: number;    // -1.0 to 1.0
}

interface ColorAdjustments {
  temperature_shift: number; // -1.0 to 1.0
  tint_shift: number;        // -1.0 to 1.0
  vibrance: number;          // -1.0 to 1.0
  saturation: number;        // -1.0 to 1.0
}

interface HSLAdjustments {
  hue: Record<Color, number>;        // -1.0 to 1.0
  saturation: Record<Color, number>; // -1.0 to 1.0
  luminance: Record<Color, number>;  // -1.0 to 1.0
}

type Color = 'red' | 'orange' | 'yellow' | 'green' | 'cyan' | 'blue' | 'purple' | 'magenta';

interface DetailAdjustments {
  sharpening: number;                // 0.0 to 1.0
  sharpen_radius: number;            // 0.0 to 1.0
  sharpen_detail: number;             // 0.0 to 1.0
  sharpen_masking: number;            // 0.0 to 1.0
  noise_reduction_luminance: number; // 0.0 to 1.0
  noise_reduction_color: number;     // 0.0 to 1.0
}

interface Effects {
  vignette: number; // -1.0 to 1.0
  grain: number;    // -1.0 to 1.0
}

interface ExportProfiles {
  lightroom: {
    value_scale: 'lightroom_native';
    conversion_required: true;
    [key: string]: any;
  };
  generic_normalized: {
    value_range: [-1, 1];
    conversion_required: false;
    [key: string]: any;
  };
}
```

## Value Normalization

All adjustment values use normalized ranges (-1.0 to 1.0) for consistency:

| Parameter | Range | Description |
|-----------|-------|-------------|
| Global adjustments | -1.0 to 1.0 | Full range of adjustment |
| Tone curve | -1.0 to 1.0 | Curve control points |
| Color adjustments | -1.0 to 1.0 | White balance and presence |
| HSL values | -1.0 to 1.0 | Per-color adjustments |
| Detail adjustments | 0.0 to 1.0 | Positive-only values |
| Effects | -1.0 to 1.0 | Full range of effect |

## Export Profiles

### Lightroom Native Scale

Lightroom uses its own value scales:
- Tone adjustments: -100 to +100
- Temperature: 2000 to 50000K
- Tint: -100 to +100
- HSL: -100 to +100
- Sharpening: 0 to 100

**Conversion Formula**:
```python
# Normalized to Lightroom
lightroom_value = normalized_value * 100

# Example: exposure 0.3 → Lightroom +30
```

### Generic Normalized

Keeps values in the -1.0 to 1.0 range. No conversion needed.

## Pydantic Implementation

```python
from pydantic import BaseModel, Field
from typing import Literal, Dict

class SourceInfo(BaseModel):
    generated_by: Literal['user', 'ai', 'hybrid']
    model: str
    app_version: str

class UserPreferences(BaseModel):
    style: Literal['professional', 'cinematic', 'soft', 'dramatic']
    intensity: float = Field(ge=0.0, le=1.0)
    skin_tone_priority: bool
    background_separation: float = Field(ge=0.0, le=1.0)
    color_temperature_bias: Literal['neutral', 'warm', 'cool']

class DominantColor(BaseModel):
    hex: str = Field(pattern=r'^#[0-9A-Fa-f]{6}$')
    percentage: float = Field(ge=0.0, le=100.0)

class ImageAnalysis(BaseModel):
    enabled: bool
    exposure_score: float = Field(ge=0.0, le=1.0)
    contrast_score: float = Field(ge=0.0, le=1.0)
    dominant_colors: list[DominantColor]
    face_detected: bool
    dynamic_range_score: float = Field(ge=0.0, le=1.0)

class GlobalAdjustments(BaseModel):
    exposure: float = Field(ge=-1.0, le=1.0)
    contrast: float = Field(ge=-1.0, le=1.0)
    highlights: float = Field(ge=-1.0, le=1.0)
    shadows: float = Field(ge=-1.0, le=1.0)
    whites: float = Field(ge=-1.0, le=1.0)
    blacks: float = Field(ge=-1.0, le=1.0)

class ToneCurve(BaseModel):
    highlights: float = Field(ge=-1.0, le=1.0)
    lights: float = Field(ge=-1.0, le=1.0)
    darks: float = Field(ge=-1.0, le=1.0)
    shadows: float = Field(ge=-1.0, le=1.0)

class ColorAdjustments(BaseModel):
    temperature_shift: float = Field(ge=-1.0, le=1.0)
    tint_shift: float = Field(ge=-1.0, le=1.0)
    vibrance: float = Field(ge=-1.0, le=1.0)
    saturation: float = Field(ge=-1.0, le=1.0)

class HSLAdjustments(BaseModel):
    hue: Dict[Literal['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'magenta'], float]
    saturation: Dict[Literal['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'magenta'], float]
    luminance: Dict[Literal['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'magenta'], float]

class DetailAdjustments(BaseModel):
    sharpening: float = Field(ge=0.0, le=1.0)
    sharpen_radius: float = Field(ge=0.0, le=1.0)
    sharpen_detail: float = Field(ge=0.0, le=1.0)
    sharpen_masking: float = Field(ge=0.0, le=1.0)
    noise_reduction_luminance: float = Field(ge=0.0, le=1.0)
    noise_reduction_color: float = Field(ge=0.0, le=1.0)

class Effects(BaseModel):
    vignette: float = Field(ge=-1.0, le=1.0)
    grain: float = Field(ge=-1.0, le=1.0)

class Adjustments(BaseModel):
    global: GlobalAdjustments
    tone_curve: ToneCurve
    color: ColorAdjustments
    hsl: HSLAdjustments
    detail: DetailAdjustments
    effects: Effects

class LightroomProfile(BaseModel):
    value_scale: Literal['lightroom_native']
    conversion_required: bool
    global: GlobalAdjustments
    tone_curve: ToneCurve
    color: ColorAdjustments
    hsl: HSLAdjustments
    detail: DetailAdjustments
    effects: Effects

class GenericNormalizedProfile(BaseModel):
    value_range: list[float] = Field(default=[-1.0, 1.0])
    conversion_required: bool
    adjustments: Adjustments

class ExportProfiles(BaseModel):
    lightroom: LightroomProfile
    generic_normalized: GenericNormalizedProfile

class ColorPreset(BaseModel):
    schema_version: str = '1.0.0'
    preset_id: str
    preset_name: str
    created_at: str
    source: SourceInfo
    user_preferences: UserPreferences
    image_analysis: ImageAnalysis
    adjustments: Adjustments
    export_profiles: ExportProfiles
```

## Validation Rules

### Required Fields
All top-level fields are required.

### String Formats
- `preset_id`: UUID v4 format
- `created_at`: ISO 8601 timestamp
- `hex`: Valid 6-digit hex color code (#RRGGBB)

### Numeric Constraints
- All adjustment values must be within their specified ranges
- Scores must be between 0.0 and 1.0
- Percentages must sum to approximately 100.0 (with some tolerance)

### Enum Values
- `generated_by`: user, ai, hybrid
- `style`: professional, cinematic, soft, dramatic
- `color_temperature_bias`: neutral, warm, cool

## Usage Examples

### Creating a New Preset

```python
from datetime import datetime
import uuid

preset = ColorPreset(
    preset_id=str(uuid.uuid4()),
    preset_name="Warm Sunset",
    created_at=datetime.utcnow().isoformat(),
    source=SourceInfo(
        generated_by="ai",
        model="gemini-1.5-pro-vision",
        app_version="1.0.0"
    ),
    user_preferences=UserPreferences(
        style="cinematic",
        intensity=0.7,
        skin_tone_priority=True,
        background_separation=0.6,
        color_temperature_bias="warm"
    ),
    # ... rest of the fields
)
```

### Validating Preset

```python
try:
    preset = ColorPreset(**preset_data)
    print("Preset is valid")
except ValidationError as e:
    print(f"Validation error: {e}")
```

## Common Patterns

### Default Values

When generating a preset, start with neutral defaults:

```python
default_global = GlobalAdjustments(
    exposure=0.0,
    contrast=0.0,
    highlights=0.0,
    shadows=0.0,
    whites=0.0,
    blacks=0.0
)
```

### HSL Color Arrays

All eight colors should be present:

```python
default_hsl = HSLAdjustments(
    hue={
        'red': 0.0, 'orange': 0.0, 'yellow': 0.0, 'green': 0.0,
        'cyan': 0.0, 'blue': 0.0, 'purple': 0.0, 'magenta': 0.0
    },
    saturation={
        'red': 0.0, 'orange': 0.0, 'yellow': 0.0, 'green': 0.0,
        'cyan': 0.0, 'blue': 0.0, 'purple': 0.0, 'magenta': 0.0
    },
    luminance={
        'red': 0.0, 'orange': 0.0, 'yellow': 0.0, 'green': 0.0,
        'cyan': 0.0, 'blue': 0.0, 'purple': 0.0, 'magenta': 0.0
    }
)
```

## Migration & Versioning

When updating the schema:

1. Increment `schema_version`
2. Document breaking changes
3. Provide migration scripts if needed
4. Update all validation logic

---

**Last Updated**: 2024-02-27
**Schema Version**: 1.0.0
**Maintainer**: Backend Team
