# Report Index Validator Module Boundary

- Decision ID: AOA-EV-D-0117
- Status: Accepted
- Date: 2026-06-03
- Owner surface: `scripts/validators/report_index.py`, `scripts/generate_eval_report_index.py`, `generated/eval_report_index.min.json`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, generated/readout
- Mechanic parents: proof-infra, proof-loop, cross-parent
- Guard families: generated/report/receipt/runtime, decision index/read-model
- Posture: active rationale

## Context

`scripts/validate_repo.py` still carried generated report-index validation
inside the root validator after lane command authority and questbook validation
were split into named surfaces.

The report index is a coherent generated/read-model boundary: it compares
`generated/eval_report_index.min.json` against
`scripts/generate_eval_report_index.py`, checks bundle-local report references,
and protects the rule that report readers are not receipts, runtime acceptance,
or verdict authority.

## Options Considered

- Keep report-index checks inside `scripts/validate_repo.py` until all generated
  readers move together.
- Fold report-index validation into `scripts/validators/generated_parity.py`.
- Move report-index payload and route checks into
  `scripts/validators/report_index.py` while keeping `scripts/validate_repo.py`
  as the compatibility entrypoint.

## Decision

Report-index validation lives in `scripts/validators/report_index.py`.

`scripts/validate_repo.py` keeps compatibility wrappers for
`load_eval_report_index_builder`, `validate_eval_report_index`, and
`validate_eval_report_index_route_surfaces`.

The generated report index remains builder-backed. Its authority is parity and
routeability only; bundle reports and source eval bundles keep proof meaning.

## Rationale

This split names the generated/read-model boundary without weakening the release
gate. It also avoids turning the broader generated-parity module into a private
home for every specialized generated reader contract.

The wrapper route preserves existing tests and callers while allowing future
work to import the focused module directly.

## Consequences

- Positive: one more coherent generated/read-model contract moved out of the
  root validator.
- Positive: report-index authority limits are isolated and easier to review.
- Tradeoff: compatibility wrappers remain until callers stop importing through
  `validate_repo.py`.
- Follow-up: continue with runtime-candidate readers or receipt/audit report
  validators as separate owner surfaces, not as one broad readout bucket.

## Current Applicability

As of 2026-06-03:

- Still valid: `scripts/validate_repo.py` remains the repo-wide validation
  entrypoint.
- Changed: generated report-index validation now has a focused validator module.
- Superseded by: none.

## Boundaries

This decision does not promote generated report indexes into source truth,
receipt publication, runtime acceptance, or verdict authority.

It does not change the release lane command sequence. Command authority remains
in `docs/validation/validation_lanes.json`.

## Validation

- `python -m pytest -q tests/test_quest_and_reader_surfaces.py -k eval_report_index`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/validate_repo.py`
