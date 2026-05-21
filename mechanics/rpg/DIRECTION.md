# RPG Direction

RPG in `aoa-evals` should make progression and unlock proof bounded,
multi-axis, and owner-reviewable without becoming a universal rank or equip
system.

This file owns the current operating direction only. It does not replace the
entry card, part map, part contracts, source bundles, decisions, or provenance
bridge.

## Source-of-truth split

- `README.md`: package entry card and shortest proof-side route.
- `DIRECTION.md`: current operating direction.
- `PARTS.md`: active RPG part map.
- `parts/`: progression-unlocks support.
- `PROVENANCE.md`: controlled bridge from active route to old progression and unlock placement.
- `legacy/`: lineage only; not a rank ledger.
- `quests/`: source obligations that remain weaker than owner acceptance.

## Current contour

- Keep the parent name `rpg`; progression and unlock support are parts.
- Keep evidence multi-axis and route-scoped.
- Keep generated unlock cards derived and example-level until owner review.
- Keep role truth, skill truth, playbook truth, runtime equip state, and stats
  outside this mechanic.

## Growth rule

Add RPG parts only when a repeated proof operation concerns progression,
unlock, equipment posture, or quest-facing RPG evidence with its own validation
and owner split.

## Stop-lines

- Do not claim universal score, automatic rank, quest acceptance, role/skill/
  playbook authority, runtime equip state, or broad capability growth.
- Do not let generated cards become unlock authority.

## Validation

Use the validation lane in [mechanics/rpg/AGENTS.md](AGENTS.md#validation).
