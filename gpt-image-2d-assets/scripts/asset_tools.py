"""Measure PNG alpha and assemble existing frames. Requires Pillow; no generation/cleanup."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageColor


def measure(path):
    path = Path(path).resolve()
    with Image.open(path) as src:
        mode = src.mode
        has_alpha = 'A' in src.getbands() or 'transparency' in src.info
        im = src.convert('RGBA')
    alpha = im.getchannel('A')
    hist = alpha.histogram()
    n = im.width * im.height
    return {
        'path': str(path), 'source_mode': mode, 'has_alpha_metadata': has_alpha,
        'size': list(im.size), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'alpha_extrema': list(alpha.getextrema()), 'transparent_pixels': hist[0],
        'partial_pixels': sum(hist[1:255]), 'near_opaque_pixels': sum(hist[250:]),
        'opaque_pixels': hist[255], 'partial_fraction': sum(hist[1:255]) / n,
        'bbox_nonzero': alpha.getbbox(),
        'bbox_alpha16': alpha.point(lambda a: 255 if a >= 16 else 0).getbbox(),
        'bbox_alpha128': alpha.point(lambda a: 255 if a >= 128 else 0).getbbox(),
        'content_state': 'empty' if hist[0] == n else 'fully_opaque' if hist[255] == n else 'has_transparency',
        'visual_acceptance': 'not_assessed',
    }


def fresh_output(path):
    path = Path(path).resolve()
    if path.exists() and (not path.is_dir() or any(path.iterdir())):
        raise ValueError('Output must be a new or empty directory; choose a new version.')
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def inspect(source, output, max_side=900):
    if max_side <= 0:
        raise ValueError('max-side must be positive')
    data = measure(source)
    with Image.open(source) as src:
        im = src.convert('RGBA')
    im.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    colors = ['#101820', '#ffffff', '#807060']
    preview = Image.new('RGB', (im.width * 3, im.height))
    for i, color in enumerate(colors):
        bg = Image.new('RGBA', im.size, color)
        bg.alpha_composite(im)
        preview.paste(bg.convert('RGB'), (i * im.width, 0))
    out = fresh_output(output)
    preview.save(out / 'backgrounds.png')
    data['preview'] = {'backgrounds': colors, 'single_tile_size': list(im.size), 'source_unchanged': True}
    save_json(out / 'measurements.json', data)
    return data


def integer_list(value, length, name):
    if not isinstance(value, list) or len(value) != length or any(type(x) is not int for x in value):
        raise ValueError(f'{name} must contain {length} integers')
    return value


def assemble(manifest, output):
    manifest = Path(manifest).resolve()
    spec = json.loads(manifest.read_text(encoding='utf-8-sig'))
    canvas = integer_list(spec['canvas'], 2, 'canvas')
    if min(canvas) <= 0:
        raise ValueError('canvas dimensions must be positive')
    if not isinstance(spec.get('frames'), list) or not spec['frames']:
        raise ValueError('frames must be a nonempty list')
    repeat = spec.get('repeat', False)
    if type(repeat) is not bool:
        raise ValueError('repeat must be a boolean')
    color = ImageColor.getrgb(spec.get('preview_background', '#303840'))
    if len(color) != 3:
        raise ValueError('preview_background must be opaque RGB')
    frames, metadata, durations = [], [], []
    # Validate every crop and offset before creating the output directory.
    for index, entry in enumerate(spec['frames']):
        path = (manifest.parent / entry['source']).resolve()
        info = measure(path)
        with Image.open(path) as src:
            im = src.convert('RGBA')
        crop = integer_list(entry.get('crop', [0, 0, im.width, im.height]), 4, 'crop')
        x0, y0, x1, y1 = crop
        if not (0 <= x0 < x1 <= im.width and 0 <= y0 < y1 <= im.height):
            raise ValueError(f'Frame {index}: crop outside source or empty')
        offset = integer_list(entry.get('offset', [0, 0]), 2, 'offset')
        x, y = offset
        if not (x >= 0 and y >= 0 and x + x1 - x0 <= canvas[0] and y + y1 - y0 <= canvas[1]):
            raise ValueError(f'Frame {index}: crop would be clipped by canvas')
        duration = entry['duration_ms']
        if type(duration) is not int or duration < 10 or duration % 10:
            raise ValueError('GIF duration_ms must be positive multiples of 10; choose explicitly')
        f = Image.new('RGBA', tuple(canvas))
        # Unmasked paste copies exact RGBA, including RGB values beneath alpha0.
        f.paste(im.crop(tuple(crop)), tuple(offset))
        frames.append(f)
        durations.append(duration)
        metadata.append({'index': index, 'source': info, 'crop': crop, 'offset': offset,
                         'duration_ms': duration, 'events': entry.get('events', []),
                         'anchor': entry.get('anchor'), 'visual_acceptance': 'not_assessed'})
    previews = []
    for f in frames:
        bg = Image.new('RGBA', tuple(canvas), (*color, 255))
        bg.alpha_composite(f)
        previews.append(bg.convert('RGB'))
    out = fresh_output(output)
    for i, f in enumerate(frames):
        f.save(out / f'frame_{i:03}.png')
    options = {'loop': 0} if repeat else {}
    gif = out / 'preview.gif'
    previews[0].save(gif, save_all=True, append_images=previews[1:], duration=durations,
                     disposal=2, optimize=False, **options)
    decoded = []
    with Image.open(gif) as g:
        for i in range(g.n_frames):
            g.seek(i)
            g.load()
            decoded.append(g.info.get('duration', 0))
        loop = g.info.get('loop')
    report = {'manifest': str(manifest), 'canvas': canvas, 'frames': metadata,
              'repeat_for_preview': repeat, 'preview_background': color,
              'processing': 'Explicit rectangle crops and padding only; no alpha cleanup, pose alignment, rescaling or interpolation.',
              'gif': {'encoded_frames': len(decoded), 'durations_ms': decoded,
                      'requested_total_ms': sum(durations), 'decoded_total_ms': sum(decoded),
                      'loop_extension': loop, 'note': 'Encoder may merge identical frames; original PNG sequence remains authoritative.'},
              'visual_acceptance': 'not_assessed'}
    save_json(out / 'assembly.json', report)
    if sum(decoded) != sum(durations):
        raise ValueError('GIF total duration differs from request; keep PNGs and inspect assembly.json')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    qc = commands.add_parser('inspect', help='Report alpha and create three-background preview')
    qc.add_argument('source', type=Path)
    qc.add_argument('--out', required=True, type=Path)
    qc.add_argument('--max-side', type=int, default=900)
    seq = commands.add_parser('assemble', help='Assemble explicit crops/timing from JSON')
    seq.add_argument('manifest', type=Path)
    seq.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    try:
        result = inspect(args.source, args.out, args.max_side) if args.command == 'inspect' else assemble(args.manifest, args.out)
    except (ValueError, KeyError, OSError, TypeError) as exc:
        parser.exit(2, f'ERROR: {exc}\n')
    print(json.dumps({'output': str(args.out.resolve()), 'visual_acceptance': result['visual_acceptance']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
