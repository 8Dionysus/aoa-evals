# 0015 Titan Canaries Mechanic Package

- Status: Accepted
- Date: 2026-05-19
- Owner surface: `mechanics/titan-canaries/`

## Context

Titan canaries were already present as seed YAML files under `evals/`, and
`scripts/validate_repo.py` already had `validate_titan_canary_surfaces` plus a
unit test for the current seed set.

The pressure is not to move the files. The pressure is that the canaries are
easy to overread: named Titan identity, summon discipline, mutation and
judgment gates, memory provenance, runtime roster, closeout receipts, and
lineage non-erasure can look like live Titan proof if the seed status is not
visible.

## Options Considered

- Leave Titan canaries as loose `evals/titan_*_canary.yaml` files plus a short
  guide.
- Move Titan canary YAML files under `mechanics/titan-canaries/`.
- Create `mechanics/titan-canaries/` as a route package while leaving canary
  YAML files under `evals/`.

## Decision

Create `mechanics/titan-canaries/` for the operation:

`Titan boundary pressure -> seed canary YAML -> shape validation -> future executable scorer route -> bounded proof or owner handoff`

The package routes Titan canary shape work without moving `evals/`,
`docs/TITAN_INCARNATION_CANARIES.md`,
`docs/TITAN_SUMMON_DISCIPLINE_CANARIES.md`, validator code, or tests.

## Rationale

The canaries already have enough live shape pressure to deserve a package:
they have many seed files, public guide surfaces, legacy naming pressure, and a
validator that constrains their shape.

The package gives future agents a place to reason about seed-defined canaries
without pretending they are executable scorer-backed proof. It also keeps the
stronger-owner split visible: `aoa-evals` owns the bounded canary proof
surface, not Titan doctrine, runtime activation, memory sovereignty, or summon
authority.

## Consequences

- Positive: Titan canary work now has a package route, local `evals/AGENTS.md`,
  and validator-backed discovery surface.
- Tradeoff: the package is a route layer, not a file move. Future maintainers
  must still read `evals/AGENTS.md` for exact seed-file editing law.
- Follow-up: later work can add executable scorer contracts, fixtures, and
  reports before any canary is promoted beyond seed-defined status.

## Boundaries

This decision does not move `evals/` or convert seed canaries into executable
scorer-backed evals.

It does not make Titan canaries full incarnation proof.

It does not authorize runtime activation, hidden arena behavior, memory
sovereignty, summon authority, mutation-gate bypass, judgment-gate bypass, or
stronger-owner Titan law changes.

## Validation

- `mechanics/titan-canaries/README.md` names the owned operation, source
  surfaces, inputs, outputs, stronger-owner split, boundaries, validation, and
  next route.
- `mechanics/titan-canaries/AGENTS.md` names local editing law.
- `evals/AGENTS.md` protects seed canary files.
- `docs/TITAN_INCARNATION_CANARIES.md` and
  `docs/TITAN_SUMMON_DISCIPLINE_CANARIES.md` route to the package.
- `mechanics/README.md`, `docs/PROOF_TOPOLOGY.md`, `docs/LEGACY_NAMING.md`,
  `README.md`, `docs/README.md`, `ROADMAP.md`, `CHANGELOG.md`, and
  `docs/decisions/README.md` route to the package.
- `python scripts/validate_repo.py`
- `python scripts/validate_semantic_agents.py`
- `python -m pytest -q tests/test_validate_repo.py -k titan_canary`
