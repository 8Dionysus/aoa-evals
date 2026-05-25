# Proof Infra Direction

Proof Infra in `aoa-evals` routes reusable proof support contracts so shared
fixtures, runners, scorers, schemas, reports, and templates stay available as
support while source bundles keep proof meaning.

Use this file for the package's current operating direction: read it after the
parent entry card and before `PARTS.md`, part contracts, source bundles,
decision records, and `PROVENANCE.md`.

## Source-of-truth split

- `README.md`: package entry card and shortest shared-support route.
- `DIRECTION.md`: current operating direction.
- `PARTS.md`: active proof-infra part map.
- `parts/`: fixture-family and reportable-contract support.
- `PROVENANCE.md`: controlled bridge from active route to old root fixture, runner, scorer, and
  schema placement.
- `legacy/`: archive-local route for old root fixture, runner, scorer, and
  schema placement after `PROVENANCE.md`.
- `evals/`: source proof objects that apply shared contracts locally.

## Current contour

- Keep shared fixtures, runners, scorers, schemas, reports, and templates
  reusable but subordinate to bundle-local meaning.
- Keep generic fixture families here when proof-infra is the narrowest active
  owner for the support operation.
- Keep reportable contracts shared; keep interpretation in each bundle or
  report.

## Growth rule

Add proof-infra parts only when several proof objects share a support operation
and proof-infra is the narrowest active owner. Domain-specific payload routes
to the owning mechanic instead of convenience placement.

## Stop-lines

| Pressure | Route |
| --- | --- |
| fixture families, runner contracts, scorer helpers, or shared schemas read as proof authority | bundle-local `EVAL.md`, `eval.yaml`, and reviewed report route |
| unclassified root payload wants a parking place | `mechanics/EVIDENCE_CLUSTERS.md`, `docs/architecture/PROOF_TOPOLOGY.md`, or the owning mechanic part |
| generated reader looks stronger than source bundle meaning | source bundle, source contract, builder, and generated check |
| domain-specific support appears in shared infrastructure | narrower active mechanic that owns the operation |

## Validation

Use the validation lane in [mechanics/proof-infra/AGENTS.md](AGENTS.md#validation).
