# 0034 Antifragility Mechanic Package

## Status

Accepted.

## Context

The antifragility evidence cluster was already present across local root
districts:

- `bundles/aoa-antifragility-posture/EVAL.md`
- `bundles/aoa-stress-recovery-window/EVAL.md`
- `bundles/aoa-repair-boundedness/EVAL.md`
- former root stress-window docs, shared fixture families, and repo-level
  schemas
- runtime-chaos selected evidence under `mechanics/audit/`
- stress-recovery paired readout under `mechanics/comparison-spine/`

`Agents-of-Abyss` names `antifragility` as the center mechanic and assigns
repair proof and regression evidence to `aoa-evals`. The eval-side parent must
therefore be `antifragility`, not a proof-adjective package and not a repair
package.

## Decision

Create `mechanics/antifragility/` as an AoA-aligned package with three active
parts:

- `posture-review`
- `stress-recovery-window`
- `repair-proof`

Source proof bundles stay under `bundles/`. The stress-recovery comparison
readout remains under `mechanics/comparison-spine/`. Runtime-chaos selected
evidence remains under `mechanics/audit/`. `aoa-diagnosis-cause-discipline`
stays a source proof bundle under `bundles/` and later decision `0037` routes
it through active `growth-cycle/diagnosis-gate`.

Former root docs, fixtures, and schemas move behind the active package route
and are mapped inside the owning legacy archive after the active
`mechanics/antifragility/PROVENANCE.md` bridge.

## Consequences

- The active parent name is AoA-compatible: `antifragility`.
- Repair proof is a part, not a parent mechanic.
- Comparison and audit boundaries stay visible instead of being absorbed by
  the antifragility package.
- Legacy names preserve old root placement without steering new topology.
- Validators can reject recreation of the old root support paths.

## Validation

Expected validation route:

```bash
python scripts/validate_repo.py --eval aoa-antifragility-posture
python scripts/validate_repo.py --eval aoa-stress-recovery-window
python scripts/validate_repo.py --eval aoa-repair-boundedness
python scripts/build_catalog.py --check
python scripts/validate_repo.py
```
