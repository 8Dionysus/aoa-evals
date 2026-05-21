# Mechanic Part Source Surface Reference Guard

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/README.md`

## Context

Concrete part README files now route payload directories and validation
commands, but their `## Source Surfaces` sections can still preserve an older
active-looking path after payload movement.

That is a future bug, not harmless history. If a part says its source surface
is `reports/...`, `tests/...`, `schemas/...`, or another old root route after
the real payload has moved into `mechanics/<parent>/parts/<part>/`, the next
worker can follow the stale source surface ref and recreate the same drift.

## Decision

Every path-like reference in a concrete
`mechanics/<parent>/parts/<part>/README.md` `## Source Surfaces` section must
resolve as one of these explicit forms:

- an existing repo-relative path;
- a repo-relative glob with at least one match;
- a repo-qualified sibling ref such as `repo:aoa-playbooks/...`;
- a placeholder route such as `quests/<lane>/<state>/AOA-EV-Q-*.yaml`.

`scripts/validate_repo.py` rejects a stale source surface ref, an absolute
local path, or a path that traverses outside the repository.

## Rationale

`Source Surfaces` is the part's truth table for "what files make this operation
real." It must not become a decorative list that lags behind moves.

The guard is deliberately reachability-oriented. It does not require every
source surface to be part-local, because some parts legitimately route source
bundles, generated readers, root release files, or repo-qualified sibling
evidence. It does require the reference to be honest and current.

## Consequences

- Positive: old root payload paths cannot remain as active source-surface
  guidance after a mechanics move.
- Positive: repo-qualified sibling refs and placeholder quest routes stay
  expressible without pretending to be local files.
- Positive: current part-local payload homes are checked from the standard repo
  validator.
- Tradeoff: moving a payload now requires updating the part README source
  surface list in the same slice.

## Boundaries

This decision does not create a new mechanic parent, move source proof bundles
out of `evals/`, or make `Source Surfaces` stronger than the owning bundle,
decision, sibling repository, generated builder, or live operator surface.

It does not execute all part validation commands. Validation command
reachability remains covered by the separate Mechanic Part Validation Command
Reachability guard.

## Validation

```bash
python -m pytest -q tests/test_validate_repo.py -k mechanic_part_source_surface
python scripts/validate_repo.py
```
