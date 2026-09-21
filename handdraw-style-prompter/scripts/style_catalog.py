#!/usr/bin/env python3
"""Read-only lookup across the original gallery and game style recipes."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def entries():
    original = json.loads((ROOT / 'references/styles.json').read_text(encoding='utf-8'))
    extended = json.loads((ROOT / 'references/game-styles.json').read_text(encoding='utf-8'))['styles']
    return [dict(row, id=row['number'], source='original-gallery') for row in original] + [dict(row, source='game-recipe') for row in extended]


def select(style):
    key = style.strip().upper().lstrip('#')
    if key.isascii() and key.isdigit():
        key = f'{int(key):03}'
    elif key.startswith('G') and key[1:].isascii() and key[1:].isdigit():
        key = f'G{int(key[1:]):02}'
    for row in entries():
        if row['id'] == key:
            return row
    raise ValueError(f'Unknown style: {style}. Use 001–261 or G01–G24.')


def search(query, limit=12):
    terms = query.strip().casefold().split()
    matches = [row for row in entries() if all(t in json.dumps(row, ensure_ascii=False).casefold() for t in terms)]
    return {'total': len(matches), 'returned': min(len(matches), limit), 'styles': matches[:limit]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--style')
    group.add_argument('--search')
    parser.add_argument('--limit', type=int, default=12)
    args = parser.parse_args()
    if args.limit < 1:
        parser.error('--limit must be positive')
    try:
        result = select(args.style) if args.style is not None else search(args.search, args.limit)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
