# RPG Distillation Log

## 2026-05-20

Distilled the first RPG proof cluster into an AoA-aligned
`mechanics/rpg/` package.

Active part:

- `progression-unlocks` for route-scoped progression evidence and bounded
  unlock proof.

Former root progression and unlock support surfaces moved behind the active
part:

- `docs/PROGRESSION_EVIDENCE_MODEL.md`
- `docs/UNLOCK_PROOF_BRIDGE.md`
- `schemas/progression_evidence.schema.json`
- `schemas/unlock_proof_catalog.schema.json`
- `examples/progression_evidence.example.json`
- `generated/unlock_proof_cards.min.example.json`

Quest source records stayed under `quests/`. Growth-cycle diagnosis later
routed through active `growth-cycle/diagnosis-gate`; repair, harvest, closeout,
and longitudinal movement stayed outside RPG for their current owner routes or
future evidence passes.
