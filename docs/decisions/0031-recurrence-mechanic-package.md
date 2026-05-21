# 0031 Recurrence Mechanic Package

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/recurrence/`

Amendment: `docs/decisions/0039-recurrence-support-parts-expansion.md`
activates `anchor-return` (`return-anchor` proof support), `memory-recall`, `recursor-boundary`, and
`stats-regrounding-boundary` as recurrence parts after a later root-district
evidence pass. The original decision remains the package creation record.

## Context

Recurrence is a named AoA mechanic, and `aoa-evals` now has enough local
proof-side evidence to route it as a live mechanic package rather than a loose
docs/root-support family.

The evidence cluster spans the recurrence proof program, the
`aoa-recurrence-control-plane-integrity` bundle, control-plane integrity docs,
fixtures, schema, example dossier, runner, scorer, tests, recurrence component
manifest, generated reader references, insertion notes, and neighboring
return-aware bundles.

## Options Considered

- Keep recurrence surfaces in root districts and only mention them from
  `docs/PROOF_TOPOLOGY.md`.
- Move every recurrence-named bundle into `mechanics/recurrence/`.
- Create `mechanics/recurrence/` as the AoA-aligned parent, move only
  control-plane support machinery into a part, and leave source proof bundles
  under `bundles/`.

## Decision

Create `mechanics/recurrence/` as the eval-side recurrence proof mechanic.

The package owns the route:

`recurrence pressure -> bounded recurrence proof question -> control-plane or return-aware evidence -> bundle-local review -> bounded report or owner handoff`

Move the control-plane integrity support surfaces into
`mechanics/recurrence/parts/control-plane-integrity/`: docs, fixtures, schema,
example dossier, runner, scorer, tests, and recurrence component manifest.

The source proof bundles stay under `bundles/`. Return-anchor,
continuity-anchor, and self-reanchor proof remain bundle-local until their
support artifacts justify narrower recurrence parts.

Historical insertion notes move behind the active `PROVENANCE.md` bridge into
the owning legacy archive, which keeps its own raw/index/distillation
accounting internally.

## Rationale

The parent name must be `recurrence` because the proof-side work materializes
the center AoA recurrence mechanic. The part name may be
`control-plane-integrity` because that is the narrower eval support operation.

This prevents two errors: hiding recurrence in root technical districts after
it has a real operation, and creating proof-organ adjective packages that split
one AoA mechanic into future-bug fragments.

## Consequences

- Positive: future recurrence proof work starts from a clear active route,
  part contract, owner split, stop-lines, validation path, and provenance
  bridge.
- Tradeoff: recurrence source bundles remain outside the package, so package
  users must keep bundle-local proof authority visible.
- Follow-up: continuity-anchor and self-reanchor should become parts only after
  source artifacts, inputs, outputs, owner split, stop-lines, and validation
  prove a recurring operation. Return-anchor now has a part through decision
  `0039`.

## Boundaries

This decision does not move recurrence source proof bundles into
`mechanics/recurrence/`.

It does not claim global recurrence completeness, hidden continuity, runtime
self-healing, automatic recursor spawn, beacon verdict authority, downstream
projection truth, owner artifact promotion, or runtime activation.

It does not transfer `Agents-of-Abyss`, `abyss-stack`, `aoa-routing`,
`aoa-memo`, `aoa-agents`, `aoa-playbooks`, `aoa-stats`, KAG, or Agon source
truth into `aoa-evals`.

## Validation

- `mechanics/recurrence/README.md` names the owned operation, source surfaces,
  inputs, outputs, stronger-owner split, stop-lines, legacy route, and
  validation.
- `mechanics/recurrence/AGENTS.md` names local editing law.
- `mechanics/recurrence/PARTS.md` names why control-plane integrity is an
  active part and why return-aware families remain bundle-local.
- `mechanics/recurrence/PROVENANCE.md` bridges old root placement questions
  into the owning legacy archive after the active route.
- `scripts/validate_repo.py` checks the package, part, provenance bridge,
  decision, and stale root paths.
- `python -m py_compile mechanics/recurrence/parts/control-plane-integrity/scorers/recurrence_control_plane_integrity.py mechanics/recurrence/parts/control-plane-integrity/scripts/run_recurrence_control_plane_integrity_eval.py`
- `python mechanics/recurrence/parts/control-plane-integrity/scripts/run_recurrence_control_plane_integrity_eval.py --case mechanics/recurrence/parts/control-plane-integrity/fixtures/recurrence-control-plane-integrity-v1/cases/RCPI-001.registry-mixed-manifests.json --check-expected --json`
- `python -m pytest -q mechanics/recurrence/parts/control-plane-integrity/tests/test_recurrence_control_plane_integrity_eval_seed.py`
- `python scripts/build_catalog.py --check`
- `python scripts/validate_repo.py`
