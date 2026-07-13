# Quest Lane-State Source Layout

- Decision ID: AOA-EV-D-0018
- Status: Accepted
- Date: 2026-05-19
- Owner surface: `quests/` and `mechanics/questbook/`

Supersession note: `docs/decisions/AOA-EV-D-0098-agon-quest-note-provenance-route.md`
supersedes the Agon markdown note placement from this decision. The lane/state
layout remains current for schema-backed `AOA-EV-Q-*` quest records.

## Index Metadata

- Original date: 2026-05-19
- Surface classes: quest/lane
- Mechanic parents: none
- Guard families: none
- Posture: active rationale

## Context

`aoa-evals` had already separated `QUESTBOOK.md`, source quest records,
generated quest readers, and the `mechanics/questbook/` operation. Earlier
decisions kept top-level quest source paths stable because validators and
generated projections were not ready to follow a physical move.

That condition has changed. Quest route docs, the questbook mechanic, generated
quest catalog and dispatch readers, and validator tests now make a lane/state
move reviewable instead of cosmetic.

## Options Considered

- Keep all source quest files at `quests/` root for compatibility.
- Move only YAML quest records and leave Agon markdown notes at root.
- Move quest source files into `quests/<lane>/<state>/`, move Agon markdown
  notes into `quests/agon/captured/`, and preserve old top-level paths as
  legacy path vocabulary.

## Decision

Move schema-backed quest records to `quests/<lane>/<state>/AOA-EV-Q-*.yaml`.

Move Agon quest notes to `quests/agon/captured/AOE-Q-AGON-*.md`.

Generated quest readers must emit the current source path. Validators must
reject duplicate or stale top-level quest source files. Old top-level paths stay
documented as legacy path vocabulary, not active source aliases.

## Rationale

The lane/state path makes quest obligations convex: the path shows both the
kind of proof pressure and the lifecycle state before a reader opens the file.
That reduces confusion between roadmap direction, active obligations, generated
dispatch hints, and proof-bundle meaning.

Duplicate alias files would make source truth ambiguous, so compatibility is
kept through legacy mapping and generated readers rather than shadow source
files.

## Consequences

- Positive: source quest paths now carry lane and lifecycle state; generated
  readers expose current paths; stale root quest files become validator errors.
- Tradeoff: consumers of old top-level paths must refresh through generated
  quest readers or the legacy naming map.
- Follow-up: future quest work can tighten lifecycle transitions and lane
  ownership without another whole-directory move.

## Boundaries

This decision does not make quests eval bundles, roadmap direction, proof
verdicts, live dispatch authority, memory truth, or sibling-owner tasks.

It does not change quest IDs, quest states, proof claims, generated-reader
authority, or bundle-local verdict meaning.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
