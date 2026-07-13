# Audit Validator Module Boundary

- Decision ID: AOA-EV-D-0128
- Status: Accepted
- Date: 2026-06-03
- Owner surface: Audit validator modules, `mechanics/audit/`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, mechanics/topology, audit/observability
- Mechanic parents: audit, proof-loop, proof-object, cross-parent
- Guard families: source/topology, trace/eval, runtime-policy
- Posture: active rationale

## Context

The audit route checks still lived inside the broad
`validate_mechanics_surfaces` body.

That block checked one coherent organ: `mechanics/audit/README.md`,
`AGENTS.md`, provenance, the parts index, selected-evidence packets,
artifact-verdict hooks, candidate readers, integrity review, legacy routing,
and the audit part-contract decision.

Meanwhile adjacent audit behavior already had focused owners:

- artifact-to-verdict hook contract refs live in
  `scripts/validators/artifact_hooks.py`;
- runtime candidate reader generated parity lives in focused
  `runtime_candidate_template_index.py` and `runtime_candidate_intake.py`
  validators;
- runtime evidence meaning stays with runtime owners and bundle-local review.

## Options Considered

- Leave audit route checks in `scripts/validate_repo.py`.
- Merge audit route checks into artifact-hook or runtime-candidate validators.
- Create an Audit validator boundary for audit route, provenance, legacy,
  and active part-contract checks.

## Decision

Audit route validation moved out of the root mechanics validator into an
Audit-specific validator boundary.

`scripts/validate_repo.py` delegates audit route-card, part-contract,
provenance, legacy, active-part, and decision checks to
`validate_audit_route_surfaces`.

Tests import audit constants from the Audit owner boundary directly.
`scripts/validate_repo.py` no longer re-exports audit compatibility aliases.

## Rationale

Audit is a boundary organ for candidate evidence and review posture. It routes
runtime artifacts toward selected evidence packets, artifact verdict hooks,
candidate readers, integrity review, and bundle-local acceptance. It does not
make runtime evidence into proof canon.

Keeping these checks in the root validator made `validate_mechanics_surfaces`
preserve historical audit knowledge directly. Moving them into an audit module
keeps the owner boundary explicit while preserving separate generated and
runtime-policy validators for the surfaces that need them.

## Consequences

- Positive: another long route-card block leaves `validate_mechanics_surfaces`.
- Positive: audit provenance, legacy routing, active parts, and part-contract
  posture now have one validator owner.
- Positive: audit test fixtures now route to the focused module instead of
  preserving root compatibility aliases.
- Follow-up: boundary-bridge and remaining large mechanics route blocks can be
  split once their owner boundaries are equally clear.

## Current Applicability

As of 2026-06-03:

- Still valid: artifact hook and runtime-candidate generated checks keep their
  focused modules.
- Changed: audit route-card and part-contract checks now have a focused
  validator module.
- Refined by: AOA-EV-D-0205 for runtime-candidate aggregate removal;
  AOA-EV-D-0228 splits the former `scripts/validators/audit.py` module into
  path, token, helper, and route validator modules.

## Boundaries

This decision does not make audit selected evidence stronger than source
bundle review.

It does not move generated runtime-candidate parity, artifact hook ref
resolution, publication receipts, or runtime integrity acceptance into the
audit route validator.

It does not publish, append, rewrite, or accept runtime evidence.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
