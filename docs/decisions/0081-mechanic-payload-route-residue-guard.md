# Mechanic Payload Route Residue Guard

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/`

## Context

The mechanics refactor already guards active mechanics route cards and part
READMEs, but route cards are not the only authored mechanics surface. Active
mechanics payload also lives in fixtures, schemas, manifests, examples,
scripts, tests, and other part-local files.

During the recursor-boundary payload audit, readiness fixtures still named a
stale authored path example: `config/codex_subagent_wiring.v2.json` as if it
were local `aoa-evals` payload. The stronger owner is `aoa-agents`, where
`repo:aoa-agents/config/codex_subagent_wiring.v2.json` is current Codex
projection wiring.
The portable-proof beacon hook also still watched `examples/runtime/*.json`
and `docs/real-runs/*runtime*`: the first was a route-card-only root district
payload route, and the second was an unresolved root-authored docs glob instead
of active selected-evidence packet routes or repo-qualified sibling evidence.
Later Agon recurrence manifests still carried root-authored docs globs such as
`docs/AGON_*.md` after those docs had moved behind the Agon mechanic.
Another Agon manifest used bare `schemas/...` route-card-only district paths
inside structured `observed_surfaces` even though the schema files were
part-local.

## Options Considered

- Fix the discovered payload references only.
- Expand the active mechanic route-card guard to scan every mechanics file.
- Add a mechanics-payload-specific guard that understands part-local paths,
  active repo paths, root route cards, and repo-qualified sibling refs.

## Decision

`scripts/validate_repo.py` now validates active mechanics payload route
residue separately from mechanics route cards.

The guard scans active files under `mechanics/` with `.json`, `.md`, `.py`,
`.txt`, `.yaml`, and `.yml` suffixes. It skips `legacy/`, `generated/`, and
route-card files already owned by other guards.

It permits:

- part-local paths when they resolve under the same mechanic or part root;
- active repo paths that currently exist;
- repo-qualified sibling refs such as `repo:aoa-agents/...`;
- root route cards such as `config/README.md`.

It rejects:

- route-card-only root district payload paths such as `config/...` or
  `examples/...` when they do not resolve locally;
- route-card-only root district payload paths such as `schemas/...` inside
  structured manifest route fields;
- unresolved root-authored docs globs such as `docs/real-runs/*runtime*` or
  `docs/AGON_*.md` inside active mechanic manifests;
- legacy mechanic parent routes such as `mechanics/agon-proof/` and
  `mechanics/titan-canaries/`.

## Rationale

Mechanics payload is where proof behavior actually runs or is exercised. If
payload keeps old root paths after the topology moves, future refactors will
not merely show stale documentation; they will execute, score, or inspect the
wrong owner boundary.

The guard stays narrower than a whole-repo string police pass. It only covers
active mechanics payload and allows local part topology, active repo topology,
and explicit sibling ownership.

## Consequences

- Active mechanics payload cannot silently revive old root districts.
- Sibling-owned evidence must stay visible as sibling-owned evidence.
- Route cards, generated readers, source bundles, decisions, and repo config
  remain covered by their own guards instead of one overbroad rule.

## Boundaries

This decision does not make `aoa-evals` own `aoa-agents` Codex projection
wiring, `abyss-stack` runtime truth, or `aoa-playbooks` real-run provenance.

It does not forbid legacy lookup inside `legacy/` surfaces.

It does not move source proof bundles into mechanics.

It does not treat generated surfaces as stronger than authored payload.

## Validation

- `python -m pytest -q tests/test_validate_repo.py -k mechanic_payload_route_residue`
- `python scripts/validate_repo.py`
