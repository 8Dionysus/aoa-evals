# Mechanic Legacy Single Bridge

- Decision ID: AOA-EV-D-0089
- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/README.md`

## Index Metadata

- Original date: 2026-05-20
- Surface classes: legacy/provenance, boundary/runtime/sibling
- Mechanic parents: cross-parent
- Guard families: legacy and provenance, sibling and boundary
- Posture: legacy/provenance rationale

## Context

Legacy in AoA mechanics is important archive flesh, not an active route.

The active mechanic should begin from `README.md`, `DIRECTION.md`, `PARTS.md`,
parts, owner split, stop-lines, and validation. `PROVENANCE.md` is the single controlled bridge from active mechanic surfaces into the legacy archive.

The previous evals wording let some active surfaces point directly at archive
internals. That makes the archive feel like a normal working surface and
invites future edits to bypass distillation.

## Decision

Active mechanic surfaces must route legacy lookup through `PROVENANCE.md`.

`scripts/validate_repo.py` rejects direct archive-internal references from
active package surfaces outside `PROVENANCE.md` and outside the legacy archive
itself, including Markdown, JSON, YAML, and part-local Python surfaces.

`PROVENANCE.md` remains allowed to open the archive, but it must not carry archive details. Legacy files remain allowed to explain their own archive
layout.

## Rationale

The topology should stay convex: active work has one visible bridge into
history, and history stays detailed without becoming a second active spine.

This keeps old names, wave material, root placement notes, and raw receipts
recoverable while preventing them from steering current mechanics work.

## Consequences

- Positive: active package cards stay short and present-tense.
- Positive: legacy remains auditable without becoming a new-work entrypoint.
- Positive: future movement cannot accidentally normalize archive-internal
  links in active route cards, manifests, hooks, or part-local helpers.
- Tradeoff: when a legacy source matters, the maintainer must cross the
  provenance bridge first.

## Boundaries

This decision does not delete legacy, weaken raw lineage, or remove archive
accounting.

It does not replace raw-payload accounting, provenance entry checks, part maps,
or part-local validation.

## Validation

```bash
python -m pytest -q tests/test_validate_repo.py -k mechanic_legacy_single_bridge
python scripts/validate_repo.py
```
