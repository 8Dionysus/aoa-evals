# 0061 Antifragility Part Contract Guard

## Status

Accepted.

## Context

`mechanics/antifragility/` is already the active AoA-aligned parent for
posture review, stress-recovery windows, and repair proof. The parent README
and `PARTS.md` named the owner split, but the part README files still used a
thin `Boundary` section instead of exposing the same contract shape used by
newer mechanic parts.

That thinness is risky here. Antifragility proof can easily overread a repair
note, stress window, runtime sidecar, or degraded-mode receipt as global
resilience, live self-healing, permanent stability, or owner-local cleanup
authority.

## Decision

Require each active antifragility part README to expose:

- `## Inputs`
- `## Outputs`
- `## Stronger Owner Split`
- `## Stop-Lines`
- `## Validation`

The protected parts are:

- `mechanics/antifragility/parts/posture-review/README.md`
- `mechanics/antifragility/parts/stress-recovery-window/README.md`
- `mechanics/antifragility/parts/repair-proof/README.md`

`posture-review` remains a bounded posture read, not repo-global resilience.
`stress-recovery-window` remains stress-window proof with comparison-spine and
audit sidecar boundaries, not federation health or runtime recovery authority.
`repair-proof` remains bounded repair proof, not a repair parent, owner-object
quality proof, or growth-cycle completion claim.

## Consequences

- Future edits must keep part-local owner split and stop-lines explicit.
- Repair and stress evidence cannot quietly become global antifragility proof.
- Runtime evidence remains candidate-only through `audit`.
- Comparison acceptance remains under `comparison-spine`.
- Diagnosis-cause discipline remains outside Antifragility because the active
  `growth-cycle/diagnosis-gate` route owns that proof support.

## Current Applicability

As of 2026-05-24:

- Still valid: the three active Antifragility part READMEs remain protected
  part contracts with inputs, outputs, stronger-owner split, stop-lines, and
  validation routes.
- Changed: part-level stop-line coverage now uses pressure-to-owner route rows,
  and validator tokens guard each route row for posture review,
  stress-recovery-window, and repair-proof.
- Superseded by: none.

## Review Log

### 2026-05-24 - Part boundary route wording

- Previous assumption: Antifragility part READMEs could keep the required
  stop-line contract as a boundary sentence followed by excluded claims.
- New reality: the part contracts now expose the same boundaries as direct
  pressure-to-owner routes.
- Reason: a low-context agent should see where global resilience, runtime
  recovery, one-score movement, owner-object quality, diagnosis pressure, and
  generated or memo overread route next without parsing a prohibition list.
- Source surfaces updated:
  `mechanics/antifragility/parts/posture-review/README.md`,
  `mechanics/antifragility/parts/stress-recovery-window/README.md`,
  `mechanics/antifragility/parts/stress-recovery-window/docs/STRESS_RECOVERY_WINDOW_EVALS.md`,
  `mechanics/antifragility/parts/repair-proof/README.md`,
  `scripts/validate_repo.py`, and `tests/test_validate_repo.py`.
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
python -m pytest -q tests/test_validate_repo.py -k antifragility_part_readmes
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python -m pytest -q
```
