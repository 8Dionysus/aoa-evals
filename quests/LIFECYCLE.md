# Quest Lifecycle Contract

## Role

`quests/LIFECYCLE.md` defines the lifecycle meaning for source quest records in
`aoa-evals`.

Use this file when a quest state changes, when a proof-loop route ends in
defer or handoff, or when a future agent needs to know whether a quest should
remain visible as an open obligation.

This contract routes state meaning between source records, `QUESTBOOK.md`
visibility, generated quest readers, proof-loop endings, roadmap direction, eval
proof meaning, and post-session harvest receipts while leaving each owner
surface in charge of its own artifact.

## Source Relationship

The source record still lives at:

`quests/<lane>/<state>/AOA-EV-Q-*.yaml`

The source schema still lives at:

`mechanics/questbook/parts/source-record-contract/schemas/quest.schema.json`

This lifecycle contract explains what each schema state means for return,
promotion, and `QUESTBOOK.md` visibility. The schema and source quest record
remain the stronger machine-readable surfaces for record shape and record data.

## State Matrix

| State | Open-index posture | Return posture | Promotion posture | Boundary held |
| --- | --- | --- | --- | --- |
| `captured` | listed in `QUESTBOOK.md` | proof pressure is preserved for later triage | no promotion yet | evidence acceptance, active work, and owner approval stay outside this state |
| `triaged` | listed in `QUESTBOOK.md` | owner route and nearest next question are known | still needs a concrete bounded action before promotion | bundle readiness and proof acceptance stay outside this state |
| `ready` | listed in `QUESTBOOK.md` | next bounded action and validation route are clear | may enter an active route after current-owner review | dispatch remains explicit and execution remains owner-routed |
| `active` | listed in `QUESTBOOK.md` | work is currently being carried through an explicit route | may close only with reviewed evidence | proof success waits for validation evidence |
| `blocked` | listed in `QUESTBOOK.md` | blocker, missing owner, or missing evidence is explicit | no promotion until the block is resolved or reanchored | blocked owner authority stays intact |
| `reanchor` | listed in `QUESTBOOK.md` | return to the last valid source anchor before continuing | no promotion until the reanchor is reviewed | continuity proof requires source evidence beyond memory or chat residue |
| `done` | closed; not listed as open | obligation has a reviewed close reason in the source record | promotion is already resolved or not needed | source history remains preserved |
| `dropped` | closed; not listed as open | obligation is rejected or retired with a reason | no promotion | evidence debt remains named in the close reason |

## Transition Discipline

- `captured -> triaged` requires enough review to name the owner route and the
  nearest next question.
- `triaged -> ready` requires a concrete bounded action and a validation route.
- `ready -> active` requires current owner intent; old backlog pressure remains
  context only.
- `active -> done` requires reviewed evidence in the source record and any
  generated projection refresh required by the changed quest.
- Any open state may move to `blocked` when the blocker is public-safe and
  explicit.
- Any open state may move to `reanchor` when the last valid source anchor must
  be recovered before continuing.
- Any state may move to `dropped` only with a reason that preserves why the
  obligation no longer belongs in active proof work.

Close a quest through the source record's reviewed evidence. Nearby reports,
receipts, generated readers, sibling refs, and proof-loop route-smoke artifacts
can support review, while closure remains a source-record decision.

## Proof-Loop Return Use

When `mechanics/proof-loop/` cannot close as a real bundle-local report or an
optional receipt, return through this lifecycle contract:

- use `captured` for newly preserved proof pressure;
- use `triaged` when the owner route and next question are known;
- use `blocked` when a public-safe blocker prevents proof review;
- use `reanchor` when the route must return to a prior valid source anchor.

`mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md`
stays route evidence below quest closure and below eval result receipt
creation. It leaves close or promote decisions with source-record review.

## Visibility Rule

Open states are:

- `captured`
- `triaged`
- `ready`
- `active`
- `blocked`
- `reanchor`

Closed states are:

- `done`
- `dropped`

`QUESTBOOK.md` must list open quest IDs and leave closed quest IDs out of
current open obligations.

Generated quest readers may include closed source records for provenance, but
closed records remain provenance rather than active obligations.

## Validation

After changing lifecycle meaning, quest states, or source quest records, use
[AGENTS](AGENTS.md#validation) for executable validation commands.
