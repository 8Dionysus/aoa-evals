# Candidate Readers

## Role

This part owns generated reader surfaces for runtime-evidence candidates.

The readers are derived from selected evidence packet examples and
artifact-to-verdict hook examples so future review can see candidate templates,
required runtime artifacts, review guides, and owner-review refs.

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
  examples, schemas, and bundle-local review surfaces.

## Stronger Owner Split

`aoa-evals` owns deterministic reader generation and candidate navigation.

Generated readers are weaker than source examples, schemas, and bundle-local
eval contracts. Runtime and sibling owners keep their source truth.

## Boundary

Generated readers are navigation and intake support. They are weaker than source
examples and must be regenerated when source examples move or change.

## Stop-Lines

- Do not hand-edit generated readers as authority.
- Do not treat candidate-reader inclusion as proof acceptance.
- Do not let generated navigation replace source examples, schemas, or
  bundle-local review.

## Validation

```bash
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check
python scripts/validate_repo.py
```
