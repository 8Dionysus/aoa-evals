# Audit / Candidate Readers Part

## Role

This part owns generated reader surfaces for runtime-evidence candidates.

The readers are derived from selected evidence packet examples and
artifact-to-verdict hook examples so future review can see candidate templates,
required runtime artifacts, runtime policy boundary metadata, memory context
boundary metadata, review guides, and owner-review refs.

## Source Surfaces

- `mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py`
- `mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py`
- `mechanics/audit/parts/candidate-readers/schemas/runtime-candidate-template-index.schema.json`
- `mechanics/audit/parts/candidate-readers/schemas/aoa-eval-candidate-packet.schema.json`
- `mechanics/audit/parts/candidate-readers/examples/aoa_eval_candidate_packet.example.json`
- `mechanics/audit/parts/candidate-readers/packets/**/*.eval_candidate.json`
- `mechanics/audit/parts/candidate-readers/reports/session-mining/*.manual-review.md`
- `mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json`
- `mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json`

## Inputs

- selected evidence packet examples from
  `mechanics/audit/parts/selected-evidence-packets/examples/`;
- artifact-to-verdict hook examples from audit and mechanic-local hook routes;
- review-guide refs, owner-review refs, candidate eval refs, and support refs
  carried by those examples.
- memory-context boundary fields carried by memo recall, contradiction, and
  writeback selected-evidence examples.
- manually reviewed session/runtime/local candidate packets whose schema keeps
  them below proof acceptance.

## Outputs

- `runtime_candidate_template_index.min.json`;
- `runtime_candidate_intake.min.json`;
- generated navigation records that route future reviewers back to source
  examples, schemas, policy or memory boundary metadata, and bundle-local
  review surfaces.
- a candidate-only packet contract for manually reviewed session/runtime/local
  evidence before queue import or proof-object design.
- a packet-backed eval-readiness queue that a new session can inspect without
  turning session evidence into verdict, score, baseline, or promotion.
- a lifecycle guard route for candidate queue next-actions that stays read-only
  and below proof promotion.

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
| memory-context metadata is missing or treated as authority | restore the selected-evidence source example and rebuild the reader; memory authority remains in `aoa-memo` |
| generated navigation conflicts with source examples, schemas, or eval contracts | follow the source surface and rebuild the reader |
| a session or runtime packet carries verdict, score, baseline, or promotion wording | reject the packet before queue import; candidate readers route evidence only |
| a candidate queue state is treated as permission to promote proof | run `python scripts/check_eval_candidate_queue_lifecycle.py --json`; queue lifecycle remains review-only |
| local candidate pressure is treated as central adoption | run `python scripts/review_eval_promotion_path.py --json`; promotion review stays dry-run until local owner review, central overlap check, and human acceptance |
| session-mining report is treated as completed proof | route to owner review or a source eval bundle; reports and packets stay candidate-only |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
