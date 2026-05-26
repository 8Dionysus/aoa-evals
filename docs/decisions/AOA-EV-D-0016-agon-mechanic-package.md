# Agon Mechanic Package

- Decision ID: AOA-EV-D-0016
- Status: Accepted
- Date: 2026-05-19
- Owner surface: `mechanics/agon/`

## Index Metadata

- Original date: 2026-05-19
- Surface classes: mechanic package, boundary/runtime/sibling
- Mechanic parents: agon
- Guard families: none
- Posture: active rationale

## Context

Agon appears across `aoa-evals` as historical and active proof-family
vocabulary: docs, seed configs, generated registries, examples, schemas,
tests, recurrence manifests, observe-only hooks, quest notes, and the
`aoa-recurrence-control-plane-integrity` bundle.

Earlier topology work intentionally kept Agon as a candidate until the
operation was clearer. The current source map shows a real recurring
operation: seed prebindings or alignments generate deterministic registries,
validators and tests constrain candidate-only status, recurrence components
observe the surfaces, and bundle-local review checks Agon stop-lines.

## Options Considered

- Leave Agon only in `docs/architecture/LEGACY_NAMING.md` and `docs/architecture/PROOF_TOPOLOGY.md`.
- Move Agon docs, configs, generated registries, manifests, scripts, tests,
  schemas, and examples into part-local homes under `mechanics/agon/`.
- Create `mechanics/agon/` only as a route package while leaving source,
  generated, recurrence, quest, and bundle files in their old districts.

## Decision

Create `mechanics/agon/` for the operation:

`Agon pressure -> part-local seed/config/docs -> deterministic registry -> candidate-only checks -> observe-only recurrence hooks -> bundle-local review or owner handoff`

The package moves Agon-owned artifact families under `mechanics/agon/parts/`
when the part owns the source, generated output, validation, and recurrence
route. Quest source records stay under `quests/` for the questbook route, and
the recurrence-control-plane bundle stays under `evals/`.

## Rationale

Agon is no longer only a vague legacy term. It has enough source artifacts,
generated companions, validators, tests, and recurrence stop-line pressure to
deserve a live operation package.

The package makes the active route explicit while preserving lineage. It also
prevents two opposite errors: treating Agon as mere flat-file history, and
treating generated alignment registries as live verdict or arena authority.

## Consequences

- Positive: future Agon work now has a current package route, part map, local
  agent guidance, and validator-backed discovery surface.
- Tradeoff: quest source records and proof bundles still live in their owning
  districts, so Agon work must keep those owner boundaries visible.
- Follow-up: if one Agon family matures into an eval bundle or stricter
  machine-readable ledger, add that proof object only after bundle-local review
  and validation can follow it.

## Boundaries

This decision does not move Agon quest source records or recurrence proof
bundles into `mechanics/agon/`.

It does not make generated Agon registries source truth.

It does not authorize live verdicts, closure grants, live summon, durable
memory writes, rank mutation, Tree of Sophia promotion, hidden scheduler
action, arena activation, or stronger-owner law changes.

## Validation

- `mechanics/agon/README.md` names the owned operation, package surfaces,
  inputs, outputs, stronger-owner split, legacy posture, boundaries,
  validation, and next route.
- `mechanics/agon/AGENTS.md` names local editing law.
- `mechanics/agon/PARTS.md` names the active part topology.
- `mechanics/README.md`, `docs/architecture/PROOF_TOPOLOGY.md`, `docs/architecture/LEGACY_NAMING.md`,
  `README.md`, `docs/README.md`, `ROADMAP.md`, `CHANGELOG.md`, and
  `docs/decisions/README.md` route to the package.
- `scripts/validate_repo.py` checks the package and decision remain
  discoverable.
- `python mechanics/agon/parts/court-prebinding/scripts/build_agon_eval_prebinding_registry.py --check`
- `python mechanics/agon/parts/ccs-alignment/scripts/build_agon_ccs_eval_alignment_registry.py --check`
- `python mechanics/agon/parts/vds-alignment/scripts/build_agon_vds_eval_alignment_registry.py --check`
- `python mechanics/agon/parts/retention-rank-alignment/scripts/build_agon_retention_rank_eval_alignment_registry.py --check`
- `python mechanics/agon/parts/mechanical-trial-suites/scripts/build_agon_mechanical_trial_eval_suites.py --check`
- `python mechanics/agon/parts/epistemic-alignment/scripts/build_agon_epistemic_eval_alignment_registry.py --check`
- `python mechanics/agon/parts/slc-alignment/scripts/build_agon_slc_eval_alignment_registry.py --check`
- `python mechanics/agon/parts/kag-alignment/scripts/build_agon_kag_eval_alignment_registry.py --check`
- `python mechanics/agon/parts/sophian-threshold-alignment/scripts/build_agon_sophian_eval_alignment_registry.py --check`
- `python mechanics/agon/parts/court-prebinding/scripts/validate_agon_eval_prebindings.py`
- `python mechanics/agon/parts/ccs-alignment/scripts/validate_agon_ccs_eval_alignment.py`
- `python mechanics/agon/parts/vds-alignment/scripts/validate_agon_vds_eval_alignment.py`
- `python mechanics/agon/parts/retention-rank-alignment/scripts/validate_agon_retention_rank_eval_alignment.py`
- `python mechanics/agon/parts/mechanical-trial-suites/scripts/validate_agon_mechanical_trial_eval_suites.py`
- `python mechanics/agon/parts/epistemic-alignment/scripts/validate_agon_epistemic_eval_alignment.py`
- `python mechanics/agon/parts/slc-alignment/scripts/validate_agon_slc_eval_alignment_registry.py`
- `python mechanics/agon/parts/kag-alignment/scripts/validate_agon_kag_eval_alignment_registry.py`
- `python mechanics/agon/parts/sophian-threshold-alignment/scripts/validate_agon_sophian_eval_alignment_registry.py`
- `python -m pytest -q mechanics/agon/parts/*/tests/test_agon*.py`
