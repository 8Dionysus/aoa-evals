# 0036 RPG Mechanic Package

## Status

Accepted.

## Context

The RPG evidence cluster entered the refactor through former root and quest
surfaces:

- `docs/PROGRESSION_EVIDENCE_MODEL.md`
- `docs/UNLOCK_PROOF_BRIDGE.md`
- former root `schemas/progression_evidence.schema.json`
- former root `schemas/unlock_proof_catalog.schema.json`
- former root `examples/progression_evidence.example.json`
- former root `generated/unlock_proof_cards.min.example.json`
- `quests/proof/captured/AOA-EV-Q-0005.yaml`
- `quests/unlock/triaged/AOA-EV-Q-0009.yaml`
- validator and test coverage in `scripts/validate_repo.py` and
  `tests/test_validate_repo.py`

`Agents-of-Abyss` names `rpg` as the center mechanic for readable progression,
quest-linked work, campaigns, skills, feats, and public presentation without
taking truth from stronger owners. Its `progression-unlocks` part routes proof
questions to `aoa-evals`.

The eval-side parent must therefore be `rpg`, not `rpg-proof`,
`progression-proof`, or `unlock-proof`.

## Decision

Create `mechanics/rpg/` as an AoA-aligned package with one active part:

- `progression-unlocks`

Progression evidence docs, unlock proof docs, schemas, examples, and generated
example cards move behind the active part. Quest source records stay under
`quests/`, and generated quest projections continue to mirror quest source records.

`growth-cycle` remains deferred. Diagnosis-cause discipline, repair boundedness,
harvest pressure, closeout ingress, and longitudinal movement still overlap
with `method-growth`, `antifragility`, and `comparison-spine`; they need a
separate evidence pass before an active parent exists.

Former root progression and unlock paths are mapped inside the owning legacy
archive after the active `mechanics/rpg/PROVENANCE.md` bridge.

## Consequences

- The active parent name is AoA-compatible: `rpg`.
- Progression evidence and unlock proof are parts/support surfaces, not parent
  mechanics.
- Old root paths remain traceable through provenance instead of steering active
  topology.
- Source quest records remain in the quest lane and generated quest readers
  remain derived.
- RPG proof support does not grant runtime equip state.
- Validators can reject recreation of old root progression/unlock support
  paths.

## Current Applicability

As of 2026-05-24:

- Still valid: `mechanics/rpg/` remains the AoA-aligned eval-side parent for
  bounded progression evidence and unlock proof support.
- Changed: active RPG route surfaces now express rank, quest, generated-card,
  runtime, stats, and broad-growth pressure as a pressure-to-owner route map
  instead of relying on exclusion prose.
- Superseded by: none.

## Review Log

### 2026-05-24 - RPG boundary routes

- Previous assumption: the parent and part surfaces could keep RPG authority
  limits readable as explicit stop-line prose.
- New reality: the active route now uses owner-route rows so an agent can move
  from pressure to owner, source surface, and validation path in one pass.
- Reason: RPG terms cross center reflection, proof, roles, skills, techniques,
  playbooks, quests, runtime, and stats; pressure-to-owner routing keeps the
  eval-side proof operation legible without turning the decision into a live
  route article.
- Source surfaces updated: `mechanics/rpg/README.md`,
  `mechanics/rpg/DIRECTION.md`, `mechanics/rpg/PARTS.md`,
  `mechanics/rpg/parts/progression-unlocks/README.md`,
  `mechanics/rpg/parts/progression-unlocks/docs/PROGRESSION_EVIDENCE_MODEL.md`,
  `mechanics/rpg/parts/progression-unlocks/docs/UNLOCK_PROOF_BRIDGE.md`, and
  `scripts/validate_repo.py`.
- Validation: RPG validator focus, unlock/progression surface validation,
  catalog check, semantic AGENTS validation, diff whitespace check, and full
  pytest are the expected checks for this slice.

## Validation

Expected validation route:

```bash
python scripts/build_catalog.py
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
