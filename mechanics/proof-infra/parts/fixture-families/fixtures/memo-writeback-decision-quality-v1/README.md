# memo-writeback-decision-quality-v1

Shared fixture family for `aoa-memo-writeback-decision-quality`.

Use this family when the bounded question is whether one
`aoa-memo-writeback` application chose the right memory writeback route,
searched the relevant evidence, selected the correct decision outcome, and
disclosed missed-evidence and privacy risk before any candidate, export,
route-only debt, or no-writeback stop line is trusted.

Canonical case archetypes:

- `write_candidate` with a local memo port, owner-source refs, session refs,
  and bounded memory-worthy pressure
- `prepare_export` with explicit owner-review posture and no durable memory
  landing
- `no_writeback_needed` where generic progress is rejected after evidence
  review
- `route_only_debt` where the owner repo is route-only or has no valid local
  memo port
- `needs_owner_review` where owner, privacy, or evidence posture is plausible
  but too thin
- `blocked` where missing evidence, stale session refs, or public-safety risk
  prevents a decision

Family invariants:

- `aoa-memo-writeback` invocation fit stays reviewable
- owner repo and stronger owner route are named before memory-worthiness is
  judged
- `.aoa` refs, source refs, landed-work refs, memo recall or pending exports,
  and local memo port status are inspected when relevant or named as gaps
- generic progress, mood, broad summaries, and unresolved speculation do not
  become memory candidates
- the selected `memo_writeback_decision` matches the evidence and port posture
- missed-evidence risk remains explicit in the readout
- raw transcript content, secrets, and operator-sensitive details stay out of
  public packets

Replacement boundary:

- local repos may replace the concrete cases only if the replacement preserves
  the same writeback-decision-quality question and still exercises the route,
  search, outcome, missed-evidence, and privacy pressures above
- replacements must stay public-safe and must not depend on hidden runtime
  stores, private transcripts, or unreviewed durable memory landing
