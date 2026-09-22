"""Build a self-contained, bounded motion review page from assembled PNG frames.

This tool only reads the outputs produced by asset_tools.py. It does not crop,
rescale, clean alpha, interpolate, or make a visual quality decision.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageColor


TOOL_VERSION = "1.0"
DECLARATION = (
    "Frames and timing are shown as supplied. This page performs no art edit, "
    "interpolation, automatic crop, alignment, or visual acceptance."
)
LOOP_NOTE = (
    "Loop end-to-start difference is a pixel-difference hint, not a quality "
    "score. Different poses may differ substantially and do not automatically fail."
)


class ReviewError(ValueError):
    """An input or output contract violation."""


def _int_pair(value: Any, name: str) -> list[int]:
    if (
        not isinstance(value, list)
        or len(value) != 2
        or any(type(item) is not int for item in value)
        or any(item <= 0 for item in value)
    ):
        raise ReviewError(f"{name} must contain two positive integers")
    return [int(value[0]), int(value[1])]


def _resolve_assembly(path_value: Any, comparison_path: Path) -> tuple[Path, Path]:
    if not isinstance(path_value, str) or not path_value.strip():
        raise ReviewError("each sequence requires an assembly directory path")
    requested = Path(path_value)
    directory = requested if requested.is_absolute() else comparison_path.parent / requested
    directory = directory.resolve()
    if directory.is_file() and directory.name.lower() == "assembly.json":
        assembly_file = directory
        directory = directory.parent
    else:
        assembly_file = directory / "assembly.json"
    if not assembly_file.is_file():
        raise ReviewError(f"assembly.json not found for sequence: {path_value}")
    return directory, assembly_file


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ReviewError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ReviewError(f"JSON object required: {path}")
    return value


def _safe_text(value: Any, name: str, default: str = "") -> str:
    if value is None:
        return default
    if not isinstance(value, str):
        raise ReviewError(f"{name} must be plain text")
    return value


def _png_data(path: Path, expected_size: tuple[int, int]) -> tuple[str, bytes, str]:
    try:
        raw = path.read_bytes()
        with Image.open(path) as image:
            image.load()
            rgba = image.convert("RGBA")
            if rgba.size != expected_size:
                raise ReviewError(
                    f"frame {path.name} has size {list(rgba.size)}; expected {list(expected_size)}"
                )
            pixels = rgba.tobytes()
    except ReviewError:
        raise
    except (OSError, SyntaxError, ValueError) as exc:
        raise ReviewError(f"invalid PNG frame {path}: {exc}") from exc
    encoded = base64.b64encode(raw).decode("ascii")
    return f"data:image/png;base64,{encoded}", pixels, hashlib.sha256(raw).hexdigest()


def _pixel_difference(first: bytes, last: bytes, size: tuple[int, int]) -> dict[str, Any]:
    different_pixels = sum(
        1
        for index in range(0, len(first), 4)
        if first[index : index + 4] != last[index : index + 4]
    )
    width, _height = size
    changed_xy = [
        ((index // 4) % width, (index // 4) // width)
        for index in range(0, len(first), 4)
        if first[index : index + 4] != last[index : index + 4]
    ]
    bbox = (
        [
            min(x for x, _y in changed_xy),
            min(y for _x, y in changed_xy),
            max(x for x, _y in changed_xy) + 1,
            max(y for _x, y in changed_xy) + 1,
        ]
        if changed_xy
        else None
    )
    return {
        "pixel_bytes_differ": different_pixels > 0,
        "different_pixel_count": different_pixels,
        "difference_bbox": list(bbox) if bbox else None,
        "note": LOOP_NOTE,
    }


def _duplicate_pairs(frames: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    pixel_pairs: list[dict[str, Any]] = []
    file_pairs: list[dict[str, Any]] = []
    for left in range(len(frames)):
        for right in range(left + 1, len(frames)):
            if frames[left]["pixels"] == frames[right]["pixels"]:
                pixel_pairs.append({"first": left, "second": right})
            if frames[left]["sha256"] == frames[right]["sha256"]:
                file_pairs.append({"first": left, "second": right})
    return pixel_pairs, file_pairs


def _background_config(spec: dict[str, Any]) -> dict[str, str]:
    selected = spec.get("background", spec.get("preview_background", "neutral"))
    if not isinstance(selected, str):
        raise ReviewError("background must be black, white, neutral, or an opaque color")
    selected = selected.strip().lower()
    named = {"black": "#000000", "white": "#ffffff", "neutral": "#303840"}
    if selected in named:
        selected_color = named[selected]
    else:
        try:
            rgb = ImageColor.getrgb(selected)
        except ValueError as exc:
            raise ReviewError("background must be black, white, neutral, or an opaque color") from exc
        if len(rgb) != 3:
            raise ReviewError("background must be an opaque color")
        selected_color = "#%02x%02x%02x" % rgb
    return {"selected": selected, "selected_color": selected_color}


def _validate_output_path(output: Path) -> Path:
    output = output.resolve()
    if output.exists():
        if not output.is_dir() or any(output.iterdir()):
            raise ReviewError("output must be a new or empty directory; refusing to overwrite")
    return output


def _validate_sequence(entry: Any, index: int, comparison_path: Path) -> dict[str, Any]:
    if not isinstance(entry, dict):
        raise ReviewError(f"sequence {index} must be an object")
    assembly_value = entry.get(
        "assembly",
        entry.get("assembly_dir", entry.get("directory", entry.get("path"))),
    )
    directory, assembly_path = _resolve_assembly(assembly_value, comparison_path)
    assembly = _read_json(assembly_path)
    canvas = _int_pair(assembly.get("canvas"), f"{assembly_path}: canvas")
    raw_frames = assembly.get("frames")
    if not isinstance(raw_frames, list) or not raw_frames:
        raise ReviewError(f"{assembly_path}: frames must be a nonempty list")
    repeat = assembly.get("repeat_for_preview", assembly.get("repeat", False))
    if type(repeat) is not bool:
        raise ReviewError(f"{assembly_path}: repeat_for_preview must be boolean")

    frame_items: list[dict[str, Any]] = []
    for frame_index, metadata in enumerate(raw_frames):
        if not isinstance(metadata, dict):
            raise ReviewError(f"{assembly_path}: frame metadata {frame_index} must be an object")
        duration = metadata.get("duration_ms")
        if type(duration) is not int or duration < 10 or duration % 10:
            raise ReviewError(f"{assembly_path}: frame {frame_index} has illegal duration_ms")
        frame_path = directory / f"frame_{frame_index:03}.png"
        if not frame_path.is_file():
            raise ReviewError(f"missing frame: {frame_path}")
        data_url, pixels, sha256 = _png_data(frame_path, tuple(canvas))
        frame_items.append(
            {
                "index": frame_index,
                "duration_ms": duration,
                "data_url": data_url,
                "pixels": pixels,
                "sha256": sha256,
            }
        )
    pixel_pairs, file_pairs = _duplicate_pairs(frame_items)
    total_duration = sum(frame["duration_ms"] for frame in frame_items)
    difference = _pixel_difference(
        frame_items[0]["pixels"], frame_items[-1]["pixels"], tuple(canvas)
    )
    sequence_id = _safe_text(entry.get("id", entry.get("name")), f"sequence {index} id", f"sequence-{index + 1}")
    if not sequence_id.strip():
        raise ReviewError(f"sequence {index} id must not be empty")
    title = _safe_text(entry.get("title", entry.get("name")), f"sequence {index} title", sequence_id)
    source_label = _safe_text(
        entry.get("source_label", entry.get("source", "")),
        f"sequence {index} source_label",
        str(assembly_value),
    )
    review = _safe_text(entry.get("review"), f"sequence {index} review")
    notes = _safe_text(entry.get("notes"), f"sequence {index} notes")
    return {
        "id": sequence_id,
        "title": title,
        "source_label": source_label,
        "review": review,
        "notes": notes,
        "canvas": canvas,
        "repeat_for_preview": repeat,
        "playback_semantics": "loop" if repeat else "one-shot",
        "assembly_path": str(assembly_path),
        "frames": [
            {"index": f["index"], "duration_ms": f["duration_ms"], "data_url": f["data_url"]}
            for f in frame_items
        ],
        "diagnostics": {
            "frame_count": len(frame_items),
            "duration_ms": [frame["duration_ms"] for frame in frame_items],
            "timing": {
                "durations_ms": [frame["duration_ms"] for frame in frame_items],
                "total_duration_ms": total_duration,
            },
            "total_duration_ms": total_duration,
            "canvas": canvas,
            "frame_dimensions": [canvas for _ in frame_items],
            "dimensions_consistent": True,
            "identical_pixel_frame_pairs": pixel_pairs,
            "identical_png_file_pairs": file_pairs,
            "identical_frame_pairs": pixel_pairs,
            "loop_end_to_start_difference": difference,
            "note": "Diagnostics are mechanical observations only; visual acceptance remains not_assessed.",
        },
    }


def _json_for_script(value: Any) -> str:
    return (
        json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )


def _build_html(payload: dict[str, Any]) -> str:
    script_data = _json_for_script(payload)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Motion review</title>
<style>
:root {{ color-scheme: light dark; font-family: system-ui, sans-serif; }}
body {{ margin: 0; padding: 1rem; background: #191b1f; color: #f4f5f6; }}
h1 {{ margin: 0 0 .25rem; font-size: 1.25rem; }}
.notice {{ color: #cbd0d7; font-size: .9rem; max-width: 68rem; }}
.toolbar {{ position: sticky; top: 0; z-index: 2; margin: 1rem 0; padding: .75rem; background: #25292f; border: 1px solid #41464f; border-radius: .5rem; }}
button, select {{ font: inherit; margin: .15rem; padding: .35rem .6rem; border-radius: .3rem; border: 1px solid #68717d; background: #303740; color: inherit; }}
button[aria-pressed="true"] {{ outline: 2px solid #9ecbff; }}
input[type="range"] {{ width: min(50rem, 70vw); vertical-align: middle; }}
.backgrounds {{ display: inline-flex; gap: .2rem; margin-left: .5rem; }}
.backgrounds button {{ min-width: 4.5rem; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(20rem, 1fr)); gap: 1rem; align-items: start; }}
.card {{ background: #24282e; border: 1px solid #454b54; border-radius: .55rem; padding: .75rem; min-width: 0; }}
.stage {{ display: grid; place-items: center; width: max-content; max-width: 100%; min-height: 0; background: #303840; overflow: auto; }}
.stage img {{ display: block; max-width: 100%; image-rendering: auto; }}
.meta {{ font-size: .86rem; color: #d3d8de; overflow-wrap: anywhere; }}
.review {{ margin-top: .5rem; padding: .5rem; background: #1b1e23; border-left: 3px solid #d6a85d; white-space: pre-wrap; overflow-wrap: anywhere; }}
.notes {{ margin-top: .5rem; padding: .5rem; background: #1b1e23; border-left: 3px solid #718096; white-space: pre-wrap; overflow-wrap: anywhere; }}
.muted {{ color: #aeb6c0; }}
</style>
</head>
<body>
<h1 id="page-title">Motion review</h1>
<p class="notice" id="declaration"></p>
<section class="toolbar" aria-label="Playback controls">
  <div>
    <button id="play" type="button">Start</button>
    <button id="restart-all" type="button">Restart all</button>
    <button id="prev" type="button">◀ Frame</button>
    <button id="next" type="button">Frame ▶</button>
    <span>Speed:</span>
    <button class="speed" data-speed="0.25" type="button">0.25×</button>
    <button class="speed" data-speed="0.5" type="button">0.5×</button>
    <button class="speed" data-speed="1" type="button" aria-pressed="true">1×</button>
    <span class="backgrounds" aria-label="Background">
      <span>Background:</span>
      <button class="background" data-background="#000000" type="button">Black</button>
      <button class="background" data-background="#ffffff" type="button">White</button>
      <button class="background" data-background="#303840" type="button" aria-pressed="true">Neutral</button>
    </span>
    <label for="display-scale">Display:</label>
    <select id="display-scale">
      <option value="128">128 px high</option>
      <option value="256" selected>256 px high</option>
      <option value="native">Original canvas pixels</option>
    </select>
  </div>
  <div>
    <label for="timeline">Timeline</label>
    <input id="timeline" type="range" min="0" max="1" step="1" value="0">
    <span id="time-readout">0 / 0 ms</span>
    <span class="muted">Each card follows its supplied loop or one-shot setting. After frame stepping, Start restarts all sequences from the beginning. Display sizing only; source PNG bytes are unchanged.</span>
  </div>
</section>
<main id="grid" class="grid"></main>
<script>
const DATA = {script_data};
const state = {{ time: 0, speed: 1, playing: false, stepMode: false, stepIndices: {{}}, background: DATA.background.selected_color, displayScale: '256' }};
const maxDuration = Math.max(...DATA.sequences.map(s => s.diagnostics.total_duration_ms));
const hasLoop = DATA.sequences.some(s => s.repeat_for_preview);
const timeline = document.getElementById('timeline');
timeline.max = String(maxDuration);
timeline.value = '0';
document.getElementById('page-title').textContent = DATA.title || 'Motion review';
document.getElementById('declaration').textContent = DATA.declaration;
const grid = document.getElementById('grid');
function frameAtTime(sequence, milliseconds) {{
  const total = sequence.diagnostics.total_duration_ms;
  let t = sequence.repeat_for_preview ? (milliseconds % total) : Math.min(milliseconds, total - 1);
  let elapsed = 0;
  for (let i = 0; i < sequence.frames.length; i++) {{
    elapsed += sequence.frames[i].duration_ms;
    if (t < elapsed) return i;
  }}
  return sequence.frames.length - 1;
}}
function frameAtStep(sequence, step) {{
  return sequence.repeat_for_preview ? ((step % sequence.frames.length) + sequence.frames.length) % sequence.frames.length : Math.min(Math.max(step, 0), sequence.frames.length - 1);
}}
function frameElapsed(sequence, index) {{
  return sequence.frames.slice(0, index).reduce((sum, f) => sum + f.duration_ms, 0);
}}
function frameIndex(sequence) {{
  return state.stepMode ? frameAtStep(sequence, state.stepIndices[sequence.id]) : frameAtTime(sequence, state.time);
}}
function makeCard(sequence) {{
  const card = document.createElement('article'); card.className = 'card'; card.dataset.sequence = sequence.id;
  const heading = document.createElement('h2'); heading.style.fontSize = '1rem'; card.appendChild(heading);
  const stage = document.createElement('div'); stage.className = 'stage'; stage.style.aspectRatio = String(sequence.canvas[0]) + ' / ' + String(sequence.canvas[1]);
  const image = document.createElement('img'); image.alt = sequence.title + ' frame'; stage.appendChild(image); card.appendChild(stage);
  const meta = document.createElement('div'); meta.className = 'meta'; card.appendChild(meta);
  const review = document.createElement('div'); review.className = 'review'; card.appendChild(review);
  const notes = document.createElement('div'); notes.className = 'notes'; card.appendChild(notes);
  card._parts = {{ heading, stage, image, meta, review, notes }};
  grid.appendChild(card);
}}
for (const sequence of DATA.sequences) makeCard(sequence);
function render() {{
  for (const sequence of DATA.sequences) {{
    const card = grid.querySelector('[data-sequence="' + CSS.escape(sequence.id) + '"]');
    const index = frameIndex(sequence); const frame = sequence.frames[index];
    card._parts.heading.textContent = sequence.title;
    card._parts.image.src = frame.data_url;
    card._parts.stage.style.background = state.background;
    const displayHeight = state.displayScale === 'native' ? sequence.canvas[1] : Number(state.displayScale);
    const displayWidth = state.displayScale === 'native' ? sequence.canvas[0] : Math.round(sequence.canvas[0] * displayHeight / sequence.canvas[1]);
    card._parts.image.style.width = displayWidth + 'px';
    card._parts.image.style.height = displayHeight + 'px';
    card._parts.meta.textContent = sequence.source_label + ' · ' + sequence.playback_semantics + ' · frame ' + (index + 1) + '/' + sequence.frames.length + ' · ' + frame.duration_ms + ' ms (starts ' + frameElapsed(sequence, index) + ' ms)';
    card._parts.review.textContent = 'Review: ' + (sequence.review || 'not assessed. Mechanical diagnostics do not constitute visual acceptance.');
    card._parts.notes.textContent = 'Notes: ' + (sequence.notes || 'none supplied.');
  }}
  const cycleProgress = Math.round(state.time % maxDuration);
  document.getElementById('time-readout').textContent = hasLoop
    ? String(Math.round(state.time)) + ' ms · cycle ' + (Math.floor(state.time / maxDuration) + 1) + ' (' + cycleProgress + ' / ' + maxDuration + ' ms)'
    : String(Math.min(Math.round(state.time), maxDuration)) + ' / ' + maxDuration + ' ms';
  const currentCycleTime = hasLoop ? (state.time % maxDuration) : Math.min(maxDuration, Math.max(0, state.time));
  timeline.value = String(Math.round(currentCycleTime));
  document.getElementById('play').textContent = state.playing ? 'Pause' : (!hasLoop && state.time >= maxDuration ? 'Restart' : 'Start');
}}
function enterStepMode() {{
  if (state.stepMode) return;
  state.stepIndices = {{}};
  for (const sequence of DATA.sequences) state.stepIndices[sequence.id] = frameAtTime(sequence, state.time);
  state.stepMode = true;
}}
function stepFrame(delta) {{
  enterStepMode();
  for (const sequence of DATA.sequences) {{
    const current = state.stepIndices[sequence.id];
    state.stepIndices[sequence.id] = frameAtStep(sequence, current + delta);
  }}
  state.playing = false; render();
}}
function restartAll() {{
  state.time = 0; state.stepIndices = {{}}; state.stepMode = false; state.playing = true; render();
}}
document.getElementById('play').addEventListener('click', () => {{
  if (state.stepMode) {{ restartAll(); return; }}
  if (!hasLoop && state.time >= maxDuration) restartAll();
  else {{
    state.playing = !state.playing;
  }}
  render();
}});
document.getElementById('restart-all').addEventListener('click', restartAll);
document.getElementById('prev').addEventListener('click', () => stepFrame(-1));
document.getElementById('next').addEventListener('click', () => stepFrame(1));
timeline.addEventListener('input', event => {{ state.stepMode = false; state.stepIndices = {{}}; state.time = Number(event.target.value); render(); }});
document.querySelectorAll('.speed').forEach(button => button.addEventListener('click', () => {{
  state.speed = Number(button.dataset.speed); document.querySelectorAll('.speed').forEach(b => b.setAttribute('aria-pressed', String(b === button))); render();
}}));
document.querySelectorAll('.background').forEach(button => button.addEventListener('click', () => {{
  state.background = button.dataset.background; document.querySelectorAll('.background').forEach(b => b.setAttribute('aria-pressed', String(b === button))); render();
}}));
document.getElementById('display-scale').addEventListener('change', event => {{ state.displayScale = event.target.value; render(); }});
let previous = performance.now();
function tick(now) {{ const delta = now - previous; previous = now; if (state.playing) {{ state.time += delta * state.speed; if (state.time > maxDuration && !DATA.sequences.some(s => s.repeat_for_preview)) {{ state.time = maxDuration; state.playing = false; }} render(); }} requestAnimationFrame(tick); }}
render(); requestAnimationFrame(tick);
</script>
</body>
</html>
'''


def build(comparison: str | Path, output: str | Path) -> dict[str, Any]:
    comparison_path = Path(comparison).resolve()
    if not comparison_path.is_file():
        raise ReviewError(f"comparison JSON not found: {comparison_path}")
    spec = _read_json(comparison_path)
    sequences = spec.get("sequences")
    if not isinstance(sequences, list) or not sequences:
        raise ReviewError("comparison JSON requires a nonempty sequences list")
    output_path = _validate_output_path(Path(output))
    background = _background_config(spec)
    validated = [_validate_sequence(entry, index, comparison_path) for index, entry in enumerate(sequences)]
    ids = [sequence["id"] for sequence in validated]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        raise ReviewError("sequence ids must be unique: " + ", ".join(duplicates))
    payload = {
        "title": _safe_text(spec.get("title"), "title", "Motion review"),
        "declaration": DECLARATION,
        "background": background,
        "sequences": validated,
        "visual_acceptance": "not_assessed",
    }
    diagnostics = {
        "tool": "motion_review",
        "tool_version": TOOL_VERSION,
        "comparison": str(comparison_path),
        "sequences": [
            {
                "id": sequence["id"],
                "title": sequence["title"],
                "source_label": sequence["source_label"],
                "assembly_path": sequence["assembly_path"],
                **sequence["diagnostics"],
                "review": sequence["review"],
                "notes": sequence["notes"],
                "playback_semantics": sequence["playback_semantics"],
            }
            for sequence in validated
        ],
        "visual_acceptance": "not_assessed",
        "scope": "Exact RGBA duplicate observations, supplied durations, frame dimensions, and loop edge pixel difference only.",
        "loop_difference_note": LOOP_NOTE,
    }

    # All input validation and image reads happen above. Only now create and write
    # the output directory, preserving the no-overwrite contract.
    output_path.mkdir(parents=True, exist_ok=True)
    (output_path / "index.html").write_text(_build_html(payload), encoding="utf-8")
    (output_path / "diagnostics.json").write_text(
        json.dumps(diagnostics, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return diagnostics


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    build_parser = commands.add_parser("build", help="build an offline motion review page")
    build_parser.add_argument("comparison", type=Path)
    build_parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    try:
        result = build(args.comparison, args.out)
    except (ReviewError, OSError, TypeError, KeyError) as exc:
        parser.exit(2, f"ERROR: {exc}\n")
    print(json.dumps({"output": str(args.out.resolve()), "visual_acceptance": result["visual_acceptance"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
