# Grouped assets and motion

Review identity, drawing style, spatial relationships and continuity separately. An attractive frame does not establish a coherent action.

## Generate related content together

Use one sheet for related actions, effect stages, object states or matching components, then split and verify them. A 3×3 sheet works for a nine-frame study; 4×4 is another common layout. Choose the count for detail and relationships, not a fixed quota. Grouping does not guarantee a precise grid, consistent identity or complete motion phases. Treat transparency failures separately from layout and continuity.

State what the cells represent:

- **Timeline:** character actions, charge/release/impact/fade, smoke or explosions. Define phases, timing, loops and events, then play in order.
- **States:** intact/damaged/destroyed objects, closed/open mechanisms or equipment directions. Preserve structure, camera and anchors. Do not present discrete states as smooth animation.
- **Components:** projectiles, trails and impacts, equipment sets or UI states. Share design and palette rules; different uses may need different sizes or anchors and no common playback order.

Do not crowd unrelated assets into a sheet at the expense of detail.

1. Inspect the shared master and fix camera, proportions, structure, palette and display size. Record equipment and facing for characters, origin and energy direction for effects, and structural correspondence for state changes. A pose sheet need not supply character identity.
2. Define each cell before generation. For example, cells 1–8 may run, 9–12 jump and 13–16 react or fall; adapt the grouping to the task. Define start/end, support/contact phases, loops and events. Runs need alternating left/right contacts, compression, passing and push-off, not near-duplicate poses.
3. Request shared scale, camera, margins and relevant spatial references. Keep bodies and effects complete and cells separate. Check feet and weapons, effect origins and boundaries, and component joints. Requested cell count is not evidence of usable outputs.
4. Inspect the original, every frame and normal-speed playback. Measure actual dimensions. Use explicit crops and shared scales/anchors. Preserve an uncorrected review version and document justified layout adjustments. Static thumbnails do not prove continuity.
5. Repair affected frames or groups using the fixed master and selected sheet. Specify invariant features and faulty phases. Retain good frames; recheck identity, neighbors and loop seams. Stop identical retries without new evidence.
6. When game integration is in scope, verify anchors, collisions, connections and events at game size under actual logic. A preview is separate from engine testing and user acceptance.

Keep each reference's identity/style/pose role explicit. Do not chain only the preceding generated frame and accumulate drift. Establish key poses and action events before choosing intermediate frames and durations. Label isolated poses as a key-pose study, not a complete animation. Record generation/revision counts, usable outputs and actual elapsed time when comparing batches; small unrelated samples are not a controlled benchmark.

## Review

- Idle/walk/run: loop seam, alternating support, foot sliding, body volume, clothing and hair flicker.
- Attack/hit: anticipation, contact, force and recovery. Repetition or ping-pong playback must not hide missing phases.
- Jump: distinguish body movement from ground projection. Preview playback does not validate engine logic.
- Effects: onset, peak, impact and fade. Residue is not complete disappearance. Check translucency and hierarchy.

Timing and hit/cancel events are handoff data. Code cannot supply a move the artwork never depicts. Without a game-integration request, record candidate events without changing combat code.

## Crop and assemble

Read actual dimensions. If equal division fails, a fist crosses a cell, a glow touches an edge or a neighbor intrudes, inspect and specify crops. Do not independently scale each frame to its subject bounds; that erases spatial relationships.

Place rectangular crops on a shared canvas with explicit offsets. Record source, crop, position, duration, optional anchors/events and manual changes. Never silently clip. Document anchor adjustments rather than using automatic alignment to hide drift. Keep before/after versions when corrections are necessary. Crop fixes do not repair motion timing.

Deliver sequential PNGs or an atlas, timing data and a GIF or suitable preview. Choose count and timing for the action. One-shot actions play once by default; looping is for cycles or explicitly labeled repeated review. GIF encoding may merge identical frames, so verify decoded timing and duration before concluding that frames were lost.
