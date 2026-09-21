# Transparency and edges

Request real transparent output and specify allowed effects. Ordinary characters usually need no floor, shadow or halo; soft effects may use translucency. Generate separately controlled shadows as separate assets. Do not ask the model to draw a checkerboard.

## Inspect

1. Check original mode and effective alpha. RGB, fully opaque, empty and partly transparent files are different outcomes. An RGBA filename or a viewer checkerboard is not proof.
2. Inspect alpha distribution alongside appearance. A maximum of 254 can still look nearly opaque; this does not justify making every character translucent.
3. Open composites on black, white and the project background. Check at display size and inspect original-resolution crops of hair, shoes, fine lines, glass and soft glows.
4. Distinguish generated residue, post-processing damage and engine sampling. If the source is clean but the imported asset is not, inspect import settings, atlas padding, sampling and blending before redrawing.

Highlights, pale hair and soft light may be legitimate. Do not remove pixels solely by color. Measurements do not automatically diagnose dirty edges.

## Repair

- Clean native alpha: retain it; do not automatically remove the background again.
- Baked background/checkerboard: use a focused Codex GPT-image-2.5 transparency edit, then check both alpha and subject changes.
- Specific residue: identify the region and structures to preserve. Do not promise pixel-perfect preservation from a generative edit.
- Continued failure: retain versions and investigate the call. Distinguish one failed output from unsupported capability. Follow the entrypoint's retry limits; do not substitute threshold masking, blur or another generator for the art task.

## Focused transparency edit

Separate structure/action generation from background removal. Pass one explicit target. Inspect a local file first and use `referenced_image_paths` when supported. Do not add the master just to retain style or combine this pass with new poses, frames, materials or grid changes.

Start with:

```text
Remove the background. Make it transparent.
```

Add only a necessary preservation constraint. Long lists of RGBA, color, grid and action requirements do not enable hidden transparency parameters. This wording has worked in local trials; it is not a guarantee.

After failure, verify the target, unrelated requirements and actual returned file. Test a representative crop to isolate the issue before applying a demonstrated method to the full sheet. Diagnostic crops are not a default plan to redraw every frame. The main task should inspect results instead of inferring missing capability from a worker's report. Change one justified factor at a time; stop on confirmed quota or permission failures.

If a small group succeeds but the full sheet fails, split existing continuous groups into strips, keeping all related phases together. Inspect each edited strip's resampling, count, layout and alpha. Remeasure new outputs rather than assuming the original grid still applies.

Acceptance requires useful alpha plus usable edges, identity, style, dimensions and layout. Alpha success alone is not visual acceptance. Retain originals and measure the returned dimensions, crops and anchors.

The API and built-in tool are separate interfaces. Use `background` or similar parameters only when exposed by the current schema. Otherwise use supported natural-language editing; do not invent fields or switch to a billed API without authorization. Check current official documentation when answering capability questions.

GIF has limited color and transparency support. RGBA PNG is the source asset. A GIF on a declared background is for motion review, not proof of source-alpha quality.
