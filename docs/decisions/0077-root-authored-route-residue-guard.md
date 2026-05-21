# Root Authored Route Residue Guard

- Status: Accepted
- Date: 2026-05-20
- Owner surface: root-facing authored guidance

## Context

The mechanics refactor made root infrastructure districts route-card-only:
`config/`, `examples/`, `fixtures/`, `manifests/`, `reports/`, `runners/`,
`schemas/`, `scorers/`, and `templates/` no longer own active payloads.

Guards already protect physical root payloads, generated/readout routes, and
authored mechanics route cards. A remaining risk is root-facing authored
surfaces: `AUDIT.md`, `EVAL_INDEX.md`, `docs/*.md`, `.agents/spark/SWARM.md`,
root route cards, and `evals/AGENTS.md` can accidentally keep examples such
as `reports/summary.schema.json` or `templates/EVAL.template.md` as if those
were still active root payload routes.

Historical context is different from active navigation. Decision notes and
provenance can name former paths, but current entry guidance should route to
`evals/<family>/<eval>/...`, active `mechanics/...` surfaces, or root route cards.

## Decision

`scripts/validate_repo.py` validates root-facing authored surfaces against
route-card-only root district payload references.

The guard scans root entry docs, root route cards, `docs/*.md`,
`.agents/spark/SWARM.md`, and `evals/AGENTS.md`. It does not scan
`docs/decisions/` because decisions preserve historical context and already
serve a different authority role.

The guard permits:

- root route cards such as `reports/README.md` and `templates/AGENTS.md`;
- real existing paths;
- active `mechanics/...` routes and `evals/<family>/<eval>/...` paths, because the
  residue token no longer begins at a root route-card-only district;
- explicitly historical lines that say former root, historical root, mapped
  through, or route-card context.

## Consequences

- Entry guidance cannot quietly teach old root payload topology after the files
  have moved.
- Historical and provenance records remain readable instead of being scrubbed
  into amnesia.
- The guard complements, but does not replace, the mechanics route-card guard
  and generated/readout route residue guard.

## Validation

- `python -m pytest -q tests/test_validate_repo.py -k root_authored_route_residue`
- `python scripts/validate_repo.py`
