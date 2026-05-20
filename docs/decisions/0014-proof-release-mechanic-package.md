# 0014 Proof Release Mechanic Package

- Status: Accepted
- Date: 2026-05-19
- Owner surface: `mechanics/proof-release/`

## Context

`aoa-evals` already has release discipline in `docs/RELEASING.md`, public
release narrative in `CHANGELOG.md`, a local release audit script in
`scripts/release_check.py`, and GitHub `Repo Validation` wired through
`.github/workflows/repo-validation.yml`.

That route has real validation pressure: release work can touch bundles, docs,
schemas, generated surfaces, sibling refs, mechanics packages, and GitHub
publication. Without a package route, future agents can confuse a green release
audit with stronger proof meaning, or confuse release notes with bundle-local
verdict authority.

## Options Considered

- Leave release work in `docs/RELEASING.md`, `CHANGELOG.md`,
  `scripts/release_check.py`, and GitHub workflow files only.
- Move release docs, checks, and workflow files under a mechanics package.
- Create `mechanics/proof-release/` as a route package while leaving release
  docs, changelog, check scripts, and GitHub workflow files in place.

## Decision

Create `mechanics/proof-release/` for the operation:

`bounded release scope -> changelog narrative -> release audit -> Repo Validation -> tag and GitHub release notes -> post-release proof posture`

The package routes release proof publication without moving `docs/RELEASING.md`,
`CHANGELOG.md`, `scripts/release_check.py`, `.github/`, generated surfaces, or
source proof bundles.

## Rationale

Release publication is a real proof-layer operation because it decides what
public state readers and downstream agents will trust as a coherent shipped
surface. It needs a route that keeps scope, changelog narrative, generated
freshness, release audit, GitHub validation, and tag/release-note posture
together.

The package also preserves the key boundary: release checks can prove that the
release package is coherent, but they do not decide the truth of each eval
claim. Bundle-local proof objects, report contracts, and review guides remain
stronger than release notes.

## Consequences

- Positive: release-prep work now has a package route and validator-backed
  discovery surface.
- Tradeoff: the package does not own GitHub automation or changelog content; it
  routes them. Future maintainers must still read `.github/AGENTS.md` and
  `docs/RELEASING.md` for exact local law.
- Follow-up: later validators can tighten release title, changelog section, and
  generated-surface parity checks if release drift appears.

## Boundaries

This decision does not create a tag, publish a GitHub Release, move release
surfaces, or alter CI behavior.

It does not make `CHANGELOG.md`, GitHub release notes, Git tags, or
`scripts/release_check.py` stronger than bundle-local `EVAL.md`, `eval.yaml`,
reports, schemas, and review docs.

It does not authorize repo-prefixed release titles, broad release batches,
status promotion by changelog, validation weakening, sibling mutation, or
release notes that overstate proof claims.

## Validation

- `mechanics/proof-release/README.md` names the owned operation, source
  surfaces, inputs, outputs, stronger-owner split, boundaries, validation, and
  next route.
- `mechanics/proof-release/AGENTS.md` names local editing law.
- `mechanics/README.md`, `docs/PROOF_TOPOLOGY.md`, `README.md`,
  `docs/README.md`, `ROADMAP.md`, `CHANGELOG.md`, and
  `docs/decisions/README.md` route to the package.
- `python scripts/validate_repo.py`
- `python scripts/validate_semantic_agents.py`
- `python scripts/release_check.py`
