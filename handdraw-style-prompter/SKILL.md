---
name: handdraw-style-prompter
description: Choose 2D styles from 261 reference images, 24 game-art recipes, custom references or mixed traits. Write prompts or generate images; route game assets to the shared gpt-image-2d-assets production and review workflow.
metadata:
  short-description: 261 reference styles and 24 game-art recipes
---

# Style Library and Prompts

Preserve the original IDs and images while supporting more 2D art directions. Follow the user's intent rather than reducing every request to prompt writing.

## Entry points

- ID and subject without a generation request: write the prompt in the user's language. Supply a genuine English translation when requested or useful; adding English labels is not translation.
- Browse: open `gallery/index.html` for the original library or `gallery/extensions.html` for game recipes. For a valid ID, retrieve only that entry. If browser policy blocks a local page, list relevant IDs and traits in chat without bypassing the denial or claiming the page opened.
- Search: `python scripts/style_catalog.py --search <keyword>`. Select an entry with `--style 063` or `--style G03`. If literal search has no results, suggest semantically relevant existing entries without inventing a match.
- Generate an illustration: use built-in GPT Image, follow the reference rules below and inspect the result.
- Produce characters, icons, components, scenes, action sheets or effects: read the sibling `../gpt-image-2d-assets/SKILL.md` and complete production there. Avoid repeated routing or stopping at prompts.

## From style to prompt

`references/styles.json` is the preserved 001–261 source index, with English style names and original Chinese annotations. `references/game-styles.json` contains G-prefixed game recipes. Entries without sample images remain unvalidated text recipes. Query both with `scripts/style_catalog.py`. Custom references and mixed traits need no numbered equivalent.

Separate visual language from example content. People, props, stories, backgrounds and layouts in an entry do not automatically belong in the output. The user's subject, canvas, text and asset requirements take priority. Use the ID, name, relevant visual traits and requested subject. Artist names may remain attribution labels. The legacy `scripts/prompt_style.py` concatenates source text; it is not a complete translator or final production prompt.

For mixing styles, adapting them to games or recording a style lock, read the sibling `../gpt-image-2d-assets/references/style-selection.md` when needed.

## References and review

Run `python scripts/resolve_reference.py --style <ID>` for original styles. The backend defaults to unknown. Pass `--model` only with evidence for the current image backend. Historical `model_capabilities.json` suggestions do not establish current activation quality. Astra is not the image backend.

Inspect any returned reference image before using it with the current tool schema. Read [reference isolation](references/reference-image.md). Explicit user references take precedence over historical routing. For G recipes without images, use their text traits rather than inventing a file path. Generate and edit only with built-in GPT Image.

The main task reviews the actual subject and visual language. Retain originals, prompts, reference IDs and roles, paths and findings. Repair specific defects within scope and review again. Neither a fixed one-repair limit nor unlimited retries is appropriate. Stop affected calls on confirmed quota or permission failures and preserve good results. Do not mark an ungenerated recipe as visually validated.
