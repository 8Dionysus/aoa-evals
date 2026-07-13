# Experience Part Contract Guard

- Decision ID: AOA-EV-D-0063

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-21
- Surface classes: mechanic part, validation guard
- Mechanic parents: experience
- Guard families: part and payload
- Posture: active guard rationale

## Context

`mechanics/experience/` is the active AoA-aligned parent for eval-side
Experience proof. The parent README and `PARTS.md` already name the owner
split and stop-lines, but the five active part README files still used thin
`Boundary` sections.

That is risky because Experience proof touches adoption, certification,
governance, runtime-boundary, office, service, release-train, KAG, ToS, memo,
and routing surfaces. Without part-local contracts, future edits can turn
bounded verdict support into live runtime activation, operator certification,
owner-local adoption, governance authority, memory canon, routing authorship,
or broad Experience success.

## Decision

Require each active Experience part README to expose:

- `## Inputs`
- `## Outputs`
- `## Stronger Owner Split`
- `## Stop-Lines`
- `## Validation`

The protected parts are:

- `mechanics/experience/parts/protocol-integrity/README.md`
- `mechanics/experience/parts/certification-gate/README.md`
- `mechanics/experience/parts/adoption-federation/README.md`
- `mechanics/experience/parts/governance-runtime-boundary/README.md`
- `mechanics/experience/parts/office-release-train/README.md`

The parts keep their current active routes. No new parent packages are created
for certification, adoption, governance, office, service, release, KAG, ToS,
memo, or routing verdict forms.

## Consequences

- Future Experience part edits must keep owner split and stop-lines explicit.
- Bounded verdict support remains below live runtime, office, release,
  adoption, certification, governance, memory, routing, KAG, and ToS authority.
- Runtime distillation candidate adoption remains outside Experience and
  routes through `mechanics/distillation/parts/runtime-candidate-adoption/`.
- Experience support surfaces remain parts under `experience`, not
  proof-adjective parent mechanics.

## Current Applicability

As of 2026-05-24:

- Still valid: active Experience part README files expose inputs, outputs,
  stronger owner split, stop-lines, and validation route markers.
- Changed: active Experience part README files now express stop-line coverage as
  owner-route pressure, and part-specific validator tokens guard full
  pressure-to-owner-route rows where this route has been applied.
- Superseded by: none.

## Review Log

### 2026-05-24 - Office release-train boundary route wording

- Previous assumption: the office release-train part contract used a direct
  "must claim no" sentence to keep installation, release, runtime, actor, and
  publication authority outside the part.
- New reality: the part contract keeps the same authority boundary through a
  pressure-to-owner-route table whose full owner-route rows are validator
  guarded.
- Reason: low-context agents orient better from actionable owner routes than
  from a dense denial sentence, while the validator protects both the same
  office-release authority pressures and their routed owners.
- Source surfaces updated:
  `mechanics/experience/parts/office-release-train/README.md` and
  `scripts/validate_repo.py`.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

### 2026-05-24 - Remaining Experience part boundary route wording

- Previous assumption: protocol-integrity, certification-gate,
  adoption-federation, and governance-runtime-boundary part contracts used
  direct exclusion prose to keep stronger owner authority outside the part.
- New reality: those part contracts keep the same authority boundary through
  pressure-to-owner-route tables whose full owner-route rows are validator
  guarded.
- Reason: the same route shape now covers all active Experience part README
  files, so low-context agents can read the owner handoff from the table rather
  than interpreting dense exclusion prose.
- Source surfaces updated:
  `mechanics/experience/parts/protocol-integrity/README.md`,
  `mechanics/experience/parts/certification-gate/README.md`,
  `mechanics/experience/parts/adoption-federation/README.md`,
  `mechanics/experience/parts/governance-runtime-boundary/README.md`, and
  `scripts/validate_repo.py`.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
