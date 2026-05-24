# Contributing to aoa-evals

Thank you for contributing.

`aoa-evals` accepts contributions that make a bounded proof claim easier to
inspect, rerun, compare, review, or route to its owner.

## Contribution Routes

Choose the owner route before opening a PR.

| Contribution pressure | Owner route |
| --- | --- |
| portable eval bundle for agents or agent-shaped workflows | source bundle under `evals/` plus bundle-local `EVAL.md` and `eval.yaml` |
| bounded comparison, regression, longitudinal, artifact-quality, authority, scope, or safety-boundary eval | owning bundle family, comparison guide, boundary guide, and generated reader route when public selection changes |
| reusable scorer, rubric, verdict logic, fixture set, report contract, or interpretation guide | owning bundle, `docs/` guide, or mechanic part that carries the repeated proof support |
| eval integrity check or proof-surface validation improvement | owning bundle, `scripts/`, `tests/`, or mechanic route card |
| repeated proof-operation support | `mechanics/README.md`, then the parent package, part README, and local `AGENTS.md` |
| contribution whose main meaning is reusable practice | route to `aoa-techniques` |
| contribution whose main meaning is executable workflow | route to `aoa-skills` |

## Intake Pressure Routes

Route these pressures before they become public proof claims:

| Pressure | Route |
| --- | --- |
| loose test or project QA without a bounded public claim | keep it local until it has an eval contract and interpretation boundary |
| private fixture, log, trace, or sensitive operational detail | security process or owning private surface before public PR |
| large run dump | selected evidence packet, compact report, or audit candidate route |
| undocumented scorer or metric | score semantics, verdict interpretation, and bundle-local review |
| claim wording grows broader than its evidence | bundle-local claim review and blind-spot disclosure |
| sibling-owner meaning appears | route to the sibling owner and keep the eval contribution to bounded proof support |

## Before opening a PR

Please make sure:
- the eval bundle is sanitized
- the bounded claim is explicit
- the bundle includes a canonical `EVAL.md`
- the object under evaluation is named clearly
- the fixture surface is described and bounded
- scoring or verdict logic is reviewable
- blind spots are named explicitly
- interpretation guidance is present
- public-safety concerns are checked
- status is set honestly
- any technique or skill traceability is stated clearly
- current public starters ship `evals/<family>/<eval>/examples/example-report.md`
- current public starters carry explicit manifest evidence for their public support artifacts
- current public starters carry an integrity-review artifact such as `checks/eval-integrity-check.md`
- `EVAL_INDEX.md` and `EVAL_SELECTION.md` stay aligned when starter posture changes

Before opening a PR, run local validation and bundle checks for:
- schema shape
- index and selection parity
- frontmatter consistency
- evidence paths that should resolve publicly
- baseline-readiness evidence when `baseline_mode` is not `none`
- integrity-check evidence for current public starters
- scorer and report contract coherence
- fixture references that should exist publicly

Local note:
- if `aoa-techniques` or `aoa-skills` are not checked out beside `aoa-evals`, local validation will skip dependency-target existence checks for those sibling repos
- CI performs the strict dependency-path existence check by exporting `AOA_TECHNIQUES_ROOT` and `AOA_SKILLS_ROOT` after checking those repos out into `.deps/`
- if `abyss-stack` is present locally only as a deployed runtime tree, export
  `ABYSS_STACK_ROOT` to the source checkout before using the repository
  validation route

## Local development setup

Use root `AGENTS.md#verify` for local setup and validation commands. Use the
nearest nested `AGENTS.md` when a contribution only touches one district such as
`docs/`, `evals/`, `mechanics/`, `scripts/`, or `tests/`.

## Preferred PR scope

Prefer:
- 1 eval bundle per PR
- or 1 maturity/status transition per PR
- or 1 focused improvement to an existing bundle
- or 1 bounded scorer / fixture / report-contract improvement

## Recommended PR title format

- `eval: add <eval-name>`
- `eval: improve <eval-name>`
- `eval: promote <eval-name> to baseline`
- `eval: promote <eval-name> to canonical`
- `eval: deprecate <eval-name>`
- `docs: refine eval guidance`
- `repo: improve validation rules`

## Review criteria

PRs are reviewed for:
- boundedness of the claim
- portability
- repeatability
- score or verdict honesty
- blind-spot disclosure
- fixture discipline
- public safety
- clarity of interpretation
- coherence with repository philosophy

## Status transitions

### draft -> bounded

Should usually demonstrate:
- a clear bounded claim
- a named object under evaluation
- a repeatable execution path
- understandable scoring or verdict logic
- explicit blind spots
- outputs that do not overstate what was learned

### bounded -> portable

Should usually demonstrate:
- the bundle survives outside one narrow origin context
- fixtures and scoring do not depend on hidden local assumptions
- interpretation remains meaningful after bounded adaptation
- portability notes or review evidence exist

### portable -> baseline

Should usually demonstrate:
- stable enough repeatability for disciplined comparison
- clear baseline or comparison semantics
- explicit `baseline_readiness` evidence when the bundle uses a non-`none` baseline mode
- fixture discipline strong enough to support comparative use
- verdicts or scores that resist false certainty
- practical reuse beyond one origin need

### baseline -> canonical

Should usually demonstrate:
- a crisp default-use rationale within its bounded claim class
- stronger validation than the baseline floor
- trustworthy comparison meaning across review cycles or contexts
- honest interpretation boundaries
- a fresh public-safety recheck

Do not mark an eval `canonical` because it feels impressive or produces tidy numbers.

### canonical -> deprecated

Requires:
- a reason
- a replacement if available
- a brief note in index or bundle history

## Report and score discipline

A strong PR should make it easy for reviewers to answer:
- what claim is being made?
- what supports that claim?
- what does the eval still fail to prove?
- what kind of regression would this bundle catch?
- where could this bundle mislead a careless reader?

If the answer depends on hidden intuition, the bundle is not ready.

## Security

If your contribution reveals a leak, secret, private fixture source, or sensitive operational detail,
do not open a public issue or PR with that material.
Use the repository security process instead.

## Final note

A good eval bundle does not try to prove everything.

It should prove one bounded thing honestly.
That is enough.
That is the standard this repository exists to protect.
