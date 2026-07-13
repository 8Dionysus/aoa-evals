# Comparison Spine Report Parts

- Decision ID: AOA-EV-D-0029
- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/comparison-spine/parts/`

## Index Metadata

- Original date: 2026-05-20
- Surface classes: mechanic part, report/release/receipt
- Mechanic parents: comparison-spine
- Guard families: part and payload, generated/report/receipt/runtime
- Posture: report/release/receipt rationale

## Context

Decision `0011` created `mechanics/comparison-spine/` as the route for
fixed-baseline, peer-compare, and longitudinal-window proof claims, but it left
the shared comparison dossiers in root `reports/`.

That was useful for the first package route. It is now too weak for the
mechanics refactor because the dossiers are not generic root reports anymore:
they are source readout surfaces for the comparison-spine operation and are
already cited by bundle `paired_readout_path` fields, generated
`proof_artifacts`, tests, and validators.

## Options Considered

- Keep all shared dossiers in root `reports/` because they are public reports.
- Move every report under `mechanics/` at once.
- Move only comparison-spine-owned shared dossiers into comparison-spine parts,
  leaving proof-loop and bundle-local reports in their current owner surfaces.

## Decision

Move comparison-spine-owned shared dossiers into package-local parts:

- `spine-overview`
- `fixed-baseline`
- `peer-compare`
- `longitudinal-window`

Bundle source truth stays in `evals/**/EVAL.md` and `evals/**/eval.yaml`.
The generated `proof_artifacts` and comparison readers stay derived from source
bundle metadata and runner contracts.

## Rationale

This makes the topology more convex: a future agent can see that fixed-baseline,
peer-compare, and longitudinal-window readout surfaces belong to the comparison
operation, not to a generic report pile.

The move also avoids pretending that every `reports/` file has the same owner.
Proof-loop smoke remains a proof-loop concern, release-support reports stay under
`mechanics/release-support/parts/`, receipt dry review stays under
`mechanics/publication-receipts/parts/`, and comparison dossiers now live under
the comparison mechanic.

## Boundaries

This decision does not move comparison bundles, bundle-local report schemas,
generated readers, or root release reports.

Comparison-spine fixture family movement is governed separately by
`docs/decisions/AOA-EV-D-0040-comparison-spine-fixture-parts.md`.

It does not make a shared dossier stronger than the source proof object, and it
does not turn `generated/comparison_spine.json` into source truth.

It does not turn fixed-baseline, peer-compare, or longitudinal-window results
into broad capability growth, repo-global scoring, runtime health, or sibling
owner acceptance.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
