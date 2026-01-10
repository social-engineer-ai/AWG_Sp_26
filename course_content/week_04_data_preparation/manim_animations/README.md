# Week 4 Manim Animations

This folder contains all Manim animation source code for Week 4: Data Preparation & Transformation.

## Prerequisites

### Install Manim
```bash
pip install manim
```

For full installation including LaTeX support:
- **Windows:** Install MiKTeX or TeX Live
- **Mac:** `brew install --cask mactex`
- **Linux:** `sudo apt install texlive-full`

Full documentation: https://docs.manim.community/en/stable/installation.html

## Quick Start

### Render a single scene (low quality preview):
```bash
manim -pql video1_wide_to_long.py WideDataProblem
```

### Render in high quality:
```bash
manim -pqh video1_wide_to_long.py WideDataProblem
```

### Render all scenes in a file:
```bash
manim -pql video1_wide_to_long.py
```

## File Structure

```
manim_animations/
├── README.md                    # This file
├── video1_wide_to_long.py       # Wide-to-long transformation animations
├── video2_unit_discovery.py     # THE critical unit discovery lesson
├── video3_data_pipeline.py      # Data pipeline best practices
└── video4_merging_data.py       # Merging datasets animations
```

## Scenes by Video

### Video 1: Wide-to-Long Transformation (`video1_wide_to_long.py`)

| Scene | Duration | Description |
|-------|----------|-------------|
| `WideDataProblem` | ~30s | Shows 229 columns problem |
| `GranularityExplainer` | ~45s | Explains data granularity |
| `MeltConceptual` | ~30s | High-level melt concept |
| `MeltStepByStep` | ~60s | Detailed step-by-step transform |
| `MeltWithCode` | ~45s | Python code alongside visual |
| `ColumnPatternAnimation` | ~30s | Division × Quarter × PriceType pattern |

**Total: ~4 minutes**

### Video 2: The Unit Discovery (`video2_unit_discovery.py`) ⭐ MOST IMPORTANT

| Scene | Duration | Description |
|-------|----------|-------------|
| `TheMystery` | ~45s | Shows wrong initial results |
| `InvestigationBegins` | ~30s | Looking at specific product |
| `CaseVsUnitReveal` | ~60s | THE "aha" moment (key scene) |
| `NormalizationFix` | ~30s | Shows the fix |
| `BeforeAfterImpact` | ~45s | Dramatic before/after comparison |
| `AlwaysCheckUnits` | ~30s | Final takeaway |
| `HistogramMorph` | ~45s | Distribution shift animation |

**Total: ~5 minutes**

### Video 3: Data Pipeline Best Practices (`video3_data_pipeline.py`)

| Scene | Duration | Description |
|-------|----------|-------------|
| `NightmareVsDream` | ~45s | Messy vs clean code contrast |
| `PipelineFlowchart` | ~30s | Standard pipeline stages |
| `ConfigurationTop` | ~30s | Config at top of notebook |
| `IntermediateSaves` | ~30s | Checkpoint saving concept |
| `AWGPipeline` | ~45s | AWG-specific pipeline |

**Total: ~3 minutes**

### Video 4: Merging Datasets (`video4_merging_data.py`)

| Scene | Duration | Description |
|-------|----------|-------------|
| `WhyMerge` | ~30s | Motivation for merging |
| `MergeTypes` | ~45s | Inner/Left/Right/Outer joins |
| `KeyMatching` | ~60s | Visual of key matching |
| `AWGMergeStrategy` | ~45s | AWG-specific approach |
| `MergeIssues` | ~45s | Common problems & solutions |

**Total: ~3.5 minutes**

## Rendering Commands

### Render all Video 2 scenes (the most important):
```bash
manim -pqh video2_unit_discovery.py TheMystery
manim -pqh video2_unit_discovery.py InvestigationBegins
manim -pqh video2_unit_discovery.py CaseVsUnitReveal
manim -pqh video2_unit_discovery.py NormalizationFix
manim -pqh video2_unit_discovery.py BeforeAfterImpact
manim -pqh video2_unit_discovery.py AlwaysCheckUnits
manim -pqh video2_unit_discovery.py HistogramMorph
```

### Batch render all scenes (shell script):
```bash
#!/bin/bash
for file in video*.py; do
    manim -qh "$file"
done
```

### Output Location
Rendered videos are saved to:
```
media/videos/{filename}/{quality}/
```

For example:
```
media/videos/video2_unit_discovery/1080p60/CaseVsUnitReveal.mp4
```

## Quality Settings

| Flag | Resolution | FPS | Use Case |
|------|------------|-----|----------|
| `-ql` | 480p | 15 | Quick preview |
| `-qm` | 720p | 30 | Draft review |
| `-qh` | 1080p | 60 | Final production |
| `-qk` | 4K | 60 | High-end production |

## Customization

### Colors
Each file defines a `COLORS` dictionary at the top. Modify to match your brand:
```python
COLORS = {
    'bc': GREEN,       # Best Choice brand
    'nb': RED,         # National Brand
    'case': ORANGE,    # Case-level prices
    'unit': BLUE,      # Unit-level prices
    ...
}
```

### Timing
Adjust `self.wait(X)` calls to control pause duration between animations.

### Text Size
Modify `font_size` parameters in `Text()` calls.

## Combining Scenes into Final Videos

Use a video editor (DaVinci Resolve, Premiere, etc.) or ffmpeg:

```bash
# Concatenate Video 2 scenes
ffmpeg -f concat -i video2_list.txt -c copy video2_final.mp4
```

Where `video2_list.txt` contains:
```
file 'media/videos/video2_unit_discovery/1080p60/TheMystery.mp4'
file 'media/videos/video2_unit_discovery/1080p60/InvestigationBegins.mp4'
file 'media/videos/video2_unit_discovery/1080p60/CaseVsUnitReveal.mp4'
...
```

## Adding Voiceover

1. Render all scenes
2. Combine into single video
3. Record voiceover separately (Audacity, etc.)
4. Sync in video editor
5. Export final video

## Troubleshooting

### LaTeX errors
- Make sure TeX is installed
- Use `Text()` instead of `MathTex()` for non-math text

### Slow rendering
- Use `-ql` for previews
- Reduce scene complexity for testing

### Missing fonts
- Manim uses system fonts; install needed fonts

## Production Checklist

- [ ] Render all scenes in high quality
- [ ] Review each scene for timing
- [ ] Combine scenes per video
- [ ] Add voiceover
- [ ] Add intro/outro cards
- [ ] Export final videos
- [ ] Upload to course platform

---

Created for BADM 550 - AWG Pricing Analysis Project
University of Illinois, Spring 2026
