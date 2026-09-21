# Delegated batches and main-task review

Use this branch only when the user or applicable instructions explicitly enable delegation and independent work exists. Reading this file does not grant permission. When enabled, use `gpt-5.6-luna` by default for suitable batches while retaining the selected main model for planning, integration and actual image review. Use subagents, not user-facing independent tasks. The main task must be able to inspect images.

## Ownership

Assign a bounded asset list, file ownership and references. Tell workers they share the codebase and must not overwrite or revert others' work. Independent characters or effect packs may run in parallel. Dependent frames share an inspected master.

One worker owns a related sheet, continuous action/effect or corresponding state set. Do not split a 16-cell sheet across 16 independent generators. State cell contents, temporal/state/component relationships, grouping, shared master and repair scope. Save each call's record and check messages before the next call; avoid long unattended generation loops.

A handoff should include:

```text
Use the Codex GPT-image-2.5 workflow and the stated identity/style/pose roles of each reference.
Write only to the assigned version directory; retain exact outputs and masters.
Asset list, phases, canvas/display size, allowed alpha effects and references: ...
Call budget and targeted repair scope, proportionate to this batch: ...
Inspect references first. Save originals, exact prompts, reference roles, output paths and failures.
Do not use external generators, change the style, paint with code or grant acceptance.
Stop affected calls on confirmed quota or permission failures; return results to the main task.
You are not alone in the codebase. Do not modify other directories.
```

Return usable output paths promptly so review can proceed. Use current agent IDs, never hard-coded sessions.

## Records

Use concise JSON or prose that tracks asset ID, purpose, worker, planned/generated/failed status, full prompt, reference roles and paths, exact original and copied outputs, actual tool and known parameters, parent/version, measurements and the main task's inspection findings. Mark unreported fields unknown. Record hashes or timing when needed for copy checks or comparison. A worker's timing is not an independent benchmark. No original file means no generated status.

## Review and repairs

The main task inspects masters, contact sheets covering every delivered item and actual playback. Enlarge complex edges, repairs and suspicious deviations. Open originals when thumbnails are insufficient. A worker report or complete manifest is not visual evidence.

Report specific defects, affected assets and invariant features. Delegate only the required repair and inspect it again. Existing direction approval remains valid; do not invent batch approval gates.

If subagents or the Codex GPT-image-2.5 workflow are unavailable, state the limitation. Do not silently switch models or providers. Continue directly within authorized scope unless the user requires delegation, in which case explain the blocker and continue possible organization and review.
