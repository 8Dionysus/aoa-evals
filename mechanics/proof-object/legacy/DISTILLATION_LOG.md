# Proof Object Distillation Log

## Role

This log accounts for proof-object lineage distilled into active parts.

It records former placement, active owner, reason, and validation route pointer.

## Entries

### 2026-05-20 - Root template and eval schemas distilled into proof-object parts

Former root placement:

- `templates/EVAL.template.md`
- `schemas/eval-frontmatter.schema.json`
- `schemas/eval-manifest.schema.json`

Active parts:

- `mechanics/proof-object/parts/eval-authoring/`
- `mechanics/proof-object/parts/eval-contracts/`

Reason:

The template and schemas constrain source proof-object authoring and validation.
Their current home is `proof-object`, keeping bundle contracts close to the
operation that owns proof-object completeness while source bundle meaning
remains under `evals/`.

Validation route:

Use [AGENTS.md](AGENTS.md#validation).
