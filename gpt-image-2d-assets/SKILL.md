---
name: gpt-image-2d-assets
description: Generate, edit and review 2D art in Codex with the current GPT-image-2.5 workflow. Choose from 261 reference styles, 24 game-art recipes, custom references or mixed traits; remove backgrounds, generate continuous frames, inspect transparency, cut sprite sheets and deliver timed animation previews.
---

# GPT Image 2D Assets for Codex

Handle style exploration, prompt writing, asset generation or review according to the user's request. Cover game assets and standalone illustrations without taking over game development. Reuse the current authorization and selected style; respect explicit discussion, direction-selection and user-acceptance gates.

## Choose a path

- Existing master or style: inspect the actual reference and reuse it. Distinguish identity, style, pose and layout references.
- Style IDs, browsing, custom or mixed styles: read [style selection](references/style-selection.md). Original IDs 001–261 and game recipes G01–G24 are separate namespaces.
- Prompt only: return a prompt without generating. An explicit production request should proceed to generation, even when it starts with a style ID.
- Unspecified style: infer from the project or offer a few concrete choices. If the user delegates the choice, select a suitable direction and make a first sample without inventing an approval gate.
- Actions, effects, states or related components: read [motion and grouped assets](references/motion.md). For unfamiliar complex motion or an existing frozen-limb/repeated-phase failure, verify the critical key-pose relationship before expansion. When comparing methods, read [motion evaluation](references/motion-evaluation.md). For alpha, assembly and playback, read [transparency](references/transparency.md) and [tools](references/tools.md).
- Read [delegation](references/delegation.md) only when delegation is explicitly enabled and independent work exists. Otherwise execute on the main task.
- For tool parameters or model questions, read [capabilities](references/capabilities.md) and check the current schema.

## Working with Codex and GPT-image-2.5

Keep the user's selected Codex model responsible for planning, reference analysis, prompts, actual image review and repair decisions. The current workflow uses GPT-image-2.5 for generation and editing; it can remove backgrounds and generate continuous-frame requests in Codex. Re-check the active schema when the environment changes. Do not invent unexposed model, seed, quality, background or FPS parameters.

Record the useful asset constraints: purpose, target display size, subject and identity, camera, proportions, observable style traits, reference roles, transparency and output organization. Omit irrelevant fields. Reuse this contract across a batch.

## Generate, review and deliver

1. Organize prompts as subject, style, asset structure and necessary constraints. Describe contours, color blocks, lighting, materials and detail density. Reference subjects, text and compositions must not leak into the requested asset. Prioritize readability at the intended size.
2. Generate and edit art through the current Codex GPT-image-2.5 workflow. Inspect local references first. Save the exact returned original, prompt, reference roles, output path and call status in a versioned directory. Background removal and continuous-frame generation are available workflow operations, but the returned files still need review. Do not guess the newest file or overwrite masters. Scripts may measure, crop, pad and assemble existing pixels; they must not draw substitutes or fabricate motion.
3. Inspect the shared master before expanding. Group related content according to its relationships and readability. For complex character motion, first validate a few opposing key poses and connected limbs, then expand with those verified references. An unverified pose or mannequin is not a reliable constraint. Play separate sequences separately and label states and key-pose boards accurately.
4. Open the actual results. Review identity, style, edges and target-size readability. For motion, trace the same connected limb through phases, weight shifts and the seam; changing hand positions does not prove the same hand moved. Retain an unaligned original, document registration, localize defects by frame, and recheck the whole sequence after focused repairs. Scripts cannot automatically certify art quality.
5. Deliver originals, components or sequences, necessary playback previews and concise records. Distinguish generation, technical checks, visual review, engine validation and user acceptance.

## Scope and stopping

Do not expand style exploration into a full asset set or treat style approval as approval of every frame. Do not edit a game unless requested. If a transparency edit fails, verify the target and try a justified, focused edit or grouped experiment. Preserve successes and stop identical retries without new evidence. Stop affected calls on confirmed quota exhaustion, permission denial or tool unavailability; continue organization and review without switching providers to evade the limitation.
