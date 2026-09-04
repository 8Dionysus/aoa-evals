# Prompt-light Agent Routes and On-demand Validation

- Decision ID: AOA-EV-D-0256
- Status: Accepted
- Date: 2026-08-30
- Owner surface: root and nested `AGENTS.md`, `README.md`, `VALIDATION.md`, and `docs/validation/`

## Index Metadata

- Original date: 2026-08-30
- Surface classes: root/topology, mechanics/topology, mechanic part, validation guard
- Mechanic parents: cross-parent
- Guard families: source/topology, route residue, part and payload
- Posture: active rationale

## Context

`aoa-evals` has grown a deep owner-aware documentation topology, but its agent
route cards also accumulated human explanation, long read-before inventories,
and executable command blocks. Most mechanic parts already have a local
`VALIDATION.md`, yet AOA-EV-D-0102 made those files route back to command blocks
in the inherited parent `parts/AGENTS.md`. As a result, an agent pays for many
unrelated child commands before it knows which child it will change.

The repository already has a stronger split for named repository lanes:
`docs/validation/validation_lanes.json` stores their command sequences and
`docs/validation/COMMAND_AUTHORITY.md` explains their ownership. The local
documentation route should extend that progressive-disclosure model without
turning README files into command ledgers or inventing a second repository-wide
command manifest.

## Options Considered

- Keep operational inventories and executable commands in the nearest
  `AGENTS.md` because agents inherit those cards automatically.
- Move executable commands into README files beside human-facing contracts.
- Put every parent and part command into one new repository-wide manifest.
- Keep named repository lanes in the existing lane manifest, move exact local
  checks into on-demand `VALIDATION.md` files, and reduce each `AGENTS.md` to
  the smallest inherited routing and ownership delta.

## Decision

`AGENTS.md` is the prompt-light operational route card for its subtree. It owns
only the local role and delta, source-owner routes, task-dependent reads,
stop-lines, the route to validation authority, and closeout expectations. It
does not own executable command blocks, general explanation, comprehensive
artifact inventories, or unconditional README reads.

`README.md` remains the human and public entry surface for concepts, package or
part meaning, usage, examples, and artifact navigation. A route card may direct
an agent to a specific README when the task needs that semantic contract, but
must not require every inherited README merely to enter the subtree. Root
`README.md` remains the repository front door. A nested README may be deleted
only when it is a proven placeholder or exact route duplicate and all human,
public, provenance, and owner navigation remains recoverable elsewhere.

`docs/validation/validation_lanes.json` remains command authority for named
repository-wide lanes. Exact parent-, legacy-, fixture-, package-, or
part-local checks live in the nearest on-demand `VALIDATION.md`; mechanic part
commands therefore move from parent `parts/AGENTS.md` blocks into that part's
existing `VALIDATION.md`. `AGENTS.md` may name a lane id or validation route,
but does not repeat its runnable command sequence.

Validators must preserve the split: reject runnable command blocks and
unconditional README inventories in agent route cards, keep local validation
commands repo-relative and reachable, preserve payload coverage anchors, and
check that named lane entrypoints still resolve through the lane manifest.

AOA-EV-D-0102 is superseded for command placement. Its requirements that a
part README route to local validation, that commands remain reachable and
repo-relative, and that payload-bearing parts retain a coverage anchor remain
in force.

## Rationale

Inherited agent context should answer how to act safely in the current subtree,
not preload every explanation and every sibling validation command. Moving
local commands one step behind an explicit validation route reduces automatic
context while improving locality: after selecting a part, the agent opens the
same part's validation surface and sees only checks relevant to that part.

The split also preserves the existing command-authority boundary. Named lanes
remain machine-readable and centrally executable; local validation stays near
the local owner rather than becoming an ever-growing global catalog. README
files continue to serve people and public readers instead of becoming hidden
agent runbooks.

## Consequences

- Positive: inherited prompt context becomes smaller and more task-specific.
- Positive: part-local validation becomes discoverable at the part itself
  instead of through a parent ledger containing unrelated siblings.
- Positive: README, agent routing, named validation lanes, and exact local
  checks each have a distinct owner role.
- Tradeoff: an agent that needs to execute a local check performs one explicit
  additional read of `VALIDATION.md`.
- Tradeoff: validators and route-token guards that encode the D-0102 chain must
  be migrated source-first rather than bypassed.
- Follow-up: process the complete tracked README/AGENTS corpus, update affected
  validation and topology sources, regenerate derived views, and compare the
  resulting context census before any integration merge.

## Current Applicability

As of 2026-08-30:

- Still valid: named repository lanes are owned by
  `docs/validation/validation_lanes.json`; part contract and payload coverage
  remain independently guarded.
- Changed: exact local commands and task-specific explanatory reads are
  on-demand surfaces rather than inherited `AGENTS.md` payload.
- Superseded by: none.

## Boundaries

This decision does not weaken validation, change eval or proof meaning, make a
README an agent authority surface, or make `VALIDATION.md` a repository-wide
lane manifest.

It does not authorize deleting a meaningful public, package, part, provenance,
schema, example, fixture, archive, generated-reader, or receipt README merely
because an agent can operate without it.

It does not make generated indexes or topology views decision authority, and
it does not prove that any documented command was executed in a particular
run.

## Validation

Regenerate decision indexes from this source record, check generated index
parity, then use the decision-lane, semantic route-card, validation-topology,
mechanic-part, and repository validators. The implementation slice must also
show that tracked `AGENTS.md` files contain no runnable command blocks, local
validation routes remain reachable, and the before/after README/AGENTS context
census is recorded.
