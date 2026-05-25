# Repo Config Route Residue Guard

- Status: Accepted
- Date: 2026-05-20
- Owner surface: repository config surfaces

## Index Metadata

- Surface classes: validation guard
- Mechanic parents: none
- Guard families: route residue
- Posture: active guard rationale

## Context

The mechanics refactor moved active payloads out of route-card-only root
districts and collapsed former wrong parent routes such as
`mechanics/titan-canaries/` into active mechanics.

Root guidance, decisions, and generated readouts already have residue guards,
but repo config surfaces can still preserve active routing by accident. The
concrete case was `.gitignore`: it still unignored
`mechanics/titan-canaries/seeds/`, which would make it easy to recreate a
former parent while the active route is
`mechanics/titan/parts/seed-boundary/seeds/`.

Repo config is not historical memory. It should route active filesystem
behavior only.

## Options Considered

- Fix `.gitignore` only.
- Fold `.gitignore` into the root authored guidance guard.
- Add a repo-config-specific guard for `.gitignore`, `pytest.ini`, and
  `.github/workflows/`.

## Decision

`scripts/validate_repo.py` validates repo config surfaces for route residue.

The guard scans:

- `.gitignore`;
- `pytest.ini`;
- `.github/workflows/*.yml`;
- `.github/workflows/*.yaml`.

It rejects:

- legacy mechanic parent routes such as `mechanics/titan-canaries/` or
  `mechanics/agon-proof/`;
- route-card-only root district payload paths such as
  `reports/summary.schema.json`.

Config surfaces must use active `mechanics/...` routes, `evals/<family>/<eval>/...`
paths, or root route cards where a root district is intentionally only a route
card.

## Rationale

Authored history can preserve former routes with explicit context. Config cannot
do that safely, because ignore rules and workflow paths are executable routing.
Leaving stale config routes turns legacy from provenance into future filesystem
permission.

## Consequences

- `.gitignore` now unignores the active Titan seed-boundary path instead of the
  rejected canary-parent path.
- Future workflow or config edits cannot reintroduce old parent routes without
  failing local validation.
- The guard complements the generated, authored, decision, and active-mechanic
  residue guards.

## Boundaries

This decision does not forbid historical route names in decisions, legacy
indexes, provenance bridges, or explicit topology maps.

It does not make repo config the owner of mechanic topology.

It does not create any new root payload aliases.

## Validation

- `python -m pytest -q tests/test_validate_repo.py -k repo_config_route_residue`
- `python scripts/validate_repo.py`
