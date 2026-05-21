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

## Validation

Expected validation route:

```bash
python -m pytest -q tests/test_validate_repo.py -k antifragility_part_readmes
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python -m pytest -q
```
