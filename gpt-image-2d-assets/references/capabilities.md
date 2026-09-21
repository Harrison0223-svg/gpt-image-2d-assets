# Tool capabilities and validation

The main workflow in this release is Codex with GPT-image-2.5. In that workflow, background removal and continuous-frame requests are available. Use the current tool schema for the active environment; do not invent unexposed model, seed, quality, background or FPS fields.

The bundled demos were produced in the Codex GPT-image workflow. Inspect actual alpha and light/dark background composites for transparent files. A file check does not establish engine behavior or user acceptance; see `examples/inventory/record.json` in the repository.

Grouped generation makes identity and style easier to compare but does not guarantee an exact grid, coherent motion or transparency. For a transparency edit, try one target image with a focused instruction such as `Remove the background. Make it transparent.` Inspect the result.

Distinguish official claims, the current tool schema and local observations. Historical findings are not permanent limitations. Keep private project paths and history out of the public distribution.
