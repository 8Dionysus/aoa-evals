# 0066 Recurrence Control-plane Contract

## Status

Accepted.

## Context

`mechanics/recurrence/` is the active AoA-aligned parent for eval-side
recurrence proof. The `control-plane-integrity` part owns the dossier schema,
fixture family, example dossier, runner, scorer, tests, control-plane eval
notes, and recurrence component manifest for
`aoa-recurrence-control-plane-integrity`.

The part README still had two weak spots:

- source surfaces named former root paths such as `docs/`, `fixtures/`,
  `examples/`, `schemas/`, `scripts/`, `scorers/`, `tests/`, and
  `manifests/` after those payloads had moved into the part-local home;
- the local boundary was a thin `Boundary` paragraph rather than explicit
  `Stronger Owner Split` and `Stop-Lines`.

That is risky because recurrence control-plane evidence touches runtime,
live-observation producers, routing, downstream projections, beacons, hooks,
Agon diagnostics, and owner review. A thin contract can turn bounded proof into
runtime status, promotion readiness, projection truth, beacon verdict
authority, or hidden continuity. The downstream projection truth stop-line is
explicit because generated or downstream readouts remain weaker than
owner-authored source truth.

## Decision

Require `mechanics/recurrence/parts/control-plane-integrity/README.md` to
expose:

- `## Inputs`
- `## Outputs`
- `## Stronger Owner Split`
- `## Stop-Lines`
- `## Validation`

Its source-surface list must name the current part-local paths for docs,
fixtures, examples, schemas, scripts, scorers, tests, and manifests.

## Consequences

- Future recurrence control-plane edits must keep owner split and stop-lines
  explicit.
- Old root payload paths remain provenance only through
  `mechanics/recurrence/PROVENANCE.md`; the owning legacy archive maps the
  historical placement internally.
- Runtime status, runtime activation, routing behavior, downstream projection
  truth, owner review acceptance, Agon source truth, beacon verdict authority,
  and portable proof acceptance remain outside this part.
- `control-plane-integrity` stays a part under `recurrence`, not a separate
  proof-adjective parent.

## Current Applicability

As of 2026-05-24:

- Still valid: `control-plane-integrity` remains the guarded recurrence
  control-plane part contract.
- Changed: the part now expresses its stop-line coverage as
  pressure-to-owner route rows, and validator tokens guard each row.
- Superseded by: none.

## Review Log

### 2026-05-24 - Control-plane boundary route wording

- Previous assumption: the control-plane contract required explicit stronger
  owner split plus stop-line terms for runtime, projection, Agon, beacon, and
  portable-proof boundaries.
- New reality: the same contract now guards full route rows that name each
  pressure and its owner route.
- Reason: recurrence control-plane evidence touches runtime, routing,
  projection, owner review, Agon, beacon, and portable-proof surfaces; the
  active part should make the handoff executable for a low-context agent.
- Source surfaces updated:
  `mechanics/recurrence/parts/control-plane-integrity/README.md` and
  `scripts/validate_repo.py`.
- Validation: recurrence validator focus, recurrence part runners and tests,
  catalog check, root validation, semantic AGENTS validation, diff whitespace
  check, and full pytest passed.

## Validation

Expected validation route:

```bash
python -m pytest -q tests/test_validate_repo.py -k recurrence_control_plane
python mechanics/recurrence/parts/control-plane-integrity/scripts/run_recurrence_control_plane_integrity_eval.py --case mechanics/recurrence/parts/control-plane-integrity/fixtures/recurrence-control-plane-integrity-v1/cases/RCPI-001.registry-mixed-manifests.json --check-expected --json
python -m pytest -q mechanics/recurrence/parts/control-plane-integrity/tests/test_recurrence_control_plane_integrity_eval_seed.py
python scripts/validate_repo.py --eval aoa-recurrence-control-plane-integrity
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python -m pytest -q
```
