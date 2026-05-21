# Proof Object Parts

## Role

`PARTS.md` lists the active parts inside `mechanics/proof-object/`.

It is not the bundle directory and not a generated catalog. A proof-object part
is active only when it keeps source bundle meaning complete, bounded, and
stronger than derived readers or emitted companions.

## Active Parts

### `bundle-authoring`

Owned operation:

`origin proof pressure -> new bundle scaffold -> bounded source proof object`

This part owns the authoring scaffold:

- `mechanics/proof-object/parts/bundle-authoring/templates/EVAL.template.md`

### `bundle-contracts`

Owned operation:

`source bundle frontmatter and manifest -> schema-backed proof-object contract -> validation`

This part owns the eval source contract schemas:

- `mechanics/proof-object/parts/bundle-contracts/schemas/eval-frontmatter.schema.json`
- `mechanics/proof-object/parts/bundle-contracts/schemas/eval-manifest.schema.json`

## Part Contract

Inputs are origin proof pressure, source bundle text, `eval.yaml` metadata,
authoring template expectations, and proof-object schema requirements.

Outputs are bounded source proof bundle scaffolds, schema-backed frontmatter and
manifest contracts, and validation routes that keep generated readers derived
from authored proof objects.

Owner split stays explicit: `bundles/*/EVAL.md` and `eval.yaml` own bundle
meaning; proof-object parts own authoring and contract support; generated
catalogs and reports stay weaker than source bundles.

Stop-lines forbid moving `bundles/` into this mechanic, turning templates into
doctrine, weakening schemas for convenience, or treating generated readers as
proof authority.

Validation is `python scripts/validate_repo.py`,
`python scripts/build_catalog.py --check`, and
`python scripts/validate_semantic_agents.py`.

## Stop-Lines

- Do not move `bundles/` into `mechanics/proof-object/`.
- Do not make the template a doctrine essay or example bundle.
- Do not weaken schemas to pass an under-specified bundle.
- Do not hand-edit generated readers as proof authority.
- Do not turn status, maturity, or catalog entries into stronger proof than
  `EVAL.md` and `eval.yaml`.

## Validation

After part movement or proof-object contract changes, run:

```bash
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python scripts/validate_semantic_agents.py
```
