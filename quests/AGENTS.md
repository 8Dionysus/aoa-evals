# AGENTS.md

## Applies to

`quests/` source quest records.

## Role

This lane holds source quest records for deferred proof obligations. Treat
`quests/` as the source quest record district, with `QUESTBOOK.md` as the human
open-obligation index, `mechanics/questbook/` as the operation package, and
generated quest files as dispatch readers.

Quests are obligation-return surfaces. They track missing proof, regression
gaps, verdict-bridge debt, proof-pressure harvest candidates, and owner
handoffs that still need a bounded next route.

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `QUESTBOOK.md`
5. `quests/README.md`
6. `quests/LIFECYCLE.md`
7. `mechanics/questbook/parts/source-record-contract/schemas/quest.schema.json`
8. `mechanics/questbook/parts/dispatch-reader/schemas/quest_dispatch.schema.json`
9. `docs/decisions/0004-questbook-topology.md`

## Boundaries

- `quests/<lane>/<state>/*.yaml` are source quest records.
- `QUESTBOOK.md` is the human index of open obligations.
- `generated/quest_catalog.min.json` and `generated/quest_dispatch.min.json`
  are derived readers.
- Eval bundle meaning stays in `evals/**/EVAL.md` and `eval.yaml`.
- Roadmap direction stays in `ROADMAP.md`.
- Former Agon markdown quest notes live behind
  `mechanics/agon/PROVENANCE.md` as Agon lineage while active lifecycle source
  records stay schema-backed YAML.
- Old top-level quest paths are legacy path vocabulary; active source files use
  lane/state placement.
- Keep markdown note forms out of `quests/<lane>/<state>/`; active quest
  records use schema-backed YAML.
- Source quest path changes require validators, generated projections, and
  compatibility posture in the same slice.
- Keep each state directory aligned with the source record `state`.
- Use `quests/LIFECYCLE.md` for open-index, closed-state, return, and
  promotion posture before changing `state`.
- Proof verdict authority remains with source eval and reviewed proof surfaces.

## Validation

After editing source quest records or quest route docs, run:

```bash
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

If generated quest outputs are stale, rebuild them through:

```bash
python scripts/build_catalog.py
```

Then rerun the checks.

## Closeout

Report which quest IDs or quest route surfaces changed, whether generated quest
projections were rebuilt, which validation ran, and whether any future
lane/state movement remains intentionally deferred.
