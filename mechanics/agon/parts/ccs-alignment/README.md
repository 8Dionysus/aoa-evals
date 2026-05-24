# Agon / CCS Alignment Part

## Role

This part owns the candidate alignment between local eval prechecks and
Agents-of-Abyss CCS law families.

It checks whether local Agon eval prechecks can reference center-law pressure
without becoming center law.

## Route

`center-law reference -> CCS alignment seed -> generated alignment registry -> precheck-only validation`

## Source Surfaces

- `mechanics/agon/parts/ccs-alignment/docs/AGON_CCS_EVAL_ALIGNMENT.md`
- `mechanics/agon/parts/ccs-alignment/config/agon_ccs_eval_alignment.seed.json`
- `mechanics/agon/parts/ccs-alignment/schemas/agon-ccs-eval-alignment*.schema.json`
- `mechanics/agon/parts/ccs-alignment/examples/agon_ccs_eval_alignment.example.json`
- `mechanics/agon/parts/ccs-alignment/generated/agon_ccs_eval_alignment_registry.min.json`
- `mechanics/agon/parts/ccs-alignment/manifests/`

## Inputs

- CCS law-family refs and local precheck refs;
- seeded alignment records with required stop-lines and forbidden effects;
- part-local schema, example, builder, validator, and test coverage.

## Outputs

- deterministic `agon_ccs_eval_alignment_registry.min.json` output;
- precheck-only candidate alignment records;
- validation failures when CCS refs, stop-lines, forbidden effects, or generated
  registry shape drift.

## Stronger Owner Split

`aoa-evals` owns the local precheck-only alignment registry and its validator.

Agents-of-Abyss owns CCS law, center doctrine, and the meaning of any law-family
ref that this part cites.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| center law or CCS law pressure | route to Agents-of-Abyss law owners; local CCS alignment stays precheck-only |
| live verdict, closure, arena action, rank mutation, scar write, memory write, or Tree of Sophia promotion pressure | route to the stronger live owner; this part records alignment evidence only |
| local registry output conflicts with the part-local seed or Agents-of-Abyss law | route back to the seed, validator, or cited law-family owner before using the registry |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
