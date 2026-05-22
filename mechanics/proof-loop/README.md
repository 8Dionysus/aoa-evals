# Proof Loop Mechanic

## Entry Route

Start with this README for role and owned operation. Then read [DIRECTION.md](DIRECTION.md) for current operating direction, [PARTS.md](PARTS.md) for active parts, and [PROVENANCE.md](PROVENANCE.md) only for legacy or former placement.

## Role

`mechanics/proof-loop/` routes the active proof operation that lets a reader
move from one proof question to one bounded result without importing machine,
runtime, sibling, or receipt authority.

Each proof-loop step keeps its owning surface. This package coordinates source
selection, support contracts, candidate evidence, bundle-local review, bounded
reporting, optional receipt routing, quest pressure, and release handoff without
strengthening those owners.

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
- `mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json`
- `docs/EVAL_REVIEW_GUIDE.md`
- `mechanics/publication-receipts/parts/receipt-payload/docs/EVAL_RESULT_RECEIPT_GUIDE.md`
- `mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md`
- `mechanics/boundary-bridge/parts/compatibility-map/docs/SIBLING_PROOF_REFS.md`
- `mechanics/proof-object/README.md`
- `mechanics/proof-infra/README.md`
- `mechanics/audit/README.md`
- `mechanics/publication-receipts/README.md`
- `mechanics/boundary-bridge/README.md`
- `mechanics/proof-loop/PARTS.md`

## Step Owners

| Step | Owner route | Output |
| --- | --- | --- |
| pick proof question | `EVAL_SELECTION.md`, `EVAL_INDEX.md`, `generated/eval_catalog.min.json` | one bounded eval candidate |
| inspect source bundle | `mechanics/proof-object/` and `evals/**/EVAL.md` | bounded claim and proof-object boundary |
| expand support contract | `mechanics/proof-infra/` plus bundle-local fixtures, runners, schemas, reports, or examples | reviewable evidence contract |
| select candidate evidence | `mechanics/audit/` or `mechanics/boundary-bridge/` | candidate packet or cited owner ref |
| review against bundle | `docs/EVAL_REVIEW_GUIDE.md` and bundle-local report contract | bounded review result |
| publish bounded report | bundle-local reports, proof-loop part-local route-smoke reports, or future root reports only when no narrower owner exists | reviewed report artifact |
| route existing reports | `generated/eval_report_index.min.json` | derived reader pointing back to source reports |
| dry-review receipt intake | `mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json` and `mechanics/publication-receipts/` | payload preview with no publication |
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
`mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md`.

It selects `aoa-verification-honesty`, follows the local proof-loop route, and
ends in a bounded route-smoke only: no eval result receipt, no bundle promotion,
and no runtime or sibling evidence acceptance.

Use it as evidence that the route can be followed locally. Do not use it as a
generic eval-result example.

## Parts

The active proof-loop parts map lives in [PARTS.md](PARTS.md).

Current parts:

- `route-smoke`: owns the first public-safe proof-loop route-smoke report.

## First Bundle-Local Report

The first schema-backed bundle-local proof-loop report is
`evals/workflow/aoa-verification-honesty/reports/aoa-evals-slice-19-lifecycle-contract.report.json`.

It evaluates the verification-truthfulness closeout for the slice 19 quest
lifecycle contract. It is a real `aoa-verification-honesty` report, not a
route-smoke, but it still does not create an eval result receipt, promote a
bundle, close a quest, accept runtime evidence, or infer sibling-owner
approval.

## Receipt Intake Dry Review

The first receipt-intake dry review is
`mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json`.

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
`mechanics/audit/` owns candidate evidence intake.
`mechanics/boundary-bridge/` owns sibling reference compatibility.
`mechanics/publication-receipts/` owns optional receipt publication.

This package only coordinates the loop between them.

## Boundaries

| Pressure | Route |
| --- | --- |
| generated reader wants proof authority | generated readers remain derived readers below bundle-local proof authority |
| runtime, machine, trace, or sibling artifact enters the loop | use the candidate evidence route or sibling-ref route before local review |
| receipt pressure appears before review | produce the reviewed bounded report first, then route optional receipt publication |
| one loop is read as a global benchmark, score, rank, trust signal, or autonomy claim | return to the selected bundle claim and report scope |
| loop step skips source bundle review | read bundle-local `EVAL.md` and `eval.yaml` before the step closes |
| hidden live dispatch appears | route runtime dispatch to the stronger runtime owner before adoption |

## Validation

Use [AGENTS](AGENTS.md#validation) for executable validation commands. This
README names the mechanic role, routes, and boundaries; the nearest route card
owns command execution.

When generated or source-support surfaces change, follow the same AGENTS
validation lane before closeout.

## Next Route

Use this package when the question is:

"How do I carry one bounded proof question from selection to reviewed result
without confusing source proof, candidate evidence, report, receipt, sibling
truth, or generated readers?"
