# Motion evaluation protocol

Use when comparing production methods or diagnosing repeated motion failures. Do not run the full suite for an ordinary icon or single-image task. Production steps are in [motion](motion.md).

## Compare methods

Hold identity, costume, style, camera, intended display size, action and reference roles stable. Change one main factor where practical. Different frame counts, stages or reference structures constitute workflow comparisons, not strict A/B experiments. Do not claim a reproducible seed when the tool exposes none.

Useful routes to compare:
- A concise grouped-action prompt as the cost baseline.
- Explicit phase and limb-relationship instructions with the same basic contract.
- A few verified opposing key poses followed by expansion, counting the extra calls.
- Validated motion-reference transfer; reject incorrect mannequin/skeleton topology before transfer.

First check the action contract, then compare natural motion and repair effort. Scores cannot compensate for limb switching, missing phases or cell contamination. Repeat the leading route independently and test another action before broadening its use. Small samples support case findings, not reliable success-rate claims.

## Regression tasks

| Suite | Critical relationships and events | Review | Failure examples |
|---|---|---|---|
| RUN | Opposing contacts, the same near hand/leg exchanging front/back, compression, push-off, flight, full two-step cycle | Trace near/far joint chains; full loop, slow playback and seam; target size; world-space sliding when integrated | Frozen hand, repeated half-cycle, wrong seam phase, joint jumps |
| WAVE | Raise, opposing wave extremes, lower; or explicitly only an active-wave loop | Trace the same shoulder/elbow/wrist through every transition and inspect movement amplitude | Switching arms, extra limbs, correct anatomy but almost no wave; short loop mislabeled complete greeting |
| JUMP | Anticipation, takeoff, ascent, apex, descent, landing compression, settle | Fixed camera/scale; ground and pelvis/head trajectory; stepping and one-shot playback | Auto-grounding, missing landing absorption, duplicated vertical motion |

For attacks, separately define anticipation, contact, follow-through, recovery and hand/weapon attachment. Mark unexecuted suites as untested; a run result does not validate attacks.

## Evidence record

Use a short table or JSON; include only applicable fields:
- Candidate, action contract, route, parent, exact prompt and each reference's role.
- Exact returned source and copy, SHA256, actual dimensions/mode/alpha, call status and errors.
- Frame count, explicit crops/offsets, durations, loop/one-shot and every timing/registration adjustment.
- Separate pass / partial / fail / unclear findings for identity, limb chains, event order, support/weight, arcs/follow-through and seam. Cite actual frames and the reviewer's reason.
- Actual review methods: source image, all stills, player execution/sampled frames, continuous viewing, engine. Do not claim methods that were not performed.
- Localized defect, repair target, changed invariants and recurring defects.
- Separate technical, motion-art, display-size, engine and user-acceptance conclusions.

For disputed images, inspect enlarged connections on the main task. Do not track the rightmost hand instead of the same hand, count uncertainty as success, or fail a key-pose board merely because it has few frames.

## Repairs and cost

Separate action, alpha and layout edits. Retain before/after sources and recheck invariants; unspecified regions may also change. Stop identical retries when the same defect recurs without new evidence. Reduce the problem or retain a labeled hold.

Record submissions, returned images, tool failures, generation/edit counts and elapsed times. Parallel call waits are not total wall-clock time. Unreported costs, quota and backend identity remain unknown. A tool failure is not a visual failure; alpha compliance is not motion success.

The 2026-09-22 fox experiments found two opposing contact poses useful for diagnosis/reference, but expansion and local/layout edits still had independent failures. No tested route established reliable production-quality animation. The [public experiment summary](https://github.com/Harrison0223-svg/gpt-image-2d-assets/blob/master/docs/motion-validation-2026-09-22.md) is optional evidence, not a runtime dependency.

## Animation principles

[Animation Mentor's walk-cycle tutorial](https://www.animationmentor.com/blog/tutorial-animating-human-walk-cycle/) covers keys, support, weight, arm motion and refinement. [Adobe's animation principles](https://www.adobe.com/creativecloud/animation/discover/principles-of-animation.html) explain pose-to-pose, arcs, timing and follow-through. These inform hypotheses and review; they do not prove GPT Image will follow them.
