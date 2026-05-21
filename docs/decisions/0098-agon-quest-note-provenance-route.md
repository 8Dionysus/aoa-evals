# Agon Quest-note Provenance Route

## Status

Accepted.

## Context

Earlier quest topology moved old `AOE-Q-AGON-*` markdown notes from top-level
`quests/` into `quests/agon/captured/` while the lane/state quest route was
still maturing. After the mechanics refactor, those notes no longer behave like
schema-backed source quest records: generated quest readers ignore them,
`QUESTBOOK.md` does not list them as open obligations, and active Agon parts now
own the relevant proof-alignment operations.

Keeping markdown quest notes under an active lifecycle path makes legacy look
like current quest state. It also contradicts the mechanics legacy posture:
lineage belongs behind the active mechanic route and its `PROVENANCE.md` bridge.

## Options Considered

- Keep `quests/agon/captured/AOE-Q-AGON-*.md` as accepted note forms.
- Convert each note into an `AOA-EV-Q-*` schema-backed quest record.
- Move the former markdown notes into Agon provenance and keep `quests/`
  schema-backed.

## Decision

Move former Agon markdown quest notes behind the Agon legacy archive and route
them through `mechanics/agon/PROVENANCE.md`.

`quests/` remains the active schema-backed source quest record district for
`quests/<lane>/<state>/AOA-EV-Q-*.yaml`. Markdown quest notes must not live under
active quest lifecycle paths.

Future Agon proof pressure that is still open must enter as a schema-backed
quest record or as an active Agon part/bundle surface, not as a markdown note
under `quests/`.

## Rationale

This keeps the questbook mechanic honest: it owns source record schema,
lifecycle posture, human visibility, and generated readers, not historical Agon
note compatibility.

It also keeps Agon mechanics convex. Former note pressure can still be traced
through the Agon legacy archive, while active work starts from
`mechanics/agon/README.md`, `PARTS.md`, part contracts, and validation.

## Consequences

- Positive: `quests/` no longer presents non-generated, non-indexed markdown
  notes as active lifecycle source.
- Positive: Agon lineage is now behind the owning mechanic provenance bridge.
- Tradeoff: readers of the old markdown note route must cross
  `mechanics/agon/PROVENANCE.md` before archive lookup.

## Boundaries

This decision does not close any schema-backed quest, publish an eval result,
or make Agon proof-alignment notes into verdict authority.

It does not remove legacy lineage. It moves the lineage to the owning archive.

It does not prevent future Agon quests; future open quest pressure must use the
schema-backed source quest record shape.

## Validation

- `quests/README.md` and `quests/AGENTS.md` state that active quest records are
  schema-backed YAML.
- Agon archive-local accounting maps former markdown note paths to the Agon
  archive.
- `scripts/validate_repo.py` rejects markdown quest notes under active quest
  lifecycle paths.
- `python -m pytest -q tests/test_validate_repo.py -k quest_route`
- `python scripts/validate_repo.py`
