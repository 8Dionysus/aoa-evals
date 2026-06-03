# RPG Progression-unlocks Contract

- Decision ID: AOA-EV-D-0067

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-21
- Surface classes: proof topology
- Mechanic parents: rpg
- Guard families: none
- Posture: active rationale

## Context

`mechanics/rpg/` is the active AoA-aligned parent for eval-side RPG proof. The
`progression-unlocks` part owns progression evidence and unlock proof support:
docs, schemas, examples, generated example cards, and quest source references.

The parent README and `PARTS.md` already name owner split and stop-lines, but
the part README still used a thin `Boundary` paragraph. That is risky because
progression and unlock language can easily become rank assignment, quest
completion, skill truth, role truth, playbook truth, hidden reward logic,
runtime equip state, or broad growth proof.

## Decision

Require `mechanics/rpg/parts/progression-unlocks/README.md` to expose:

- `## Inputs`
- `## Outputs`
- `## Stronger Owner Split`
- `## Stop-Lines`
- `## Validation`

`progression-unlocks` remains a part under `rpg`, not an RPG parent
substitute, growth-cycle claim, quest acceptance gate, runtime equip route, or
proof-adjective parent.

## Consequences

- Future RPG part edits must keep owner split and stop-lines explicit.
- Quest source records stay under `quests/`, and generated unlock cards remain
  derived navigation only.
- Role, rank, skill, technique, playbook, party, campaign, quest, runtime, and
  stats truth remain with stronger owners.
- Diagnosis, repair, harvest, closeout, and longitudinal movement remain
  outside this part until separate eval-side evidence proves their active
  routes.

## Current Applicability

As of 2026-05-24:

- Still valid: `progression-unlocks` remains the active RPG part for bounded
  progression evidence and unlock proof support.
- Changed: the required `## Stop-Lines` section now acts as a
  pressure-to-owner route map for quest, rank, role, skill, playbook, runtime,
  generated-card, growth-cycle, and stats pressure; quest pressure uses the
  quest source owner and questbook lifecycle route, and runtime pressure uses
  the runtime route after owner gates.
- Superseded by: none.

## Review Log

### 2026-05-24 - Progression-unlocks owner-route map

- Previous assumption: the part contract could remain clear by listing the
  claims outside the local proof operation.
- New reality: the part README now routes each pressure class to the owner
  surface that can carry it, while keeping proof wording, schemas, examples,
  cautions, and claim limits in `aoa-evals`.
- Reason: an agent entering through `progression-unlocks` needs the next owner
  route immediately: quest owners for acceptance, `aoa-agents` for rank and
  role, `aoa-skills` and `aoa-techniques` for ability and feat truth,
  `aoa-playbooks` for campaign and party method, `abyss-stack` for runtime
  state, `aoa-stats` for derived summaries, and comparison/growth mechanics
  for broad movement claims.
- Source surfaces updated:
  `mechanics/rpg/parts/progression-unlocks/README.md`,
  `mechanics/rpg/parts/progression-unlocks/docs/PROGRESSION_EVIDENCE_MODEL.md`,
  `mechanics/rpg/parts/progression-unlocks/docs/UNLOCK_PROOF_BRIDGE.md`, and
  `scripts/validate_repo.py`.
- Validation: `python -m pytest -q tests/test_mechanic_surface_contracts.py -k rpg_progression_unlocks`,
  `python scripts/validate_repo.py`, `python scripts/build_catalog.py --check`,
  `python scripts/validate_semantic_agents.py`, and full pytest are the
  expected checks for this slice.

## Validation

Expected validation route:

```bash
python -m pytest -q tests/test_mechanic_surface_contracts.py -k rpg_progression_unlocks
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python scripts/validate_semantic_agents.py
python -m pytest -q
```
