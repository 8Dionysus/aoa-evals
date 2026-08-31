# AGENTS.md

## Entry Route

When package semantics or direction are relevant, consult the package README and then the `mechanics/questbook/DIRECTION.md`, `mechanics/questbook/PARTS.md`, and `mechanics/questbook/PROVENANCE.md` routes as needed for the touched source.

## Applies to

`mechanics/questbook/` and the questbook operation route.

## Role

This package protects the quest obligation loop:

`source quest record -> human index -> generated quest reader -> deferred return or reviewed promotion`

## Operating Card

| Field | Route |
| --- | --- |
| role | questbook operation route for source quest records and generated quest readers |
| input | source quest record, `QUESTBOOK.md` obligation, lane/state change, generated quest reader drift, lifecycle posture, or post-session harvest pressure |
| output | source quest record update, human index route, generated reader check, deferred return, reviewed promotion route, or owner handoff |
| owner | quest source records own quest state; this package owns the questbook route and generated reader bridge |
| next route | `mechanics/questbook/README.md`, `DIRECTION.md`, `PARTS.md`, `QUESTBOOK.md`, `quests/AGENTS.md`, `quests/LIFECYCLE.md`, and affected source quest record |
| tools | catalog builder, root validator, semantic AGENTS validator |
| validation | this card's `Validation` section |

## Read before editing
Read only the route needed for the touched source: consult the nearest README when its human or semantic contract is required, then follow the source-owner and validation routes conditionally.
Each package keeps current operating direction in `DIRECTION.md`; the active-to-archive bridge in `PROVENANCE.md` is consulted only when legacy names are involved.

## Route Rules

- Change `quests/<lane>/<state>/*.yaml` paths together with generated
  projection and validator support in the same slice.
- Keep old top-level quest paths as legacy path vocabulary in route docs.
- Keep former root quest-schema aliases as historical compatibility
  vocabulary; the active schema contracts are part-local under
  `mechanics/questbook/parts/`.
- Keep the state directory aligned with the source record `state`.
- Keep lifecycle meaning aligned with `quests/LIFECYCLE.md`.
- List closed quests through their closed-state route below active obligations.
- Treat quest harvest output as review input below proof authority and owner
  acceptance.
- Route post-session promotion through the owning review path.
- Create sibling-owner tasks from quest metadata only through that owner route.

## Validation

Use the on-demand [VALIDATION.md](VALIDATION.md) route for executable checks.

Run:

If source quest records changed intentionally and generated readers must be
refreshed, rebuild them before rerunning the checks:

## Closeout

Report whether the change touched source quest records, `QUESTBOOK.md`,
generated quest readers, lane/state migration posture, or post-session harvest
boundaries.
