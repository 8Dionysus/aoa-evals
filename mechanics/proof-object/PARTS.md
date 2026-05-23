# Proof Object / Part Index

## Role

`PARTS.md` lists the active parts inside `mechanics/proof-object/`.

Source eval packages stay under `evals/`, and generated catalogs stay derived
from source packages. A proof-object part is active only when it keeps source
eval meaning complete, bounded, and stronger than derived readers or emitted
companions.

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

Stop-lines route source-package movement, template doctrine pressure, schema
weakening pressure, and generated-reader authority pressure back to their
owning surfaces.

Validation routes through [AGENTS](AGENTS.md#validation) and the affected part
route cards.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| source eval package movement appears | keep source eval packages under `evals/` |
| template reads as doctrine essay or example eval | route meaning to repo proof guides or the source proof package |
| schema loosening would make an under-specified eval pass | route back to source package completeness |
| generated reader needs a proof change | edit the source package and rebuild the reader |
| status, maturity, or catalog entry reads stronger than source proof | return to `EVAL.md`, `eval.yaml`, and bundle-local review |

## Validation

After part movement or proof-object contract changes, use
[AGENTS](AGENTS.md#validation) for executable validation commands.
