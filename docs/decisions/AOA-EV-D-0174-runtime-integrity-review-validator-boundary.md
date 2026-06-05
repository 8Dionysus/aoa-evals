# Runtime Integrity Review Validator Boundary

- Decision ID: AOA-EV-D-0174
- Status: Superseded
- Superseded by: AOA-EV-D-0212-runtime-integrity-review-layer-split
- Date: 2026-06-04
- Owner surface: `scripts/validators/runtime_integrity_review.py`, `mechanics/audit/parts/integrity-review/`
- Refined by: AOA-EV-D-0203

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, runtime-policy, audit/observability
- Mechanic parents: audit, cross-parent
- Guard families: runtime-policy, trace/eval, source/topology
- Posture: superseded rationale

## Context

`scripts/validators/runtime_audit.py` still carried the full candidate-only
runtime integrity review contract check: guide tokens, schema closure, example
payload, replay requirements, no-authority forbidden claims, budget ref, and
repo-qualified evidence refs.

That contract is adjacent to runtime audit, but it is not the same boundary as
trace/eval bridge validation or selected-evidence packet promotion. It protects
the integrity-review part from silently becoming runtime activation, owner
override, canon write, or sealed proof-verdict authority.

## Decision

Runtime integrity review validation lives in
`scripts/validators/runtime_integrity_review.py`.

The module owns:

- integrity-review guide token checks;
- integrity-review schema title, closure, required field, replay, evidence-ref,
  and forbidden-claim checks;
- example payload schema validation and candidate-only posture checks;
- `Agents-of-Abyss` Experience budget-ref resolution; and
- bounded repo-qualified evidence ref resolution.

As of AOA-EV-D-0203, `scripts/validators/runtime_audit.py` is removed and
callers invoke this focused module directly.

## Rationale

Runtime audit should not be a historical bucket for every audit-adjacent
runtime guard. Trace/eval bridge validation and selected-evidence packet
validation protect runtime routing and promotion evidence. Runtime integrity
review protects a separate no-authority candidate contract.

Splitting that contract makes the owner surface explicit while preserving the
existing repo-wide validation entrypoint and injected resolver context.

## Consequences

- Positive: `runtime_audit.py` narrows to trace/eval bridge and selected
  evidence packet checks.
- Positive: integrity-review guide/schema/example checks have their own
  validator, inventory entry, mechanics ledger row, and decision rationale.
- Positive: tests import the focused integrity-review module directly instead
  of relying on runtime-audit aliases.
- Tradeoff: the integrity-review validator still depends on injected repo-ref
  and named-surface context because the contract explicitly proves bounded
  evidence and Experience budget-ref routing.

## Current Applicability

As of 2026-06-04:

- Still valid: runtime integrity review remains `candidate_only` and
  `human_review_needed`; it does not accept runtime activation or proof canon.
- Changed: integrity-review guide/schema/example validation moved out of
  `runtime_audit.py` and into `runtime_integrity_review.py`; active validation
  later split across docs, schema, example, and helper-only constants modules.
- Further changed by: AOA-EV-D-0203 removes the runtime-audit compatibility
  adapter; integrity-review validation is called directly from readout
  orchestration and tests.
- Superseded by: AOA-EV-D-0203 for the compatibility-alias posture.
- Superseded by: AOA-EV-D-0212 for the aggregate integrity-review validator
  shape.

## Boundaries

This decision does not make `runtime_integrity_review.py` the owner of
trace/eval bridge schema meaning, selected-evidence packet promotion,
generated candidate readers, runtime activation, owner override, canon write, or
sealed verdict authority.

It checks the candidate-only integrity-review contract only.

## Validation

- `python -m py_compile scripts/validators/runtime_integrity_review_common.py scripts/validators/runtime_integrity_review_docs.py scripts/validators/runtime_integrity_review_schema.py scripts/validators/runtime_integrity_review_example.py scripts/validators/evidence_readouts.py`
- `python -m pytest -q tests/test_runtime_evidence_surfaces.py -k runtime_integrity_review`
- `python -m json.tool docs/validation/script_inventory.json`
- `python -m json.tool docs/validation/validator_inventory.json`
- `python scripts/generate_decision_indexes.py`
- `python scripts/ci_gate.py --mode source-fast`
