# Agon / Part Index

## Purpose

Agon is one mechanic. Its parts are artifact families that own a bounded piece
of the local proof-alignment operation.

A part exists when it has source artifacts and a checkable route: docs or
config, generated output when relevant, schemas or examples when relevant,
builder or validator code, tests, and recurrence surfaces when present.

## Part Map

| Part | Owns | Main validation surface |
| --- | --- | --- |
| `court-prebinding` | court prebinding model, court prebinding docs, seed config, generated prebinding registry, schemas, examples, recurrence component, hooks | `mechanics/agon/parts/court-prebinding/scripts/validate_agon_eval_prebindings.py` through `mechanics/agon/AGENTS.md#validation` |
| `ccs-alignment` | Agon CCS law alignment seed and registry | `mechanics/agon/parts/ccs-alignment/scripts/validate_agon_ccs_eval_alignment.py` through `mechanics/agon/AGENTS.md#validation` |
| `vds-alignment` | verdict draft status alignment and verdict draft checks | `mechanics/agon/parts/vds-alignment/scripts/validate_agon_vds_eval_alignment.py` through `mechanics/agon/AGENTS.md#validation` |
| `mechanical-trial-suites` | candidate trial-suite alignment against mechanical trial surfaces | `mechanics/agon/parts/mechanical-trial-suites/scripts/validate_agon_mechanical_trial_eval_suites.py` through `mechanics/agon/AGENTS.md#validation` |
| `retention-rank-alignment` | retention and rank pressure alignment with rank and trust authority routed to stronger owners | `mechanics/agon/parts/retention-rank-alignment/scripts/validate_agon_retention_rank_eval_alignment.py` through `mechanics/agon/AGENTS.md#validation` |
| `epistemic-alignment` | epistemic boundary alignment with doctrine and live judgment routed to owner surfaces | `mechanics/agon/parts/epistemic-alignment/scripts/validate_agon_epistemic_eval_alignment.py` through `mechanics/agon/AGENTS.md#validation` |
| `slc-alignment` | schools, lineages, and campaigns alignment with canon and arena authority routed to owners | `mechanics/agon/parts/slc-alignment/scripts/validate_agon_slc_eval_alignment_registry.py` through `mechanics/agon/AGENTS.md#validation` |
| `kag-alignment` | KAG promotion-path alignment with KAG canon and source truth routed to KAG owner surfaces | `mechanics/agon/parts/kag-alignment/scripts/validate_agon_kag_eval_alignment_registry.py` through `mechanics/agon/AGENTS.md#validation` |
| `sophian-threshold-alignment` | Sophian threshold alignment with Tree of Sophia canon writes routed to ToS owner surfaces | `mechanics/agon/parts/sophian-threshold-alignment/scripts/validate_agon_sophian_eval_alignment_registry.py` through `mechanics/agon/AGENTS.md#validation` |

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

Stop-lines route live verdict, promotion, arena, rank, trust, doctrine rewrite,
and sibling-owner acceptance to stronger owners.

Validation routes through [AGENTS](AGENTS.md#validation). This part map names
the primary validation surfaces without owning executable commands.

## Routing Rules

- Put a new Agon artifact in the part that owns its proof-alignment question.
- Create a new part only when no existing part can own the source, generated,
  and validation route honestly.
- Grow one future-extensible operation inside its parent part. A proof-suffix
  child starts only when the new work has a different source, generated, and
  validation route.
- Keep historical wave landing files behind `PROVENANCE.md` unless they are
  distilled into an active part surface.
