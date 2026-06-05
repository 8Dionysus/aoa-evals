# Phase Alpha Matrix Validator Module Boundary

- Decision ID: AOA-EV-D-0119
- Status: Accepted
- Date: 2026-06-03
- Owner surface: focused Phase Alpha matrix validators and `mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/`
- Refined by: AOA-EV-D-0207

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, generated/readout, boundary/runtime/sibling
- Mechanic parents: boundary-bridge, cross-parent
- Guard families: generated/report/receipt/runtime, sibling and boundary
- Posture: active rationale

## Context

AOA-EV-D-0046 moved the Phase Alpha eval matrix into the
`boundary-bridge/phase-alpha-eval-matrix` part. The remaining validator body
still lived inside `scripts/validate_repo.py`.

That body checked a coherent boundary: local generated matrix parity, the
part-local schema, runtime-lane posture, support refs, and strict sibling
compatibility against `aoa-playbooks` when the strict sibling gate is enabled.

## Options Considered

- Keep the Phase Alpha matrix validator body inside `scripts/validate_repo.py`.
- Fold it into generic generated parity because the matrix is generated.
- Move it into `scripts/validators/phase_alpha_matrix.py` while keeping
  `scripts/validate_repo.py` as the compatibility entrypoint.

## Decision

Phase Alpha eval matrix validation lives in
`scripts/validators/phase_alpha_matrix.py`.

`scripts/validate_repo.py` keeps compatibility aliases for the matrix paths and
wrappers for `load_phase_alpha_eval_matrix_builder` and
`validate_phase_alpha_eval_matrix`.

The part-local builder remains the projection builder. The new validator module
checks generated parity and sibling-boundary integrity; it does not own
`aoa-playbooks` run truth.

## Rationale

The Phase Alpha matrix is a boundary-bridge read-model, not a release receipt,
not a runtime acceptance record, and not a source proof verdict.

Naming the validator module lets the root validator keep orchestration while
the boundary logic lives beside other focused validator organs. It also keeps
strict sibling compatibility visible as a sibling-boundary concern instead of a
generic generated freshness rule.

## Consequences

- Positive: another generated/sibling read-model leaves the root validator.
- Positive: Phase Alpha matrix authority limits are explicit in inventory and
  decision history.
- Tradeoff: compatibility wrappers remain because tests and callers still route
  through `scripts/validate_repo.py`.
- Follow-up: receipt/publication validators should be extracted only as their
  own owner surface, not mixed with Phase Alpha matrix validation.

## Current Applicability

As of 2026-06-03:

- Still valid: `scripts/validate_repo.py` remains the repo-wide validation
  entrypoint.
- Changed: Phase Alpha matrix validation now has a focused validator module.
- As of AOA-EV-D-0207: `scripts/validators/phase_alpha_matrix.py` is removed;
  local generated projection checks live in `phase_alpha_matrix_projection.py`,
  strict sibling compatibility lives in `phase_alpha_matrix_sibling_compat.py`,
  and shared JSON/schema/repo-ref/builder helpers live in
  `phase_alpha_matrix_common.py`.
- Superseded by: AOA-EV-D-0207 for aggregate module shape.

## Boundaries

This decision does not change `aoa-playbooks` authority over Phase Alpha run
truth, reviewed-run refs, or scenario composition.

It does not make the generated matrix a verdict, acceptance record, receipt, or
runtime policy decision.

It does not authorize sibling repository edits.

## Validation

- `python -m py_compile scripts/validators/phase_alpha_matrix_common.py scripts/validators/phase_alpha_matrix_projection.py scripts/validators/phase_alpha_matrix_sibling_compat.py scripts/validators/evidence_readouts.py tests/test_downstream_feed_contracts.py`
- `python -m pytest -q tests/test_downstream_feed_contracts.py -k phase_alpha`
- `python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py --check`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_test_topology.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/validate_repo.py`
