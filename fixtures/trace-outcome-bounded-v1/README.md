# trace-outcome-bounded-v1

Shared fixture family for `aoa-trace-outcome-separation`.

Use this family when the bounded question is whether final outcome and
execution-path quality can be judged separately before any combined reading.

Canonical case archetypes:
- strong outcome and weak path case
- weak outcome and strong path case
- strong outcome and strong path case
- weak outcome and weak path case
- materially divergent mixed case where both surfaces remain reviewable

Family invariants:
- both outcome evidence and path evidence are visible to a bounded outside reviewer
- outcome and path remain distinct notes before any combined reading
- polished outcome does not erase weak path evidence
- disciplined path does not rescue weak outcome evidence
- the public readout stays weaker than the separate outcome and path evidence

Replacement boundary:
- local repos may replace the concrete cases only if they preserve the same
  outcome-vs-path split question and still exercise all five bounded split
  pressures above
- replacements must stay public-safe and must not depend on one hidden ideal
  trace or hidden reviewer-only outcome standards
