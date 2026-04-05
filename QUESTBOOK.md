# QUESTBOOK.md — aoa-evals

This file is the public tracked surface for deferred proof, regression, and verdict-bridge obligations that belong to `aoa-evals`.

Use it for:
- missing proof bundles that survive current work
- regression-surface gaps
- trace-to-verdict and artifact/process bridge repairs
- repeated blind-spot or caution patterns that should become canonical eval surfaces

Do not use it for:
- a pile of one-off benchmark ideas
- private evaluator notes
- replacing the meaning of an eval bundle
- turning every local test tweak into a tracked quest

## Frontier
- `AOA-EV-Q-0005` - define a multi-axis progression evidence contract for reviewed advancement
- `AOA-EV-Q-0006` - define router orchestrator proof anchors for boundary adherence and source-of-truth selection
- `AOA-EV-Q-0007` - define review orchestrator proof anchors for evidence completeness and honest closure
- `AOA-EV-Q-0008` - define bounded-execution orchestrator proof anchors for smallest-step quality and scope discipline
- `AOA-EV-Q-0009` - define bounded unlock-proof doctrine for bridge-wave grants, gates, holds, and revokes

## Near
- `AOA-EV-Q-0003` - tighten the trace-eval bridge and artifact-process separation for portable verdicts

## Latent / parked
- `AOA-EV-Q-0004` - harvest repeated blind-spot and caution-language repairs into reusable eval patterns and rubrics

## Harvest candidates
- `AOA-EV-Q-0004` - harvest repeated blind-spot and caution-language repairs into reusable eval patterns and rubrics

## Quest-harvest posture

`aoa-quest-harvest` may be installed at `.agents/skills/aoa-quest-harvest` as a post-session aid for proof-surface triage in this repo.

- use it only after a reviewed run, closure, or pause
- do not use it inside an active route
- it does not define orchestrator identity
- it does not replace playbook, memo, eval, or source-owned doctrine
- do not promote on one anecdotal repeat

Allowed verdicts:

- `keep/open quest`
- `promote to skill`
- `promote to playbook`
- `promote to orchestrator surface`
- `promote to proof surface`
- `promote to memo surface`

## Backing files

- `quests/*.yaml`
- `schemas/quest.schema.json`
- `schemas/quest_dispatch.schema.json`
- `generated/quest_catalog.min.json`
- `generated/quest_dispatch.min.json`
- `generated/quest_catalog.min.example.json`
- `generated/quest_dispatch.min.example.json`

The live generated quest pair is a repo-local review and validation projection.
The example pair is its example mirror.
Neither pair replaces eval bundle meaning or becomes live portable verdict authority.
