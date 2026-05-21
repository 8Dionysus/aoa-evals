# tool-trajectory-bounded-v1

Shared fixture family for `aoa-tool-trajectory-discipline`.

Use this family when the bounded question is whether tool use stayed
disciplined, proportionate, and reviewable on tasks where the tool path itself
materially matters.

Canonical case archetypes:
- sequencing-matters case
- avoidable-churn case
- skipped-obvious-tool-check case
- disciplined-versus-noisy same-outcome case
- tool-misuse-hides-risk case

Family invariants:
- the reason tool path matters is visible before the trajectory is judged
- tool evidence is inspectable by a bounded outside reviewer
- avoidable churn and obvious omissions stay visible as separate path failures
- the review does not require one hidden ideal sequence
- the public readout stays weaker than the visible tool-path evidence

Replacement boundary:
- local repos may replace the concrete cases only if they preserve the same
  path-sensitive tool-discipline question and still exercise all five bounded
  pressures above
- replacements must stay public-safe and must not depend on hidden runtime-only
  telemetry or one hard-coded perfect tool sequence
