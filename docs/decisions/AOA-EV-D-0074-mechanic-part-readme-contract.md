# Mechanic Part README Contract

- Decision ID: AOA-EV-D-0074
- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/`, `scripts/validate_repo.py`

## Index Metadata

- Original date: 2026-05-20
- Surface classes: mechanic part
- Mechanic parents: cross-parent
- Guard families: part and payload
- Posture: active rationale

## Context

The mechanics refactor moved real proof operations out of root districts into
active parent packages and concrete parts. Parent-level allowlists and
part-specific guards are not enough by themselves: a future part could appear
under `mechanics/<parent>/parts/<part>/README.md` without being routed by the
parent `PARTS.md`, or without the same input/output/boundary contract that keeps
parts from becoming accidental parent mechanics.

## Options Considered

- Keep only named part validators: this protects current known parts but lets a
  new part directory bypass the contract until someone remembers to add a
  bespoke guard.
- Require exact full README paths in every parent `PARTS.md`: this is strong but
  too noisy for parent maps that already route parts by exact slug.
- Add a generic concrete-part guard: every active part README must expose the
  common contract headings, and parent `PARTS.md` must route the part by README
  path or exact part slug.

## Decision

`scripts/validate_repo.py` validates every concrete active part README under
`mechanics/<parent>/parts/<part>/README.md`.

Each part README must contain:

- `## Source Surfaces`
- `## Inputs`
- `## Outputs`
- `## Stronger Owner Split`
- `## Stop-Lines`
- `## Validation`

The `## Stop-Lines` section must expose a pressure-to-owner route table with a
`Pressure` column and a `Route` or `Owner route` column. A part may introduce
that table with route-specific boundary prose such as `Boundary routes keep ...`,
but the table is the checked contract. This keeps the section as an operational
proof boundary instead of a bare prohibition scaffold.

The same guard also rejects an orphan part by requiring the parent `PARTS.md` to
route each concrete part by README path or exact backticked part slug.

## Rationale

This keeps the growth principle local and reusable: a parent mechanic can grow
new parts, but the new part must immediately state what it consumes, what it
names as source surfaces, what it consumes, what it emits, which stronger owner
keeps truth, where it stops, and how it is checked.
That is the minimal shape needed for future `agon`, `titan`, proof-loop, and
evals-native growth without recreating wrong parent forms.

## Consequences

- Positive: new parts cannot silently appear as unreviewed topology.
- Positive: part stop-lines now route pressure to the owner that can act on it,
  so low-context agents can read the boundary as an operational route instead
  of a list of detached prohibitions.
- Tradeoff: experimental part directories need a README contract before they can
  live under active mechanics.
- Follow-up: part-specific validators still add stronger local invariants where
  a part has schemas, generated artifacts, reports, or seed files.

## Boundaries

This decision does not say every part is equally mature, executable, or
proof-complete. It only defines the minimum active topology contract for a part.
It does not promote legacy raw files, generated readers, seeds, reports, or
fixtures into stronger authority than their mechanic README and owning source
surfaces.

## Current Applicability

As of 2026-05-24:

- Still valid: concrete part READMEs under
  `mechanics/<parent>/parts/<part>/README.md` must expose source surfaces,
  inputs, outputs, stronger owner split, stop-lines, and validation.
- Changed: lower part indexes at `mechanics/<parent>/parts/README.md` now also
  carry an operating-card contract with role, input, output, owner, next route,
  tools, validation, active parts, and part admission route. Every active
  `mechanics/<parent>/parts/` directory now needs that lower index.
- Superseded by: none.

## Review Log

### 2026-06-14 - Stop-lines route table guard

- Previous assumption: a single generic Stop-Lines lead-in string could define
  the active part boundary across every mechanic part.
- New reality: active parts now use pressure-specific route tables, sometimes
  introduced by route-specific `Boundary routes keep ...` prose and sometimes
  starting directly at the table.
- Reason: the route table is the durable contract: it names the pressure and the
  owner route that can carry it, while allowing local part wording to stay
  precise.
- Source surfaces updated: `scripts/validators/mechanic_part_readme_contract.py`,
  `scripts/validators/mechanic_part_contract_common.py`, and
  `tests/test_mechanic_part_contracts.py`.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

### 2026-05-24 - Lower parts index operating-card guard

- Previous assumption: lower `parts/README.md` files could stay as short route
  cards while parent `PARTS.md`, part READMEs, and `parts/AGENTS.md` carried
  the operational detail.
- New reality: every active lower parts index is now an agent operating card
  with active part map, owner pressure/admission route, tool lane, and
  validation lane.
- Reason: agents often enter a directory from the file tree. The lower index
  must answer where the agent is, what the part operation consumes and emits,
  who owns stronger truth, which tools/checks apply, and where new part
  pressure routes next.
- Source surfaces updated: active `mechanics/*/parts/README.md` lower indexes,
  `scripts/validate_repo.py`, and `tests/test_validate_repo.py`.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

### 2026-05-24 - Missing lower parts indexes closed

- Previous assumption: parent `PARTS.md` could carry enough local part-index
  detail even when `mechanics/<parent>/parts/README.md` was absent.
- New reality: `checkpoint`, `experience`, and `recurrence` now expose lower
  `parts/README.md` operating cards like the rest of active mechanics.
- Reason: agents often enter from the file tree at `parts/`; the directory
  itself needs a route surface before the agent chooses a concrete part.
- Source surfaces updated: `mechanics/checkpoint/parts/README.md`,
  `mechanics/experience/parts/README.md`,
  `mechanics/recurrence/parts/README.md`, `scripts/validate_repo.py`, and
  `tests/test_validate_repo.py`.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
