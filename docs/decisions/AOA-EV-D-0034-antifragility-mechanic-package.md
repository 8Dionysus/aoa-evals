# Antifragility Mechanic Package

- Decision ID: AOA-EV-D-0034

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-21
- Surface classes: mechanic package
- Mechanic parents: antifragility
- Guard families: none
- Posture: active rationale

## Context

The antifragility evidence cluster was already present across local root
districts:

- `evals/stress/aoa-antifragility-posture/EVAL.md`
- `evals/comparison/longitudinal-window/aoa-stress-recovery-window/EVAL.md`
- `evals/workflow/aoa-repair-boundedness/EVAL.md`
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

Source proof bundles stay under `evals/`. The stress-recovery comparison
readout remains under `mechanics/comparison-spine/`. Runtime-chaos selected
evidence remains under `mechanics/audit/`. `aoa-diagnosis-cause-discipline`
stays a source proof bundle under `evals/` and later decision `0037` routes
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

## Current Applicability

As of 2026-05-24:

- Still valid: `mechanics/antifragility/` remains the AoA-aligned eval-side
  parent for posture review, stress-recovery windows, and bounded repair proof.
- Changed: parent-level boundary coverage now uses pressure-to-owner routes in
  `README.md`, `PARTS.md`, and `DIRECTION.md`, with validator tokens guarding
  the parent route rows.
- Superseded by: none.

## Review Log

### 2026-05-24 - Parent boundary route wording

- Previous assumption: parent-level Antifragility surfaces expressed boundaries
  through exclusion prose around global resilience, runtime self-healing,
  one-score health, deletion/cleanup authority, generated or memo overread, and
  diagnosis/growth-cycle pressure.
- New reality: the parent route keeps the same authority split through
  pressure-to-owner-route rows.
- Reason: AoA center doctrine keeps antifragility law and owner-request
  vocabulary, while `aoa-evals` keeps bounded proof reading; the active package
  should show the next owner route directly.
- Source surfaces updated: `mechanics/antifragility/README.md`,
  `mechanics/antifragility/PARTS.md`, `mechanics/antifragility/DIRECTION.md`,
  and `scripts/validate_repo.py`.
- Validation: `python -m pytest -q tests/test_validate_repo.py -k
  antifragility`, `python scripts/validate_repo.py --eval
  aoa-antifragility-posture`, `python scripts/validate_repo.py --eval
  aoa-stress-recovery-window`, `python scripts/validate_repo.py --eval
  aoa-repair-boundedness`, `python scripts/validate_repo.py`, `python
  scripts/validate_semantic_agents.py`, `python scripts/build_catalog.py
  --check`, `git diff --check`, and `python -m pytest -q`.

## Validation

Expected validation route:

```bash
python scripts/validate_repo.py --eval aoa-antifragility-posture
python scripts/validate_repo.py --eval aoa-stress-recovery-window
python scripts/validate_repo.py --eval aoa-repair-boundedness
python scripts/build_catalog.py --check
python scripts/validate_repo.py
```
