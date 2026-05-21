# Proof Object / Part Index

## Role

`PARTS.md` lists the active parts inside `mechanics/proof-object/`.

It is not the source eval package directory and not a generated catalog. A
proof-object part is active only when it keeps source eval meaning complete,
bounded, and stronger than derived readers or emitted companions.

## Active Parts

### `eval-authoring`

Owned operation:

`origin proof pressure -> new eval scaffold -> bounded source proof object`

This part owns the authoring scaffold:

- `mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md`

### `eval-contracts`

Owned operation:

`source eval frontmatter and manifest -> schema-backed proof-object contract -> validation`

This part owns the eval source contract schemas:

- `mechanics/proof-object/parts/eval-contracts/schemas/eval-frontmatter.schema.json`
- `mechanics/proof-object/parts/eval-contracts/schemas/eval-manifest.schema.json`

## Part Contract

Inputs are origin proof pressure, source eval text, `eval.yaml` metadata,
authoring template expectations, and proof-object schema requirements.

Outputs are bounded source eval scaffolds, schema-backed frontmatter and
manifest contracts, and validation routes that keep generated readers derived
from authored proof objects.

Owner split stays explicit: `evals/**/EVAL.md` and `eval.yaml` own source eval
meaning; proof-object parts own authoring and contract support; generated
catalogs and reports stay weaker than source eval packages.

Stop-lines forbid moving `evals/` into this mechanic, turning templates into
doctrine, weakening schemas for convenience, or treating generated readers as
proof authority.

Validation routes through [AGENTS](AGENTS.md#validation) and the affected part
route cards.

## Stop-Lines

- Do not move `evals/` into `mechanics/proof-object/`.
- Do not make the template a doctrine essay or example eval.
- Do not weaken schemas to pass an under-specified eval package.
- Do not hand-edit generated readers as proof authority.
- Do not turn status, maturity, or catalog entries into stronger proof than
  `EVAL.md` and `eval.yaml`.

## Validation

After part movement or proof-object contract changes, use
[AGENTS](AGENTS.md#validation) for executable validation commands.
