# Source Bundle Route Residue Guard

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `evals/`

## Context

Source proof bundles are source proof objects stronger than generated readers,
route cards, reports, and release-support snapshots. If a bundle carries an ambiguous old path, the
mistake is not just navigation residue: it can become proof-object meaning.

The mechanics refactor already guards generated readers, root guidance,
decisions, repo config, and active mechanic route cards. A remaining class was
inside bundles themselves. Two stale authored path examples exposed the risk:

- stale authored path example: `aoa-a2a-summon-return-checkpoint` named an `aoa-sdk` fixture as
  `examples/a2a/...`, which looked like a route-card-only root district payload
  under local root `examples/` even though the
  stronger owner is `aoa-sdk`;
- stale authored path example: `aoa-eval-integrity-check` used generic `fixtures/contract.json` checklist
  wording for target bundles, which looked like a local root or owning-bundle
  path instead of `evals/<family>/<target>/fixtures/contract.json`.

## Options Considered

- Fix the two bundle lines only.
- Let root-authored or decision guards cover bundles.
- Add a source-bundle-specific guard that understands bundle-local paths and
  repo-qualified sibling references.

## Decision

`scripts/validate_repo.py` validates source proof bundles for route residue.

The guard scans authored files under `evals/` with `.md`, `.json`, `.yaml`,
`.yml`, and `.txt` suffixes.

It permits:

- bundle-local paths when the path exists under the owning bundle root;
- repo-root paths that currently exist;
- `evals/<family>/<target>/...` paths;
- repo-qualified sibling refs such as `repo:aoa-sdk/...`;
- root route cards such as `examples/README.md`.

It rejects:

- ambiguous route-card-only root payload paths such as `examples/a2a/...` when
  they do not exist under the owning bundle;
- legacy mechanic parent routes such as `mechanics/agon-proof/` or
  `mechanics/titan-canaries/`.

## Rationale

Bundles should remain self-contained proof objects, but self-contained does not
mean pretending sibling-owned evidence is local. Sibling evidence should be
repo-qualified. Local support artifacts should resolve under the owning bundle.
Target-bundle checklist wording should name `evals/<family>/<target>/...` instead of a
bare root-looking path.

## Consequences

- Bundle source cannot silently revive old root districts after mechanics
  movement.
- Bundle-local fixtures, reports, runners, schemas, and examples remain valid
  when they actually exist under the bundle.
- Sibling evidence remains visible as sibling evidence.

## Boundaries

This decision does not make bundles own sibling artifacts.

It does not forbid bundle-local support paths.

It does not move source proof bundles into mechanics.

It does not treat generated readers as stronger than bundles.

## Validation

- `python -m pytest -q tests/test_validate_repo.py -k source_bundle_route_residue`
- `python scripts/validate_repo.py`
