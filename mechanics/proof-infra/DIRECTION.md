# Proof Infra Direction

Proof Infra in `aoa-evals` should keep reusable proof support contracts
available without becoming a junk drawer or a stronger source of bundle
meaning.

This file owns the current operating direction only. It does not replace the
entry card, part map, part contracts, source bundles, decisions, or provenance
bridge.

## Source-of-truth split

- `README.md`: package entry card and shortest shared-support route.
- `DIRECTION.md`: current operating direction.
- `PARTS.md`: active proof-infra part map.
- `parts/`: fixture-family and reportable-contract support.
- `PROVENANCE.md`: controlled bridge from active route to old root fixture, runner, scorer, and
  schema placement.
- `legacy/`: lineage only; not a support-file dump.
- `evals/`: source proof objects that apply shared contracts locally.

## Current contour

- Keep shared fixtures, runners, scorers, schemas, reports, and templates
  reusable but subordinate to bundle-local meaning.
- Keep generic fixture families here only when no narrower active mechanic
  owns the domain.
- Keep reportable contracts shared; keep interpretation in each bundle or
  report.

## Growth rule

Add proof-infra parts only when several proof objects share a support operation
and a narrower mechanic is not the owner. Do not move domain-specific payload
here for convenience.

## Stop-lines

- Do not treat fixture families, runner contracts, scorer helpers, or shared
  schemas as proof authority.
- Do not hide unclassified root payload under proof-infra.
- Do not make generated readers stronger than source bundles.

## Validation

Use the validation lane in [mechanics/proof-infra/AGENTS.md](AGENTS.md#validation).
