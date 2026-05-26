# Growth-cycle Diagnosis-gate Contract

- Decision ID: AOA-EV-D-0065

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-21
- Surface classes: proof topology
- Mechanic parents: growth-cycle
- Guard families: none
- Posture: active rationale

## Context

`mechanics/growth-cycle/` is deliberately narrow. The active eval-side
operation is `diagnosis-gate` for `aoa-diagnosis-cause-discipline`; repair,
progression, closeout, harvest, quest promotion, and owner followthrough remain
outside the package until separate evidence proves active parts.

The package README and `PARTS.md` already preserve this route, but the
`diagnosis-gate` part README still used a thin `Boundary` section instead of
explicit `Stronger Owner Split` and `Stop-Lines`.

## Decision

Require `mechanics/growth-cycle/parts/diagnosis-gate/README.md` to expose:

- an eval-backed thin support route statement when it has no part-local
  payload subdirectories;
- `## Inputs`
- `## Outputs`
- `## Stronger Owner Split`
- `## Stop-Lines`
- `## Validation`

`diagnosis-gate` remains a cause-hypothesis discipline part. It does not become
a repair parent, owner-fit proof route, final object-quality proof, broad growth
score, reviewed-closeout chain, donor-harvest approval, quest-promotion
gate, memory canon, runtime activation, or owner-local landing authority.
The explicit broad growth score stop-line is part of this contract.

## Consequences

- Future Growth Cycle edits must keep diagnosis before repair as a proof
  boundary, not a broad growth claim.
- Repair proof remains under `mechanics/antifragility/parts/repair-proof/`.
- Repeated-window movement remains under
  `mechanics/comparison-spine/parts/longitudinal-window/`.
- RPG progression and unlock proof remains under
  `mechanics/rpg/parts/progression-unlocks/`.
- Closeout, harvest, quest promotion, and owner followthrough remain
  obligations or ingress pressure until separate eval-side operations exist.

## Current Applicability

As of 2026-05-24:

- Still valid: `diagnosis-gate` remains the guarded Growth Cycle diagnosis
  part contract for `aoa-diagnosis-cause-discipline`.
- Changed: the part now expresses stop-line coverage as pressure-to-owner
  route rows, and validator tokens guard each row.
- Superseded by: none.

## Review Log

### 2026-05-24 - Diagnosis-gate boundary route wording

- Previous assumption: the diagnosis-gate contract required explicit stronger
  owner split plus stop-line terms for repair, owner fit, final quality, broad
  growth, closeout, harvest, quest, memory, runtime, automation, and owner
  landing.
- New reality: the same contract now guards full route rows that name each
  pressure and its owner route.
- Reason: diagnosis evidence should help an agent choose the next owner route
  without making diagnosis proof impersonate repair, progression, closeout,
  quest, memory, runtime, automation, or owner acceptance.
- Source surfaces updated:
  `mechanics/growth-cycle/parts/diagnosis-gate/README.md` and
  `scripts/validate_repo.py`.
- Validation: growth-cycle validator focus, diagnosis bundle validation,
  catalog check, root validation, semantic AGENTS validation, diff whitespace
  check, and full pytest passed.

### 2026-05-24 - Lower parts index operating route

- Previous assumption: the lower Growth Cycle parts README could remain a
  compact active/deferred note because `PARTS.md` and `diagnosis-gate/README.md`
  carried the detailed contract.
- New reality: `mechanics/growth-cycle/parts/README.md` now acts as the
  lower-index operating card for selecting `diagnosis-gate`, routing stronger
  owner pressure, and deciding whether a future Growth Cycle part is justified.
- Reason: diagnosis, repair, progression, closeout, quest, memory, runtime, and
  owner-followthrough pressure should route from the directory index itself
  before a future agent adds a part by proximity.
- Source surfaces updated: `mechanics/growth-cycle/parts/README.md`,
  `scripts/validate_repo.py`, and `tests/test_validate_repo.py`.
- Validation: focused lower-index validator tests, diagnosis bundle
  validation, root validation, semantic AGENTS validation, generated catalog
  check, diff whitespace check, and full pytest.

## Validation

Expected validation route:

```bash
python -m pytest -q tests/test_validate_repo.py -k growth_cycle_diagnosis_gate
python scripts/validate_repo.py --eval aoa-diagnosis-cause-discipline
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python scripts/validate_semantic_agents.py
python -m pytest -q
```
