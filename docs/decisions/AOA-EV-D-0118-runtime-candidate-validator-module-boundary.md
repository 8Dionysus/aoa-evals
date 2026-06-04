# Runtime Candidate Validator Module Boundary

- Decision ID: AOA-EV-D-0118
- Status: Accepted
- Date: 2026-06-03
- Owner surface: `scripts/validators/runtime_candidates.py`, `mechanics/audit/parts/candidate-readers/`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, generated/readout
- Mechanic parents: audit, checkpoint, cross-parent
- Guard families: generated/report/receipt/runtime, runtime-candidate/read-model
- Posture: active rationale

## Context

The runtime-candidate template index and intake reader are generated
read-models over candidate-reader builders, selected-evidence packet examples,
artifact-verdict hook examples, and the eval catalog.

They are useful because they make review posture explicit before a runtime
candidate can be treated as more than a candidate. They are dangerous if their
generated surface starts owning runtime acceptance, receipt publication, or
bundle verdict meaning.

## Options Considered

- Keep runtime-candidate reader checks inside `scripts/validate_repo.py`.
- Fold them into receipt or audit-report validators because they mention
  runtime evidence.
- Move them into `scripts/validators/runtime_candidates.py` and keep
  `scripts/validate_repo.py` as the compatibility entrypoint.

## Decision

Runtime-candidate reader validation lives in
`scripts/validators/runtime_candidates.py`.

`scripts/validate_repo.py` keeps compatibility wrappers for
`load_runtime_candidate_template_index_builder`,
`validate_runtime_candidate_template_index`,
`load_runtime_candidate_intake_builder`, and
`validate_runtime_candidate_intake`.

Receipt validators, audit reports, and runtime-evidence selection examples stay
in their existing owner surfaces. The new module checks candidate-reader parity
and review posture only.

## Rationale

This split names a coherent generated/projection boundary without turning
runtime-candidate readers into runtime policy or acceptance authority.

Candidate readers derive from part-local builders and examples. They should
fail when generated payloads drift, when eval anchors no longer resolve, or
when review posture stops matching the source examples. They should not decide
whether an agent run is allowed, accepted, rolled back, or published.

## Consequences

- Positive: another generated/read-model contract leaves the root validator.
- Positive: candidate-reader authority limits are explicit in inventory and
  decision history.
- Tradeoff: path constants and wrappers remain in `scripts/validate_repo.py` for
  existing tests and callers.
- Follow-up: extract receipt/audit-report validators only as their own owner
  surfaces, not as a combined runtime bucket.

## Current Applicability

As of 2026-06-03:

- Still valid: `scripts/validate_repo.py` remains the repo-wide validation
  entrypoint.
- Changed: runtime-candidate generated reader checks now have a focused
  validator module.
- Superseded by: none.

## Boundaries

This decision does not change runtime policy, receipt publication, artifact
verdict authority, bundle-local proof meaning, or human review requirements.

It does not create a new release command. Lane command authority remains in
`docs/validation/validation_lanes.json`.

## Validation

- `python -m pytest -q tests/test_quest_and_reader_surfaces.py -k runtime_candidate`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_test_topology.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/validate_repo.py`
