# AGENTS.md

Root route card for `aoa-evals`.

## Purpose

`aoa-evals` is the bounded proof canon of AoA.
It stores portable evaluation bundles for bounded claims about workflow quality, boundaries, regressions, artifact quality, comparison posture, repeated-window movement, and framed progression or checkpoint evidence.
Claim limit: evals here prove only the bounded claim their source bundle,
evidence, verdict logic, and validation route can support.

## Owner lane

This repository owns:

- eval bundle wording, bounded claim framing, verdict shape, categories, baselines, reports, comparisons, caveats, and generated proof surfaces
- doctrine about claim limits and proof boundaries
- progression, recurrence, and checkpoint proof posture only when explicitly defined here
- owner-local statistical questions and source-backed measurement declarations about eval-owned surfaces under `stats/`
- the admitted repo-specific `aoa-evals-skills` callable procedure under top-level
  `skills/`; it routes central proof work while source bundles and admitted
  evidence keep proof authority
- the owner-local semantic capability tree under `capabilities/`; it exposes
  typed discovery and task-local composition contracts without owning runtime
  DAG instances or generated graph authority

Route outward for:

- shared skill workflow meaning, technique practice meaning, role policy, routing, playbooks, memory objects, cross-owner statistical composition or dashboards, or hidden private benchmark truth

## Operational map

| Field | Route |
| --- | --- |
| entry | `README.md`, then the nearest nested `AGENTS.md` for the touched path |
| source proof meaning | `evals/**/EVAL.md` and `evals/**/eval.yaml` |
| authority class | `docs/architecture/PROOF_TOPOLOGY.md` and `docs/architecture/AGENT_INDEX.md` |
| proof operation | `mechanics/README.md`, then parent `README.md`, `DIRECTION.md`, `PARTS.md`, and part `README.md` |
| roadmap direction | `ROADMAP.md` |
| local memory candidates | `memo/AGENTS.md`, `memo/README.md`, and `memo/PORT.yaml` |
| local statistics | `stats/AGENTS.md`, `stats/README.md`, and `stats/port.manifest.json` |
| owner callable procedure | `skills/AGENTS.md`, `skills/README.md`, `skills/port.manifest.json`, then `skills/aoa-evals-skills/SKILL.md` |
| owner capability tree | `capabilities/AGENTS.md`, `capabilities/port.manifest.json`, then `capabilities/families/*.yaml` |
| output | bounded reports, receipts, generated readers, or owner handoffs only through their owning surface |
| tools and checks | this card's `Verify` section and the nearest nested `AGENTS.md` |

## Start here
Read only the route needed for the touched source: consult the nearest README when its human or semantic contract is required, then follow the source-owner and validation routes conditionally.
For architecture or topology work, consult `DESIGN.md`, `DESIGN.AGENTS.md`, and `mechanics/EVIDENCE_CLUSTERS.md` as needed for the touched surface.
## AGENTS stack law

- Start with this root card, then follow the nearest nested `AGENTS.md` for every touched path.
- Root guidance owns repository identity, owner boundaries, route choice, and the shortest honest verification path.
- Nested guidance owns local contracts, local risk, exact files, and local checks.
- Authored source surfaces own meaning. Generated, exported, compact, derived, runtime, and adapter surfaces summarize, transport, or support meaning.
- Self-agency, recurrence, quest, progression, checkpoint, or growth language must stay bounded, reviewable, evidence-linked, and reversible.
- Report what changed, what was verified, what was not verified, and where the next agent should resume.

## Memory route

For recall, continuity, compaction recovery, comparison with past work, or
preserved lessons, start with `aoa-memo` and the workspace memory map. Session
grounding routes through `.aoa`; local candidate writing routes through this
repository's `memo/` port; durable reviewed memory lands through `aoa-memo`.

## Route away when

- wording turns bounded proof into broad intelligence, trust, general safety, or autonomous-self claims
- the change rewrites upstream skill or technique meaning
- a stats surface, trace, or comparison becomes stronger than the evidence it carries

## Audit and review route

`AUDIT.md` is the audit surface map. This route card owns the mandatory audit
law: boundaries, approval gates, verification routes, review severity, and
report shape.

Treat these as high-risk surfaces:

- `evals/**/EVAL.md`, `evals/**/eval.yaml`, and fields such as
  `object_under_evaluation`, `claim_type`, `category`, `status`,
  `baseline_mode`, and `report_format`
