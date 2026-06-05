# Runtime Audit Aggregate Removal

- Decision ID: AOA-EV-D-0203
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused trace/eval bridge, runtime evidence selection, and integrity-review validators

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, runtime-policy, audit/observability
- Mechanic parents: audit, proof-loop, proof-object, cross-parent
- Guard families: runtime-policy, trace/eval, source/topology
- Posture: active rationale

## Context

AOA-EV-D-0131 moved runtime audit behavior out of root validation and into
`scripts/validators/runtime_audit.py`. AOA-EV-D-0174 then moved the
candidate-only runtime integrity review contract into
`runtime_integrity_review.py`, but left compatibility aliases and an adapter in
`runtime_audit.py`.

The remaining aggregate still mixed:

- artifact-to-verdict trace bridge schema/example checks;
- selected runtime evidence packet schema/example checks;
- injected runtime audit context; and
- a compatibility route to the integrity-review validator.

These are adjacent runtime-policy checks, but they repair through different
audit parts and should not share one historical runtime bucket.

## Decision

`scripts/validators/runtime_audit.py` is removed.

Runtime audit validation now routes through focused modules:

- `runtime_trace_eval_bridge.py` owns artifact-to-verdict hook schema/example
  checks, eval-anchor resolution, optional playbook compatibility, contract
  refs, trace surfaces, verdict bundle refs, and report expectations.
- `runtime_evidence_selection.py` owns selected evidence packet schema/example
  checks, candidate eval refs, source schema refs, selected evidence refs, and
  abyss-stack allowed-root validation.
- `runtime_integrity_review.py` remains the focused candidate-only integrity
  review validator and is called directly.
- `runtime_audit_common.py` is helper-only injected runtime audit context.

`evidence_readouts.py` calls the focused validators directly.

## Rationale

Runtime policy validators should preserve specific boundaries: trace/eval
handoff, selected evidence promotion, and candidate-only integrity review.
Keeping them behind a broad runtime-audit module made adapter behavior look like
a current owner surface and let future runtime checks drift into a historical
bucket.

The split keeps repo-ref and sibling compatibility context injected from root
orchestration while making each audit part own its validation failure route.

## Consequences

- Positive: no runtime audit aggregate validator remains.
- Positive: trace bridge, selected evidence, and integrity-review failures now
  name separate owner modules.
- Positive: tests import focused runtime validators directly instead of
  runtime-audit aliases.
- Tradeoff: `evidence_readouts.py` imports more focused runtime validators
  because it orchestrates readout validation.

## Review Log

### 2026-06-05 - Runtime degradation pairing contract

- Changed: `runtime_evidence_selection.py` now hard-checks the
  `runtime-chaos-window` packet as degradation/fallback sidecar evidence paired
  to `artifact_to_verdict_hook.trace-integrity-chaos.example.json` and
  `TRACE_EVAL_BRIDGE_CHAOS_WAVE1.md`.
- Reason: behavior degradation evidence must preserve a bounded target eval,
  selected artifact roles, source schema refs, trace/eval hook contracts, and
  explicit stop-lines before it becomes route-visible runtime behavior evidence.
- Boundary: the check proves selection hygiene and trace/eval pairing only; it
  does not prove live runtime health, replace an eval verdict, publish raw logs,
  or move runtime-owner closeout into `aoa-evals`.
- Source surfaces updated: selected-evidence README, validation inventories,
  mechanics evidence clusters, and runtime evidence surface tests.

### 2026-06-05 - Policy-sensitive hook boundary contract

- Changed: `runtime_trace_eval_bridge.py` now hard-checks
  `runtime_policy_boundary` metadata for policy-sensitive artifact hooks:
  approval boundary, tool trajectory, scope drift, A2A summon-return, and
  runtime-chaos recovery.
- Reason: trace/eval hook metadata can name authorization, approval, fallback,
  and rollback artifacts only when those artifacts are explicit hook inputs and
  when stop-lines forbid reading the hook as tool permission, runtime policy
  enforcement, runtime-owner approval, or cost/time cap proof.
- Boundary: the check proves candidate policy metadata hygiene only. It does
  not implement a runtime policy engine, approve tool calls, certify cost/time
  caps, or replace runtime/route-owner review.
- Source surfaces updated: artifact-verdict hook schema/examples, trace bridge
  guide, generated runtime-candidate readers, validation inventories, mechanics
  evidence clusters, and runtime evidence surface tests.

## Current Applicability

As of 2026-06-05:

- Still valid: runtime audit validation does not accept runtime activation,
  owner override, canon writes, or proof verdict authority.
- Changed: runtime audit behavior no longer lives in `runtime_audit.py`; it is
  split across focused runtime-policy validators and a helper-only context.
- Further changed on 2026-06-05: selected-evidence validation owns bounded
  runtime degradation/fallback pairing only when the packet, paired trace/eval
  hook, bridge doc, target eval, selected roles, and stop-lines agree.
- Further changed on 2026-06-05: trace/eval bridge validation owns
  policy-sensitive hook metadata only when authorization, approval,
  fallback/rollback, and forbidden-claim fields agree with the hook input
  boundary.
- Supersedes: the aggregate module shape left by AOA-EV-D-0131 and the
  compatibility alias posture left by AOA-EV-D-0174.

## Boundaries

This decision does not make selected runtime evidence proof canon.

It does not let trace/eval bridge validation own selected-evidence packet
promotion, integrity-review no-authority posture, generated candidate readers,
runtime activation, owner override, canon write, or sealed verdict authority.

It does not create a replacement runtime audit aggregate under another name.

## Validation

- `python -m py_compile scripts/validators/runtime_audit_common.py scripts/validators/runtime_trace_eval_bridge.py scripts/validators/runtime_evidence_selection.py scripts/validators/runtime_integrity_review_common.py scripts/validators/runtime_integrity_review_docs.py scripts/validators/runtime_integrity_review_schema.py scripts/validators/runtime_integrity_review_example.py scripts/validators/evidence_readouts.py tests/test_runtime_evidence_surfaces.py tests/validate_repo_fixtures.py tests/test_quest_and_reader_surfaces.py`
- `python -m pytest -q tests/test_runtime_evidence_surfaces.py tests/test_quest_and_reader_surfaces.py tests/test_validate_repo.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/ci_gate.py --mode source-fast`
