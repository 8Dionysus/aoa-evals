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

## Current Applicability

As of 2026-05-24:

- Still valid: root route-card-only districts remain route signs for old root
  paths and compatibility lookup.
- Changed: `reports/README.md` now names source bundles and reviewed reports as
  the owner route for eval-claim strength when release-support reports appear
  in the report route map.
- Historical text: the original decision still explains why root report
  payloads stay out of the root route-card district.
- Superseded by: none.

## Review Log

### 2026-05-24 - Reports route card names proof-strength owner

- Previous assumption: the release-support report row could preserve proof
  limits by saying that handoff reports do not strengthen eval claims.
- New reality: the route card now names the stronger owner route: source
  bundles and reviewed reports keep eval-claim strength.
- Reason: route-card-only README surfaces should show where a report reader
  goes next rather than carrying prohibition-style proof caveats.
- Source surfaces updated: `reports/README.md`, `scripts/validate_repo.py`,
  `tests/test_validate_repo.py`, and this decision.
- Validation: root validation, generated-reader checks, semantic AGENTS
  validation, and focused root route-card tests.

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
