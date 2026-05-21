# Active Mechanic Route Residue Guard

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/` route cards and part READMEs

## Context

The mechanics refactor made root infrastructure districts route-card-only and
moved active payloads into bundles or mechanic-local parts. Generated/readout
JSON already has a residue guard, but authored mechanics route cards are also
agent-facing source. A stale authored path example such as
`fixtures/old/README.md`, `reports/summary.schema.json`, or
`mechanics/titan-canaries/README.md` can
teach the next agent the old topology even when the files are gone.

The guard must stay context-aware. A part README may validly mention local
`examples/...` or `schemas/...` when those files exist under the same part
root. A parent route card may validly mention root route cards such as
`fixtures/README.md`. It must not treat a former root payload path as active
ownership.

## Decision

`scripts/validate_repo.py` validates authored mechanics route cards for two
residue classes:

- root route-card-only payload paths under `config/`, `examples/`, `fixtures/`,
  `manifests/`, `reports/`, `runners/`, `schemas/`, `scorers/`, and
  `templates/`; this is the authored route-card companion to the
  route-card-only root district guard;
- legacy parent routes such as `mechanics/agon-proof/`,
  `mechanics/titan-canaries/`, `mechanics/proof-release/`,
  `mechanics/runtime-evidence/`, `mechanics/sibling-proof-refs/`, and
  `mechanics/repair/`.

The guard scans active authored mechanics route cards: `mechanics/README.md`,
each parent `AGENTS.md`, `README.md`, `PARTS.md`, `parts/README.md`, and each
concrete `mechanics/<parent>/parts/<part>/README.md`.

The guard permits:

- root route cards such as `fixtures/README.md` and `reports/AGENTS.md`;
- local sibling paths that resolve inside the same part root;
- bundle-local routes written as `evals/<family>/<eval>/...` instead of pretending a
  former root payload district is active.

## Consequences

- Authored route cards now get the same anti-residue protection as generated
  readers.
- Part-local topology remains usable; the guard follows the same part root
  before rejecting a local `examples/...`, `schemas/...`, or `reports/...`
  reference.
- Old parent names remain available as legacy vocabulary, but active route
  cards cannot link through their former package paths.

## Validation

- `python -m pytest -q tests/test_validate_repo.py -k active_mechanic_route_residue`
- `python scripts/validate_repo.py`
