# AUDIT.md

This file is the repo-local audit contract for `aoa-evals`.

Read it after `AGENTS.md` and before making changes.

## Repository role

`aoa-evals` is the bounded proof canon of AoA.

It owns:

- public eval bundles,
- bounded claim framing, object-under-evaluation wording, and verdict posture,
- category, status, baseline mode, report format, caveats, blind spots, and interpretation guidance,
- shared proof infrastructure contracts that stay weaker than bundle-local meaning,
- generated catalogs, capsules, sections, and comparison-spine surfaces for routing and selection.

It does **not** own:

- reusable technique truth in `aoa-techniques`,
- execution workflow meaning in `aoa-skills`,
- routing authority outside eval selection surfaces,
- agent, playbook, or memo ownership of artifact-contract meaning,
- hidden telemetry, private benchmark infrastructure, or secret-bearing operational detail.

## Source-of-truth docs

Default reading order for audits:

1. `README.md`
2. `docs/ARCHITECTURE.md`
3. `docs/EVAL_PHILOSOPHY.md`
4. `EVAL_INDEX.md`
5. `EVAL_SELECTION.md`
6. `docs/COMPARISON_SPINE_GUIDE.md`
7. `docs/ARTIFACT_PROCESS_SEPARATION_GUIDE.md`
8. `docs/REPEATED_WINDOW_DISCIPLINE_GUIDE.md`
9. `docs/SHARED_PROOF_INFRA_GUIDE.md`
10. `docs/TRACE_EVAL_BRIDGE.md`
11. the target `bundles/*/EVAL.md`
12. the target `bundles/*/eval.yaml`
13. bundle-local support artifacts when present:
   - `notes/blind-spots.md`
   - `reports/summary.schema.json`
   - `reports/example-report.json`
   - `runners/contract.json`
   - `fixtures/contract.json`
   - `checks/` or `examples/`
14. the matching generated surfaces as **derived routing aids only**:
   - `generated/eval_catalog.json`
   - `generated/eval_catalog.min.json`
   - `generated/eval_capsules.json`
   - `generated/eval_sections.full.json`
   - `generated/comparison_spine.json`

Also apply the nearest nested `AGENTS.md` when working in subdirectories.

## High-risk surfaces

### Claim and verdict posture

- `bundles/*/EVAL.md`
- `bundles/*/eval.yaml`
- `object_under_evaluation`, `claim_type`, `category`, `status`, `baseline_mode`, and `report_format`
- blind spots, interpretation guidance, and failure-vs-readout wording
- any wording that turns bounded proof into a broad capability or trust claim

### Public routing and chooser semantics

- `EVAL_INDEX.md`
- `EVAL_SELECTION.md`
- `docs/COMPARISON_SPINE_GUIDE.md`
- `generated/eval_catalog.json`
- `generated/comparison_spine.json`
- any change that makes a `draft` or `bounded` surface sound `baseline` or `canonical` by association

### Comparison spine and anti-overread surfaces

- `bundles/aoa-regression-same-task/`
- `bundles/aoa-output-vs-process-gap/`
- `bundles/aoa-longitudinal-growth-snapshot/`
- `bundles/aoa-eval-integrity-check/`
- `docs/ARTIFACT_PROCESS_SEPARATION_GUIDE.md`
- `docs/REPEATED_WINDOW_DISCIPLINE_GUIDE.md`

### Shared proof infrastructure

- `fixtures/`
- `scorers/`
- `runners/`
- `reports/`
- `schemas/`
- `docs/SHARED_PROOF_INFRA_GUIDE.md`
- any path or helper naming that implies shared infra is stronger than bundle-local meaning

### Trace / evidence seam

- `docs/TRACE_EVAL_BRIDGE.md`
- `examples/artifact_to_verdict_hook.*.example.json`
- anything that could shift verdict ownership out of `aoa-evals`

## Hard boundaries

Never:

