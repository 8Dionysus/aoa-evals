# AGENTS.md

## Applies to

`mechanics/release-support/legacy/` provenance and lineage files.

## Role

This directory preserves old proof-release and root report placement history
behind the active `release-support` mechanic.

It is not a release procedure, readiness audit, PR handoff, changelog, tag
record, GitHub status source, or place for new release work.

## Read before editing

1. root `AGENTS.md`
2. `mechanics/release-support/AGENTS.md`
3. `mechanics/release-support/README.md`
4. `mechanics/release-support/PARTS.md`
5. `mechanics/release-support/PROVENANCE.md`
6. `docs/RELEASING.md`
7. `docs/LEGACY_NAMING.md`

## Boundaries

- Start from active release-support parts before reading legacy.
- Keep `proof-release` as historical wording, not parent topology.
- Do not recreate root report payloads or `mechanics/proof-release/`.
- Do not treat a legacy note as release publication, PR status, or goal
  completion.

## Validation

```bash
python scripts/validate_repo.py
python scripts/release_check.py
```
