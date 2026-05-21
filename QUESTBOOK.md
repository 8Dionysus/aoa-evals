# QUESTBOOK.md - aoa-evals

## Role

`QUESTBOOK.md` is the public human index for deferred proof, regression, and
verdict-bridge obligations that belong to `aoa-evals`.

It is not the roadmap, not an eval bundle, not a generated dispatch surface, and
not a live verdict authority.

- Direction lives in [ROADMAP.md](ROADMAP.md).
- Source quest records live in `quests/<lane>/<state>/*.yaml`.
- Quest topology guidance lives in `quests/README.md` and
  `quests/AGENTS.md`.
- Quest lifecycle meaning lives in `quests/LIFECYCLE.md`.
- Generated quest readers live in `generated/quest_catalog.min.json` and
  `generated/quest_dispatch.min.json`.
- Proof meaning lives in `bundles/*/EVAL.md` and `bundles/*/eval.yaml`.

## Use It For

- missing proof bundles that survive current work;
- regression-surface gaps;
- trace-to-verdict and artifact/process bridge repairs;
- repeated blind-spot or caution patterns that should become canonical eval
  surfaces;
- proof-pressure ingress that needs a return route before it becomes an eval
  bundle, decision, mechanic, or release item.

Do not use it for:

- a pile of one-off benchmark ideas;
- private evaluator notes;
- replacing the meaning of an eval bundle;
- turning every local test tweak into a tracked quest;
- treating generated quest readers as portable verdict authority.

## Current Open Obligations

### Frontier

- `AOA-EV-Q-0005` - define a multi-axis progression evidence contract for
  reviewed advancement
- `AOA-EV-Q-0006` - define router orchestrator proof anchors for boundary
  adherence and source-of-truth selection
- `AOA-EV-Q-0007` - define review orchestrator proof anchors for evidence
  completeness and honest closure
- `AOA-EV-Q-0008` - define bounded-execution orchestrator proof anchors for
  smallest-step quality and scope discipline
- `AOA-EV-Q-0009` - define bounded unlock-proof doctrine for bridge-wave grants,
  gates, holds, and revokes

### Near

- `AOA-EV-Q-0003` - tighten the trace-eval bridge and artifact-process
  separation for portable verdicts

### Latent

- `AOA-EV-Q-0004` - harvest repeated blind-spot and caution-language repairs
  into reusable eval patterns and rubrics
- `AOA-EV-Q-0010` - capture checkpoint automation proof-pressure as early eval
  evidence
- `AOA-EV-Q-0011` - capture chaos-wave1 proof-pressure as early eval evidence
- `AOA-EV-Q-0012` - capture reviewed workspace closeout proof-pressure as early
  eval evidence
- `AOA-EV-Q-0013` - capture Agents-of-Abyss v0.4.0 proof-pressure as early eval
  evidence

## Closed Foundation Records

Closed source records stay in `quests/` and generated projections, but they are
not listed as open obligations here and are not enumerated in this human index.

## Harvest Candidates

Harvest candidates are open obligations whose evidence may become proof
surfaces after review. They are not promotions by themselves.

- `AOA-EV-Q-0004`
- `AOA-EV-Q-0010`
- `AOA-EV-Q-0011`
- `AOA-EV-Q-0012`
- `AOA-EV-Q-0013`

## Quest Topology Posture

Current source placement is lane/state based:

- `quests/<lane>/<state>/AOA-EV-Q-*.yaml` are source quest records;
- former Agon markdown quest notes are Agon lineage behind
  `mechanics/agon/PROVENANCE.md`, not active quest lifecycle source records;
- old top-level quest paths are legacy path vocabulary, not active source
  files.

Current topology uses paths such as:

`quests/<lane>/<state>/<quest-id>.*`

Candidate lanes:

- `proof`
- `trace`
- `orchestrator`
- `unlock`
- `runtime`
- `closeout`
- `agon`
- `harvest`
- `questbook`

The state directory must match the record's `state` field. Validators and
generated projections must follow any future path change in the same slice.

State meaning is defined in `quests/LIFECYCLE.md`: `captured`, `triaged`,
`ready`, `active`, `blocked`, and `reanchor` remain open obligations; `done`
and `dropped` remain closed provenance and are not listed as current open
obligations.

## Quest-Harvest Posture

`aoa-quest-harvest` may be installed at `.agents/skills/aoa-quest-harvest` as a
post-session aid for proof-surface triage in this repo.

- use it only after a reviewed run, closure, or pause;
- do not use it inside an active route;
- it does not define orchestrator identity;
- it does not replace playbook, memo, eval, or source-owned doctrine;
- do not promote on one anecdotal repeat.

Allowed verdicts:

- `keep/open quest`
- `promote to skill`
- `promote to playbook`
- `promote to orchestrator surface`
- `promote to proof surface`
- `promote to memo surface`

## Backing Files

- `quests/<lane>/<state>/*.yaml`
- `mechanics/questbook/parts/source-record-contract/schemas/quest.schema.json`
- `mechanics/questbook/parts/dispatch-reader/schemas/quest_dispatch.schema.json`
- `generated/quest_catalog.min.json`
- `generated/quest_dispatch.min.json`
- `generated/quest_catalog.min.example.json`
- `generated/quest_dispatch.min.example.json`

The live generated quest pair is a repo-local review and validation projection.
The example pair is its example mirror.
Neither pair replaces eval bundle meaning or becomes live portable verdict
authority.
