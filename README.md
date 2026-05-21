# aoa-evals Bounded Proof Canon

`aoa-evals` is the AoA proof canon: the portable home for bounded eval bundles,
proof-support mechanics, generated readers, receipts, and routeable evidence
about agent-shaped work.

Where `aoa-techniques` preserves reusable practice and `aoa-skills` preserves
bounded execution workflows, this repository preserves the proof surfaces that
make quality, boundary, regression, artifact, comparison, and repeated-window
claims reviewable outside the original project.

An eval here is a bounded proof surface. It carries a claim, fixtures or cases,
scoring or verdict logic, known limits, and a local validation route. It is not
a universal intelligence score, general safety claim, or proof of selfhood.

Current release: `v0.3.3`. See [CHANGELOG.md](CHANGELOG.md).

## First Route

For first orientation, read:

1. [DESIGN.md](DESIGN.md) for the system form.
2. [DESIGN.AGENTS.md](DESIGN.AGENTS.md) for agent-facing route shape.
3. [docs/AGENT_INDEX.md](docs/AGENT_INDEX.md) for the pass-through chain from
   repo to authority class, operation, part, payload, and validation.
4. [docs/PROOF_TOPOLOGY.md](docs/PROOF_TOPOLOGY.md) for source, generated,
   runtime-candidate, receipt, sibling, legacy, and mechanic authority classes.
5. [mechanics/README.md](mechanics/README.md) for repeatable proof operations.
6. [docs/README.md](docs/README.md) for the full documentation map.

The quickest concrete proof object is
[evals/workflow/aoa-bounded-change-quality/EVAL.md](evals/workflow/aoa-bounded-change-quality/EVAL.md).
Current public eval discovery lives in
[Eval Bundle Selection Chooser](EVAL_SELECTION.md) and
[Eval Bundle Index](EVAL_INDEX.md).

## Surface Map

| Need | Surface |
| --- | --- |
| Proof meaning | `evals/**/EVAL.md` and `evals/**/eval.yaml` |
| Agent pass-through index | `docs/AGENT_INDEX.md` |
| Current direction | [ROADMAP.md](ROADMAP.md) |
| Open obligations | [QUESTBOOK.md](QUESTBOOK.md) and [quests/README.md](quests/README.md) |
| Architecture and limits | `DESIGN.md`, `DESIGN.AGENTS.md`, `docs/ARCHITECTURE.md`, `docs/EVAL_PHILOSOPHY.md` |
| Authority classes | `docs/PROOF_TOPOLOGY.md` |
| Durable rationale | `docs/decisions/README.md` and numbered decisions |
| Proof operations | `mechanics/README.md` and parent `README.md` / `PARTS.md` / `DIRECTION.md` |
| Generated readers | `generated/eval_catalog.min.json`, `generated/eval_capsules.json`, `generated/eval_sections.full.json`, `generated/eval_report_index.min.json` |
| Route law | nearest `AGENTS.md` |

Agent lane routing is under `.agents/AGENTS.md` and `.agents/spark/AGENTS.md`.
Legacy, provenance, and accepted-input vocabulary are kept explicit in
[docs/LEGACY_NAMING.md](docs/LEGACY_NAMING.md).

## Proof Support

For eval authoring and eval contracts, start with
`mechanics/proof-object/README.md` and
`mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md`.

For interpretation and support layers, use
[docs/SCORE_SEMANTICS_GUIDE.md](docs/SCORE_SEMANTICS_GUIDE.md),
[docs/VERDICT_INTERPRETATION_GUIDE.md](docs/VERDICT_INTERPRETATION_GUIDE.md),
[docs/EVAL_RUBRIC.md](docs/EVAL_RUBRIC.md),
[docs/EVAL_REVIEW_GUIDE.md](docs/EVAL_REVIEW_GUIDE.md),
[docs/COMPARISON_SPINE_GUIDE.md](docs/COMPARISON_SPINE_GUIDE.md),
`generated/comparison_spine.json`,
[docs/REPEATED_WINDOW_DISCIPLINE_GUIDE.md](docs/REPEATED_WINDOW_DISCIPLINE_GUIDE.md),
[docs/ARTIFACT_PROCESS_SEPARATION_GUIDE.md](docs/ARTIFACT_PROCESS_SEPARATION_GUIDE.md),
and [docs/SHARED_PROOF_INFRA_GUIDE.md](docs/SHARED_PROOF_INFRA_GUIDE.md).

The active public runtime path remains:

`pick -> inspect -> expand -> object use`

## Evidence Anchors

These anchors are entry points, not replacements for their owning mechanics:

- first bundle-local proof-loop report:
  `evals/workflow/aoa-verification-honesty/reports/aoa-evals-slice-19-lifecycle-contract.report.json`
- receipt-intake dry review:
  `mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json`
- release-support readiness audit:
  `mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json`
- strategic closeout audit:
  `mechanics/release-support/parts/strategic-closeout/reports/strategic-closeout-audit-v1.json`
- release-prep PR handoff:
  `mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json`

Receipt, runtime, sibling, trace, and release-support artifacts remain evidence
or handoff surfaces until a bundle-local review accepts a bounded interpretation.

## Validation

Use [AGENTS.md#verify](AGENTS.md#verify) and the nearest nested `AGENTS.md` for
executable validation routes. This README is the public proof-organ entry, not the command ledger.

For bundle edits, start with [evals/AGENTS](evals/AGENTS.md). For generated
reader parity, start with [generated/AGENTS](generated/AGENTS.md). For proof
operation or mechanics movement, start with [mechanics/AGENTS](mechanics/AGENTS.md).

## Owner Boundary

Good candidates belong here when they are portable eval bundles, bounded
workflow evaluations, comparison or regression surfaces, verdict schemas,
fixtures, runners, scorers, rubrics, or report contracts.

Route away by owner:

- `aoa-techniques` for reusable practice meaning;
- `aoa-skills` for bounded workflow meaning;
- `aoa-routing` for navigation and dispatch;
- `aoa-agents` for role posture and handoff contracts;
- `aoa-playbooks` for scenario composition.

In short:

`practice canon -> workflow canon -> proof canon`

## License

Apache-2.0
