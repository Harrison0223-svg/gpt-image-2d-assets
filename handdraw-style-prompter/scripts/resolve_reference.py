#!/usr/bin/env python3
"""Resolve whether a numbered image reference is needed for a model and style."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
POLICY = SKILL / "references" / "model_capabilities.json"
STYLES = SKILL / "references" / "styles.json"
ALLOWED = {"strong", "weak", "none", "unknown"}


def positive_traits(traits: str) -> str:
    parts = (part.strip() for part in traits.replace("。", "；").split("；"))
    return "；".join(part for part in parts if part and not any(word in part for word in ("避免", "不要", "不准")))


def reference_path(number: int) -> Path:
    bucket_start = ((number - 1) // 200) * 200 + 1
    bucket = f"{bucket_start:03}-{bucket_start + 199:03}"
    folder = SKILL / "images" / "individual" / bucket
    grid = folder / f"{number:03}_grid.jpg"
    return grid if grid.exists() else folder / f"{number:03}.png"


def resolve(model: str, style: str) -> dict:
    styles = json.loads(STYLES.read_text(encoding="utf-8"))
    try:
        number = int(style)
    except ValueError as error:
        raise ValueError("Style must be a number.") from error
    if not 1 <= number <= len(styles):
        raise ValueError(f"Style must be a number from 001 to {len(styles):03}.")
    selected = styles[number - 1]
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    entry = dict(policy["default"])
    profile = policy.get("models", {}).get(model, {})
    entry.update({key: value for key, value in profile.items() if key != "styles"})
    entry.update(profile.get("styles", {}).get(f"{number:03}", {}))
    name_activation = entry.get("name_activation", "unknown")
    traits_activation = entry.get("traits_activation", "unknown")
    if name_activation not in ALLOWED or traits_activation not in ALLOWED:
        raise ValueError("Invalid model capability policy.")
    traits = positive_traits(selected.get("traits", ""))
    if name_activation == "strong":
        source, use_image, prompt_traits = "name+style", False, ""
    elif traits_activation == "strong" and traits:
        source, use_image, prompt_traits = "name+style+traits", False, traits
    else:
        source, use_image, prompt_traits = "reference-image", True, ""
    path = reference_path(number) if use_image else None
    return {
        "model": model,
        "style": f"{number:03}",
        "activation_source": source,
        "use_reference_image": use_image,
        "prompt_traits": prompt_traits,
        "reference_path": str(path) if path else None,
        "reference_exists": path.exists() if path else None,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="unknown", help="Verified image backend only; omit when unknown. Astra is not an image backend.")
    parser.add_argument("--style", required=True)
    args = parser.parse_args()
    print(json.dumps(resolve(args.model, args.style), ensure_ascii=False))
