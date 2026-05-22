# AGENTS.md

## Applies to

`mechanics/release-support/legacy/` provenance and lineage files.

## Role

This directory preserves old proof-release and root report placement history
behind the active `release-support` mechanic.

## Operating Card

| Field | Route |
| --- | --- |
| role | Provenance and lineage route for former proof-release, root report, readiness, PR handoff, changelog, tag, and GitHub-status placement. |
| input | Old proof-release path, root report path, readiness note, PR handoff, changelog residue, tag record, or historical lookup question. |
| output | Active release-support parent or part route plus any needed `PROVENANCE.md`, `legacy/INDEX.md`, `legacy/DISTILLATION_LOG.md`, or raw accounting update. |
| owner | `mechanics/release-support/` owns current release-support proof work; release procedures and GitHub status route through their active owner surfaces; this legacy district owns archive-local lookup and lineage accounting. |
| next route | `../AGENTS.md`, `../README.md`, `../DIRECTION.md`, `../PARTS.md`, `../PROVENANCE.md`, then `INDEX.md` and `DISTILLATION_LOG.md` for archive detail. |
| tools | Root validators, semantic-agent validator, and release check listed below. |
| validation | Run the Validation commands after route-card, provenance, index, log, or raw changes. |

## Read before editing

1. root `AGENTS.md`
2. `mechanics/release-support/AGENTS.md`
3. `mechanics/release-support/README.md`
4. `mechanics/release-support/PARTS.md`
5. `mechanics/release-support/PROVENANCE.md`
6. `docs/RELEASING.md`
7. `docs/LEGACY_NAMING.md`

## Route Rules

- Start from active release-support parts before reading legacy.
- Keep `proof-release` as historical wording that maps back to active
  release-support topology.
- Place current root report payloads, release procedure, readiness audit, PR
  handoff, changelog, tag, and GitHub status work in the active owner surface.
- Treat legacy notes as provenance for old placement and release-support
  lineage.

## Validation

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
python scripts/release_check.py
```

## Closeout

Report which release-support legacy source was mapped, which active part owns
the current route, which archive accounting changed, and which checks ran.
