# Runtime Audit Validator Module Boundary

- Decision ID: AOA-EV-D-0131
- Status: Accepted
- Date: 2026-06-03
- Historical owner surface: `scripts/validators/runtime_audit.py`, `mechanics/audit/`
- Refined by: AOA-EV-D-0174, AOA-EV-D-0203

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, runtime-policy, audit/observability
- Mechanic parents: audit, proof-loop, proof-object, cross-parent
- Guard families: runtime-policy, source/topology, trace/eval
- Posture: active rationale

## Context

After root compatibility aliases were removed, runtime audit checks still lived
in `scripts/validate_repo.py`.

That area checked one coherent runtime-policy boundary:

- artifact-to-verdict trace bridge schemas and examples;
- selected runtime evidence packet schemas and examples;
- the integrity-review guide, schema, example payload, candidate-only posture,
  no-authority language, replay requirements, repo-qualified evidence refs, and
  weakened-schema rejections.

The root file also carried repo-ref resolver functions used by other checks, so
moving this behavior by copying resolver logic would have created another
historical script pile.

## Decision

Runtime audit trace/eval and selected-evidence validation lives in
`scripts/validators/runtime_audit.py`.

`scripts/validate_repo.py` delegates to
`validate_trace_eval_bridge_surfaces`,
`validate_runtime_evidence_selection_surfaces`, and
`validate_runtime_integrity_review_surface`.

As of the 2026-06-04 follow-up split,
`validate_runtime_integrity_review_surface` is a compatibility adapter that
delegates to `scripts/validators/runtime_integrity_review.py`.

It supplies a `RuntimeAuditContext` containing the root-owned repo-ref,
named-surface, abyss-stack-ref, strict sibling compatibility, and live root
resolver context.

Shared issue, JSON, schema, and mapping helpers live in
`scripts/validators/common.py`. That helper owns no mechanic meaning and exists
only to keep focused validators from duplicating low-level parsing and issue
formatting behavior.

## Rationale

Runtime audit is not the same as audit route topology. The audit parent routes
candidate evidence, while the runtime audit validator checks whether trace
bridge, selected-evidence, and integrity-review artifacts preserve boundaries
around authority, replay, cross-repo refs, abyss-stack evidence refs, and
candidate-only posture before any stronger runtime or bundle owner accepts
them.

Keeping those checks inside `scripts/validate_repo.py` left runtime-policy
knowledge in the root entrypoint after audit route checks already moved to a
focused module. Moving them into `runtime_audit.py` keeps the runtime-policy
boundary explicit without duplicating root resolver authority.

## Consequences

- Positive: trace bridge, runtime evidence selection, and runtime integrity
  review behavior moved out of `scripts/validate_repo.py`.
- Positive: `scripts/validate_repo.py` keeps orchestration and resolver context
  but no longer owns runtime-audit constants or schema semantics.
- Positive: focused validators can share low-level JSON and schema helpers
  without creating another broad validator.
- Follow-up: the remaining readout-domain generated checks can move later only
  when their projection owners are equally clear.

## Review Log

### 2026-06-04 - Runtime integrity review split

- Previous assumption: `runtime_audit.py` owned trace/eval bridge validation,
  selected-evidence packet validation, and the candidate-only runtime integrity
  review guide/schema/example contract.
- New reality: candidate-only runtime integrity review checks live in
  `scripts/validators/runtime_integrity_review.py`; `runtime_audit.py` keeps
  compatibility aliases and delegates the public function.
- Reason: integrity review is a bounded no-authority contract under
  `mechanics/audit/parts/integrity-review`, while trace bridge and
  selected-evidence packet validation are runtime-audit routing surfaces.
- Source surfaces updated: `scripts/validators/runtime_audit.py`,
  `scripts/validators/runtime_integrity_review.py`, validation inventories, and
  mechanics residual classification.
- Validation: see AOA-EV-D-0174.

## Current Applicability

As of 2026-06-04:

- Still valid: `scripts/validate_repo.py` remains the repo-wide command
  entrypoint and owns live repo-ref resolver context.
- Changed: trace/eval bridge and selected-evidence validation live in
  `scripts/validators/runtime_audit.py`; candidate-only runtime integrity
  review contract checks live in `scripts/validators/runtime_integrity_review.py`.
- Further changed on 2026-06-04: AOA-EV-D-0203 removes
  `scripts/validators/runtime_audit.py`; active runtime audit validation is
  split across trace/eval bridge, selected-evidence, integrity-review, and
  helper modules.
- Superseded by: AOA-EV-D-0203 for the aggregate module shape.

## Boundaries

This decision does not accept runtime activation, runtime evidence, or selected
evidence as proof canon.

It does not make `runtime_audit.py` the owner of the integrity-review guide,
schema, example payload, replay requirements, no-authority claims, or
activation routing posture.

It does not let `scripts/validators/common.py` define source, audit, runtime,
generated, or release meaning.

## Validation

- `python -m py_compile scripts/validators/runtime_audit_common.py scripts/validators/runtime_trace_eval_bridge.py scripts/validators/runtime_evidence_selection.py scripts/validators/runtime_integrity_review.py scripts/validators/evidence_readouts.py tests/test_runtime_evidence_surfaces.py`
- `python -m pytest -q tests/test_runtime_evidence_surfaces.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_test_topology.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/validate_repo.py`
- `python scripts/ci_gate.py --mode source-fast`
- `python -m pytest -q`
- `python scripts/release_check.py`
