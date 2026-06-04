# Runtime Audit Validator Module Boundary

- Decision ID: AOA-EV-D-0131
- Status: Accepted
- Date: 2026-06-03
- Owner surface: `scripts/validators/runtime_audit.py`, `mechanics/audit/`

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

Runtime audit validation lives in `scripts/validators/runtime_audit.py`.

`scripts/validate_repo.py` delegates to
`validate_trace_eval_bridge_surfaces`,
`validate_runtime_evidence_selection_surfaces`, and
`validate_runtime_integrity_review_surface`.

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
  review behavior have one focused validator owner.
- Positive: `scripts/validate_repo.py` keeps orchestration and resolver context
  but no longer owns runtime-audit constants or schema semantics.
- Positive: focused validators can share low-level JSON and schema helpers
  without creating another broad validator.
- Follow-up: the remaining readout-domain generated checks can move later only
  when their projection owners are equally clear.

## Current Applicability

As of 2026-06-03:

- Still valid: `scripts/validate_repo.py` remains the repo-wide command
  entrypoint and owns live repo-ref resolver context.
- Changed: runtime audit validation now lives in
  `scripts/validators/runtime_audit.py`.
- Superseded by: none.

## Boundaries

This decision does not accept runtime activation, runtime evidence, or selected
evidence as proof canon.

It does not let `scripts/validators/common.py` define source, audit, runtime,
generated, or release meaning.

## Validation

- `python -m py_compile scripts/validate_repo.py scripts/validators/common.py scripts/validators/runtime_audit.py tests/test_runtime_evidence_surfaces.py`
- `python -m pytest -q tests/test_runtime_evidence_surfaces.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_test_topology.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/validate_repo.py`
- `python scripts/ci_gate.py --mode source-fast`
- `python -m pytest -q`
- `python scripts/release_check.py`
