# Choose and apply a style

Resolve the sibling `handdraw-style-prompter` from this skill's parent directory, not the project working directory. Query selected entries instead of loading the whole library. If the companion is absent, use the user's descriptions or references and disclose that numbered lookup is unavailable. Do not guess IDs.

## Find a direction

Run from the companion directory, or use an absolute script path:

```sh
python scripts/style_catalog.py --search watercolor
python scripts/style_catalog.py --style 063
python scripts/style_catalog.py --style G03
```

- **001–261:** preserved original index and images. Browse `gallery/index.html`.
- **G01–G24:** game-art text recipes with observable traits, uses and adaptation notes. Browse `gallery/extensions.html`. A recipe without a reviewed sample is not a validated master.
- **Custom:** use the user's reference or description directly.
- **Mixed:** name one primary style and a few secondary traits. Explain what each contributes, such as cel color blocks with cut-paper edges. Percentages express intent, not precise mixing controls. Avoid contradictory media requirements.

For an authorized visual comparison, keep the subject, camera and proportions constant across a few samples. Do not generate for text-only advice. Respect a reserved direction-selection gate; when selection is delegated, choose and inspect a first sample without repeated approval requests.

## Adapt to the asset

Separate visual traits from example content. Inherit linework, shapes, color, lighting and material treatment. Do not import example characters, props, jokes, white backgrounds or large margins over the user's subject, alpha or camera requirements. Artist names are index labels; a production prompt must describe the needed visual traits.

For an original style, use `scripts/resolve_reference.py --style 063`. The current target workflow is Codex with GPT-image-2.5. Pass `--model` only when the active environment exposes and documents that parameter. `activation_source` is a historical routing suggestion, not a validation report. Explicit reference requests override it.

Inspect local references before use and label each as identity, style, pose or layout. For a style-only image, specify that it supplies linework, brushwork, color and texture; the current asset brief controls subject, identity, action, layout, background and text. Follow the actual tool schema for recent-image references rather than inventing paths.

- Transparent characters and icons: keep texture within the subject; do not add paper backdrops, floors or baked checkerboards. Specify intentional translucent effects.
- Pixel assets: establish display resolution and inspect clusters, color blocks, edges and sampling. A low-resolution thumbnail is not proof of pixel-art quality.
- Action sheets: lock identity, proportions, camera and major color blocks. Reduce cells when detail becomes unreadable.
- Scenes and tiles: lock view and scale. Require and inspect seams only when tiling is requested.
- UI and components: fix edge treatment, light direction, relative dimensions and text space. Do not invent lettering.

## Record the choice

A single image needs only a concise generation record. For ongoing production, keep `style-lock.json` or equivalent: ID or custom description, visual traits, reference roles, exact reviewed master path, target size, fixed features and candidate/user-approved status. Only explicit user approval permits user-approved status. Record the main task's visual review separately. Reuse this contract for new assets and preserve unaffected constraints during repairs.
