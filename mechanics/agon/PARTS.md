# Agon Parts

## Purpose

Agon is one mechanic. Its parts are artifact families that own a bounded piece
of the local proof-alignment operation.

A part exists when it has source artifacts and a checkable route: docs or
config, generated output when relevant, schemas or examples when relevant,
builder or validator code, tests, and recurrence surfaces when present.

## Part Map

| Part | Owns | Main Check |
| --- | --- | --- |
| `court-prebinding` | court prebinding model, court prebinding docs, seed config, generated prebinding registry, schemas, examples, recurrence component, hooks | `python mechanics/agon/parts/court-prebinding/scripts/validate_agon_eval_prebindings.py` |
| `ccs-alignment` | Agon CCS law alignment seed and registry | `python mechanics/agon/parts/ccs-alignment/scripts/validate_agon_ccs_eval_alignment.py` |
| `vds-alignment` | verdict draft status alignment and verdict draft checks | `python mechanics/agon/parts/vds-alignment/scripts/validate_agon_vds_eval_alignment.py` |
| `mechanical-trial-suites` | candidate trial-suite alignment against mechanical trial surfaces | `python mechanics/agon/parts/mechanical-trial-suites/scripts/validate_agon_mechanical_trial_eval_suites.py` |
| `retention-rank-alignment` | retention and rank pressure alignment without rank or trust mutation | `python mechanics/agon/parts/retention-rank-alignment/scripts/validate_agon_retention_rank_eval_alignment.py` |
| `epistemic-alignment` | epistemic boundary alignment without doctrine rewrite or live judgment | `python mechanics/agon/parts/epistemic-alignment/scripts/validate_agon_epistemic_eval_alignment.py` |
| `slc-alignment` | schools, lineages, and campaigns alignment without canon or arena authority | `python mechanics/agon/parts/slc-alignment/scripts/validate_agon_slc_eval_alignment_registry.py` |
| `kag-alignment` | KAG promotion-path alignment without KAG canon or source-truth transfer | `python mechanics/agon/parts/kag-alignment/scripts/validate_agon_kag_eval_alignment_registry.py` |
| `sophian-threshold-alignment` | Sophian threshold alignment without Tree of Sophia canon write | `python mechanics/agon/parts/sophian-threshold-alignment/scripts/validate_agon_sophian_eval_alignment_registry.py` |

## Part Contract

Each part keeps its source and generated surfaces together:

- `docs/` explains the bounded alignment question;
- `config/` owns seed inputs when the part is config-backed;
- `schemas/` owns structural constraints;
- `examples/` owns public-safe example payloads;
- `generated/` owns builder output only;
- `scripts/` owns the builder and validator for that part;
- `tests/` owns regression tests for the part;
- part-local `mechanics/agon/parts/<part>/manifests/recurrence/` owns
  observe-only recurrence components and hooks when the part participates in
  recurrence review.

Inputs are part-local docs, seed configs, schemas, examples, and recurrence
pressure for one Agon proof-alignment question.

Outputs are deterministic registries, validation results, test coverage, and
observe-only recurrence hooks that remain candidate-only until bundle-local
review or owner handoff.

Owner split stays explicit: `aoa-evals` owns proof-alignment shape and local
validation; `Agents-of-Abyss`, Tree of Sophia, KAG, or other stronger owners
keep their doctrine, canon, and live authority.

Stop-lines are part of the contract: no Agon part grants live verdict,
promotion, arena, rank, trust, doctrine rewrite, or sibling-owner acceptance.

Validation is the part-local builder, validator, and test path named in the
part map.

## Routing Rules

- Put a new Agon artifact in the part that owns its proof-alignment question.
- Create a new part only when no existing part can own the source, generated,
  and validation route honestly.
- Do not split one future-growing operation into a proof-suffix child. Grow the
  parent part unless the new work has a different source, generated, and
  validation route.
- Keep historical wave landing files behind `PROVENANCE.md` unless they are
  distilled into an active part surface.
