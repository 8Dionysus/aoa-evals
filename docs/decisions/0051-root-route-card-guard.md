# 0051 Root Route-card Guard

- Status: Accepted
- Date: 2026-05-20
- Owner surface: root route-card districts

## Context

The mechanics refactor moved active payloads out of several root technical
districts. After those moves, these roots should no longer silently accept new
mechanic-owned payloads:

- `config/`
- `examples/`
- `fixtures/`
- `manifests/`
- `reports/`
- `runners/`
- `schemas/`
- `scorers/`
- `templates/`

Some of those districts already had route-card wording. Others still lacked a
human-facing `README.md`, which made it too easy for future work to recreate an
old root payload path instead of using the active mechanic part.

## Options Considered

- Leave the roots as-is and rely on convention.
- Delete the root directories entirely.
- Keep root route cards, add missing README cards, and validate that active
  payload files or stray payload directories do not return without an explicit
  topology change.

## Decision

Keep these root districts as route-card-only surfaces for now.

Active mechanic-owned payloads must live under their owning part. The root
route-card districts may contain only their route cards unless a future
decision updates `docs/PROOF_TOPOLOGY.md` and the validator allowlist.

## Rationale

The empty root directories are useful as navigation signs because old paths and
habits still point there. They should not become active payload homes again by
accident.

This keeps the topology convex: a future agent can see that root examples,
schemas, config, manifests, templates, runners, scorers, reports, and fixtures
are not the first place to put a new mechanic artifact.

## Consequences

- Positive: `python scripts/validate_repo.py` now notices active payload and
  stray directory drift in route-card-only root districts.
- Positive: missing `README.md` cards for `config/`, `examples/`,
  `manifests/`, `schemas/`, and `templates/` now explain the active owner
  routes.
- Tradeoff: a future real repo-wide shared payload must update the allowlist
  deliberately instead of just adding a file.

## Boundaries

This decision does not move `evals/`, root repo-wide `scripts/`, root
repo-wide `tests/`, root `generated/` readers, `quests/`, or source guidance in
`docs/`.

It does not forbid bundle-local examples or reports. Those stay under the
owning bundle. It also does not forbid mechanic-owned examples, schemas,
config, scripts, tests, reports, or generated readers under active
`mechanics/*/parts/` routes.

## Validation

- `config/README.md`
- `examples/README.md`
- `manifests/README.md`
- `schemas/README.md`
- `templates/README.md`
- `docs/PROOF_TOPOLOGY.md`
- `scripts/validate_repo.py`
- `tests/test_validate_repo.py`
- `python scripts/validate_repo.py`
- `python -m pytest -q tests/test_validate_repo.py`
