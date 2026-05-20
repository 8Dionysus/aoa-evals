# Runtime Evidence Mechanic

## Role

`mechanics/runtime-evidence/` routes the recurring operation that lets runtime,
trace, machine, and stack artifacts enter `aoa-evals` as candidate evidence
without becoming proof canon.

It is not a runtime implementation, benchmark leaderboard, machine-health
dashboard, receipt publisher, or hidden judge.

## Owned Operation

The owned operation is:

`runtime or trace artifact -> public-safe selected evidence packet -> runtime candidate template index -> candidate intake reader -> bundle-local review -> bounded report or optional receipt`

This package keeps the intake route coherent while source proof meaning remains
in eval bundles and runtime truth remains with the runtime owner.

## Source Surfaces

- `docs/RUNTIME_BENCH_PROMOTION_GUIDE.md`
- `docs/RUNTIME_INTEGRITY_REVIEW.md`
- `docs/TRACE_EVAL_BRIDGE.md`
- `docs/RECURRENCE_PROOF_PROGRAM.md`
- `schemas/runtime-evidence-selection.schema.json`
- `schemas/artifact-to-verdict-hook.schema.json`
- `schemas/runtime-candidate-template-index.schema.json`
- `generated/runtime_candidate_template_index.min.json`
- `generated/runtime_candidate_intake.min.json`
- `examples/runtime_evidence_selection.*.example.json`
- `examples/artifact_to_verdict_hook.*.example.json`
- `scripts/generate_runtime_candidate_template_index.py`
- `scripts/generate_runtime_candidate_intake.py`
- `scripts/validate_repo.py`

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

The active package name is `runtime-evidence` because the living operation is
candidate evidence intake, not runtime ownership.

## Validation

After changing runtime evidence examples, schemas, docs, generated readers, or
this mechanic, run:

```bash
python scripts/generate_runtime_candidate_template_index.py --check
python scripts/generate_runtime_candidate_intake.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

If source examples changed and generated readers are stale, rebuild them with:

```bash
python scripts/generate_runtime_candidate_template_index.py
python scripts/generate_runtime_candidate_intake.py
```

Then rerun the checks.

## Next Route

The next honest runtime-evidence movement is a proof-side intake decision that
can say which selected runtime packets are allowed to travel upward, which stay
local-only, which become bundle candidates, and which are rejected as
overclaiming or private evidence.
