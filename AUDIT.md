# Audit Surface Map

This file maps the repo-local audit surfaces for `aoa-evals`.

This surface owns audit orientation, claim-pressure routes, review severity,
and report shape. Root [`AGENTS.md`](AGENTS.md) keeps the inherited proof
boundary and approval stop-line. Root [`VALIDATION.md`](VALIDATION.md) and the
nearest local validation companion own executable checks.

Read it after `AGENTS.md` when the work needs audit or review orientation.

## Repository role

`aoa-evals` is the bounded proof canon of AoA.

It owns:

- public eval bundles,
- bounded claim framing, object-under-evaluation wording, and verdict posture,
- category, status, baseline mode, report format, caveats, blind spots, and interpretation guidance,
- shared proof infrastructure contracts that stay weaker than bundle-local meaning,
- generated catalogs, capsules, sections, and comparison-spine surfaces for routing and selection.

Route outward for:

- reusable technique truth: `aoa-techniques`,
- execution workflow meaning: `aoa-skills`,
- routing authority outside eval selection: the owning routing or source layer,
- agent, playbook, or memo artifact-contract meaning:
  `aoa-agents`, `aoa-playbooks`, or `aoa-memo`,
- hidden telemetry, private benchmark infrastructure, or secret-bearing
  operational detail: the private/runtime owner and a sanitized evidence route
  before public proof.

## Source-of-truth docs

Default reading order for audits:

1. `README.md`
2. `docs/architecture/ARCHITECTURE.md`
3. `docs/guides/EVAL_PHILOSOPHY.md`
4. `EVAL_INDEX.md`
5. `EVAL_SELECTION.md`
6. `docs/guides/COMPARISON_SPINE_GUIDE.md`
7. `docs/guides/ARTIFACT_PROCESS_SEPARATION_GUIDE.md`
8. `docs/guides/REPEATED_WINDOW_DISCIPLINE_GUIDE.md`
9. `docs/guides/SHARED_PROOF_INFRA_GUIDE.md`
10. `mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md`
11. the target `evals/**/EVAL.md`
12. the target `evals/**/eval.yaml`
13. bundle-local support artifacts when present:
   - `evals/<family>/<eval>/notes/blind-spots.md`
   - `evals/<family>/<eval>/reports/summary.schema.json`
   - `evals/<family>/<eval>/reports/example-report.json`
   - `evals/<family>/<eval>/runners/contract.json`
   - `evals/<family>/<eval>/fixtures/contract.json`
   - `evals/<family>/<eval>/checks/` or `evals/<family>/<eval>/examples/`
14. the matching generated surfaces as **derived routing aids only**:
   - `generated/eval_catalog.json`
   - `generated/eval_catalog.min.json`
   - `generated/eval_capsules.json`
   - `generated/eval_sections.full.json`
   - `generated/comparison_spine.json`

Also apply the nearest nested `AGENTS.md` when working in subdirectories.

## High-risk surfaces

### Claim and verdict posture

- `evals/**/EVAL.md`
- `evals/**/eval.yaml`
- `object_under_evaluation`, `claim_type`, `category`, `status`, `baseline_mode`, and `report_format`
- blind spots, interpretation guidance, and failure-vs-readout wording
- any wording that turns bounded proof into a broad capability or trust claim

### Public routing and chooser semantics

- `EVAL_INDEX.md`
- `EVAL_SELECTION.md`
- `docs/guides/COMPARISON_SPINE_GUIDE.md`
- `generated/eval_catalog.json`
- `generated/comparison_spine.json`
- any change that makes a `draft` or `bounded` surface sound `baseline` or `canonical` by association

### Comparison spine and anti-overread surfaces

- `evals/comparison/fixed-baseline/aoa-regression-same-task/`
- `evals/comparison/peer-compare/aoa-output-vs-process-gap/`
- `evals/comparison/longitudinal-window/aoa-longitudinal-growth-snapshot/`
- `evals/capability/aoa-eval-integrity-check/`
- `docs/guides/ARTIFACT_PROCESS_SEPARATION_GUIDE.md`
- `docs/guides/REPEATED_WINDOW_DISCIPLINE_GUIDE.md`

### Shared proof infrastructure

- root route cards such as `fixtures/README.md`, `runners/README.md`,
  `scorers/README.md`, `reports/README.md`, and `schemas/README.md`
- active mechanic-local proof-infra parts under
  `mechanics/proof-infra/parts/fixture-families/` and
  `mechanics/proof-infra/parts/reportable-contracts/`
- `docs/guides/SHARED_PROOF_INFRA_GUIDE.md`
- any path or helper naming that implies shared infra is stronger than bundle-local meaning

### Trace / evidence seam

- `mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md`
- `mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.*.example.json`
- anything that could shift verdict ownership out of `aoa-evals`

## Claim pressure routes

| Pressure | Route |
| --- | --- |
| broad intelligence, trust, general safety, or autonomous-self claim | keep wording scoped to the source bundle, evidence, verdict logic, and validation route; send wider meaning to its owner |
| canonical readiness or direct agent-behavior verdict | require a source owner or a new bounded proof bundle before public wording changes |
| generated reader, chooser doc, or index outranking source proof | return to bundle-local `EVAL.md` and `eval.yaml`, then rebuild from source |
| draft, bounded, baseline, or growth language strengthening by association | keep status, baseline mode, and report posture explicit; use the approval stop-line before public interpretation changes |
| private dataset, secret-bearing fixture, hidden telemetry, or skipped validation | route to the private owner, a sanitized fixture, or rerun evidence before public proof |

## Review severity

- P0: secret-bearing or private evidence presented as public proof; bounded eval
  wording converted into broad intelligence, safety, or trust claims; public
  chooser/comparison wording silently changing baseline or maturity meaning.
- P1: `EVAL.md` and `eval.yaml` semantic drift; verdict wording stronger than
  support artifacts; erased blind spots; generated or comparison drift; shared
  infrastructure implying stronger proof; trace/eval ownership drift; claimed
  validation without evidence.

Ignore wording nits unless the task explicitly asks for copyediting.

## Report shape

An audit return names scope and risk, changed or inspected proof surfaces,
whether claim or public posture moved, checks run and skipped, current claim
limits, remaining uncertainty, and the next owner route.

## Route law

Use root `AGENTS.md` for inherited proof boundaries and approval stop-lines.
Use root `VALIDATION.md` plus the nearest local `VALIDATION.md` for executable
checks.

When touching comparison, baseline, peer-compare, or repeated-window surfaces,
re-read the changed bundle's `EVAL.md` and `eval.yaml`, public chooser surfaces,
generated comparison spine, and the comparison guide named above. This file maps
the audit scope; validation companions own commands and root/local agent cards
own stop-lines and closeout routing.
