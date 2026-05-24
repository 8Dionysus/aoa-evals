# Distillation / Parts Route

`mechanics/distillation/parts/` is the lower index for active eval-side
Distillation proof parts. Use it after the parent Distillation route has
selected a proof-side support operation and the next agent needs the exact
part, payload home, owner route, tool lane, and validation lane.

## Operating Card

| Field | Route |
| --- | --- |
| role | lower index for Distillation proof-side support parts |
| input | witness-facing source, compost artifact, visible source ref, review state, runtime candidate mapping, reviewed memo adoption evidence, receipt visibility, or recall surface |
| output | part README route, fixture family route, generated proof-artifact path, report expectation, owner handoff, or bundle-local review route |
| owner | `aoa-evals` owns bounded proof interpretation; AoA center, Tree of Sophia, memo, agents, runtime, KAG, and owner repositories keep source authority |
| next route | `mechanics/distillation/PARTS.md`, selected part README, affected source bundle, stronger-owner route, and parent validation lane |
| tools | bundle-local checks, generated catalog check, repo validator, and semantic AGENTS validator through `mechanics/distillation/AGENTS.md#validation` |
| validation | `mechanics/distillation/parts/AGENTS.md#validation` and `mechanics/distillation/AGENTS.md#validation` |

## Active Parts

| Part | Operation | Start surface |
| --- | --- | --- |
| `compost-provenance/` | provenance-preserving compost proof support for witness-derived abstraction | `compost-provenance/README.md` |
| `runtime-candidate-adoption/` | reviewed runtime distillation candidate adoption proof support | `runtime-candidate-adoption/README.md` |

## Owner Pressure Routes

| Pressure | Route |
| --- | --- |
| raw deletion authority or summary-as-proof | source trace, source bundle, and owner source-retention route |
| memory canon or live memory-ledger behavior | `aoa-memo` memory route |
| runtime activation or hidden runtime-store truth | `abyss-stack` runtime route |
| owner acceptance or final promotion | owner repository acceptance route |
| ToS canon or compost authority | Tree of Sophia canon route |
| KAG bridge promotion or graph lift | `aoa-kag` graph-lift route |
| generic adoption readiness | `mechanics/experience/parts/adoption-federation/` route |
| active recurrence memory recall | `mechanics/recurrence/parts/memory-recall/` route |

## Part Admission Route

| Source signal | Operation test | Next route |
| --- | --- | --- |
| witness-derived abstraction needs provenance-preserving proof | source refs and compost-proof support contract exist | `compost-provenance/README.md` |
| reviewed runtime candidate adoption needs proof support | candidate mapping, reviewed memo evidence, receipt visibility, and fixture route exist | `runtime-candidate-adoption/README.md` |
| contradiction, writeback, witness trace, pairing, or adoption pressure appears | stronger owner or existing mechanic owns current proof route | route outward before adding a Distillation part |
| future Distillation operation | distinct source surface, payload home, owner split, and validation lane exist | parent `PARTS.md` update plus decision review |
