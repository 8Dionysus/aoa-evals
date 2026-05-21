# compost-provenance-v1

Shared fixture family for `aoa-compost-provenance-preservation`.

Use this family when the bounded question is whether a witness-derived note,
synthesis, or principle candidate preserved provenance and review posture while
becoming cleaner than the upstream witness-facing input.

Canonical case archetypes:
- witness-to-note case
- note-to-principle-candidate case with visible refs
- provisional-review-state case
- contradiction, staleness, or demotion preserved case
- canon-pressure holdback case

Family invariants:
- source refs remain visible and specific enough to trace back to the witness-facing input
- review state remains explicit rather than implied by polish
- current limits stay visible as the artifact becomes cleaner
- promotion toward principle or canon remains bounded and review-gated
- contradiction, staleness, or demotion posture remains possible

Replacement boundary:
- local repos may replace the concrete cases only if they preserve the same
  provenance-preserving compost question and still exercise all five bounded
  provenance pressures above
- replacements must stay public-safe and must not depend on hidden private
  references or canon claims that outrun the visible evidence
