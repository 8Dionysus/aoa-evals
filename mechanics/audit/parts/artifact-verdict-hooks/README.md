# Artifact Verdict Hooks

## Role

This part owns bridge metadata for routes where playbook, trace, or runtime
artifacts need to meet an `aoa-evals` verdict anchor.

It keeps artifact inputs, contract refs, verification surfaces, and report
expectations visible without moving verdict logic into runtime, playbooks, or
agent layers.

## Source Surfaces

- `mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md`
- `mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE_CHAOS_WAVE1.md`
- `mechanics/audit/parts/artifact-verdict-hooks/schemas/artifact-to-verdict-hook.schema.json`
- generic `mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.*.example.json`
- mechanic-local hook examples such as
  `mechanics/checkpoint/parts/*/examples/artifact_to_verdict_hook.*.example.json`

## Inputs

- playbook, trace, runtime, or mechanic-local artifact refs;
- eval anchors and expected report-shape refs;
- contract refs that constrain how an artifact may be read;
- owner-review refs for later candidate intake or bundle-local review.

## Outputs

- schema-backed `artifact_to_verdict_hook.*.example.json` metadata;
- generated candidate-reader intake entries;
- bridge guidance that keeps artifact inputs tied to eval anchors;
- stop-line evidence for routes that must hand off to sibling or runtime
  owners.

## Stronger Owner Split

`aoa-evals` owns the hook schema, generic bridge guidance, and candidate-reader
intake route.

The artifact-producing owner keeps artifact meaning. Mechanic-local hook
examples stay with the mechanic part that owns the proof route.

## Boundary

The hook is metadata for review. It is not a judge, scorer, receipt, or proof
canon. A hook example may live under the mechanic part that owns the proof
route; this audit part still owns the schema and generated candidate-reader
intake.

## Stop-Lines

- Do not turn hook metadata into verdict execution.
- Do not move mechanic-specific proof meaning into the audit parent.
- Do not accept playbook, runtime, trace, or sibling artifacts without
  bundle-local review.

## Validation

Payload coverage anchor: `mechanics/audit/parts/artifact-verdict-hooks/`.

```bash
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check
python scripts/validate_repo.py
```
