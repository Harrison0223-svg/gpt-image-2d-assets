# Inspection and assembly tools

Requires Python 3 and Pillow. Prefer an existing runtime. The tools do not use the network or a generator. `--out` must be new or empty; use a new version directory for each run.

## Alpha measurements and background previews

```sh
python "<skill-dir>/scripts/asset_tools.py" inspect "<asset.png>" --out "<new-review-dir>"
```

Writes `measurements.json` and `backgrounds.png`, retaining original mode, alpha distribution, threshold bounds and SHA256. Converting RGB for measurement does not create meaningful transparency. Exit code 0 means inspection completed; `content_state=fully_opaque/empty` may identify a rejected result. Open the actual preview.

Previews scale uniformly to a maximum side of 900 pixels. Use `--max-side` or inspect original-resolution crops for detailed edges. A thumbnail is not evidence that every edge is clean.

## Explicit crops and timing

Create project-local JSON. Relative `source` paths resolve from the JSON directory; absolute paths also work. Replace example coordinates and durations with measured values:

```json
{
  "canvas": [520, 444],
  "repeat": false,
  "preview_background": "#303840",
  "frames": [
    {"source": "sheet.png", "crop": [0, 0, 444, 444], "offset": [40, 0], "duration_ms": 120},
    {"source": "sheet.png", "crop": [444, 0, 887, 444], "offset": [40, 0], "duration_ms": 80}
  ]
}
```

```sh
python "<skill-dir>/scripts/asset_tools.py" assemble "<sequence.json>" --out "<new-frames-dir>"
```

- `crop`: `[left, top, right, bottom]`, excluding right/bottom. Omit for the full source.
- `offset`: cropped image's top-left position on the shared canvas; defaults to `[0,0]`. No automatic character alignment.
- `duration_ms`: required, positive and divisible by 10 for GIF. Do not silently round timing.
- `repeat`: defaults to false for one playback; true loops indefinitely. Repetition does not prove a clean seam.
- Optional `anchor` and `events` are retained verbatim; the project defines their meaning.

Writes full RGBA PNG frames, a GIF on the specified background and `assembly.json`. Validates crops, placements and timing before output. Out-of-bounds crops and insufficient canvases fail instead of clipping. No grid inference, alpha cleanup, character rescaling or generated in-between frames.

RGBA crops retain source pixels; transparent padding is technical assembly. GIF is a preview and may merge identical frames. The report preserves decoded frame count and total duration; PNGs retain every input frame.

When changing the script, run:

```sh
python "<skill-dir>/scripts/test_asset_tools.py"
```

Tests cover alpha classification, exact crops/padding, GIF duration, bounds rejection and non-overwrite behavior. They do not replace art review.
