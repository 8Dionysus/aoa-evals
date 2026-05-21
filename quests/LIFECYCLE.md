# Quest Lifecycle Contract

## Role

`quests/LIFECYCLE.md` defines the lifecycle meaning for source quest records in
`aoa-evals`.

It is not `QUESTBOOK.md`, not a generated quest reader, not a proof bundle, not
the roadmap, and not a post-session harvest receipt.

Use this file when a quest state changes, when a proof-loop route ends in
defer or handoff, or when a future agent needs to know whether a quest should
remain visible as an open obligation.

## Source Relationship

The source record still lives at:

`quests/<lane>/<state>/AOA-EV-Q-*.yaml`

The source schema still lives at:

`mechanics/questbook/parts/source-record-contract/schemas/quest.schema.json`

This lifecycle contract explains what each schema state means for return,
promotion, and `QUESTBOOK.md` visibility. It does not replace the schema or the
source quest record.

## State Matrix

| State | Open-index posture | Return posture | Promotion posture | Must not imply |
| --- | --- | --- | --- | --- |
| `captured` | listed in `QUESTBOOK.md` | proof pressure is preserved for later triage | no promotion yet | accepted evidence, active work, or owner approval |
| `triaged` | listed in `QUESTBOOK.md` | owner route and nearest next question are known | still needs a concrete bounded action before promotion | bundle readiness or proof acceptance |
| `ready` | listed in `QUESTBOOK.md` | next bounded action and validation route are clear | may enter an active route after current-owner review | hidden dispatch or automatic execution |
| `active` | listed in `QUESTBOOK.md` | work is currently being carried through an explicit route | may close only with reviewed evidence | proof success before validation |
| `blocked` | listed in `QUESTBOOK.md` | blocker, missing owner, or missing evidence is explicit | no promotion until the block is resolved or reanchored | permission to bypass the blocked owner |
| `reanchor` | listed in `QUESTBOOK.md` | return to the last valid source anchor before continuing | no promotion until the reanchor is reviewed | continuity proof from memory or chat residue |
| `done` | closed; not listed as open | obligation has a reviewed close reason in the source record | promotion is already resolved or not needed | deletion of source history |
| `dropped` | closed; not listed as open | obligation is rejected or retired with a reason | no promotion | silent loss of evidence or ignored debt |

## Transition Discipline

- `captured -> triaged` requires enough review to name the owner route and the
  nearest next question.
- `triaged -> ready` requires a concrete bounded action and a validation route.
- `ready -> active` requires current owner intent, not only old backlog
  pressure.
- `active -> done` requires reviewed evidence in the source record and any
  generated projection refresh required by the changed quest.
- Any open state may move to `blocked` when the blocker is public-safe and
  explicit.
- Any open state may move to `reanchor` when the last valid source anchor must
  be recovered before continuing.
- Any state may move to `dropped` only with a reason that preserves why the
  obligation no longer belongs in active proof work.

Do not move a quest to `done` because a nearby report, receipt, generated
reader, sibling ref, or proof-loop route-smoke exists. Closure belongs to the
quest's source record and its reviewed evidence.

## Proof-Loop Return Use

When `mechanics/proof-loop/` cannot close as a real bundle-local report or an
optional receipt, return through this lifecycle contract:

- use `captured` for newly preserved proof pressure;
- use `triaged` when the owner route and next question are known;
- use `blocked` when a public-safe blocker prevents proof review;
- use `reanchor` when the route must return to a prior valid source anchor.

`mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md` is route evidence, not quest
closure. It does not create an eval result receipt and does not close or promote
any quest by itself.

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

`QUESTBOOK.md` must list open quest IDs and must not list closed quest IDs as
current open obligations.

Generated quest readers may include closed source records for provenance, but
they do not turn closed records into active obligations.

## Validation

After changing lifecycle meaning, quest states, or source quest records, use
[AGENTS](AGENTS.md#validation) for executable validation commands.
