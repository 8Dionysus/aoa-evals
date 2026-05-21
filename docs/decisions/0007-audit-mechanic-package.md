# 0007 Audit Mechanic Package

- Status: Accepted
- Date: 2026-05-19
- Owner surface: `mechanics/audit/`

## Context

After the `questbook` mechanic landed, the next candidate package had to be
chosen by live proof pressure, not by symmetry.

The runtime evidence selection route already has a real audit operation:
selected evidence packet
examples, artifact-to-verdict hook examples, runtime candidate template and
intake generated readers, schemas, generator scripts, runtime promotion docs,
runtime integrity review docs, and validation tests. It also sits on a fragile
authority boundary with `abyss-stack`, machine evidence, trace surfaces, sibling
owners, and bundle-local review.

## Options Considered

- Build the boundary-bridge package next because sibling path drift was the
  first repaired validation failure.
- Build the audit package next because candidate intake already has generated
  readers, examples, schemas, builders, tests, and an active proof-loop seam.
- Defer all remaining mechanics until package movement is needed.

## Decision

Create `mechanics/audit/` as a live mechanic package.

The package owns the route:

`runtime or trace artifact -> public-safe selected evidence packet -> runtime candidate template index -> candidate intake reader -> bundle-local review -> bounded report or optional receipt`

Place the active runtime-evidence artifacts inside part-local audit package
homes:

- `parts/selected-evidence-packets/` for selected runtime evidence packet docs,
  schemas, and examples;
- `parts/artifact-verdict-hooks/` for trace/playbook artifact hook docs,
  schemas, and examples;
- `parts/candidate-readers/` for generated runtime candidate readers and their
  builders;
- `parts/integrity-review/` for candidate-only W10 runtime integrity review
  docs, schema, and example.

Route `mechanics/recurrence/docs/RECURRENCE_PROOF_PROGRAM.md` through the
`recurrence` mechanic because it is a broader recurrence/proof-program surface,
not an audit part.

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
  proof-side audit operation instead of scattered root docs, root examples, and
  root generated readers.
- Tradeoff: there is now a package-local home for a still-candidate seam, so
  validators must keep candidate-only language strong.
- Follow-up: `boundary-bridge` remains a strong next candidate, but should be
  created only when its compatibility map and validation shape are ready.

## Boundaries

This decision does not turn runtime evidence into proof canon.

It does not authorize raw log ingestion, host-private publication, runtime
activation, runtime implementation work, machine maintenance, global rankings,
or bundle promotion by receipt accumulation.

It does not transfer `abyss-stack`, `aoa-playbooks`, `aoa-agents`, `aoa-memo`,
or `aoa-stats` owner truth into `aoa-evals`.

## Validation

- `mechanics/audit/README.md` names source surfaces, inputs, outputs,
  stronger-owner split, boundaries, legacy posture, validation, and next route.
- `mechanics/audit/PARTS.md` names why the package has parts rather
  than standalone sub-mechanics.
- `mechanics/audit/AGENTS.md` names local editing law.
- `python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check`
- `python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check`
- `python scripts/validate_repo.py`
- `python scripts/validate_semantic_agents.py`