- turn a bounded eval into a total intelligence score, global safety claim, or canonical-readiness proof by itself,
- let `EVAL_INDEX.md`, `EVAL_SELECTION.md`, or generated catalogs outrank bundle-local `EVAL.md` or `eval.yaml`,
- upgrade draft or bounded status, baseline semantics, or growth language by association,
- use private datasets, secret-bearing fixtures, or hidden telemetry as if they were public proof surfaces,
- rewrite skill or technique meaning here instead of evaluating it,
- use `aoa-eval-integrity-check` as a direct agent-behavior verdict,
- claim validation that was not actually run.

## Approval-required changes

Do not make these changes without explicit human confirmation:

- changing `category`, `status`, `baseline_mode`, `report_format`, `claim_type`, or `object_under_evaluation`,
- changing default public baseline or comparison-ladder wording,
- adding or changing a shared fixture family, paired dossier, scorer helper, runner surface, or report schema,
- adding a new eval bundle or changing current starter-selection posture,
- changing bundle-local support artifact shape in a way that affects public interpretation.

## Mandatory verification

### Minimum after meaningful changes

```bash
python scripts/validate_repo.py
```

### When touching manifests, catalogs, chooser docs, or generated surfaces

```bash
python scripts/build_catalog.py
python scripts/validate_repo.py
```

### When touching comparison, baseline, peer-compare, or repeated-window surfaces

Re-read and reconcile all of the following against the changed bundle:

- `generated/comparison_spine.json`
- the target `EVAL.md`
- the target `eval.yaml`
- `EVAL_INDEX.md`
- `EVAL_SELECTION.md`
- `docs/COMPARISON_SPINE_GUIDE.md`

### When touching scorer logic or shared proof infrastructure

Run the nearest `pytest` modules for the affected surfaces, for example:

```bash
python -m pytest tests/test_bounded_rubric_breakdown.py tests/test_build_catalog.py
```

### When touching AGENTS or instruction-layering docs

```bash
python -m pytest tests/test_nested_agents_docs.py tests/test_validate_repo.py
```

Do not list a command in the report unless it was actually run.

## Review guidelines

Use these severity rules for Codex GitHub review and local `/review`.

### Treat as P0

- secret-bearing fixtures, private benchmark data, or hidden telemetry presented as public proof surfaces
- wording that converts a bounded eval into a broad intelligence, general safety, or universal trust claim
- public chooser or comparison wording that silently changes default baseline or public maturity meaning without matching bundle contract and evidence

### Treat as P1

- `EVAL.md` and `eval.yaml` drift on category, status, baseline, or report semantics
- verdict wording becomes stronger than support-artifact coverage
- blind spots or nearby-bundle distinctness are erased
- comparison spine or generated routing surfaces drift away from bundle-local contracts
- shared infra names or paths imply stronger proof than the bundle supports
- trace/eval bridge wording shifts verdict interpretation out of `aoa-evals`
- claiming validation that was not actually run

Ignore low-value wording nits unless the task explicitly requests copyediting.

## Required report shape

Every audit or patch report for this repo should include:

### PLAN

- task restatement
- touched or inspected bundles or public surfaces
- main risk: overclaiming, chooser drift, comparison semantics, shared proof infra, or trace/evidence seam

### DIFF

- what changed
- whether bounded claim meaning changed or only metadata, docs, or generated surfaces changed
- whether category, status, baseline mode, or report posture changed

### VERIFY

- `python scripts/validate_repo.py` status
- `python scripts/build_catalog.py` status when relevant
- any `pytest` modules actually run
- what comparison or chooser surfaces were manually re-read
- what was not run

### REPORT

- current bounded claim after the change
- what the changed surface still does **not** prove
- whether public chooser, comparison, or integrity-sidecar posture changed
- any downstream follow-up likely needed in `aoa-skills` or neighboring layer repos

### RESIDUAL RISK

- thin evidence or support artifacts not refreshed
- neighboring bundles not yet re-read for distinctness drift
- comparison or routing surfaces not fully re-audited

## Routing rule

If the requested work mainly changes:

- execution workflow meaning, trigger boundaries, or skill posture, route to `aoa-skills`;
- reusable engineering practice or technique truth, route to `aoa-techniques`;
- agent, playbook, or memo ownership of artifact contracts or eval anchors, route to the owning layer repo;
- ecosystem ownership or layer-map language, route to `Agents-of-Abyss`.
