# Boundary Bridge Phase Alpha Eval Matrix

- Decision ID: AOA-EV-D-0046
- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/`

## Index Metadata

- Original date: 2026-05-20
- Surface classes: generated/readout, boundary/runtime/sibling
- Mechanic parents: boundary-bridge
- Guard families: generated/report/receipt/runtime, sibling and boundary
- Posture: generated/readout rationale

## Context

The Phase Alpha eval matrix entered the refactor split across former root
districts:

- former root `examples/phase_alpha_eval_matrix.example.json`
- former root `schemas/phase-alpha-eval-matrix.schema.json`
- former root `scripts/generate_phase_alpha_eval_matrix.py`
- former root `generated/phase_alpha_eval_matrix.min.json`

Together those files form a real operation. They read the sibling-owned
`aoa-playbooks` Phase Alpha run matrix, check local eval-anchor mappings and
support refs, and emit a generated eval matrix used by validation,
release-support, and recurrence beacon checks.

The live operation is not generic audit, release, recurrence, or proof-object
work. Audit and checkpoint provide support refs. Release-support and recurrence
consume the check. `aoa-playbooks` owns the run truth. `aoa-evals` owns the
bridge that maps those runs to local proof anchors.

## Options Considered

- Leave the source plan, schema, builder, and generated matrix in root
  districts.
- Move the matrix into `audit` because some support refs are runtime evidence
  packets and artifact-to-verdict hooks.
- Move the matrix into `recurrence` because portable-proof beacons run the
  freshness check.
- Move the matrix into `boundary-bridge` as a part.

## Decision

Move the Phase Alpha eval matrix operation to:

`mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/`

The parent remains `boundary-bridge`. `phase-alpha-eval-matrix` is a part, not
a parent mechanic.

The moved part owns the local source plan, schema, builder, and generated
matrix. Root validation, release-support, and recurrence-beacon checks now call
the part-local builder.

## Rationale

This keeps topology convex. A future agent can see that the operation crosses a
sibling boundary into `aoa-playbooks`, but the eval-side mapping and generated
readout are local proof routing surfaces.

It also avoids creating a false `phase-alpha` parent or burying the bridge
inside audit or recurrence. The artifact shape is a matrix; the mechanic is
the boundary bridge.

## Consequences

- Positive: root `examples/`, `schemas/`, `scripts/`, and `generated/` lose one
  narrower bridge-owned operation.
- Positive: the matrix now has a part card with owner split, stop-lines, and
  validation.
- Tradeoff: validation commands become longer because the builder is
  part-local.
- Follow-up: if future playbook-to-eval bridges appear, place them under this
  part only when they share the Phase Alpha matrix operation; otherwise prove a
  separate bridge part.

## Boundaries

This decision does not make the generated matrix a verdict.

It does not make `aoa-playbooks` accept local eval interpretation.

It does not move audit selected evidence, checkpoint hook examples, source
proof bundles, release publication, or recurrence beacon ownership into this
part.

It does not authorize sibling repository edits.

## Validation

- `mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/README.md` names the
  part operation, owner split, stop-lines, and validation route.
- `scripts/validate_repo.py` validates the part-local schema, builder, and
  generated matrix.
- `python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py --check`
- `python scripts/validate_repo.py`
- `python scripts/validate_semantic_agents.py`
