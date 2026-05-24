# Comparison Spine / Parts Route

`mechanics/comparison-spine/parts/` is the lower index for package-local
comparison fixture and readout parts. Use it after the parent Comparison Spine
route has selected a comparison mode and the next agent needs the exact part,
payload home, owner route, tool lane, and validation lane.

## Operating Card

| Field | Route |
| --- | --- |
| role | lower index for comparison-spine fixture and readout parts |
| input | comparison claim, bundle comparison surface, fixture contract, runner contract, generated comparison reader, or bounded report pressure |
| output | comparison part route, fixture family route, dossier route, generated-reader route, or bundle-local review handoff |
| owner | source bundles own claim meaning; comparison-spine owns comparison posture, read order, shared support fixtures, and bounded readouts |
| next route | `mechanics/comparison-spine/PARTS.md`, selected part README, affected source bundle, generated comparison reader, and parent validation lane |
| tools | comparison-spine builder, generated-surface checks, repo validator, and focused tests through `mechanics/comparison-spine/AGENTS.md#validation` |
| validation | `mechanics/comparison-spine/parts/AGENTS.md#validation` and `mechanics/comparison-spine/AGENTS.md#validation` |

## Active Parts

| Part | Operation | Start surface |
| --- | --- | --- |
| `spine-overview/` | cross-mode comparison-spine read order | `spine-overview/README.md` |
| `fixed-baseline/` | same-task fixed-baseline fixture family and dossier | `fixed-baseline/README.md` |
| `peer-compare/` | artifact/process paired fixture families and dossiers | `peer-compare/README.md` |
| `longitudinal-window/` | repeated-window fixture family plus repeated-window and stress-recovery dossiers | `longitudinal-window/README.md` |

## Owner Pressure Routes

| Pressure | Route |
| --- | --- |
| source claim meaning or bundle promotion | bundle-local `EVAL.md`, `eval.yaml`, and review route |
| style-only movement as capability movement | source bundle support note plus selected comparison-mode report |
| repo-global score or broad growth proof | source bundle review plus longitudinal evidence and growth/progression owner route |
| shared dossier outranking source proof object | source bundle and selected comparison part route |
| generated comparison reader as source truth | source bundle, builder, and generated check route |

## Part Admission Route

| Source signal | Operation test | Next route |
| --- | --- | --- |
| cross-mode comparison read order | overview dossier owns the read order | `spine-overview/README.md` |
| same-task frozen baseline | fixed-baseline fixture and report contract exist | `fixed-baseline/README.md` |
| side-by-side artifact/process comparison | peer fixture and paired report contract exist | `peer-compare/README.md` |
| repeated-window or stress-recovery comparison | longitudinal fixture and report contract exist | `longitudinal-window/README.md` |
| new comparison mode pressure | distinct comparison surface, fixture/report contract, generated route, and validation lane exist | parent `PARTS.md` update plus decision review |

## Validation

Use [AGENTS](AGENTS.md#validation) for executable validation commands. This
parts index names the active parts and their roles; the parts route card owns
the command lane.
