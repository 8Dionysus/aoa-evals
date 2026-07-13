# Root Authored Route Residue Guard

- Decision ID: AOA-EV-D-0077
- Status: Accepted
- Date: 2026-05-20
- Owner surface: root-facing authored guidance

## Index Metadata

- Original date: 2026-05-20
- Surface classes: validation guard, root/topology
- Mechanic parents: none
- Guard families: route residue
- Posture: active guard rationale

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

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.

## Current Applicability

As of 2026-05-24:

- Still valid: root-facing authored guidance stays current by routing readers
  to active source surfaces, mechanics routes, or root route cards.
- Changed: `CONTRIBUTING.md` now has an operating card and positive proof
  criteria for contribution intake, validation evidence, and security handoff.
- Source surfaces updated: `CONTRIBUTING.md`, `scripts/validate_repo.py`, and
  `tests/test_validate_repo.py`.
- Validation route: use the focused contribution-route check and repository
  lane owned by command authority and the nearest `AGENTS.md`.

## Review Log

### 2026-05-24 - Contributing route card clarified

- Previous assumption: the public contribution guide could rely on checklist
  wording and several negative readiness warnings.
- New reality: contributors and low-context agents need the owner route,
  validation route, review evidence route, and security handoff visible before
  the checklist.
- Reason: `CONTRIBUTING.md` is root-facing authored guidance; it should route
  public proof work to the right owner without duplicating agent workflow law.
- Source surfaces updated: `CONTRIBUTING.md`, `scripts/validate_repo.py`, and
  `tests/test_validate_repo.py`.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.
