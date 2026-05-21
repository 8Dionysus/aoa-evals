# Audit Mechanic

## Entry Route

Start with this README for role and owned operation. Then read [DIRECTION.md](DIRECTION.md) for current operating direction, [PARTS.md](PARTS.md) for active parts, and [PROVENANCE.md](PROVENANCE.md) only for legacy or former placement.

## Role

`mechanics/audit/` routes the recurring operation that lets runtime, trace,
machine, and stack artifacts enter `aoa-evals` as candidate evidence without
becoming proof canon.

It is not a runtime implementation, benchmark leaderboard, machine-health
dashboard, receipt publisher, or hidden judge.

## Owned Operation

The owned operation is:

`runtime or trace artifact -> public-safe selected evidence packet -> runtime candidate template index -> candidate intake reader -> bundle-local review -> bounded report or optional receipt`

This package keeps the intake route coherent while source proof meaning remains
in eval bundles and runtime truth remains with the runtime owner.

## Source Surfaces

- `mechanics/audit/PARTS.md`
- `mechanics/audit/parts/README.md`
- `mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md`
- `mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md`
- `mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md`
- `mechanics/recurrence/docs/RECURRENCE_PROOF_PROGRAM.md`
- `mechanics/audit/parts/selected-evidence-packets/schemas/runtime-evidence-selection.schema.json`
- `mechanics/audit/parts/artifact-verdict-hooks/schemas/artifact-to-verdict-hook.schema.json`
- `mechanics/audit/parts/candidate-readers/schemas/runtime-candidate-template-index.schema.json`
- `mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json`
- `mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json`
- `mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.*.example.json`
- generic `mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.*.example.json`
- mechanic-local hook examples such as
  `mechanics/checkpoint/parts/*/examples/artifact_to_verdict_hook.*.example.json`
- `mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py`
- `mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py`
- `scripts/validate_repo.py`

## Part Topology

- `selected-evidence-packets/` owns public-safe runtime evidence curation.
- `artifact-verdict-hooks/` owns bridge schema and candidate-reader intake from
  artifacts to eval anchors; mechanic-local hook examples may live under the
  mechanic part that owns the proof route.
- `candidate-readers/` owns generated candidate intake readers.
- `integrity-review/` owns the owner-local candidate-only runtime integrity
  review contract.

These are parts because none of them completes the operation alone. The mechanic
becomes useful when the packet/hook surfaces feed generated readers and then
route to bundle-local review.

## Inputs

- selected `abyss-stack` runtime evidence;
- trace and playbook artifacts that can be reviewed against an eval anchor;
- machine or host facts only after public-safe selection;
- sibling-owned artifact refs that keep their stronger owner truth;
- candidate packets that still need human or bundle-local review.

## Outputs

- schema-backed runtime evidence selection examples;
- artifact-to-verdict hook examples;
- runtime candidate template index;
- runtime candidate intake reader;
- owner-review refs for later bundle-local review;
- bounded report or optional receipt only after review accepts the evidence.

## Stronger Owner Split

`aoa-evals` owns bounded claim wording, verdict logic, comparison semantics,
interpretation guidance, review posture, and proof acceptance.

`abyss-stack` owns runtime behavior, live logs, deployed state, host facts, and
runtime implementation. `aoa-playbooks` owns scenario composition.
`aoa-agents` owns agent artifact contracts. `aoa-memo` owns memory and
checkpoint meaning. `aoa-stats` owns shared event envelope vocabulary.

This package may route selected evidence from those owners. It does not absorb
their authority.

## Boundaries

- Runtime evidence stays candidate-only until bundle-local review.
- Generated runtime candidate readers are navigation and intake surfaces, not
  proof authority.
- Do not ingest raw uncurated dumps, secrets, private host fingerprints, or
  unreduced operator traces.
- Do not read latency, load, recovery, or context-stress evidence as global
  intelligence, safety, capability, or agent-quality ranking.
- Do not let a receipt, hook packet, or candidate intake entry promote a bundle
  by itself.
- Do not repair `abyss-stack` or machine maintenance from this package unless
  the current proof gate explicitly requires it.

## Legacy Posture

The names `runtime-candidate`, `artifact-to-verdict`, `phase-alpha`, and `W10`
remain accepted compatibility vocabulary where existing examples, schemas,
docs, or generated readers use them.

The active package name is `audit` because the living operation is evidence
intake, risk routing, and proof-boundary review. `runtime-evidence` remains an
accepted evidence-class and schema vocabulary inside the package; it is not the
parent mechanic.

## Validation

Use [AGENTS](AGENTS.md#validation) for executable validation commands. This
README names the mechanic role, routes, and boundaries; the nearest route card
owns command execution.

When generated or source-support surfaces change, follow the same AGENTS
validation lane before closeout.

## Next Route

The next honest audit movement is a proof-side intake decision that
can say which selected runtime packets are allowed to travel upward, which stay
local-only, which become bundle candidates, and which are rejected as
overclaiming or private evidence.
