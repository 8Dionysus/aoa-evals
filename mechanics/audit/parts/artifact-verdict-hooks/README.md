# Audit / Artifact Verdict Hooks Part

## Role

This part owns bridge metadata for routes where playbook, trace, or runtime
artifacts need to meet an `aoa-evals` verdict anchor.

It keeps artifact inputs, contract refs, verification surfaces, report
expectations, and handoff owners visible for later eval review.

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
- runtime policy boundary metadata for policy-sensitive hooks;
- owner-review refs for later candidate intake or bundle-local review.

## Outputs

- schema-backed `artifact_to_verdict_hook.*.example.json` metadata;
- generated candidate-reader intake entries;
- bridge guidance that keeps artifact inputs tied to eval anchors;
- policy-boundary metadata that names authorization, approval, and
  fallback/rollback artifacts without granting runtime permission;
- stop-line evidence for routes that must hand off to sibling or runtime
  owners.

## Stronger Owner Split

`aoa-evals` owns the hook schema, generic bridge guidance, and candidate-reader
intake route.

The artifact-producing owner keeps artifact meaning. Mechanic-local hook
examples stay with the mechanic part that owns the proof route.

## Boundary

The hook is review metadata. Verdict execution routes to eval verdict logic,
receipt publication routes to publication receipts, and mechanic-specific proof
meaning stays with the mechanic part that owns the proof route.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| hook metadata is asked to execute a verdict | route to the owning eval bundle, scorer, runner, or report contract |
| hook metadata is read as tool permission, runtime-policy enforcement, runtime-owner approval, or cost/time cap proof | route to the runtime or route owner before using it as enforcement evidence |
| mechanic-specific proof meaning appears | keep the example under the mechanic part that owns that proof route |
| playbook, runtime, trace, or sibling artifact acceptance is requested | send the artifact through owner review and bundle-local eval review |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
