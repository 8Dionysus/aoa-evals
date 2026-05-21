# AGENTS.md

## Applies to

`quests/` source quest records.

## Role

This lane holds source quest records for deferred proof obligations.

Quests are obligation-return surfaces. They track missing proof, regression
gaps, verdict-bridge debt, proof-pressure harvest candidates, and owner
handoffs that are not yet eval bundles.

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
- Eval bundle meaning stays in `bundles/*/EVAL.md` and `eval.yaml`.
- Roadmap direction stays in `ROADMAP.md`.
- Former Agon markdown quest notes live behind
  `mechanics/agon/PROVENANCE.md` as Agon lineage, not active quest lifecycle
  source records.
- Old top-level quest paths are legacy path vocabulary, not active source
  files.
- Do not add markdown note forms under `quests/<lane>/<state>/`; active quest
  records are schema-backed YAML.
- Do not change source quest paths without updating validators, generated
  projections, and compatibility posture in the same slice.
- Keep each state directory aligned with the source record `state`.
- Use `quests/LIFECYCLE.md` for open-index, closed-state, return, and
  promotion posture before changing `state`.
- Do not treat a quest as proof verdict authority.

## Validation

After editing source quest records or quest route docs, run:

```bash
python scripts/build_catalog.py --check
python scripts/validate_repo.py
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
