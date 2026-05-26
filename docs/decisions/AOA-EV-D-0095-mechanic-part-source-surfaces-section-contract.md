# Mechanic Part Source Surfaces Section Contract

- Decision ID: AOA-EV-D-0095
- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/README.md`

## Index Metadata

- Original date: 2026-05-20
- Surface classes: mechanic part
- Mechanic parents: cross-parent
- Guard families: part and payload
- Posture: active rationale

## Context

The source-surface reference guard validates path-like refs inside a concrete
part README `## Source Surfaces` section. That leaves an escape hatch: a part
can use `## Source Surface`, `## Active Surfaces`, or a path list inside
`## Role`, and the source refs will look active to a reader while bypassing the
standard source-surface guard.

This matters because the mechanics refactor is about proof anatomy, not just
file movement. A part without the same source-surface section shape is easier
to overread, easier to leave stale, and harder to audit across all active
parents.

## Decision

Every concrete `mechanics/<parent>/parts/<part>/README.md` must expose a
plural `## Source Surfaces` section with at least one path-like source ref.

`scripts/validate_repo.py` rejects:

- a missing plural section;
- not `## Source Surface`: a singular section does not satisfy the contract;
- not `## Active Surfaces`: an active-surface substitute does not satisfy the
  contract;
- an empty `## Source Surfaces` section with no path-like source ref.

The source refs themselves remain governed by the separate Mechanic Part Source
Surface Reference Guard.

## Rationale

The plural section name gives future agents one predictable place to inspect
what makes a part real. It also keeps the validator honest: source-surface refs
cannot hide in prose or in a near-miss heading after files move.

The section is a route surface, not an authority upgrade. It points to sources
that the part receives or owns; it does not make the part stronger than bundles,
generated builders, sibling repos, GitHub state, live receipts, or legacy
archive lineage.

## Consequences

- Positive: every part has the same source-surface entry point.
- Positive: old root paths cannot survive by being listed under `## Role` or
  `## Active Surfaces`.
- Positive: audits can compare all active parts without bespoke heading rules.
- Tradeoff: adding or reshaping a part now requires naming at least one real
  source surface immediately.

## Boundaries

This decision does not require every source surface to live under the part.
Some parts legitimately cite source bundles, generated readers, root release
entrypoints, quest records, or repo-qualified sibling refs.

It does not create new parent mechanics, move source proof bundles out of
`evals/`, or make `Source Surfaces` active legacy archive routing.

## Validation

```bash
python -m pytest -q tests/test_validate_repo.py -k mechanic_part_source_surfaces_section
python scripts/validate_repo.py
```
