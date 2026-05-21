# Questbook Parts

## Role

`mechanics/questbook/parts/` holds active support parts for the quest
obligation loop.

Parts support quest source records and generated readers. They do not own
roadmap direction, eval bundle meaning, sibling owner acceptance, or proof
verdicts.

## Active Parts

- `source-record-contract/`: schema-backed source quest record and lifecycle
  contract.
- `dispatch-reader/`: generated quest catalog and dispatch projection contract.

## Validation

```bash
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
