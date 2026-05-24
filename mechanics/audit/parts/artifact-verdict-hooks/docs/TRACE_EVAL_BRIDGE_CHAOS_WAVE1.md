# Trace Eval Bridge Chaos Wave 1

This note narrows the existing bridge rules for the chaos-wave runtime seed.

## Core rule

`aoa-evals` may read the evidence.
It still owns:
- verdict logic
- bounded claim wording
- report interpretation

Neighbor ownership stays explicit:
- runtime execution routes to `abyss-stack`
- routing posture routes to `aoa-routing`
- playbook scenario composition routes to `aoa-playbooks`
- KAG health truth routes to `aoa-kag`
- trace object meaning routes to `aoa-memo` or `aoa-agents`

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
reviewable trace context. Runtime-judge pressure routes to the runtime owner.

## Runtime evidence-selection lane

Use `../../selected-evidence-packets/examples/runtime_evidence_selection.runtime-chaos-window.example.json`
when curated chaos-wave receipts and closeout examples should travel upward only
as weaker sidecar evidence for `aoa-stress-recovery-window`.

This lane is example-backed on purpose.
Live-log publication pressure stays with the runtime owner; global runtime
health pressure routes to runtime review before eval proof can use it.

## Ownership note

If `trace_integrity_receipt` becomes a first-class schema later, land it in the
owning runtime, role, or memory repository first.
`aoa-evals` consumes that surface after the owner repo lands it.
