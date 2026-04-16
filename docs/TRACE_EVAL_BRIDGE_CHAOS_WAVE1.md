# Trace Eval Bridge Chaos Wave 1

This note narrows the existing bridge rules for the chaos-wave runtime seed.

## Core rule

`aoa-evals` may read the evidence.
It still owns:
- verdict logic
- bounded claim wording
- report interpretation

It does not own:
- runtime execution
- routing posture
- playbook scenario composition
- KAG health truth
- trace object meaning in `aoa-memo` or `aoa-agents`

## Artifact-to-verdict hook lane

Use `../examples/artifact_to_verdict_hook.trace-integrity-chaos.example.json`
when `AOA-P-0032 runtime-chaos-recovery` has already named one bounded proof
handoff candidate and one adjacent witness sidecar.

That hook stays bounded by three rules:
- the playbook still owns the artifact set and re-entry posture
- `aoa-memo` still owns witness-trace meaning
- `aoa-evals` only decides whether the selected witness-facing bundle can read
  the handoff honestly

The current hook lands on `aoa-witness-trace-integrity` because the seed needs
reviewable trace context, not a new runtime judge.

## Runtime evidence-selection lane

Use `../examples/runtime_evidence_selection.runtime-chaos-window.example.json`
when curated chaos-wave receipts and closeout examples should travel upward only
as weaker sidecar evidence for `aoa-stress-recovery-window`.

This lane is example-backed on purpose.
It is not a live-log publication surface and it does not prove global runtime
health.

## Ownership note

If `trace_integrity_receipt` becomes a first-class schema later, land it in the
owning runtime, role, or memory repository first.
`aoa-evals` should only consume that surface after the owner repo makes it
real.
