# Mechanic Part Validation Command Ownership

- Decision ID: AOA-EV-D-0102
- Status: Accepted
- Date: 2026-05-21
- Owner surface: `mechanics/README.md`

## Current Applicability

As of 2026-05-24:

- Still valid: executable child validation checks live in parent
  `mechanics/<parent>/parts/AGENTS.md` route cards, keyed by child
  `VALIDATION.md` paths.
- Clarified: active atlas and topology surfaces should describe the route as a
  validation route, with command ownership staying in AGENTS.
- Source surfaces updated: `mechanics/README.md`,
  `docs/architecture/PROOF_TOPOLOGY.md`, `scripts/validate_repo.py`, and
  `tests/test_validate_repo.py`.
- Validation route: `mechanics/AGENTS.md#validation` and root
  `AGENTS.md#verify`.

## Review Log

### 2026-05-24 - Active surfaces use validation-route language

- Previous assumption: active topology docs could use command-reachability
  wording directly because the validator still parses python commands.
- New reality: low-context agents orient better when active maps name the
  validation route first and route executable checks to AGENTS-owned lanes.
- Reason: the active atlas should show `README -> VALIDATION.md -> parts/AGENTS.md`
  as the route, while validator internals keep checking reachable commands
  inside the AGENTS owner lane.
- Source surfaces updated: `mechanics/README.md`,
  `docs/architecture/PROOF_TOPOLOGY.md`, validator message text, and validator tests.
- Validation: use the mechanic validation route in
  `mechanics/AGENTS.md#validation`.

## Index Metadata

- Original date: 2026-05-21
- Surface classes: mechanic part, validation guard
- Mechanic parents: cross-parent
- Guard families: part and payload
- Posture: active guard rationale

## Context

Decision 0087 made mechanic part validation command reachability a guard: python
commands must stay repo-relative, reachable, and anchored to the payload they
claim to check.

The refactor after that decision exposed a different placement problem. Part
README files and mechanic index surfaces had become command ledgers. That
conflicts with the sibling repo pattern where README/PARTS files are maps,
`VALIDATION.md` files are part-local validation route markers, and nearest
`AGENTS.md` cards own executable commands.

## Options Considered

- Keep executable commands directly in every part README.
- Move commands into each part `VALIDATION.md`.
- Centralize executable child validation commands in parent
  `mechanics/<parent>/parts/AGENTS.md` route cards while keeping each part
  `VALIDATION.md` as the local route marker.
- Keep mechanic `PARTS.md` and `parts/README.md` files as command lists.

## Decision

Every concrete `mechanics/<parent>/parts/<part>/README.md` `## Validation`
section routes to `mechanics/<parent>/parts/<part>/VALIDATION.md`.

Every part `VALIDATION.md` routes to the parent
`mechanics/<parent>/parts/AGENTS.md` validation lane.

Executable python command ownership lives in the parent `parts/AGENTS.md`
centralized child validation block, keyed by the child `VALIDATION.md` path.

Mechanic index surfaces such as `mechanics/<parent>/PARTS.md` and
`mechanics/<parent>/parts/README.md` route to the nearest `AGENTS.md` validation
lane instead of carrying command blocks.

The reachability guard still rejects a stale validation path, absolute local
path, missing python command, naked route-wide command without a payload
coverage anchor, or a README that carries executable python command blocks
instead of routing them to `VALIDATION.md` or parent `parts/AGENTS.md`.

## Rationale

This keeps README files readable as part contracts, keeps validation discoverable
from the part itself, and keeps commands in the nearest agent route card where
future workers expect operational instructions.

It also keeps `PARTS.md` and `parts/README.md` readable as part maps rather than
turning them into duplicate command ledgers.

It also preserves the 0087 proof concern: the command path still has to exist,
and payload-bearing parts still need a payload coverage anchor.

## Consequences

- Positive: README files remain contract maps.
- Positive: mechanic index surfaces remain maps instead of command ledgers.
- Positive: part validation commands are visible in the route card that owns
  editing and closeout behavior for the parent parts lane.
- Positive: moving a part-local script or test has one executable command home:
  the parent `parts/AGENTS.md` centralized child validation block.
- Tradeoff: a part validation route now spans README, `VALIDATION.md`, and
  parent `parts/AGENTS.md`, so validators must check all three together.
- Follow-up: future child validation generators should update parent
  `parts/AGENTS.md` instead of writing command blocks into README files.

## Boundaries

This decision does not make decision records current law. Current source
surfaces define the active route; this record explains why the command owner
moved.

It does not prove that every command was executed in a given run, and it does
not let validation commands strengthen bundle claims, sibling truth, generated
readers, or runtime authority.

## Validation

Use the nearest `AGENTS.md` validation lane for executable checks.
