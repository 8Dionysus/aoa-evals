# SLC Alignment

## Role

This part owns Schools / Lineages / Campaigns alignment surfaces while keeping
schools, lineages, and campaigns non-authoritative inside `aoa-evals`.

It checks candidate SLC pressure without moving school, lineage, or campaign
canon into the eval layer.

## Route

`SLC pressure -> alignment seed -> generated registry -> non-canon validation`

## Source Surfaces

- `mechanics/agon/parts/slc-alignment/docs/AGON_SLC_EVAL_ALIGNMENT.md`
- `mechanics/agon/parts/slc-alignment/docs/AGON_SLC_EVAL_BOUNDARY.md`
- `mechanics/agon/parts/slc-alignment/config/agon_slc_eval_alignment.seed.json`
- `mechanics/agon/parts/slc-alignment/schemas/agon-slc-eval-alignment*.schema.json`
- `mechanics/agon/parts/slc-alignment/examples/agon_slc_eval_alignment.example.json`
- `mechanics/agon/parts/slc-alignment/generated/agon_slc_eval_alignment_registry.min.json`
- `mechanics/agon/parts/slc-alignment/manifests/`

## Inputs

- school, lineage, campaign, and owner-boundary alignment records;
- candidate-only status, forbidden effects, and no-canon stop-lines;
- part-local docs, schema, example, builder, validator, and tests.

## Outputs

- deterministic `agon_slc_eval_alignment_registry.min.json` output;
- non-canon candidate alignment records;
- validation failures when a record implies campaign authority, canon transfer,
  live verdict, or owner-truth takeover.

## Stronger Owner Split

`aoa-evals` owns candidate SLC alignment and local validation.

The owners of schools, lineages, campaigns, Tree of Sophia canon, and
Agents-of-Abyss law keep their own source truth and promotion authority.

## Stop-Lines

- Do not canonize schools, lineages, campaigns, or Tree of Sophia meaning from
  this part.
- Do not issue live verdicts, arena actions, rank mutations, scars, memory
  writes, or hidden scheduler actions.
- Do not treat SLC alignment as owner acceptance or campaign authority.

## Validation

```bash
python mechanics/agon/parts/slc-alignment/scripts/build_agon_slc_eval_alignment_registry.py --check
python mechanics/agon/parts/slc-alignment/scripts/validate_agon_slc_eval_alignment_registry.py
python -m pytest -q mechanics/agon/parts/slc-alignment/tests/test_agon_slc_eval_alignment_registry.py
```
