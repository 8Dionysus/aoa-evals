# Audit Direction

Audit in `aoa-evals` should let runtime, trace, machine, and stack artifacts
enter as public-safe candidate evidence without turning audit into a hidden
judge or runtime owner.

Use this file for the package's current operating direction: read it after the
parent entry card and before `PARTS.md`, part contracts, source bundles,
decision records, and `PROVENANCE.md`.

## Source-of-truth split

- `README.md`: package entry card and shortest candidate-evidence route.
- `DIRECTION.md`: current operating direction.
- `PARTS.md`: active audit part map.
- `parts/`: selected-evidence packets, artifact-verdict hooks, candidate
  readers, and integrity-review support.
- `PROVENANCE.md`: controlled bridge from active route to old runtime-evidence placement.
- `legacy/`: lineage only; not an evidence dump.
- `evals/`: source proof objects that decide whether candidate evidence is
  accepted.

## Current contour

- Keep candidate evidence public-safe, schema-backed, and below bundle-local
  review.
- Keep generated candidate readers derived from selected packet examples and
  schemas, not from private runtime truth.
- Keep artifact-to-verdict hooks as bridge shape, not live judging.
- Keep runtime owner truth in `abyss-stack`, machine owners, or sibling repos.

## Growth rule

Add audit parts only when a repeated intake or review operation has a clear
candidate-evidence contract and validation. Do not create new audit surfaces
just to store raw logs, private traces, or broad benchmark claims.

## Stop-lines

- Do not treat selected evidence as proof acceptance.
- Do not ingest secrets, raw private logs, or host fingerprints.
- Do not let generated candidate readers outrank source packets.
- Do not turn audit into release support, receipt publication, or runtime
  monitoring.

## Validation

Use the validation lane in [mechanics/audit/AGENTS.md](AGENTS.md#validation).
