# 0007 Runtime Evidence Mechanic Package

- Status: Accepted
- Date: 2026-05-19
- Owner surface: `mechanics/runtime-evidence/`

## Context

After the `questbook` mechanic landed, the next candidate package had to be
chosen by live proof pressure, not by symmetry.

`runtime-evidence` already has a real operation: runtime evidence selection
examples, artifact-to-verdict hook examples, runtime candidate template and
intake generated readers, schemas, generator scripts, runtime promotion docs,
runtime integrity review docs, and validation tests. It also sits on a fragile
authority boundary with `abyss-stack`, machine evidence, trace surfaces, sibling
owners, and bundle-local review.

## Options Considered

- Build `sibling-proof-refs` next because sibling path drift was the first
  repaired validation failure.
- Build `runtime-evidence` next because candidate intake already has generated
  readers, examples, schemas, builders, tests, and an active proof-loop seam.
- Defer all remaining mechanics until package movement is needed.

## Decision

Create `mechanics/runtime-evidence/` as the second live mechanic package.

The package owns the route:

`runtime or trace artifact -> public-safe selected evidence packet -> runtime candidate template index -> candidate intake reader -> bundle-local review -> bounded report or optional receipt`

It does not move existing runtime examples, schemas, docs, or generated files.

## Rationale

This package strengthens the active proof loop without connecting `aoa-evals`
too early to runtime authority. It makes candidate-only posture, public-safe
selection, generated reader derivation, and bundle-local review visible in one
place.

It also keeps the `abyss-stack` lesson bounded: runtime may provide selected
candidate evidence, but `aoa-evals` owns proof interpretation only after
bundle-local review.

## Consequences

- Positive: runtime and machine evidence can be routed through an explicit
  proof-side operation instead of scattered docs and generated readers.
- Tradeoff: there is now a package for a still-candidate seam, so validators
  must keep candidate-only language strong.
- Follow-up: `sibling-proof-refs` remains a strong next candidate, but should be
  created only when its compatibility map and validation shape are ready.

## Boundaries

This decision does not turn runtime evidence into proof canon.

It does not authorize raw log ingestion, host-private publication, runtime
activation, runtime implementation work, machine maintenance, global rankings,
or bundle promotion by receipt accumulation.

It does not transfer `abyss-stack`, `aoa-playbooks`, `aoa-agents`, `aoa-memo`,
or `aoa-stats` owner truth into `aoa-evals`.

## Validation

- `mechanics/runtime-evidence/README.md` names source surfaces, inputs, outputs,
  stronger-owner split, boundaries, legacy posture, validation, and next route.
- `mechanics/runtime-evidence/AGENTS.md` names local editing law.
- `python scripts/generate_runtime_candidate_template_index.py --check`
- `python scripts/generate_runtime_candidate_intake.py --check`
- `python scripts/validate_repo.py`
- `python scripts/validate_semantic_agents.py`
