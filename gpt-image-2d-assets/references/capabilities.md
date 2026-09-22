# Tool capabilities and validation

The main workflow in this release is Codex with GPT-image-2.5. In that workflow, background removal and continuous-frame requests are available. Use the current tool schema for the active environment; do not invent unexposed model, seed, quality, background or FPS fields.

The bundled demos were produced in the Codex GPT-image workflow. Inspect actual alpha and light/dark background composites for transparent files. A file check does not establish engine behavior or user acceptance; see `examples/inventory/record.json` in the repository.

Grouped generation makes identity and style easier to compare but does not guarantee an exact grid, coherent motion or transparency. For a transparency edit, try one target image with a focused instruction such as `Remove the background. Make it transparent.` Inspect the result.

Distinguish official claims, the current tool schema and local observations. Historical findings are not permanent limitations. Keep private project paths and history out of the public distribution.

## Motion experiment snapshot — 2026-09-22

Fifteen built-in GPT Image submissions produced fourteen retained images; one had no retained result or diagnostic. Opposing contact poses improved limb readability in this fox case, but repeated expansions still introduced local errors. The refined run and jump remain candidates; the wave remains on hold because its repaired poses lack sufficient motion. Eleven utility tests pass; this is not continuous human viewing, engine validation or user acceptance. The tool did not report a backend model, price or quota. See the optional [experiment summary](https://github.com/Harrison0223-svg/gpt-image-2d-assets/blob/master/docs/motion-validation-2026-09-22.md); it is not a runtime dependency.
