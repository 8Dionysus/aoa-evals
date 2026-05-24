# Agon / Parts Route

`mechanics/agon/parts/` is the lower index for active Agon proof-alignment
parts. Use it after the parent Agon route has selected one proof-alignment
question and the next agent needs the exact part, payload home, owner route,
tool lane, and validation lane.

## Operating Card

| Field | Route |
| --- | --- |
| role | lower index for Agon proof-alignment artifact families |
| input | Agon alignment pressure, seed config, generated registry, schema/example payload, recurrence component, hook, or new alignment question |
| output | part README route, part-local payload home, deterministic registry, validation lane, recurrence route, or stronger-owner handoff |
| owner | `aoa-evals` owns local proof-alignment shape and validation; stronger owners keep doctrine, canon, arena, rank, trust, and live authority |
| next route | `mechanics/agon/PARTS.md`, selected part README, part-local source surfaces, generated payloads, and stronger-owner route |
| tools | part-local builders and validators routed through `mechanics/agon/AGENTS.md#validation` |
| validation | `mechanics/agon/parts/AGENTS.md#validation` and `mechanics/agon/AGENTS.md#validation` |

## Active Parts

| Part | Operation | Start surface |
| --- | --- | --- |
| `court-prebinding/` | court prebinding model, seed config, generated registry, schemas, examples, recurrence component, and hooks | `court-prebinding/README.md` |
| `ccs-alignment/` | Agon CCS law alignment seed and registry | `ccs-alignment/README.md` |
| `vds-alignment/` | verdict draft status alignment and verdict draft checks | `vds-alignment/README.md` |
| `mechanical-trial-suites/` | candidate trial-suite alignment against mechanical trial surfaces | `mechanical-trial-suites/README.md` |
| `retention-rank-alignment/` | retention and rank pressure alignment while rank/trust authority stays outside evals | `retention-rank-alignment/README.md` |
| `epistemic-alignment/` | epistemic boundary alignment while doctrine and live judgment stay outside evals | `epistemic-alignment/README.md` |
| `slc-alignment/` | schools, lineages, and campaigns alignment while canon and arena authority stay outside evals | `slc-alignment/README.md` |
| `kag-alignment/` | KAG promotion-path alignment while KAG canon and source truth stay outside evals | `kag-alignment/README.md` |
| `sophian-threshold-alignment/` | Sophian threshold alignment while Tree of Sophia canon stays outside evals | `sophian-threshold-alignment/README.md` |

## Owner Pressure Routes

| Pressure | Route |
| --- | --- |
| AoA doctrine, court law, or Agon canon | `Agents-of-Abyss` owner route |
| Tree of Sophia canon or Sophian source meaning | Tree of Sophia owner route |
| KAG promotion or graph truth | `aoa-kag` owner route |
| live verdict, arena, rank, trust, or promotion authority | owning role/runtime route before eval proof wording changes |
| generated registry drift | part-local builder, generated payload, and validator route |
| recurrence component or hook pressure | part-local recurrence manifest route plus `mechanics/recurrence/` when the pressure becomes recurrence proof |

## Part Admission Route

| Source signal | Operation test | Next route |
| --- | --- | --- |
| alignment pressure matches an existing part's source and validation route | existing part can own source, generated, and validation surfaces honestly | selected part README |
| alignment pressure has a different source shape, generated surface, and validator lane | distinct proof-alignment operation exists | parent `PARTS.md` update plus decision review |
| historical wave landing pressure | active part route can absorb distilled source truth | parent `PROVENANCE.md` before any active surface change |
