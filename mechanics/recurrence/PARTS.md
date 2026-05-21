# Recurrence / Part Index

`mechanics/recurrence/parts/` contains the active parts of the eval-side
recurrence proof operation.

The mechanic owns the route:

`recurrence pressure -> bounded recurrence proof question -> selected evidence -> bundle-local review -> bounded report or owner handoff`

## Parts

| Part | Role | Active surfaces |
| --- | --- | --- |
| `control-plane-integrity` | Maintains the recurrence control-plane dossier scorer, runner, fixtures, schema, example, and manifest route. | `mechanics/recurrence/parts/control-plane-integrity/README.md` |
| `anchor-return` | Maintains return-anchor fixture support and runtime sidecar routing for bounded return and honest re-entry proof. | `mechanics/recurrence/parts/anchor-return/README.md` |
| `memory-recall` | Maintains memo recall fixture and phase-alpha report support while keeping memory truth with `aoa-memo`. | `mechanics/recurrence/parts/memory-recall/README.md` |
| `recursor-boundary` | Maintains recursor witness/executor readiness-only fixtures, scorer, runner, and tests. | `mechanics/recurrence/parts/recursor-boundary/README.md` |
| `stats-regrounding-boundary` | Maintains stats-derived re-grounding boundary fixtures and report-shape tests. | `mechanics/recurrence/parts/stats-regrounding-boundary/README.md` |
| `portable-proof-beacons` | Maintains the recurrence beacon manifest, hook binding, and closure guidance for portable-proof, progression-evidence, and overclaim pressure. | `mechanics/recurrence/parts/portable-proof-beacons/README.md` |

## Part Contract

Inputs are recurrence dossiers, manifests, hook observations, beacons, review
decisions, downstream projections, Agon stop-line diagnostics, return anchors,
memo recall read paths, recursor readiness contracts, stats re-grounding
signals, selected runtime return evidence, portable-proof pressure, progression
evidence pressure, and overclaim signals.

Outputs are bounded recurrence proof reports, per-axis scorer results,
not-observed limitations, return-anchor and memo-recall report checks,
recursor-boundary run reports, stats-regrounding report checks, adjacent bundle
route notes, portable-proof beacon status ladders, decision-packet closure
guidance, and owner handoffs.

Owner split stays explicit: `Agents-of-Abyss` owns recurrence law; runtime,
memory, routing, playbook, agent, stats, KAG, and Agon owners keep their local
truth; `aoa-evals` owns bounded proof interpretation.

Stop-lines forbid global recurrence completeness, hidden continuity, runtime
self-healing, automatic recursor spawn, beacon verdicts, owner promotion, or
source-truth transfer to generated projections. Portable-proof beacons must not
be read as accepted portable proof.

Validation routes through [AGENTS](AGENTS.md#validation), including the
part-local runner, part-local tests, generated catalog check, and repo
validation lane.

## Deferred Part Families

Continuity-anchor and self-reanchor proof remain bundle-local for now. They may
become recurrence parts only when their support artifacts have their own source
surfaces, inputs, outputs, owner split, stop-lines, and validation beyond
bundle-local proof-object routing.
