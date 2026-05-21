# Repair Proof Part

## Role

This part owns the support route for bounded repair proof through
`aoa-repair-boundedness`.

This repair-proof route keeps the shared repair fixture family under the
Antifragility mechanic
because AoA antifragility routes repair proof and regression evidence to
`aoa-evals`. The source proof bundle stays under `bundles/`.

## Source Surfaces

- `bundles/aoa-repair-boundedness/EVAL.md`
- `bundles/aoa-repair-boundedness/eval.yaml`
- `bundles/aoa-repair-boundedness/fixtures/contract.json`
- `bundles/aoa-repair-boundedness/runners/contract.json`
- `bundles/aoa-repair-boundedness/reports/summary.schema.json`
- `bundles/aoa-repair-boundedness/reports/example-report.json`
- `mechanics/antifragility/parts/repair-proof/fixtures/repair-boundedness-v1/README.md`

## Inputs

- one repair or reanchor trail;
- one named target seam;
- owner-boundary notes;
- ambiguity before and after the repair move;
- downstream follow-through artifact refs.

## Outputs

- bounded repair-quality verdict;
- repair note per reviewed move;
- ambiguity-reduction note;
- owner handoff route when a repair move requires local execution authority.

## Stronger Owner Split

`Agents-of-Abyss` owns antifragility doctrine and the center meaning of repair
as a proof pressure. The owner repository owns the repair execution, target
object, local rollback, and downstream follow-through. `growth-cycle` owns
diagnosis-gate pressure once cause discipline is being evaluated as growth
cycle behavior.

`aoa-evals` owns bounded repair proof only: claim wording, evidence review,
ambiguity-reduction reading, report interpretation, and the stop-line between
repair quality evidence and owner-object quality.

## Stop-Lines

This part must not claim:

- final owner-object quality proof;
- permanent stability;
- authority widening after a repair;
- that `repair-proof` is a parent mechanic;
- that `aoa-diagnosis-cause-discipline` has been solved or absorbed by this
  package;
- growth-cycle improvement without a separate growth-cycle proof route.

## Validation

```bash
python scripts/validate_repo.py --eval aoa-repair-boundedness
python scripts/build_catalog.py --check
python scripts/validate_repo.py
```
