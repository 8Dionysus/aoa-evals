# long-horizon-restart-v1

Shared fixture family for `aoa-long-horizon-depth`.

Use this family when the bounded question is whether a checkpoint-based
long-horizon inquiry route can relaunch with its axis, contradictions, and
delta boundaries still reviewably intact.

Canonical case archetypes:
- complete checkpoint with stable relaunch case
- open-contradiction-preserved relaunch case
- explicit `memory_delta` versus `canon_delta` separation case
- summary-theater pressure case where a weak checkpoint looks cleaner than it is
- hidden-raw-history pressure case where relaunch would fail without bounded pack fidelity

Family invariants:
- a real `inquiry_checkpoint` remains inspectable per case
- the active axis, open questions, and next tests are visible before relaunch is judged
- contradictions stay visible as contradictions rather than being cleaned away for smoothness
- `memory_delta` and `canon_delta` remain distinct review objects when both are present
- the public readout stays weaker than the visible checkpoint and relaunch evidence

Replacement boundary:
- local repos may replace the concrete cases only if they preserve the same
  checkpoint-and-relaunch fidelity question and still exercise all five bounded
  pressures above
- replacements must stay public-safe and must not depend on hidden transcript
  continuity or final-answer grading masquerading as restart fidelity
