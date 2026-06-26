# Validation result — one-time acceptance test

Compared our HyperFrames render against the ground-truth reference produced by the
old Playwright+ffmpeg pipeline.

- **Ours:** `projects/podcast/renders/chapter-break-b.mov` (ProRes 4444, alpha)
- **Reference:** `Testing video/chapter-break-b-prores4444.mov` (verified ground truth)
- **Method:** `validation/validate_match.py` — composites both frames over an identical
  black background (so only *visible* pixels are compared) and measures per-frame diff,
  timing, corner transparency, and the cream strip's color.

## Result: **[PASS]**

| frame | % pixels within diff≤16 | max diff | opaque% ours | opaque% ref | timing |
|------:|------------------------:|---------:|-------------:|------------:|--------|
| 5     | 99.78% | 246 | 0.73% | 0.65% | OK |
| 30    | 99.30% | 246 | 2.50% | 2.21% | OK |
| 60    | 99.30% | 246 | 2.50% | 2.21% | OK |
| 90    | 99.67% | 246 | 1.12% | 0.99% | OK |

Point checks @ frame 60:
- top-right (1900,20) alpha = **0 / 0** (transparent in both)
- inside strip (100,1050): ours `(246,237,214,255)` vs ref `(245,237,214,255)` — alpha 255, cream RGB within 1.

The only differences (max 246) are sub-pixel **anti-aliased edges** — visually identical.

## Reproduce
```
python3 validation/validate_match.py "projects/podcast/renders/chapter-break-b.mov" "../Testing video/chapter-break-b-prores4444.mov"
```
(Re-render first with `tools\render.ps1 podcast chapter-break-b` if the .mov is missing.)
