# 0016 Agon Proof Mechanic Package

- Status: Accepted
- Date: 2026-05-19
- Owner surface: `mechanics/agon-proof/`

## Context

Agon appears across `aoa-evals` as historical and active proof-family
vocabulary: docs, seed configs, generated registries, examples, schemas,
tests, recurrence manifests, observe-only hooks, quest notes, and the
`aoa-recurrence-control-plane-integrity` bundle.

Earlier topology work intentionally kept `agon-proof` as a candidate until the
operation was clearer. The current source map shows a real recurring
operation: seed prebindings or alignments generate deterministic registries,
validators and tests constrain candidate-only status, recurrence components
observe the surfaces, and bundle-local review checks Agon stop-lines.

## Options Considered

- Leave Agon only in `docs/LEGACY_NAMING.md` and `docs/PROOF_TOPOLOGY.md`.
- Move Agon docs, configs, generated registries, manifests, and quest notes
  under `mechanics/agon-proof/`.
- Create `mechanics/agon-proof/` as a route package while leaving source,
  generated, recurrence, quest, and bundle files in place.

## Decision

Create `mechanics/agon-proof/` for the operation:

`Agon proof pressure -> seed prebinding or alignment config -> deterministic generated registry -> observe-only recurrence component and hooks -> Agon stop-line review -> bundle-local proof or owner handoff`

The package routes Agon proof alignment work without moving `docs/AGON_*`,
`config/agon_*`, `generated/agon_*`, recurrence manifests, Agon quest notes,
or recurrence-control-plane bundle files.

## Rationale

Agon is no longer only a vague legacy term. It has enough source artifacts,
generated companions, validators, tests, and recurrence stop-line pressure to
deserve a live operation package.

The package makes the active route explicit while preserving lineage. It also
prevents two opposite errors: treating Agon as mere flat-file history, and
treating generated alignment registries as live verdict or arena authority.

## Consequences

- Positive: future Agon work now has a current package route, local agent
  guidance, and validator-backed discovery surface.
- Tradeoff: the package is a route layer, not a file move. Maintainers must
  still read the source docs, configs, manifests, and bundle files where they
  currently live.
- Follow-up: if one Agon family matures into an eval bundle or stricter
  machine-readable ledger, add that proof object only after bundle-local review
  and validation can follow it.

## Boundaries

This decision does not move Agon source surfaces into `mechanics/agon-proof/`.

It does not make generated Agon registries source truth.

It does not authorize live verdicts, closure grants, live summon, durable
memory writes, rank mutation, Tree of Sophia promotion, hidden scheduler
action, arena activation, or stronger-owner law changes.

## Validation

- `mechanics/agon-proof/README.md` names the owned operation, source surfaces,
  inputs, outputs, stronger-owner split, legacy posture, boundaries,
  validation, and next route.
- `mechanics/agon-proof/AGENTS.md` names local editing law.
- `mechanics/README.md`, `docs/PROOF_TOPOLOGY.md`, `docs/LEGACY_NAMING.md`,
  `README.md`, `docs/README.md`, `ROADMAP.md`, `CHANGELOG.md`, and
  `docs/decisions/README.md` route to the package.
- `scripts/validate_repo.py` checks the package and decision remain
  discoverable.
- `python scripts/build_agon_eval_prebinding_registry.py --check`
- `python scripts/build_agon_ccs_eval_alignment_registry.py --check`
- `python scripts/build_agon_vds_eval_alignment_registry.py --check`
- `python scripts/build_agon_retention_rank_eval_alignment_registry.py --check`
- `python scripts/build_agon_mechanical_trial_eval_suites.py --check`
- `python scripts/build_agon_epistemic_eval_alignment_registry.py --check`
- `python scripts/build_agon_slc_eval_alignment_registry.py --check`
- `python scripts/build_agon_kag_eval_alignment_registry.py --check`
- `python scripts/build_agon_sophian_eval_alignment_registry.py --check`
- `python scripts/validate_agon_eval_prebindings.py`
- `python scripts/validate_agon_ccs_eval_alignment.py`
- `python scripts/validate_agon_vds_eval_alignment.py`
- `python scripts/validate_agon_retention_rank_eval_alignment.py`
- `python scripts/validate_agon_mechanical_trial_eval_suites.py`
- `python scripts/validate_agon_epistemic_eval_alignment.py`
- `python scripts/validate_agon_slc_eval_alignment_registry.py`
- `python scripts/validate_agon_kag_eval_alignment_registry.py`
- `python scripts/validate_agon_sophian_eval_alignment_registry.py`
- `python -m pytest -q tests/test_agon*.py`
