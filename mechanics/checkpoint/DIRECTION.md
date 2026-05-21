# Checkpoint Direction

Checkpoint in `aoa-evals` should make return, restart, and self-agent
checkpoint pressure reviewable as bounded proof without implementing checkpoint
runtime or memory canon.

This file owns the current operating direction only. It does not replace the
entry card, part map, part contracts, source bundles, decisions, or provenance
bridge.

## Source-of-truth split

- `README.md`: package entry card and shortest proof-side route.
- `DIRECTION.md`: current operating direction.
- `PARTS.md`: active checkpoint part map.
- `parts/`: A2A summon-return, restartable-inquiry, and self-agent posture
  support.
- `PROVENANCE.md`: controlled bridge from active route to old checkpoint placement.
- `legacy/`: lineage only; not a checkpoint implementation backlog.
- `bundles/`: source proof objects that remain stronger than support parts.

## Current contour

- Keep the parent name `checkpoint`; summon-return, restartable inquiry, and
  self-agent posture are parts.
- Keep checkpoint evidence bounded to reviewed artifacts, return plans,
  health/approval records, and owner refs.
- Keep memo writeback and checkpoint object truth with `aoa-memo`.
- Keep runtime dry-run and return behavior with runtime owners.

## Growth rule

Add a checkpoint part only when a repeated checkpoint proof operation has its
own support payload and validation. Do not split parts around every artifact
name that happens to include checkpoint language.

## Stop-lines

- Do not claim checkpoint implementation authority, memory canon, runtime
  activation, or automatic self-agent continuity.
- Do not use checkpoint proof posture to bypass approval, rollback, or owner
  review.

## Validation

Use the validation lane in [mechanics/checkpoint/AGENTS.md](AGENTS.md#validation).
