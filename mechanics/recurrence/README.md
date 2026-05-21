# Recurrence Mechanic

## Entry Route

Start with this README for role and owned operation. Then read [DIRECTION.md](DIRECTION.md) for current operating direction, [PARTS.md](PARTS.md) for active parts, and [PROVENANCE.md](PROVENANCE.md) only for legacy or former placement.

## Role

`mechanics/recurrence/` routes bounded proof work for recurrence
control-plane, anchor return, memory recall, recursor boundary,
stats-regrounding, and portable proof beacons.

It receives recurrence pressure as source bundles, part-local manifests,
fixtures, scorers, hooks, selected evidence, generated/readout support, and
owner handoff context.

## Owned Operation

`mechanics/recurrence/` owns the eval-side recurrence proof operation:

`recurrence pressure -> bounded recurrence proof question -> control-plane, anchor-return, memory-recall, recursor-boundary, regrounding, or portable-proof-beacon evidence -> bundle-local review -> bounded report, decision packet, or owner handoff`

This package is AoA-aligned. It keeps the parent name `recurrence` because the
operation materializes the center recurrence mechanic on the proof side.

## Source Surfaces

- `mechanics/recurrence/docs/RECURRENCE_PROOF_PROGRAM.md`
- `mechanics/recurrence/parts/control-plane-integrity/docs/RECURRENCE_CONTROL_PLANE_EVALS.md`
- `evals/boundary/aoa-recurrence-control-plane-integrity/EVAL.md`
- `evals/workflow/aoa-return-anchor-integrity/EVAL.md`
- `evals/workflow/aoa-memo-recall-integrity/EVAL.md`
- `evals/boundary/aoa-stats-regrounding-boundary-integrity/EVAL.md`
- `evals/capability/aoa-continuity-anchor-integrity/EVAL.md`
- `evals/boundary/aoa-self-reanchor-correctness/EVAL.md`
- `mechanics/recurrence/parts/control-plane-integrity/fixtures/recurrence-control-plane-integrity-v1/README.md`
- `mechanics/recurrence/parts/control-plane-integrity/scripts/run_recurrence_control_plane_integrity_eval.py`
- `mechanics/recurrence/parts/control-plane-integrity/scorers/recurrence_control_plane_integrity.py`
- `mechanics/recurrence/parts/anchor-return/fixtures/return-anchor-v1/README.md`
- `mechanics/recurrence/parts/memory-recall/fixtures/memo-recall-guardrail-v1/README.md`
- `mechanics/recurrence/parts/recursor-boundary/scripts/run_recursor_readiness_boundary_eval.py`
- `mechanics/recurrence/parts/recursor-boundary/scorers/recursor_readiness_boundary.py`
- `mechanics/recurrence/parts/stats-regrounding-boundary/fixtures/stats-regrounding-boundary-v1/README.md`
- `mechanics/recurrence/parts/portable-proof-beacons/README.md`
- `mechanics/recurrence/parts/portable-proof-beacons/manifests/recurrence/component.evals.portable-proof-beacons.json`
- `mechanics/recurrence/parts/portable-proof-beacons/manifests/recurrence/hooks/component.evals.portable-proof-beacons.hooks.json`
- `mechanics/recurrence/parts/portable-proof-beacons/docs/RECURRENCE_REVIEW_DECISION_CLOSURE.md`

## Parts

See [PARTS.md](PARTS.md).

The current active parts are `control-plane-integrity`, `anchor-return`,
`memory-recall`, `recursor-boundary`, `stats-regrounding-boundary`, and
`portable-proof-beacons`. Continuity-anchor and self-reanchor bundles remain
source proof objects under `evals/` until their support artifacts justify a
narrower part.

## Inputs

- recurrence control-plane run dossiers;
- return decisions, anchor refs, re-entry notes, or safe-stop notes;
- memo recall read paths, provenance threads, lifecycle posture, and
  stronger-source escalation notes;
- recursor witness/executor readiness contracts and candidate-only projection
  payloads;
- stats surface profiles, source-coverage summaries, SDK policy decisions,
  routing advisory hints, and owner-truth targets;
- public-safe runtime return evidence selected through audit;
- recurrence manifests, portable proof beacons, hooks, downstream projections,
  and Agon stop-line diagnostics.

## Outputs

- bounded recurrence integrity reports;
- per-axis scorer results;
- missing-axis limitations;
- bounded return-anchor, memo-recall, recursor-boundary, and stats-regrounding
  report or test readouts;
- portable-proof beacon status ladders, drift signals, and decision-packet
  closure guidance that remain below bundle-local review;
- owner handoff or adjacent bundle route notes;
- no global recurrence score or runtime activation.

## Stronger Owner Split

`Agents-of-Abyss` owns recurrence doctrine and center law.
`abyss-stack` owns runtime return policy and runtime logs.
`aoa-routing` owns live navigation behavior.
`aoa-memo` owns memory anchors and recall.
`aoa-agents` owns self-agent and handoff posture.
`aoa-playbooks` owns scenario choreography.

`aoa-evals` owns bounded proof wording, verdict logic, report interpretation,
and recurrence evidence review.

## Stop-Lines

Do not use this package to claim:

- global recurrence completeness;
- hidden continuity;
- automatic recursor or agent spawn;
- runtime self-healing;
- owner artifact promotion;
- beacon verdict authority;
- portable proof acceptance by recurrence manifest;
- routing, stats, KAG, or Agon source truth.

## Legacy

Use [PROVENANCE.md](PROVENANCE.md) only when old recurrence insertion notes,
root docs placement, or landing traces must be audited. New recurrence proof
work starts from this README, [PARTS.md](PARTS.md), and the active part.

## Validation

Use [AGENTS](AGENTS.md#validation) for executable validation commands. This
README names the mechanic role, routes, and boundaries; the nearest route card
owns command execution.

When generated or source-support surfaces change, follow the same AGENTS
validation lane before closeout.

## Next Route

Use this mechanic before changing recurrence control-plane support, return
anchor support, memo-recall guardrails, recursor-boundary readiness,
stats-regrounding boundary support, portable-proof beacons, recurrence
manifests, or observe-only hook posture.

For runtime return behavior, memory canon, live routing, scenario choreography,
stats truth, Agon source truth, or owner decisions, follow the stronger owner
route before changing eval-side proof support.
