# Questbook / Parts Route

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

Use [AGENTS](AGENTS.md#validation) for executable validation commands. This
parts index names the active parts and their roles; the parts route card owns
the command lane.
