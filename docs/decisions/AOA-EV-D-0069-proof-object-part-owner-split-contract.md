# Proof-object Part Owner-split Contract

- Decision ID: AOA-EV-D-0069

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-21
- Surface classes: mechanic part
- Mechanic parents: proof-object
- Guard families: part and payload, sibling and boundary
- Posture: active rationale

## Context

`mechanics/proof-object/` is an evals-native parent for the operation around
source proof objects. Its active parts are support surfaces:

- `eval-authoring` owns the starter `EVAL.md` scaffold.
- `eval-contracts` owns schema-backed frontmatter and manifest validation.

Neither part is the source proof object. The source proof object remains
`evals/**/EVAL.md`, `evals/**/eval.yaml`, and bundle-local support artifacts.
Without explicit stronger-owner split, templates and schemas can accidentally
be read as doctrine, accepted proof meaning, bundle maturity, generated-reader
authority, or registry approval.

## Decision

Require both proof-object part README files to expose `## Stronger Owner Split`
and `## Stop-Lines`:

- `mechanics/proof-object/parts/eval-authoring/README.md`
- `mechanics/proof-object/parts/eval-contracts/README.md`

`eval-authoring` remains scaffold support. `eval-contracts` remains schema
validation support. Source proof bundle meaning stays under `evals/`, and
generated readers, reports, receipts, runtime candidates, sibling refs, quests,
and release surfaces stay weaker than bundle-local review.

## Consequences

- Future proof-object part edits must preserve the split between authoring
  support, schema validation support, and source bundle meaning.
- A template may shape a draft, but it must not become active proof meaning or
  doctrine.
- Schema acceptance may prove metadata shape, but it must not claim evidence
  acceptance, status maturity, publication, release readiness, or verdict truth.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
