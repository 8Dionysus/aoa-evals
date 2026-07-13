# Readout Lane Orchestration Split

- Decision ID: AOA-EV-D-0239
- Status: Accepted
- Date: 2026-06-05
- Owner surface: `scripts/validate_repo.py` and focused readout lane modules

## Index Metadata

- Original date: 2026-06-05
- Surface classes: validation guard, projection/generated, runtime-policy, observability/audit
- Mechanic parents: audit, boundary-bridge, publication-receipts, release-support, titan, cross-parent
- Guard families: projection/generated, runtime-policy, trace/eval, observability/audit, release/nightly
- Posture: active rationale

## Context

AOA-EV-D-0156 moved repo-wide readout orchestration out of
`scripts/validate_repo.py` and into `scripts/validators/evidence_readouts.py`.
That was useful while removing the historical root validator body, but it left a
new broad bucket.

The module grouped generated read-model parity, runtime trace/eval and selected
evidence checks, runtime integrity review, runtime candidate readers,
publication receipts, live receipt logs, release-support audit reports, report
index parity, Phase Alpha projection and sibling compatibility, and Titan
canaries.

Those checks are adjacent only because a full repo validation run needs them.
They repair through different owner surfaces and should not share one active
validator organ.

## Options Considered

- Keep `evidence_readouts.py` as a named orchestration boundary.
- Keep it as a compatibility facade that delegates to smaller modules.
- Remove it and route readout lanes explicitly from `scripts/validate_repo.py`.

## Decision

`scripts/validators/evidence_readouts.py` is removed.

Readout validation now routes through focused lane modules:

- `readout_contexts.py` builds injected runtime and generated read-model
  contexts.
- `runtime_readouts.py` routes trace/eval bridge, selected evidence, runtime
  integrity review, and runtime candidate reader checks.
- `generated_readouts.py` routes generated catalog, capsule, section, and
  comparison-spine parity checks for repo-wide and target-eval runs.
- `observability_readouts.py` routes publication receipt, live receipt,
  release-support report, and report-index checks.
- `phase_alpha_readouts.py` routes local Phase Alpha projection and strict
  sibling compatibility checks.

`scripts/validate_repo.py` remains the source-scope selector and calls these
lane modules directly.

## Rationale

Readout checks protect different boundaries: projection parity, runtime-policy
evidence, observability receipts, release-support reports, and sibling-derived
Phase Alpha parity. A single active module made those boundaries look like one
organ again.

Splitting the route keeps the root CLI honest: it selects scope and calls the
right lane, but it does not hide broad behavior behind another aggregate. The
focused validators still own their rule meaning, and the new lane modules only
group calls that share an owner route.

## Consequences

- Positive: no active evidence/readout aggregate validator remains.
- Positive: target-eval validation now calls runtime and generated readout
  routes directly.
- Positive: runtime tests import the context helper instead of an aggregate.
- Tradeoff: `scripts/validate_repo.py` has a few more explicit lane calls.
- Follow-up: future cleanup can apply the same pattern to remaining route
  orchestrators only when they start mixing unrelated owner lanes.

## Current Applicability

As of 2026-06-05:

- Still valid: generated validators check projection parity, runtime validators
  check runtime-policy/readout evidence, and observability validators check
  receipts/reports below live publication truth.
- Changed: `evidence_readouts.py` no longer exists as an active owner surface.
- Superseded by: none.

## Boundaries

This decision does not make `scripts/validate_repo.py` the owner of generated
meaning, runtime acceptance, receipt publication, release evidence, sibling
truth, Titan behavior, or source proof meaning.

It also does not create compatibility aliases for the removed aggregate.
Historical decisions may mention `evidence_readouts.py` as a former route, but
current inventories and topology must point to the focused lane modules.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
