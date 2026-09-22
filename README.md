# GPT Image 2D Assets

Pick a style, make a sprite sheet, and turn it into a GIF. A pair of Codex skills for making and reviewing 2D art with Codex's current GPT-image-2.5 workflow.

The main workflow is Codex. In the current setup, GPT-image-2.5 can remove backgrounds and generate continuous frames. Always inspect the returned files: model output can still drift between frames or change an identity.

## A fox, nine frames

![Fox run preview](examples/fox-motion/preview.gif)

This demo started as a 3×3 sheet. We cut it into nine PNGs and assembled a loop at 90 ms per frame. The first attempt repeated similar poses, so we pointed out the issue and generated a revised sheet. Both versions are included. The gait still needs refinement before use in a game.

[Sprite sheet](examples/fox-motion/fox-run-3x3-v2.png) · [Individual frames](examples/fox-motion) · [Timing and crop data](examples/fox-motion/sequence-v2.json)

## Motion workflow update — September 2026

The [motion experiments](docs/motion-validation-2026-09-22.md) compare direct sheets, explicit phases, key poses and targeted repairs. The skill now checks opposing key poses and connected limbs before expanding unfamiliar motion, and includes a small offline comparison player. The refined run and jump are review candidates; the wave remains on hold. These tests do not establish reliable production-quality animation. The original demo above is preserved.

## Try a different look

![The same fox in cel, pixel and watercolor styles](examples/fox-motion/fox-style-comparison.png)

Same character, outfit and standing pose: **Clean Cel (G03)**, **Pixel Cluster (G01)** and **Watercolor Ink (G05)**. The pixel version is a visual exploration; it has not been checked as a pixel-perfect game sprite.

Choose from **261 reference styles**, **24 game-art recipes**, your own reference images, or a mix of specific traits.

## What you can make

- Characters, portraits, expressions and action sheets.
- Inventory icons, UI pieces and object states.
- Effects with charge, release, impact and fade stages.
- Backgrounds and tiles, with seam checks when tiling is needed.

![Inventory icons](examples/inventory/small-preview.png)

The included tools inspect alpha, crop sheets with explicit coordinates, and assemble timed PNG sequences and GIF previews. They do not draw replacement art or invent missing animation frames.

## Install

Use Codex with the GPT-image-2.5 image workflow. Copy both folders into your Codex skills directory, usually `~/.codex/skills/`:

```text
gpt-image-2d-assets/
handdraw-style-prompter/
```

Back up existing folders with these names before updating. You can also give Codex this repository URL and ask it to install both skills.

The crop and inspection tools need Python 3 and Pillow:

```sh
python -m pip install Pillow
```

## Try it

```text
In Codex, call `$gpt-image-2d-assets` to make a fox courier in G03 style.
Keep the background transparent.

Make a 3×3 run cycle for this fox, facing right.
Cut the sheet into frames and make a GIF preview.

Show this same character in cel, pixel and watercolor styles.
Keep the outfit, camera and pose the same.

Make a matching set of a potion, key, gem and scroll.
Check how they read at inventory-icon size.
```

Start with `gpt-image-2d-assets` for asset production. Use `handdraw-style-prompter` to browse styles or write prompts. A prompt-only request does not trigger image generation.

```sh
python handdraw-style-prompter/scripts/style_catalog.py --style G03
python handdraw-style-prompter/scripts/style_catalog.py --search watercolor
python gpt-image-2d-assets/scripts/asset_tools.py inspect examples/inventory/inventory-sheet.png --out review-v1
```

The selected Codex model plans the work and reviews the actual images. GPT-image-2.5 handles the current generation and editing workflow, including background removal and continuous-frame requests. Re-check the active tool schema when the environment changes; the model name is not a promise of a hidden parameter.

## Examples and notes

[How the fox demo was made](docs/fox-demo.md) · [Game style recipes](handdraw-style-prompter/gallery/extensions.html) · [Original gallery](handdraw-style-prompter/gallery/index.html)

Download the HTML galleries and open them locally. Original source annotations remain in Chinese; style IDs, English style names and reference images are preserved. The public skill instructions and guides are in English.

Image generation can drift between frames. Alpha checks, visual review, playback, engine testing and user approval are recorded separately. A successful file check does not establish animation quality or game readiness.

```sh
python gpt-image-2d-assets/scripts/test_asset_tools.py
```

## Credits

The style workflow started by calling [Yang's handdraw-style skill](https://github.com/yang0/handraw-style). Its 261 original styles and images are preserved here, and this repository adds 24 game-art recipes, the asset workflow, inspection tools and demos. The source baseline is `70bf51d6b4c301805dd6c083355a2ad18db1023b`.

See [the upstream license](UPSTREAM-LICENSE.txt). The reference images and artist index are credited source material, not original artwork by this project. Their inclusion is not a guarantee of rights to use them as commercial game assets.
