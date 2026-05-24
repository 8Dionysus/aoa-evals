# Questbook / Quest Dispatch Reader Part

## Role

This part owns the projection contract for generated quest readers.

It routes generated quest navigation. Source quest truth stays in quest source
records, human open-obligation visibility stays in `QUESTBOOK.md`, proof
verdicts stay with bundle-local proof surfaces, and live dispatch authority
stays with the owner route.

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
records; generated JSON is updated through the builder.

Eval bundles, proof mechanics, sibling repositories, and owner-local surfaces
own any later proof verdict, promotion, acceptance, or implementation work.
`aoa-evals` owns only the reader schema, projection shape, and claim limits
for generated quest navigation.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| generated reader used in place of source quest record | `quests/<lane>/<state>/AOA-EV-Q-*.yaml` |
| generated reader used as eval bundle or portable verdict authority | bundle-local proof surface |
| hand edit to generated quest reader | `scripts/build_catalog.py` and source quest record update |
| missing source quest hidden by projection patch | source quest record repair |
| generated dispatch used as live task assignment, owner acceptance, release readiness, or proof-surface promotion | owner route, release-support route, or bundle/mechanic proof evidence |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
