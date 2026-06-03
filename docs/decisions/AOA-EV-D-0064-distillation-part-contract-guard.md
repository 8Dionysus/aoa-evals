# Distillation Part Contract Guard

- Decision ID: AOA-EV-D-0064

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-21
- Surface classes: mechanic part, validation guard
- Mechanic parents: distillation
- Guard families: part and payload
- Posture: active guard rationale

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

## Current Applicability

As of 2026-05-24:

- Still valid: active Distillation part README files expose inputs, outputs,
  stronger owner split, stop-lines, and validation route markers.
- Changed: active Distillation part README files express stop-line coverage as
  owner-route pressure, and part-specific validator tokens guard full
  pressure-to-owner-route rows.
- Superseded by: none.

## Review Log

### 2026-05-24 - Distillation part boundary route wording

- Previous assumption: compost-provenance and runtime-candidate-adoption part
  contracts used direct exclusion prose to keep stronger owner authority outside
  the part.
- New reality: those part contracts keep the same authority boundary through
  pressure-to-owner-route tables whose full owner-route rows are validator
  guarded.
- Reason: low-context agents can follow concrete ToS, memo, runtime, receipt,
  KAG, comparison, and owner handoffs from the table without interpreting dense
  exclusion prose.
- Source surfaces updated:
  `mechanics/distillation/parts/compost-provenance/README.md`,
  `mechanics/distillation/parts/runtime-candidate-adoption/README.md`, and
  `scripts/validate_repo.py`.
- Validation: `python -m pytest -q tests/test_validate_repo.py -k
  distillation_part_readmes`, bundle-local distillation eval checks,
  `python scripts/validate_repo.py`, and
  `python scripts/validate_semantic_agents.py`.

## Validation

Expected validation route:

```bash
python -m pytest -q tests/test_mechanic_surface_contracts.py -k distillation_part_readmes
python scripts/validate_repo.py --eval aoa-compost-provenance-preservation
python scripts/validate_repo.py --eval aoa-memo-reviewed-candidate-adoption-integrity
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python -m pytest -q
```
