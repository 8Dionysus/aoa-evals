# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/questbook/DIRECTION.md` for current operating direction, `mechanics/questbook/PARTS.md` for active parts, and `mechanics/questbook/PROVENANCE.md` only when legacy or former placement matters.

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

1. root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/PROOF_TOPOLOGY.md`
5. `mechanics/README.md`
6. `mechanics/questbook/README.md`
7. `mechanics/questbook/PARTS.md`
8. `mechanics/questbook/PROVENANCE.md`
9. `QUESTBOOK.md`
10. `quests/README.md`
11. `quests/AGENTS.md`
12. `quests/LIFECYCLE.md`
13. `mechanics/questbook/parts/source-record-contract/schemas/quest.schema.json`
14. `mechanics/questbook/parts/dispatch-reader/schemas/quest_dispatch.schema.json`
15. `docs/decisions/0004-questbook-topology.md`
16. `docs/decisions/0006-questbook-mechanic-package.md`
17. `docs/decisions/0047-questbook-schema-parts.md`

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

Run:

```bash
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

If source quest records changed intentionally and generated readers must be
refreshed, rebuild them before rerunning the checks:

```bash
python scripts/build_catalog.py
```

## Closeout

Report whether the change touched source quest records, `QUESTBOOK.md`,
generated quest readers, lane/state migration posture, or post-session harvest
boundaries.
