# AGENTS.md

## Entry Route

When package semantics or direction are relevant, consult the package README and then the `mechanics/agon/DIRECTION.md`, `mechanics/agon/PARTS.md`, and `mechanics/agon/PROVENANCE.md` routes as needed for the touched source.

## Applies to

`mechanics/agon/` and all Agon mechanic parts.

## Role

This package protects the local Agon proof-alignment loop:

`part source -> generated registry -> candidate-only check -> observe-only recurrence signal -> bundle-local review or owner handoff`

## Operating Card

| Field | Route |
| --- | --- |
| role | Agon proof-alignment loop for eval-side part sources and generated registries |
| input | part-local source config, generated registry drift, candidate-only check, observe-only recurrence signal, stop-line pressure, or owner handoff question |
| output | part-local source update, generated registry check, bundle-local review, or owner handoff |
| owner | `aoa-evals` owns local proof-alignment routes; Agents-of-Abyss and stronger owners keep live verdict, summon, memory, rank, KAG, ToS, scheduler, and arena authority |
| next route | `mechanics/agon/README.md`, `DIRECTION.md`, `PARTS.md`, target part surfaces, Agon owner handoff docs, and affected source bundle |
| tools | touched part builder, validator, tests, root validator, semantic AGENTS validator |
| validation | this card's `Validation` section |

current operating direction `mechanics/agon/DIRECTION.md`; active-to-archive bridge `mechanics/agon/PROVENANCE.md`.

## Route Rules

- Treat `mechanics/agon/` as the parent mechanic and `parts/*` as owned
  artifact families.
- Keep part-local source config stronger than generated registry output.
- Keep part-local builders and validators with the artifacts they build and
  validate.
- Keep Agents-of-Abyss law stronger than local eval alignment wording.
- Keep recurrence manifests and hooks observe-only.
- Keep quest source records under `quests/` unless the questbook mechanic moves
  them with source-path compatibility.
- Route live verdict, closure, summon, memory write, rank mutation, KAG
  promotion, Tree of Sophia promotion, hidden scheduler, and arena authority to
  stronger owners.
- Preserve explicit stop-line tokens such as `no_live_verdict`,
  `no_closure_grant`, `no_live_summon`, `no_durable_memory_write`,
  `no_rank_mutation`, and `no_tree_of_sophia_promotion`.
- Fix registry inputs or route evidence instead of weakening Agon stop-lines.

## Validation

Use the on-demand [VALIDATION.md](VALIDATION.md) route for executable checks.

Run the touched part builder, validator, and test first. For a full Agon pass:

## Closeout

Report which Agon part changed, which source and generated artifacts moved or
changed, which stop-lines were preserved, and which validation ran.
