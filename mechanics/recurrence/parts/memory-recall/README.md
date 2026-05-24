# Recurrence / Memory Recall Part

## Role

`memory-recall` routes the support surface for `aoa-memo-recall-integrity`.

It checks whether memo recall stays narrow, provenance-visible, and
staleness-honest across explicit inspect, capsule, expand, or stronger-source
consumer paths.

## Source Surfaces

- `evals/workflow/aoa-memo-recall-integrity/EVAL.md`
- `evals/workflow/aoa-memo-recall-integrity/fixtures/contract.json`
- `evals/workflow/aoa-memo-recall-integrity/runners/contract.json`
- `evals/workflow/aoa-memo-recall-integrity/reports/phase-alpha-memo-recall-rerun.report.json`
- `mechanics/recurrence/parts/memory-recall/fixtures/memo-recall-guardrail-v1/README.md`
- `mechanics/recurrence/parts/memory-recall/tests/test_memo_recall_phase_alpha_report.py`
- `mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.phase-alpha-memo-recall-rerun.example.json`

## Inputs

- memo recall contracts, catalogs, capsules, sections, provenance threads, and
  lifecycle examples from the stronger memo owner;
- selected runtime evidence kept candidate-only by audit;
- bundle-local report artifacts and runner contracts.

## Outputs

- bounded memo-recall integrity reports;
- fixture replacement constraints for recall guardrail cases;
- stronger-source escalation notes when memo grounding is thin.

## Stronger Owner Split

`aoa-memo` owns memory objects, lifecycle posture, writeback meaning, and recall
implementation truth. `aoa-evals` owns the bounded proof bundle and report
interpretation. Authority beyond that proof reading routes through the stronger
owner split above.

## Stop-Lines

Boundary routes keep memory-recall pressure with the owner that can act on it:

| Pressure | Owner route |
| --- | --- |
| general memory quality pressure | `aoa-memo` recall quality route |
| contradiction handling pressure | `aoa-memo` provenance and conflict route |
| permission inference pressure | source owner plus role/approval route |
| memory canon pressure | `aoa-memo` memory-object route |
| runtime ranking behavior pressure | runtime owner route |
| future writeback acceptance pressure | `aoa-memo` writeback acceptance route plus source-owner review |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
