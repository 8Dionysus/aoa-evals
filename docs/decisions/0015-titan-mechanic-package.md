# 0015 Titan Mechanic Package

- Status: Accepted
- Date: 2026-05-19
- Owner surface: `mechanics/titan/`

## Context

Titan canaries began as seed YAML files under `evals/`, and
`scripts/validate_repo.py` already had `validate_titan_canary_surfaces` plus
unit coverage for the current seed set.

The pressure is that the canaries are easy to overread: named Titan identity,
summon discipline, mutation and judgment gates, memory provenance, runtime
roster, closeout receipts, and lineage non-erasure can look like live Titan
proof if the seed status is not visible.

During the mechanics refactor, `evals/` proved to be only a historical holding
district for Titan seed files, not a repo-wide proof district. The seed family
therefore belongs in the owning mechanic package.

## Options Considered

- Leave Titan canaries as loose root `evals/titan*.yaml` files plus a short
  guide.
- Keep `mechanics/titan/` as a route package while leaving canary YAML
  files under `evals/`.
- Move Titan seed YAML files under
  `mechanics/titan/parts/seed-boundary/seeds/` and make the mechanic the active source
  home.

## Decision

Use `mechanics/titan/` for the operation:

`Titan boundary pressure -> seed canary YAML -> shape validation -> future executable scorer route -> bounded proof or owner handoff`

Move the seed YAML files and seed-local guidance into
`mechanics/titan/parts/seed-boundary/seeds/`.

`mechanics/titan/parts/seed-boundary/docs/TITAN_INCARNATION_CANARIES.md` and
`mechanics/titan/parts/seed-boundary/docs/TITAN_SUMMON_DISCIPLINE_CANARIES.md` stay as public guides that route to
the package.

## Rationale

The canaries already have enough live shape pressure to deserve a package:
they have many seed files, public guide surfaces, legacy naming pressure, and a
validator that constrains their shape.

Putting the seed files in the package makes `mechanics/titan/` a real
source home instead of a route-only wrapper over a root holding directory. It
also lets the validator see the whole seed family through the mechanic route,
including Titan YAML files that do not end with `_canary`.

The package still keeps the stronger-owner split visible: `aoa-evals` owns the
bounded canary seed surface, not Titan doctrine, runtime activation, memory
sovereignty, or summon authority.

This is an owner-named evals-native parent. The local operation belongs to
`aoa-evals` because it shapes proof-seed boundary canaries, but the `titan`
name follows the stronger Titan subject. `aoa-agents` keeps Titan role,
bearer, summon, and incarnation law.

## Consequences

- Positive: Titan canary work now has a package-local seed home,
  `mechanics/titan/parts/seed-boundary/seeds/AGENTS.md`, and validator-backed discovery
  surface.
- Tradeoff: old `evals/titan*.yaml` path vocabulary becomes legacy path
  memory only; current references must use
  `mechanics/titan/parts/seed-boundary/seeds/titan*.yaml`.
- Follow-up: later work can add executable scorer contracts, fixtures, and
  reports before any canary is promoted beyond seed-defined status.

## Boundaries

This decision moves the seed YAML files. It does not convert seed canaries into
executable scorer-backed evals.

It does not make Titan canaries full incarnation proof.

It does not authorize runtime activation, hidden arena behavior, memory
sovereignty, summon authority, mutation-gate bypass, judgment-gate bypass, or
stronger-owner Titan law changes.

## Validation

- `mechanics/titan/README.md` names the owned operation, source
  surfaces, inputs, outputs, stronger-owner split, boundaries, validation, and
  next route.
- `mechanics/titan/AGENTS.md` names local editing law.
- `mechanics/titan/parts/seed-boundary/seeds/AGENTS.md` protects seed canary files.
- `mechanics/titan/parts/seed-boundary/seeds/titan*.yaml` carries the source seed family.
- `mechanics/titan/parts/seed-boundary/docs/TITAN_INCARNATION_CANARIES.md` and
  `mechanics/titan/parts/seed-boundary/docs/TITAN_SUMMON_DISCIPLINE_CANARIES.md` route to the package.
- `mechanics/README.md`, `docs/PROOF_TOPOLOGY.md`, `docs/LEGACY_NAMING.md`,
  `README.md`, `docs/README.md`, `ROADMAP.md`, `CHANGELOG.md`, and
  `docs/decisions/README.md` route to the package.
- `python scripts/validate_repo.py`
- `python scripts/validate_semantic_agents.py`
- `python -m pytest -q tests/test_validate_repo.py -k titan_canary`
