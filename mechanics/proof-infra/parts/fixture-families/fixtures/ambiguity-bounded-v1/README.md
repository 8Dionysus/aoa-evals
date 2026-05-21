# ambiguity-bounded-v1

Shared fixture family for `aoa-ambiguity-handling`.

Use this family when the bounded question is whether incomplete, conflicting,
or underspecified task meaning was handled through clarification, branching, or
bounded disclosed assumptions instead of one silent unearned interpretation.

Canonical case archetypes:
- incomplete requirements with multiple reasonable implementations
- conflicting instructions that force a question or explicit branch
- underspecified acceptance criteria
- narrow fallback-assumption case with explicit disclosure
- silent path-choice case where one interpretation would materially change the work surface

Family invariants:
- the ambiguity is visible to a bounded outside reviewer
- permission or authority uncertainty stays separate from task-meaning ambiguity
- clarification, branching, and bounded assumptions remain distinguishable handling moves
- assumptions stay narrower than the visible task can support
- the public readout stays weaker than the ambiguity-bearing evidence

Replacement boundary:
- local repos may replace the concrete cases only if they preserve the same
  task-meaning ambiguity question and still exercise all five bounded ambiguity
  pressures above
- replacements must stay public-safe and must not depend on hidden reviewer-only
  context or house-style answers to determine the correct interpretation
