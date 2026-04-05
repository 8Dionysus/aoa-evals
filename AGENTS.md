# AGENTS.md

Guidance for coding agents and humans contributing to `aoa-evals`.

## Purpose

`aoa-evals` is the bounded proof canon of AoA. It stores portable evaluation bundles for bounded claims about workflow quality, boundaries, regressions, artifact quality, comparative behavior, and repeated-window movement.

This repository is for bounded proof surfaces, not for universal scores or broad claims of intelligence.

## Owns

This repository is the source of truth for:

- eval bundle wording
- bounded claim framing
- verdict-shape wording
- review posture and caveats at the eval layer
- eval metadata and generated catalogs, capsules, and section surfaces
- repository-level doctrine about what an eval does and does not prove

## Does not own

Do not treat this repository as the source of truth for:

- reusable engineering practice in `aoa-techniques`
- bounded execution workflows in `aoa-skills`
- routing and dispatch logic in `aoa-routing`
- role contracts in `aoa-agents`
- scenario composition in `aoa-playbooks`
- memory objects or recall surfaces in `aoa-memo`
- private benchmark data, hidden telemetry, or private infrastructure detail

## Core rule

Only contribute evals that make bounded, reviewable claims.

Every eval should make it easy to answer:

- what this supports
- what this does not prove
- what evidence shape it uses
- where interpretation must stay cautious

## Read this first

Before making changes, read in this order:

1. `README.md`
2. `docs/ARCHITECTURE.md`
3. `docs/EVAL_PHILOSOPHY.md`
4. the target `bundles/*/EVAL.md`
5. any generated catalogs, capsules, comparison surfaces, or section surfaces tied to that bundle

If the task changes a claim, inspect the upstream skill or technique surfaces the eval depends on before editing.

If a deeper directory defines its own `AGENTS.md`, follow the nearest one.

## Primary objects

The most important objects in this repository are:

- canonical eval bundles under `bundles/*/EVAL.md`
- bundle manifests and metadata inputs
- generated catalogs, capsules, comparison surfaces, and section surfaces under `generated/`
- proof infra families under `fixtures/`, `runners/`, `scorers/`, `reports/`, and `schemas/`
- philosophy, architecture, and comparison docs under `docs/`

## Hard NO

Do not:

- make broad intelligence claims disguised as bounded evals
- use score theater with no clear claim boundary
- depend on secret context that is not present in the repository
- let metadata imply stronger proof than the bundle supports
- rewrite upstream skill or technique meaning here
- conceal uncertainty with polished wording

## Contribution doctrine

Use this flow: `PLAN -> DIFF -> VERIFY -> REPORT`

### PLAN

State:

- which eval is changing
- what bounded claim it supports
- what it does not prove
- which upstream skills, techniques, or runtime artifacts it depends on
- whether verdict shape or comparison posture will change

### DIFF

Keep the change focused. Do not mix unrelated benchmark cleanup into an eval change unless it is necessary for repository integrity.

### VERIFY

Minimum validation for bundle or generated-surface changes:

```bash
python scripts/validate_repo.py
```

If catalogs or capsules changed, also run:

```bash
python scripts/build_catalog.py
python scripts/build_catalog.py --check
```

For the current full non-mutating repo integrity battery, also run:

```bash
python scripts/generate_runtime_candidate_template_index.py --check
python scripts/generate_runtime_candidate_intake.py --check
python scripts/generate_phase_alpha_eval_matrix.py --check
python -m pytest -q tests
```

Confirm that:

- the claim remains bounded
- caveats and blind spots remain visible
- verdict shape still matches the claim
- public reading of the eval is not stronger than the evidence it carries

### REPORT

Summarize:

- what changed
- whether claim meaning changed or only docs, metadata, or generated surfaces changed
- whether category, verdict shape, dependencies, or comparison posture changed
- what validation you actually ran
- any remaining caveats or interpretation risks

## Validation

Do not claim checks you did not run.

## Audit contract

For repository audits and GitHub review, read `AUDIT.md` after the core docs.

## Review guidelines

For GitHub review in this repository, treat the following as P0:

- secret-bearing fixtures, private benchmark data, or hidden telemetry presented as public proof surfaces
- wording that converts a bounded eval into a broad intelligence, general safety, or universal trust claim
- public chooser or comparison wording that silently changes default baseline or public maturity meaning without matching bundle contract and evidence

Treat the following as P1:

- `EVAL.md` and `eval.yaml` drift on category, status, baseline, or report semantics
- verdict wording becomes stronger than support-artifact coverage
- blind spots or nearby-bundle distinctness are erased
- comparison spine or generated routing surfaces drift away from bundle-local contracts
- shared infra names or paths imply stronger proof than the bundle supports
- trace/eval bridge wording shifts verdict interpretation out of `aoa-evals`
- claiming validation that was not actually run

Ignore trivial wording nits unless the task explicitly asks for copyediting.

When the task crosses repo boundaries, use the neighboring repositories for their owned meaning:

- `aoa-techniques` for upstream practice
- `aoa-skills` for the bounded workflows under evaluation
- `aoa-routing` for smallest-next-object navigation
- `aoa-agents` for role and evaluation posture context
- `aoa-playbooks` for scenario-level context
