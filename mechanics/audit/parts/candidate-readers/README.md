# Audit / Candidate Readers Part

## Role

This part owns generated reader surfaces for runtime-evidence candidates.

The readers are derived from selected evidence packet examples and
artifact-to-verdict hook examples so future review can see candidate templates,
required runtime artifacts, runtime policy boundary metadata, review guides,
and owner-review refs.

## Source Surfaces

- `mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py`
- `mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py`
- `mechanics/audit/parts/candidate-readers/schemas/runtime-candidate-template-index.schema.json`
- `mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json`
- `mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json`

## Inputs

- selected evidence packet examples from
  `mechanics/audit/parts/selected-evidence-packets/examples/`;
- artifact-to-verdict hook examples from audit and mechanic-local hook routes;
- review-guide refs, owner-review refs, candidate eval refs, and support refs
  carried by those examples.

## Outputs

- `runtime_candidate_template_index.min.json`;
- `runtime_candidate_intake.min.json`;
- generated navigation records that route future reviewers back to source
  examples, schemas, policy boundary metadata, and bundle-local review surfaces.

## Stronger Owner Split

`aoa-evals` owns deterministic reader generation and candidate navigation.

Generated readers are weaker than source examples, schemas, and bundle-local
eval contracts. Runtime and sibling owners keep their source truth.

## Boundary

Generated readers are navigation and intake support. Reader changes start in
source examples, schemas, or builders, then refresh through the parent
validation lane.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| generated reader content needs to change | edit the source example, schema, or builder, then regenerate through `parts/AGENTS.md` |
| reader inclusion is treated as proof acceptance | route to bundle-local review before any proof read |
| generated navigation conflicts with source examples, schemas, or eval contracts | follow the source surface and rebuild the reader |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
