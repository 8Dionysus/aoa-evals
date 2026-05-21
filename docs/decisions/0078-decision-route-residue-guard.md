# Decision Route Residue Guard

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `docs/decisions/`

## Context

The mechanics refactor made root infrastructure districts route-card-only:
`config/`, `examples/`, `fixtures/`, `manifests/`, `reports/`, `runners/`,
`schemas/`, `scorers/`, and `templates/` no longer own active payloads. Each
one is now a route-card-only root district.

Root-facing authored guidance is already guarded, but decision records have a
different role: they preserve why a move happened and may name former root
paths. That historical context is valid only when it is explicit. A decision
line that simply says `reports/summary.schema.json` can teach a future agent
that the old root payload route is still current.

## Options Considered

- Leave `docs/decisions/` outside residue validation because decisions are
  historical.
- Reuse the root-facing authored guard and treat every former root path as a
  violation.
- Add a decision-specific guard that allows historical context while rejecting
  unmarked current-looking root payload routes.

## Decision

`scripts/validate_repo.py` validates decision records for route-card-only root
district payload references.

The guard scans `docs/decisions/*.md` except local route cards and templates.
It rejects unmarked paths under root route-card-only districts and permits:

- root route cards such as `reports/README.md` and `schemas/AGENTS.md`;
- real existing paths;
- `bundles/<bundle>/...` paths;
- active `mechanics/...` routes;
- explicitly historical context such as former root, historical root, legacy,
  provenance, mapped through, or route-card wording.

## Rationale

This preserves the decision layer as memory without letting it become active
route authority by accident. Decisions can still explain former placement, but
current navigation must point at the active mechanic part, bundle-local
surface, or root route card.

## Consequences

- Decision records can preserve legacy and former root vocabulary without
  flattening history.
- Future decisions must mark old root payload paths as historical or use active
  routes.
- The guard complements the generated, active-mechanic, and root-authored
  residue guards instead of replacing them.

## Boundaries

This decision does not scrub old decisions into amnesia.

It does not make `docs/decisions/` the active topology map.

It does not forbid bundle-local reports, schemas, examples, fixtures, runners,
or scorer paths.

It does not authorize active root payload aliases under route-card-only
districts.

## Validation

- `python -m pytest -q tests/test_validate_repo.py -k decision_route_residue`
- `python scripts/validate_repo.py`
