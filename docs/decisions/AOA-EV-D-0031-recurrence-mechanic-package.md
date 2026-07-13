# Recurrence Mechanic Package

- Decision ID: AOA-EV-D-0031
- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/recurrence/`

Amendment: `docs/decisions/AOA-EV-D-0039-recurrence-support-parts-expansion.md`
activates `anchor-return` (`return-anchor` proof support), `memory-recall`, `recursor-boundary`, and
`stats-regrounding-boundary` as recurrence parts after a later root-district
evidence pass. The original decision remains the package creation record.

## Index Metadata

- Original date: 2026-05-20
- Surface classes: mechanic package
- Mechanic parents: recurrence
- Guard families: none
- Posture: active rationale

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
  `docs/architecture/PROOF_TOPOLOGY.md`.
- Move every recurrence-named bundle into `mechanics/recurrence/`.
- Create `mechanics/recurrence/` as the AoA-aligned parent, move only
  control-plane support machinery into a part, and leave source proof bundles
  under `evals/`.

## Decision

Create `mechanics/recurrence/` as the eval-side recurrence proof mechanic.

The package owns the route:

`recurrence pressure -> bounded recurrence proof question -> control-plane or return-aware evidence -> bundle-local review -> bounded report or owner handoff`

Move the control-plane integrity support surfaces into
`mechanics/recurrence/parts/control-plane-integrity/`: docs, fixtures, schema,
example dossier, runner, scorer, tests, and recurrence component manifest.

The source proof bundles stay under `evals/`. Return-anchor,
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

## Current Applicability

As of 2026-05-24:

- Still valid: `mechanics/recurrence/` remains the AoA-aligned eval-side parent
  for recurrence proof support.
- Changed: parent-level boundary coverage now uses pressure-to-owner routes in
  `README.md`, `PARTS.md`, and `DIRECTION.md`, with validator tokens guarding
  the route rows.
- Superseded by: none.

## Review Log

### 2026-05-24 - Parent boundary route wording

- Previous assumption: parent-level Recurrence surfaces expressed boundaries
  through exclusion prose around global completeness, hidden continuity,
  recursor spawn, runtime self-healing, owner promotion, beacon verdicts,
  portable proof acceptance, and source-truth transfer.
- New reality: the parent route keeps the same authority split through
  pressure-to-owner-route rows.
- Reason: Agents-of-Abyss owns recurrence law, owner repositories accept local
  truth, and `aoa-evals` keeps bounded proof support; the active package should
  show the next owner route directly.
- Source surfaces updated: `mechanics/recurrence/README.md`,
  `mechanics/recurrence/PARTS.md`, `mechanics/recurrence/DIRECTION.md`, and
  `scripts/validate_repo.py`.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

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

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
