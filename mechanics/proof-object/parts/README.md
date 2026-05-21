# Proof Object / Parts Route

## Role

`mechanics/proof-object/parts/` holds support parts for source proof-object
authoring and validation.

Parts support `evals/**/EVAL.md` and `evals/**/eval.yaml`. They do not own
source eval meaning and do not replace generated readers.

## Active Parts

- `eval-authoring/`: starter template for bounded eval package authoring.
- `eval-contracts/`: schema-backed frontmatter and manifest contracts.

## Validation

Use [AGENTS](AGENTS.md#validation) for executable validation commands. This
parts index names the active parts and their roles; the parts route card owns
the command lane.
