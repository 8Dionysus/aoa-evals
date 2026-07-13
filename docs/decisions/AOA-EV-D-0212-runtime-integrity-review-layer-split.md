# Runtime Integrity Review Layer Split

- Decision ID: AOA-EV-D-0212
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused runtime integrity review docs, schema, and example validators

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, runtime-policy, audit/observability
- Mechanic parents: audit, cross-parent
- Guard families: runtime-policy, trace/eval, source/topology
- Posture: active rationale

## Context

AOA-EV-D-0174 moved candidate-only runtime integrity review checks out of
`runtime_audit.py` into `scripts/validators/runtime_integrity_review.py`.

That file stayed focused on one part, but it still mixed three different
contract layers:

- guide and Agon landing-note wording;
- runtime integrity review JSON Schema closure and exact no-authority fields;
  and
- example payload schema conformance, budget-ref resolution, evidence-ref
  resolution, replay posture, and forbidden claims.

Those layers protect the same runtime-policy boundary, but they fail through
different repair routes.

## Options Considered

- Keep `runtime_integrity_review.py` as one part-local validator.
- Keep `runtime_integrity_review.py` as a delegating compatibility facade.
- Remove the aggregate and let `evidence_readouts.py` orchestrate focused
  runtime integrity review validators directly.

## Decision

`scripts/validators/runtime_integrity_review.py` is removed.

Active runtime integrity review validation now routes through:

- `runtime_integrity_review_docs.py` for guide tokens, docs-map presence, and
  Agon landing-note posture.
- `runtime_integrity_review_schema.py` for schema title, closure, required
  fields, replay keys, evidence-ref shape, forbidden claims, notes, and
  no-authority constants.
- `runtime_integrity_review_example.py` for schema conformance, budget-ref
  resolution, repo-qualified evidence refs, replay requirements,
  `human_review_needed`, forbidden claims, and notes.
- `runtime_integrity_review_common.py` for helper-only constants.

`evidence_readouts.py` validates docs, validates schema once, then passes the
schema validator into the example validator.

## Rationale

Runtime integrity review is a candidate-only contract. Its schema cannot become
runtime activation authority, and its example cannot become proof-canon truth.
Splitting the validator keeps each layer weaker than the stronger owner it
references: docs describe the posture, schema closes the allowed shape, and the
example proves bounded replay/reference routing.

This also prevents one long runtime-policy file from becoming a quiet bucket for
future runtime, proof-canon, or cross-repo authority checks.

## Consequences

- Positive: guide, schema, and example failures route to the exact contract
  layer that owns the drift.
- Positive: schema validation is performed once in repo-wide readout
  orchestration and reused by the example validator.
- Positive: `runtime_integrity_review_common.py` is helper-only and cannot
  become a hidden aggregate.
- Tradeoff: tests and readout orchestration import more focused modules.

## Current Applicability

As of 2026-06-04:

- Still valid: runtime integrity review remains `candidate_only` and
  `human_review_needed`; it does not accept runtime activation or proof canon.
- Changed: the broad `runtime_integrity_review.py` module no longer exists.
- Supersedes: AOA-EV-D-0174 for aggregate runtime integrity review validator
  shape.

## Boundaries

This decision does not accept runtime activation, owner override, canon write,
sealed verdict authority, proof-canon promotion, receipt publication, or
sibling-owner approval.

It also does not move trace/eval bridge, selected-evidence packet promotion,
generated candidate readers, or source eval meaning into runtime integrity
review.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
