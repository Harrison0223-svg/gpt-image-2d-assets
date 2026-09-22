# Grouped assets and motion

Review identity, limb connections, temporal continuity, natural motion and import readiness separately. A grid, transparent PNG or working GIF does not establish animation quality.

## Choose the relationship

- Time sequences: define order, contact/support/release events and loop or one-shot behavior.
- Corresponding states: preserve structure and anchors; do not present discrete states as smooth animation.
- Related components: share design, palette and connection rules without forcing one size or playback order.

Use a stable identity master and label pose/style/layout references. Do not combine unrelated actions to fill a grid. Eight, nine and sixteen cells are possible layouts, not quality requirements.

## Character-motion workflow

A previously validated simple action can go straight to a grouped sheet. For unfamiliar complex motion, production-quality requests or an existing failure, use this short loop. These are checks the main agent performs within the authorized work, not additional user-approval gates.

1. **Define the action.** Record purpose, display size, camera, proportions, active and inactive body parts, events, timing and loop behavior. Distinguish in-place animation from root motion. For jumps, decide whether vertical travel belongs in the drawings or the engine; do not apply it twice.
2. **Test the critical relationship.** Start with two opposing key poses, adding a few more only when useful. For a free-arm run, opposite contacts must exchange the same near arm and leg. For a wave, trace the same shoulder/elbow/wrist at both extremes. For a jump, inspect anticipation, flight and landing support. These are key poses, not a finished animation.
3. **Inspect connected limbs.** Follow shoulder–elbow–wrist and hip–knee–ankle, including occlusion. Clothing seams, overlap and lighter-near/darker-far shading can help. If identity is unclear, repair the pose or readability first. A generated color-coded mannequin can also contain mixed or disconnected limbs; validate it before using it as a pose reference.
4. **Expand verified keys.** Identify each reference's role and the key poses' positions in the new sequence. Describe intervening support, passing, push-off, flight or recovery. Expand one action at a time with sufficient cell margins. Do not rely solely on the preceding generated frame and accumulate drift.
5. **Review and repair one defect.** Inspect every frame, actual timed playback, slow motion, adjacent frames and the loop seam. Name the frame and connected limb, such as “frame 8 has the near leg and near arm both forward; the near arm must swing back.” Repair a frame or short group, then recheck the whole sequence and invariants. Keep pose, layout and transparency edits separate.
6. **Refine natural motion.** Once the main action works, refine timing, weight, joint arcs and restrained tail/clothing follow-through. Change one supported factor and retain the original timing for comparison. Review at the target display size. If game integration is in scope, also test displacement, foot sliding, attachments and events.

Do not repeat increasingly long prompts without new evidence. If a targeted edit repeats the defect, reduce it to a smaller relationship test, reduce the action group, or retain a clearly labeled hold. Reordering, ping-pong playback, mirroring the whole character, interpolation and code-drawn substitutes must not disguise missing phases.

## What to inspect

| Action | Required visible evidence | Repair signals |
|---|---|---|
| Free-arm biped run | Opposite contacts; the same near hand goes behind/in front of its shoulder and returns; readable compression, push-off and flight | Repeated half-cycle, frozen hand, switching arms, wrong seam phase |
| Wave | The same shoulder/elbow/wrist; intended movement in upper arm, forearm and wrist; stable inactive hand | Switching arms, extra limbs, body bobbing instead of waving, anatomy repaired by removing the motion |
| Jump | Anticipation, takeoff, apex, descent, landing absorption and settling | Auto-grounding erases flight, missing landing compression, camera follows the jump, duplicated engine displacement |
| One-shot attack/hit | Preparation, release/contact, follow-through and recovery; visible event frames | Missing recovery hidden by looping, weapon changes hands, disconnected grip |
| Effects | Start, peak, interaction and dissipation, with clear attachment points | Residue labeled fully gone, random core changes, unrelated effects presented as one sequence |

Apply the action contract: shield carrying, constrained arms, hovering and mechanical motion may intentionally differ from ordinary biped mechanics.

Tracking “the rightmost hand” changes the tracked object when limbs cross. Record actual connected chains and frame evidence. When reviewers disagree, the main agent inspects enlarged source regions rather than averaging prose scores. Unresolved limb identity, support or phase relationships cannot be offset by a high overall score.

## Cropping, registration and playback

Measure the actual image. Equal grid divisions are provisional: inspect cell crossing, neighboring fragments and non-divisible dimensions. If rectangular crops cannot retain the whole figure while excluding neighbors, request a separate GPT Image layout repair. Do not ship frames with a neighboring ear or boot fragment; recheck the action after layout edits.

Retain an unaligned review before applying explicit crops and offsets on a shared canvas. Document registration. Prefer a consistent pelvis X and virtual ground reference; do not center each silhouette, rescale individual figures or align every frame's lowest pixel. Raised feet during flight are not automatically registration drift. Uniform preview scaling is distinct from altering individual source poses.

Deliver source PNGs; GIF is a preview. See [tools](tools.md) for `asset_tools.py` and the offline `motion_review.py` player. Exact duplicates and pixel differences are diagnostic hints, not animation scores. Valid holds may repeat frames; loops do not require a duplicated endpoint.

Normal speed reveals rhythm, slow motion helps trace structure, and stepping localizes errors. Label screenshot/contact-sheet inspection as static review. Running a player and sampling screenshots does not establish continuous human viewing. One-shot actions play once by default; label repeated review playback explicitly. A key-pose display is not a complete animation.

For in-game motion, compare planted feet in world coordinates and relate movement speed to stride length. Test stopping, blocking, turning and transitions. Without integration authorization, deliver candidate anchors/events and record engine validation as not performed.

## Delivery

Provide sources, ordered PNGs/atlas, timings/events, crop/registration records, previews and specific findings. Keep technical checks, connected poses, temporal/natural-motion review, display-size review, engine validation and user acceptance separate.

Limb switching, missing phases, broken anatomy, cell contamination or unexplained jumps block an “art passed” conclusion. A clearly labeled candidate or key pose can still be delivered. Compare production methods with the [motion evaluation protocol](motion-evaluation.md), retaining the route that meets the action contract with a reasonable repair burden.
