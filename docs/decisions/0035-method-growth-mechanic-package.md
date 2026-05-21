# 0035 Method-growth Mechanic Package

## Status

Accepted.

## Context

The method-growth evidence cluster was already present across local root
districts:

- `evals/capability/aoa-candidate-lineage-integrity/EVAL.md`
- `evals/boundary/aoa-owner-fit-routing-quality/EVAL.md`
- former root shared fixture families `fixtures/candidate-lineage-v1/` and
  `fixtures/owner-fit-routing-v1/`
- bundle-local fixture contracts, runner contracts, report schemas, and
  example reports
- generated catalog, capsule, and section readers derived from those contracts
- `EVAL_SELECTION.md`, `ROADMAP.md`, and `CHANGELOG.md` growth-refinery
  wording

`Agents-of-Abyss` names `method-growth` as the center mechanic for turning
repeated work into reviewable owner-shaped routes without claiming final object
truth. The eval-side parent must therefore be `method-growth`, not
`growth-refinery`, `candidate-lineage`, or a proof-adjective package.

## Decision

Create `mechanics/method-growth/` as an AoA-aligned package with two active
parts:

- `candidate-lineage`
- `owner-landing`

Source proof bundles stay under `evals/`. The shared fixture families move
behind the active parts, and bundle-local contracts point at the part-local
fixture paths.

`aoa-diagnosis-cause-discipline` remains a source proof bundle under
`evals/` and later decision `0037` routes it through active
`growth-cycle/diagnosis-gate`. `aoa-repair-boundedness` remains under
`mechanics/antifragility/parts/repair-proof/`. RPG progression and unlock
surfaces later route through `mechanics/rpg/parts/progression-unlocks/`.

The method-growth package routes proof support only; it does not claim final owner-object truth.

Former root fixture paths are mapped inside the owning legacy archive after
the active `mechanics/method-growth/PROVENANCE.md` bridge.

## Consequences

- The active parent name is AoA-compatible: `method-growth`.
- Candidate lineage and owner-fit routing are parts, not parent mechanics.
- Source proof bundles remain the strongest local proof meaning.
- Legacy fixture paths preserve old placement without steering new topology.
- Validators can reject recreation of the old root fixture paths.

## Validation

Expected validation route:

```bash
python scripts/validate_repo.py --eval aoa-candidate-lineage-integrity
python scripts/validate_repo.py --eval aoa-owner-fit-routing-quality
python scripts/build_catalog.py --check
python scripts/validate_repo.py
```
