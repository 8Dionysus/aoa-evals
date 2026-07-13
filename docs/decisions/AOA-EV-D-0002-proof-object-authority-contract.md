# Proof Object Authority Contract

- Decision ID: AOA-EV-D-0002
- Status: Accepted
- Date: 2026-05-19
- Owner surface: proof bundle and shared proof-contract surfaces

## Index Metadata

- Original date: 2026-05-19
- Surface classes: proof topology
- Mechanic parents: proof-object
- Guard families: none
- Posture: active rationale

## Context

The repository contains generated catalogs, runtime-candidate readers, receipts,
reports, examples, schemas, quests, and sibling references. These surfaces are
useful, but the refactor plan needs a stable local rule for what owns a bounded
proof claim.

The existing architecture already says an eval bundle packages a bounded claim,
object under evaluation, fixture or case surface, scoring or verdict logic,
execution guidance, baseline or comparison mode, report expectations, and blind
spots. The root design spine turns that into the organizing authority contract.

## Options Considered

- Treat generated catalogs as the main proof map because they are compact.
- Treat reports or receipts as proof authority because they record outcomes.
- Treat the source proof object as the authority and keep derived or emitted
  surfaces subordinate.

## Decision

`aoa-evals` treats the proof object as the source authority for a bounded eval
claim.

For an existing bundle, that proof object is primarily `evals/**/EVAL.md` plus
`evals/**/eval.yaml`, supported by bundle-local notes, fixtures, runners,
schemas, reports, and examples when present.

Generated readers, runtime candidates, machine evidence, sibling references,
and receipts may route, summarize, or carry evidence. They do not accept a
verdict without bundle-local review.

## Rationale

This keeps the proof layer self-contained and honest. It lets generated and
runtime-facing surfaces become useful without becoming stronger than the
authored claim, evidence boundary, verdict logic, and blind spots they describe.

## Consequences

- Positive: future mechanics and validators can ask which proof object a
  candidate, report, receipt, or generated entry belongs to.
- Tradeoff: some convenience surfaces must remain visibly weaker even when they
  are easier for agents to consume.
- Follow-up: later validators should check candidate-only posture,
  generated-source derivation, receipt subordination, and proof-object
  completeness more directly.

## Boundaries

This decision does not freeze the current bundle schema forever.

It does not prevent future proof-object drafts outside `evals/` during
mechanics work, but those drafts must name their authority and promotion route
before being read as accepted eval bundles.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.

## Current Applicability

As of 2026-05-24:

- Still valid: the source proof object owns bounded claim meaning, evidence
  boundary, scoring or verdict logic, and blind spots.
- Clarified: `docs/guides/SCORE_SEMANTICS_GUIDE.md` now expresses score semantics as
  positive interpretation-route criteria: distinct axes, one bounded claim part
  per axis, stable comparison semantics, explicit interpretation bounds, and a
  return route to evidence when a score obscures the claim.
- Clarified: `docs/guides/EVAL_REVIEW_GUIDE.md` now expresses maturity deferral as
  concrete gap routes: explicit review evidence, default-use rationale,
  interpretation bounds, bundle-shaped blind spots, and weaker claim language.
- Clarified: `docs/guides/BLIND_SPOT_DISCLOSURE_GUIDE.md` now expresses blind-spot
  disclosure as concrete review gap routes: unsupported claims, false-pass or
  false-fail paths, local-shape assumptions, nearby-bundle routes, and
  bundle-shaped specificity.
- Clarified: core proof guides now express relation, baseline comparison,
  artifact/process, fixture, repeated-window, and philosophy routes through
  direct evidence, claim scope, uncertainty, status-bounded interpretation, and
  owner review criteria.
- Source surfaces updated: `docs/guides/SCORE_SEMANTICS_GUIDE.md`,
  `docs/guides/EVAL_REVIEW_GUIDE.md`, `docs/guides/BLIND_SPOT_DISCLOSURE_GUIDE.md`,
  `docs/guides/EVAL_RUBRIC.md`, `docs/guides/BASELINE_COMPARISON_GUIDE.md`,
  `docs/guides/EVAL_PHILOSOPHY.md`,
  `docs/guides/ARTIFACT_PROCESS_SEPARATION_GUIDE.md`,
  `docs/guides/FIXTURE_SURFACE_GUIDE.md`,
  `docs/guides/REPEATED_WINDOW_DISCIPLINE_GUIDE.md`, `scripts/validate_repo.py`, and
  `tests/test_validate_repo.py`.
- Validation route: use the focused proof-guide checks and repository lane
  owned by command authority and the nearest `AGENTS.md`.

## Review Log

### 2026-05-24 - Score semantics route language clarified

- Previous assumption: score guidance could rely on warning phrasing around
  axis overlap, whole-claim pressure, comparative validity, and caution notes.
- New reality: low-context agents need result interpretation to name the route
  criteria directly before a scalar, comparative, or mixed result can be read.
- Reason: scoring guidance is proof-object authority support; it should preserve
  claim limits by naming evidence, comparison, and interpretation routes.
- Source surfaces updated: score semantics guide, root validator, and focused
  validator tests.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

### 2026-05-24 - Eval review route language clarified

- Previous assumption: maturity review guidance could rely on broad defer
  warnings around default-use rationale, broad wish lists, theater risk, and
  hidden reviewer intuition.
- New reality: low-context agents need maturity review to name the exact gap
  route: review evidence, default-use rationale, interpretation bounds,
  bundle-shaped blind spots, unstable meaning, or weaker claim language.
- Reason: review guidance supports proof-object authority by deciding when a
  source bundle is ready for bounded, baseline, or canonical public reading.
- Source surfaces updated: eval review guide, root validator, and focused
  validator tests.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

### 2026-05-24 - Blind-spot disclosure routes clarified

- Previous assumption: blind-spot guidance could describe weak disclosure and
  review blocking cases through broad warning language.
- New reality: low-context agents need disclosure gaps to route directly to
  unsupported claims, false-pass or false-fail paths, local-shape assumptions,
  nearby-bundle routes, and bundle-shaped specificity.
- Reason: blind spots are part of proof-object honesty; review should defer by
  naming the missing disclosure route, not by leaving generic caution prose.
- Source surfaces updated: blind-spot disclosure guide, root validator, and
  focused validator tests.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

### 2026-05-24 - Proof guide route phrasing aligned

- Previous assumption: central proof guides could rely on shorthand contrast
  phrasing around relation semantics, portability, comparison drift, noisy
  variation, artifact/process grouping, fixture scope, repeated windows, and
  proof philosophy.
- New reality: low-context agents need those guides to name the route criteria
  directly: direct dependency separation, status-bounded portability,
  comparison disclosure, uncertainty preservation, explicit evidence, claim
  scope, distinct artifact/process readings, and owner-routed growth claims.
- Reason: these guides support proof-object authority without adding new
  validator law to a wording-only route clarification.
- Source surfaces updated: eval rubric, baseline comparison guide, eval
  philosophy, artifact/process separation guide, fixture surface guide, and
  repeated-window discipline guide.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.
