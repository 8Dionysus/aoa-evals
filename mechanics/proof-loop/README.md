# Proof Loop Mechanic

## Role

`mechanics/proof-loop/` routes the active proof operation that lets a reader
move from one proof question to one bounded result without importing machine,
runtime, sibling, or receipt authority.

It is not a proof bundle, generated catalog, runtime intake, report directory,
receipt publisher, questbook, or release process.

## Owned Operation

The owned operation is:

`proof question -> selection route -> source proof object -> support contract -> candidate evidence packet -> bundle-local review -> bounded report -> optional receipt`

This package makes that route followable from local `aoa-evals` surfaces. It
does not replace the packages that own each step.

## Source Surfaces

- `README.md`
- `DESIGN.md`
- `ROADMAP.md`
- `EVAL_SELECTION.md`
- `EVAL_INDEX.md`
- `generated/eval_catalog.min.json`
- `generated/eval_capsules.json`
- `generated/eval_sections.full.json`
- `generated/eval_report_index.min.json`
- `generated/runtime_candidate_intake.min.json`
- `docs/EVAL_REVIEW_GUIDE.md`
- `docs/EVAL_RESULT_RECEIPT_GUIDE.md`
- `docs/TRACE_EVAL_BRIDGE.md`
- `docs/SIBLING_PROOF_REFS.md`
- `mechanics/proof-object/README.md`
- `mechanics/proof-infra/README.md`
- `mechanics/runtime-evidence/README.md`
- `mechanics/publication-receipts/README.md`
- `mechanics/sibling-proof-refs/README.md`

## Step Owners

| Step | Owner route | Output |
| --- | --- | --- |
| pick proof question | `EVAL_SELECTION.md`, `EVAL_INDEX.md`, `generated/eval_catalog.min.json` | one bounded eval candidate |
| inspect source bundle | `mechanics/proof-object/` and `bundles/*/EVAL.md` | bounded claim and proof-object boundary |
| expand support contract | `mechanics/proof-infra/` plus bundle-local fixtures, runners, schemas, reports, or examples | reviewable evidence contract |
| select candidate evidence | `mechanics/runtime-evidence/` or `mechanics/sibling-proof-refs/` | candidate packet or cited owner ref |
| review against bundle | `docs/EVAL_REVIEW_GUIDE.md` and bundle-local report contract | bounded review result |
| publish bounded report | bundle-local reports or `reports/` | reviewed report artifact |
| route existing reports | `generated/eval_report_index.min.json` | derived reader pointing back to source reports |
| dry-review receipt intake | `reports/eval-result-receipt-intake-dry-review-v1.json` and `mechanics/publication-receipts/` | payload preview with no publication |
| emit optional receipt | `mechanics/publication-receipts/` | subordinate receipt sidecar |

## Inputs

- one proof question;
- one selected eval bundle or clearly marked proof-object draft;
- source bundle claim and manifest metadata;
- support artifacts needed by that bundle;
- candidate evidence only when public-safe and owner-routed;
- a review path that can say approve, defer, reject, or hand off without
  widening the claim.

## Outputs

- one selected proof route;
- one bundle-local review boundary;
- one bounded report or explicit defer/handoff;
- optional receipt only after the reviewed report exists;
- next quest, sibling-owner, runtime-owner, or release route when the proof
  loop cannot close locally.

When the loop ends in defer or handoff, use `quests/LIFECYCLE.md` to choose the
quest state. A route-smoke report does not close a quest, promote a bundle, or
emit an eval result receipt by itself.

## Pilot Report

The first reviewed local route-smoke is
`reports/proof-loop-local-route-smoke-v1.md`.

It selects `aoa-verification-honesty`, follows the local proof-loop route, and
ends in a bounded route-smoke only: no eval result receipt, no bundle promotion,
and no runtime or sibling evidence acceptance.

Use it as evidence that the route can be followed locally. Do not use it as a
generic eval-result example.

## First Bundle-Local Report

The first schema-backed bundle-local proof-loop report is
`bundles/aoa-verification-honesty/reports/aoa-evals-slice-19-lifecycle-contract.report.json`.

It evaluates the verification-truthfulness closeout for the slice 19 quest
lifecycle contract. It is a real `aoa-verification-honesty` report, not a
route-smoke, but it still does not create an eval result receipt, promote a
bundle, close a quest, accept runtime evidence, or infer sibling-owner
approval.

## Receipt Intake Dry Review

The first receipt-intake dry review is
`reports/eval-result-receipt-intake-dry-review-v1.json`.

It derives a schema-valid `candidate_payload_preview` from the first
bundle-local proof-loop report, then stops before receipt publication. Its
`receipt_status` stays `not_published`: no `event_kind`, no `event_id`, no
`stats-event-envelope` sidecar, no publisher run, and no `.aoa/live_receipts/`
append.

## Stronger Owner Split

`aoa-evals` owns the bounded proof interpretation only through the source
bundle and reviewed report.

`mechanics/proof-object/` owns proof-object completeness routing.
`mechanics/proof-infra/` owns reusable support contracts.
`mechanics/runtime-evidence/` owns candidate evidence intake.
`mechanics/sibling-proof-refs/` owns sibling reference compatibility.
`mechanics/publication-receipts/` owns optional receipt publication.

This package only coordinates the loop between them.

## Boundaries

- Do not use this package to promote generated readers into proof authority.
- Do not accept runtime, machine, trace, or sibling artifacts without the
  candidate evidence or sibling-ref route.
- Do not publish a receipt without a reviewed bounded report.
- Do not turn one loop into a global benchmark, score, rank, trust signal, or
  autonomy claim.
- Do not bypass bundle-local `EVAL.md` and `eval.yaml`.
- Do not create hidden live dispatch behavior.

## Validation

After changing proof-loop route surfaces, run:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

If generated readers, runtime candidate readers, quest readers, or receipt
surfaces change, also run their owning builders or tests.

## Next Route

Use this package when the question is:

"How do I carry one bounded proof question from selection to reviewed result
without confusing source proof, candidate evidence, report, receipt, sibling
truth, or generated readers?"
