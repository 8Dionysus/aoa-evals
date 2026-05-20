# AGENTS.md

## Applies to

`mechanics/questbook/` and the questbook operation route.

## Role

This package protects the quest obligation loop:

`source quest record -> human index -> generated quest reader -> deferred return or reviewed promotion`

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/PROOF_TOPOLOGY.md`
5. `mechanics/README.md`
6. `mechanics/questbook/README.md`
7. `QUESTBOOK.md`
8. `quests/README.md`
9. `quests/AGENTS.md`
10. `quests/LIFECYCLE.md`
11. `schemas/quest.schema.json`
12. `schemas/quest_dispatch.schema.json`
13. `docs/decisions/0004-questbook-topology.md`
14. `docs/decisions/0006-questbook-mechanic-package.md`

## Boundaries

- Do not change `quests/<lane>/<state>/*.yaml` paths without generated
  projection and validator support in the same slice.
- Do not reintroduce old top-level quest paths except as legacy path vocabulary
  in route docs.
- Keep the state directory aligned with the source record `state`.
- Keep lifecycle meaning aligned with `quests/LIFECYCLE.md`.
- Do not list closed quests as active obligations.
- Do not treat quest harvest output as proof authority or owner acceptance.
- Do not use active-route evidence as a post-session promotion verdict.
- Do not create sibling-owner tasks from quest metadata without routing to that
  owner.

## Validation

Run:

```bash
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

## Closeout

Report whether the change touched source quest records, `QUESTBOOK.md`,
generated quest readers, lane/state migration posture, or post-session harvest
boundaries.