- `EVAL_INDEX.md`, `EVAL_SELECTION.md`, generated catalogs, comparison-spine
  readers, and public chooser wording
- comparison, repeated-window, anti-overread, shared proof-infra, trace bridge,
  receipt, runtime-candidate, sibling-reference, and release-support surfaces

Claim pressure routes:

| Pressure | Route |
| --- | --- |
| broad intelligence, trust, general safety, or autonomous-self claim | keep the eval language scoped to its source bundle, evidence, verdict logic, and validation route; send wider meaning to the owning layer |
| canonical readiness or direct agent-behavior verdict | route to the source owner or a new bounded proof bundle before public wording changes |
| generated reader, chooser doc, or index outranking source proof | return to bundle-local `EVAL.md` and `eval.yaml`, then rebuild generated surfaces from source |
| draft, bounded, baseline, or growth language strengthening by association | keep status, baseline mode, and report posture explicit; use the approval gate before public interpretation changes |
| private dataset, secret-bearing fixture, hidden telemetry, or skipped validation | route to the private owner, a sanitized fixture, or a rerun validation record before public proof |

Get explicit human confirmation before changing category, status, baseline
mode, report format, claim type, object under evaluation, default public
baseline or comparison-ladder wording, shared fixture/scorer/runner/report
shape, a new eval bundle, starter-selection posture, or bundle-local support
artifact shape that affects public interpretation.

Review severity:

- P0: secret-bearing or private evidence presented as public proof; bounded eval
  wording converted into broad intelligence, safety, or trust claims; public
  chooser/comparison wording silently changing baseline or maturity meaning
- P1: `EVAL.md` and `eval.yaml` semantic drift; verdict wording stronger than
  support artifacts; erased blind spots; generated or comparison drift; shared
  infra names implying stronger proof; trace/eval bridge ownership drift;
  claimed validation lacking evidence

Ignore low-value wording nits unless the task explicitly requests copyediting.

## Decision memory

After a meaningful structural, topology, workflow, validation, public-contract,
legacy, runtime-candidate, sibling-reference, or agent-route change, review
`docs/decisions/`.

Add or update a decision note when future agents need to know why the route was
chosen. Decision notes preserve rationale; release notes, generated output,
runtime logs, and bundle-local proof meaning route to their owning surfaces.

## GitHub landing workflow

Root `AGENTS.md` owns the repository-wide branch, PR, CI, and merge route.
`.github/AGENTS.md` owns the GitHub-native files that support it.

When the user asks to commit, push, and merge in this repository, use this route:

1. Start from a branch based on the current `origin/main`. If the worktree is already dirty, inventory it first and carry forward only the intended diff.
2. Commit the intended change with a message that names the changed surface.
3. Push the branch and open a pull request that states changed surfaces, validation run, skipped checks, and remaining risk.
4. Wait for GitHub `Repo Validation` and any required GitHub checks. If a check fails, fix the branch and wait for the new result.
5. Merge through GitHub after green validation. Use squash unless repository settings report a different required method; report the method that landed.
6. Return to `main`, fast-forward from `origin/main`, and confirm the worktree is clean before closeout.

If GitHub status or merge permissions cannot be observed, stop the landing route and report the exact blocker instead of guessing.

## Verify

Install local dependencies when the environment lacks the development tools:

Minimum repository validation:

Use the non-mutating proof-surface battery when authored sources, generated
readers, runtime-candidate readers, or mechanic readouts need parity:

Refresh generated readers only when the change intentionally rewrites them:

Use the narrower route card first when the change is local to `evals/`,
`generated/`, `docs/`, `mechanics/`, `scripts/`, or `tests/`.

## Report

For audits, reviews, and non-trivial patches, report:

- plan: task restatement, touched or inspected bundles or public surfaces, and
  main risk
- diff: what changed, whether bounded claim meaning changed, and whether
  category, status, baseline mode, or report posture changed
- verify: exact checks run, comparison or chooser surfaces re-read, and skipped
  checks
- report: current bounded claim, remaining proof limits, public chooser or
  comparison impact, and downstream follow-up if needed
- residual risk: thin evidence, stale support artifacts, neighboring bundles
  not re-read, or comparison/routing surfaces not fully re-audited

## Full reference

`docs/operations/AGENTS_ROOT_REFERENCE.md` preserves the former detailed root guidance, including branch docs, audit contract, review priorities, and cross-repo routes.
