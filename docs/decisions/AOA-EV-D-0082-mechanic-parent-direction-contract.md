# Mechanic Parent Direction Contract

- Decision ID: AOA-EV-D-0082

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-21
- Surface classes: proof topology
- Mechanic parents: cross-parent
- Guard families: parent and package
- Posture: active rationale

## Context

Mechanic parents need an active current-direction surface between the package
entry card and part-local contracts. Without that surface, future edits can
jump from a package README into parts or legacy without seeing the current
operating contour.

## Decision

Every active mechanic parent must expose `DIRECTION.md`.

`DIRECTION.md` owns the current operating direction, source-of-truth split,
current contour, growth rule, stop-lines, and validation posture for the
parent. It is not `PARTS.md`, not a part map, and not provenance.

Parent `README.md` must expose `## Role`, `## Owned Operation`, `## Validation`,
and `## Next Route` around the entry route. The README is the short package
entry card: it names the operation, points validation to `AGENTS.md#validation`,
and tells the next agent which proof pressure belongs here next.

Parent `README.md` and parent `AGENTS.md` must route `DIRECTION.md` from their
entry route before part growth or legacy lookup.

Legacy remains behind `PROVENANCE.md`. Archive details stay inside the owning
`legacy/` archive.

Validator coverage follows the focused mechanic-parent direction route in
command authority and the nearest `AGENTS.md`.

## Consequences

Future edits encounter active direction before part growth or legacy lookup.
This makes the active route harder to bypass and keeps archive material from
setting current direction directly.

## Current Applicability

As of 2026-05-24:

- Still valid: `DIRECTION.md` owns the current operating direction,
  source-of-truth split, current contour, growth rule, stop-lines, and
  validation posture for each active mechanic parent.
- Changed: parent direction source splits now name `legacy/` as the
  archive-local route opened by `PROVENANCE.md`.
- Changed: parent README and AGENTS entry routes now name `PROVENANCE.md` as
  the active-to-archive bridge for legacy or former-placement lookup.
- Superseded by: no new decision; this is a route-language amendment of the
  same parent direction contract.

## Review Log

### 2026-05-24 - Legacy row made route-positive

- Previous assumption: parent direction files described `legacy/` with
  lineage-only negative role phrases.
- New reality: parent direction files route `legacy/` as the archive-local
  route reached after `PROVENANCE.md`.
- Reason: low-context agents should see the active-to-archive handoff in the
  source-of-truth split before opening parts or legacy.
- Source surfaces updated: `mechanics/*/DIRECTION.md`,
  `scripts/validate_repo.py`, and `tests/test_validate_repo.py`.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

### 2026-05-24 - Parent entry provenance route made positive

- Previous assumption: parent README and AGENTS entry routes treated
  `PROVENANCE.md` as an only-when legacy side path.
- New reality: parent README and AGENTS entry routes name `PROVENANCE.md` as
  the active-to-archive bridge for historical and former-placement lookup.
- Reason: low-context agents should see the provenance handoff as part of the
  active route before opening archive-local legacy details.
- Source surfaces updated: `mechanics/*/README.md`,
  `mechanics/*/AGENTS.md`, one part-local recurrence `AGENTS.md` handoff,
  `scripts/validate_repo.py`, and `tests/test_validate_repo.py`.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.
