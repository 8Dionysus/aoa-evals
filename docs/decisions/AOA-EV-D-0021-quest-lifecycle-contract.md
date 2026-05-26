# Quest Lifecycle Contract

- Decision ID: AOA-EV-D-0021
- Status: Accepted
- Date: 2026-05-19
- Owner surface: `quests/`

## Index Metadata

- Original date: 2026-05-19
- Surface classes: quest/lane
- Mechanic parents: none
- Guard families: none
- Posture: active rationale

## Context

Quest source records now use `quests/<lane>/<state>/AOA-EV-Q-*.yaml`, and
validators already prove that each source path matches its `state` field.

That protects topology, but not lifecycle meaning. After the proof-loop route
smoke, the next weak point was return semantics: a future agent could see
`captured`, `triaged`, `ready`, `active`, `blocked`, `reanchor`, `done`, and
`dropped` as mere enum values instead of proof-return states with open-index
and promotion consequences.

## Options Considered

- Leave lifecycle meaning in `quests/README.md` prose.
- Put lifecycle meaning under `docs/` as a general guide.
- Add `quests/LIFECYCLE.md` as a source-adjacent lifecycle contract and validate
  that it covers every schema state.

## Decision

Add `quests/LIFECYCLE.md`.

The file defines the open-index posture, return posture, promotion posture, and
must-not-imply boundary for every quest schema state. It also routes proof-loop
defer and handoff endings back into quest lifecycle without treating the
proof-loop route-smoke report as quest closure.

Validators must keep this lifecycle contract discoverable and must fail when a
schema state is not represented in the state matrix.

## Rationale

Lifecycle meaning belongs beside source quest records because state changes are
source changes. Keeping the contract under `quests/` makes the route easier for
low-context agents: source record, state directory, lifecycle meaning, human
index, and generated readers are one local path.

Putting the state contract only in a general docs guide would make it easier to
skip during edits. Leaving it in prose without coverage would keep the most
important invariant invisible: open states remain open obligations; closed
states remain provenance, not current work.

## Consequences

- Positive: every quest state now has explicit return, promotion, and
  open-index meaning.
- Positive: proof-loop defer and handoff outcomes now have a local quest return
  route.
- Tradeoff: quest state edits now require one more source-adjacent surface to
  stay aligned.
- Follow-up: future lifecycle transitions can become stricter only after an
  actual state movement needs them.

## Boundaries

This decision does not change any current quest state, create a new quest,
close a quest, promote a quest into an eval bundle, publish a receipt, or make
generated quest readers authoritative.

It does not turn `mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md` into quest
closure or bundle-local proof success.

## Validation

- `quests/LIFECYCLE.md`
- `quests/README.md`
- `quests/AGENTS.md`
- `mechanics/questbook/README.md`
- `mechanics/proof-loop/README.md`
- `scripts/validate_repo.py`
- `python scripts/build_catalog.py --check`
