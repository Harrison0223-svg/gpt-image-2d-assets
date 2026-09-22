# Motion workflow experiments — 2026-09-22

The original fox demo remains unchanged. It is evidence of a recurring failure: a valid transparent sheet and GIF can still lack a convincing full gait and arm swing.

## What was tested

The session submitted 15 built-in GPT Image calls and retained 14 returned images. One parallel call had no retained result or diagnostic; it is excluded from visual comparisons. The tool did not report a backend model, price or quota. These were small workflow experiments, not controlled success-rate measurements.

| Route | Observation | Decision |
|---|---|---|
| Concise eight-frame run | Some arm reversal, but ambiguous leg identity and irregular phases | Keep as a baseline, not accepted animation |
| Detailed per-frame run instructions | More prompt detail did not establish the requested full gait | Do not rely on instructions as evidence |
| Four key poses | Arm reversal became easier to inspect; leg identity remained unclear | Useful diagnosis, not a finished cycle |
| Color-coded mannequin | A connected arm mixed near/far colors | Reject the reference before character transfer |
| Two opposing contact poses, then expansion | The near/far limb relationship was clearest; two repeated expansions still produced different local errors | Preferred route for this fox, with repair and review |
| Wave and targeted edits | Initial versions switched arms; the last repair reduced the intended wave to similar raised-hand poses | Hold as animation; static poses only |
| Jump | Anticipation, flight, descent and landing-compression poses are recognizable | Candidate requiring temporal and integration review |

The preferred run route then received a local last-frame arm correction and a separate spacing edit. The spacing edit removed the need for cuts that clip a boot or include a neighboring ear. It does not prove natural timing or gameplay readiness.

## Selected evidence

Refined run candidate:

![Run candidate, not final acceptance](../examples/motion-validation-20260922/run-preview.gif)

The candidate has clearer near-arm reversal and opposing contacts than the original demo. The compressed phases and far-arm transitions remain review concerns. Foot planting, world-space speed, turns/stops and continuous human viewing have not been accepted.

The wave remains on hold:

![Wave hold: similar raised-hand poses](../examples/motion-validation-20260922/wave-hold.png)

[Jump preview](../examples/motion-validation-20260922/jump-preview.gif) and prompts are included in the [selected evidence](../examples/motion-validation-20260922). Full-resolution source sheets and crop manifests remain in the local experiment archive after upload timeouts; this public subset contains review previews, not an import-ready asset pack. The jump drawings already contain vertical movement; integration must not apply it twice. The wave's shorter active-loop experiment does not fulfill the earlier complete greeting action.

## Changes retained in the skill

- Verify the most error-prone opposing relationship before expanding unfamiliar motion.
- Follow the same shoulder–elbow–wrist and hip–knee–ankle, not whichever hand or foot is rightmost.
- Separate pose, layout and alpha repairs; recheck the whole sequence and unchanged requirements.
- Retain holds and ambiguity rather than turning file checks into art approval.
- Use a small offline comparison player for timing, frame stepping and background checks.

The generation/crop utilities do not draw replacement poses, interpolate frames or automatically judge animation quality. Fixed frame counts, larger prompts and more process are not the objective.

## Validation and limits

Both skill frontmatters validate. The existing asset utility's five tests and the new review player's six tests pass. Browser checks exercised normal/slow playback, pause, stepping, looping and one-shot stopping. Source images, all selected stills and sampled player frames were inspected.

This is technical playback plus image/sequence review, not completed continuous human viewing, game-engine validation or user acceptance. No tested method established reliable commercial-quality animation. All original demos are preserved.

[Animation Mentor](https://www.animationmentor.com/blog/tutorial-animating-human-walk-cycle/) and [Adobe](https://www.adobe.com/creativecloud/animation/discover/principles-of-animation.html) supplied animation-principle references, not evidence of model success.
