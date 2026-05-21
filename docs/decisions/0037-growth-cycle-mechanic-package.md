# 0037 Growth-cycle Mechanic Package

## Status

Accepted.

## Context

The Growth Cycle evidence pass found one active eval-side operation and several
nearby deferred pressures.

The active operation is diagnosis-cause discipline:

- `evals/workflow/aoa-diagnosis-cause-discipline/EVAL.md`
- `evals/workflow/aoa-diagnosis-cause-discipline/eval.yaml`
- `evals/workflow/aoa-diagnosis-cause-discipline/notes/diagnosis-contract.md`
- `evals/workflow/aoa-diagnosis-cause-discipline/examples/example-report.md`
- `evals/workflow/aoa-diagnosis-cause-discipline/checks/eval-integrity-check.md`
- `mechanics/method-growth/PARTS.md` already deferred this bundle toward
  `growth-cycle/diagnosis-gate`

The nearby pressures are real but not active Growth Cycle parts yet:

- `aoa-repair-boundedness` already routes through
  `mechanics/antifragility/parts/repair-proof/`
- `aoa-longitudinal-growth-snapshot` and repeated-window readouts already
  route through `mechanics/comparison-spine/parts/longitudinal-window/`
- RPG progression and unlock proof already routes through
  `mechanics/rpg/parts/progression-unlocks/`
- reviewed closeout and donor harvest evidence is currently quest or ingress
  pressure, not a part-local Growth Cycle proof operation

`Agents-of-Abyss` names `growth-cycle` as the center mechanic for checkpoint,
reviewed closeout, donor harvest, progression, route choice, automation,
diagnosis, repair, quest promotion, and owner followthrough. On the eval side,
that does not mean every center stage becomes a package part immediately.

## Decision

Create `mechanics/growth-cycle/` as an AoA-aligned package with one active
part:

- `diagnosis-gate`

Source proof bundles stay under `evals/`. No root file movement is performed
in this slice.

Repair, progression-lift, reviewed-closeout-chain, donor-harvest,
quest-promotion, and owner-followthrough remain deferred until local eval-side
evidence proves a real proof operation with inputs, outputs, owner split,
stop-lines, and validation.

The package routes diagnosis proof support only; it does not claim repair
success, final owner-object quality, broad growth, owner acceptance, memory
canon, runtime activation, or quest promotion.

Deferred pressure is mapped inside the owning legacy archive after the active
`mechanics/growth-cycle/PROVENANCE.md` bridge.

## Consequences

- The active parent name is AoA-compatible: `growth-cycle`.
- Diagnosis-cause discipline is a `diagnosis-gate` part, not a
  `diagnosis-proof` parent.
- Source proof bundles remain the strongest local proof meaning.
- Repair proof stays under `antifragility`; longitudinal movement stays under
  `comparison-spine`; RPG progression and unlock proof stays under `rpg`.
- Closeout, harvest, quest, and owner-followthrough pressure remains visible
  without becoming active package topology too early.
- Validators can require the active `growth-cycle` route and prevent future
  broadening without route cards.

## Validation

Expected validation route:

```bash
python scripts/validate_repo.py --eval aoa-diagnosis-cause-discipline
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
