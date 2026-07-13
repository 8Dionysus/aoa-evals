# Questbook Mechanic Package

- Decision ID: AOA-EV-D-0006
- Status: Accepted
- Date: 2026-05-19
- Owner surface: `mechanics/questbook/`

## Index Metadata

- Original date: 2026-05-19
- Surface classes: mechanic package, quest/lane
- Mechanic parents: questbook
- Guard families: none
- Posture: active rationale

## Context

After the proof topology map landed, `aoa-evals` needed to choose whether
`mechanics/` should remain deferred or start with one real package.

The questbook operation is already live: source quest records, `QUESTBOOK.md`,
generated quest catalog and dispatch readers, quest schemas, local route cards,
and a post-session harvest skill all exist. The operation is recurring and has
validation pressure, while the source paths are intentionally not ready to move.

## Options Considered

- Keep all mechanics deferred until several packages can be created together.
- Create a broad mechanics atlas with directories for every candidate family.
- Create only the atlas plus one `questbook` package, because it has a current
  operation, source surfaces, generated readers, validation, and deferred
  lane/state movement pressure.

## Decision

Create `mechanics/README.md`, `mechanics/AGENTS.md`, and
`mechanics/questbook/`.

The `questbook` package owns the operation that keeps quest obligations
routeable:

`source quest record -> human open-obligation index -> generated quest reader -> deferred return or reviewed promotion`

Current quest source paths remain in place.

## Rationale

This starts mechanics with no empty taxonomy. `questbook` is the smallest live
operation that already crosses source records, human index, generated readers,
post-session harvest posture, and validation.

The package lets future lane/state migration happen from an owned operation
rather than from a desire to make the tree look mature.

## Consequences

- Positive: the first mechanic package has a real job and a validator-backed
  route.
- Tradeoff: `mechanics/` now exists, so future changes must resist filling it
  with candidate directories before they own operations.
- Follow-up: the next package should be chosen only when `boundary-bridge`,
  `audit`, or another candidate has comparable live operation
  pressure and validation.

## Boundaries

This decision does not move `quests/*.yaml`, Agon notes, generated quest
readers, or `aoa-quest-harvest`.

It does not make quests eval bundles, roadmap direction, proof verdicts, or
downstream owner acceptance.

It does not authorize broad mechanics package creation by analogy.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
