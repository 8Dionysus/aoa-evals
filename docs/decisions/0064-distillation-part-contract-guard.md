# 0064 Distillation Part Contract Guard

## Status

Accepted.

## Context

`mechanics/distillation/` is the active AoA-aligned parent for eval-side
Distillation proof. The parent README and `PARTS.md` already name the owner
split and stop-lines, but the two active part README files still used a thin
`Boundary` section.

That is risky because Distillation proof touches compost, canon-facing
meaning, runtime candidate mappings, reviewed memory adoption, receipts,
recall inspectability, KAG lift, Experience adoption, and owner-local
acceptance. Without part-local contracts, future edits can turn bounded
provenance or adoption evidence into Tree-of-Sophia canon, memory canon,
runtime promotion, graph lift, bridge-ready truth, or owner acceptance.
In this decision, `ToS canon` is shorthand for Tree-of-Sophia canon, and
receipt publication remains outside the runtime-candidate-adoption part.

## Decision

Require each active Distillation part README to expose:

- `## Inputs`
- `## Outputs`
- `## Stronger Owner Split`
- `## Stop-Lines`
- `## Validation`

The protected parts are:

- `mechanics/distillation/parts/compost-provenance/README.md`
- `mechanics/distillation/parts/runtime-candidate-adoption/README.md`

`compost-provenance` remains bounded provenance-preservation proof, not ToS
canon, principle truth, run-quality proof, or artifact/process comparison.
`runtime-candidate-adoption` remains reviewed candidate-adoption proof, not
memory canon, live memory-ledger behavior, runtime-pack authority, receipt
publication, Experience adoption federation, KAG lift, bridge-ready truth, or
owner-local acceptance.

## Consequences

- Future Distillation part edits must keep owner split and stop-lines explicit.
- Compost and candidate adoption support remain under the `distillation`
  parent instead of becoming proof-adjective parents.
- Memo recall, memo contradiction, confirmed writeback-act integrity, and
  generic Experience adoption remain outside Distillation until separate
  evidence proves a local Distillation operation.
- Runtime candidate evidence remains below bundle-local review and stronger
  owner authority.

## Validation

Expected validation route:

```bash
python -m pytest -q tests/test_validate_repo.py -k distillation_part_readmes
python scripts/validate_repo.py --eval aoa-compost-provenance-preservation
python scripts/validate_repo.py --eval aoa-memo-reviewed-candidate-adoption-integrity
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python -m pytest -q
```
