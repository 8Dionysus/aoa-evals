# Quest Dispatch Reader

## Role

This part owns the projection contract for generated quest readers.

It is not the source quest record, human quest index, proof verdict, or portable
live dispatch authority.

## Owned Operation

`source quest record -> generated catalog and dispatch reader -> deferred return route`

## Source Surfaces

- `mechanics/questbook/parts/dispatch-reader/schemas/quest_dispatch.schema.json`
- `generated/quest_catalog.min.json`
- `generated/quest_dispatch.min.json`
- `generated/quest_catalog.min.example.json`
- `generated/quest_dispatch.min.example.json`
- `scripts/build_catalog.py`
- `scripts/validate_repo.py`

## Inputs

- validated source quest records;
- quest lifecycle posture;
- open and closed quest state;
- optional orchestrator class refs and capability targets.

## Outputs

- generated quest catalog reader;
- generated dispatch reader;
- example mirrors for public-safe projection shape;
- validation errors when source and generated readers drift.

## Stronger Owner Split

`quests/<lane>/<state>/AOA-EV-Q-*.yaml` owns source quest truth.
`mechanics/questbook/parts/source-record-contract/` owns the source schema and
lane/state contract. `quests/LIFECYCLE.md` owns lifecycle state vocabulary.

`QUESTBOOK.md` owns human open-obligation visibility. This part owns the
generated projection contract and drift detection for quest catalog and
dispatch readers. `scripts/build_catalog.py` derives those readers from source
records; generated JSON is not edited as truth.

Eval bundles, proof mechanics, sibling repositories, and owner-local surfaces
own any later proof verdict, promotion, acceptance, or implementation work.
`aoa-evals` owns only the reader schema, projection shape, and claim limits
for generated quest navigation.

## Stop-Lines

- Generated readers do not replace source quest records.
- Generated readers do not become eval bundles or portable verdict authority.
- Do not hand-edit generated quest readers as source truth.
- Do not hide a missing source quest by patching the projection.
- Do not treat generated dispatch as live task assignment, owner acceptance,
  release readiness, or proof-surface promotion.

## Validation

Payload coverage anchor: `mechanics/questbook/parts/dispatch-reader/`.

```bash
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
