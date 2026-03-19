# Contributing to aoa-evals

Thank you for contributing.

## What belongs here

Good contributions:
- portable eval bundles for agents or agent-shaped workflows
- bounded comparison surfaces
- artifact-quality evals
- regression and longitudinal evals
- authority, scope, or safety boundary evals
- reusable scorers, rubrics, and verdict logic
- portable fixture sets
- compact report contracts and interpretation guides
- eval integrity checks

Bad contributions:
- random tests without a bounded public evaluation contract
- private project QA with no generalization path
- secret-bearing fixtures, logs, or traces
- giant uncurated run dumps
- undocumented scoring logic
- metrics with no interpretation boundary
- bundles that imply broader claims than they support
- techniques that should live in `aoa-techniques`
- execution workflows that should live in `aoa-skills`

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
- current public starters ship `examples/example-report.md`
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

## Local development setup

Recommended local setup:
- `python -m pip install -r requirements-dev.txt`
- `python scripts/validate_repo.py`
- `python -m pytest`

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
