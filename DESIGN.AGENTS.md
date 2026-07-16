# aoa-evals Agent Surface Design

## Role

`DESIGN.AGENTS.md` describes the desired form of agent-facing guidance within
`aoa-evals`.

Use it when the question is agent-facing shape: card placement, nearest-card
authority, source truth, generated companions, validation posture, closeout, and
return routes for low-context agents.

Adjacent routes:

- executable local law: root `AGENTS.md`, then the nearest nested `AGENTS.md`
- repo direction: `ROADMAP.md`
- proof-object meaning: bundle-local `EVAL.md` and `eval.yaml`
- durable rationale: `docs/decisions/`
- validator contracts: `scripts/validate_repo.py` and owning test surfaces
- generated navigation: `generated/` and its builders

It answers one question:

What shape should agent-facing surfaces take so agents can change proof objects
while preserving source truth, evidence boundaries, reviewability, and return
routes?

## Design Thesis

`aoa-evals` should give agents a proof-aware guidance mesh: compact root route,
local cards, source surfaces, validation routes, and closeout paths.

The mesh should let a low-context agent answer:

- where am I in the proof layer?
- which surface owns the claim?
- which evidence is source, derived, candidate, receipt, legacy, or sibling
  owned?
- which validator checks this movement?
- what must the closeout say so the next agent can resume?

The root card names the proof owner lane.
The nearest card narrows the local risk.
The bundle keeps the proof claim.
The validator tests the changed contract.
The closeout returns the work to review.

## Design as Appearance

Agent guidance should look like a readable route network:

- a compact root `AGENTS.md`;
- local cards for durable districts such as `evals/`, `docs/`, `generated/`,
  `examples/`, `reports/`, `schemas/`, `scripts/`, `tests/`, `quests/`, `stats/`,
  `skills/`, `.agents/`, and `mechanics/`;
- deep cards for high-risk surfaces such as decisions, generated read models,
  receipts, legacy bridges, runtime candidates, and package parts;
- consistent sections that name role, source surfaces, boundaries, validation,
  and closeout;
- generated companions only when they point back to source cards and authored
  surfaces.

The layer should make correct movement the obvious path.

## Design as Anatomy

The agent-facing layer contains several different guidance classes.

### Root card

Root `AGENTS.md` owns repository identity, owner boundaries, start route,
route-away conditions, broad validation posture, decision review posture, and
closeout expectations.

It should stay short once root design and depth docs exist.

### District cards

Top-level district cards own local editing risks and validation routes.

For example, `docs/AGENTS.md` protects proof-meaning docs,
`generated/AGENTS.md` protects derived reader posture, and `scripts/AGENTS.md`
protects deterministic builders and validators.

### Proof bundle cards

`evals/AGENTS.md` and any future bundle-local cards should remind agents that
bundle-local `EVAL.md` and `eval.yaml` own the specific bounded claim, object
under evaluation, verdict shape, evidence posture, blind spots, and adaptation
rules.

### Local stats cards

`stats/AGENTS.md` routes eval-owned statistical questions and reference
measurements without allowing a derived count or ratio to become a proof
verdict. The embedded contract and owner evidence remain stronger than the
route card.

### Decision cards

`docs/decisions/AGENTS.md` should protect durable rationale. Decisions explain
why topology, workflow, authority, or validation moved; the changed source
surface keeps the active route.

### Quest cards

`quests/AGENTS.md` protects proof obligations and lifecycle state under
`quests/<lane>/<state>/`. Quest source records carry return routes for missing
proof; eval bundle meaning stays in `evals/**/EVAL.md`, and roadmap direction
stays in `ROADMAP.md`.

### Runtime candidate and receipt cards

Runtime-candidate, machine-evidence, trace, and receipt surfaces need cards or
nearby docs that keep candidate evidence below bundle-local review.

### Mechanic package cards

Active mechanic packages carry package cards that name the owned operation,
source surfaces, inputs, outputs, stop-lines, validators, legacy bridges, and
closeout requirements. A new package may be added only after the evidence map,
route cards, decisions, and validators prove the parent.
Before changing package boundaries, agents should read
`mechanics/EVIDENCE_CLUSTERS.md` for the root-district reconnaissance ledger,
residual root-authored surface classification, and active parent evidence
dimensions.

### Maintained agent lanes

Maintained agent lanes should live under `.agents/<lane>/`. They route
execution posture for agents. Proof meaning stays with source proof objects and
bundle-local review. The current Spark lane lives under `.agents/spark/` and
stays bounded to narrow proof-surface work.

### Repository skills

A repo-specific callable procedure may become a skill only after its own
trigger, input/output contract, composition value, coexistence behavior, and
improvement over a no-skill baseline have been demonstrated manually. Its
canonical source then lives under top-level `skills/`; runtime projections are
derived delivery surfaces, not alternate owners.

`skills/aoa-evals/` is the admitted canonical owner bundle with internal
`select`, `review`, and `evolve` modes. `.agents/skills/aoa-evals/` is its exact
generated repo projection. Shared cross-repository selection and local apply
remain owned by `aoa-skills`; source eval bundles and admitted evidence keep
proof authority.

### Legacy cards

`PROVENANCE.md` names the bridge and current owner route. Legacy homes explain
old accepted names, source lineage, and archive-local accounting after that
bridge is crossed.

## Design as Operation

A safe agent move in `aoa-evals` follows this route:

1. Read root `AGENTS.md`.
2. Read `DESIGN.md` or this file when the change alters repository shape,
   proof anatomy, or agent-facing guidance.
3. Read the nearest local `AGENTS.md` for every touched path.
4. Read the owning source surface: usually a bundle, schema, guide, decision,
   quest record, builder, or validator.
5. Name the evidence class being touched: source, derived, candidate, receipt,
   legacy, sibling reference, or runtime/machine input.
6. Make the smallest change that preserves the bounded proof owner lane.
7. Run the narrow validation first, then broader gates when generated,
   structural, release-facing, or sibling-reference surfaces move.
8. Close out with changed surfaces, checks run, checks skipped, known drift, and
   the next owner route.

## Design as Authority

Agent guidance may:

- route proof work;
- name local risks;
- name source surfaces;
- require reading order;
- require validation;
- preserve anti-overread boundaries;
- keep generated, runtime, receipt, sibling, and legacy surfaces subordinate to
  their owners.

When guidance pressure touches stronger meaning, route it to the owner surface:

| Pressure | Owner route |
| --- | --- |
| bundle claim wording | bundle-local `EVAL.md` and `eval.yaml` |
| generated reader authority | authored source surface and builder |
| runtime candidate verdict pressure | bundle-local review and candidate-evidence route |
| receipt publication pressure | reviewed report and receipt mechanic |
| sibling owner truth | sibling repository and local compatibility surface |
| hidden benchmark or private evaluator pressure | public-safe evidence review or route-away boundary |
| "docs-only" semantic pressure | source surface plus nearest `AGENTS.md` validation route |
| mythic, quest, progression, or recurrence pressure | evidence surface, quest lifecycle, or owning mechanic |

## Canonical Card Shape

Durable local cards should begin from this shape:

```markdown
# AGENTS.md

## Applies to

## Role

## Read before editing

## Boundaries

## Validation

## Closeout
```

Optional sections may be added when they sharpen the local route: `Purpose`,
`Owner lane`, `Source surfaces`, `Generated surfaces`, `Decision review`,
`Legacy posture`, `Runtime boundary`, `Post-change route review`, or package
equivalents.

## Design Principles

### 1. Nearest route before broad memory

Conversation memory and working notes help orientation, but the nearest
repo-local source surface should govern the edit.

### 2. Proof class before command

An agent should know whether it is touching a source proof object, generated
reader, candidate packet, receipt, sibling ref, or legacy alias before it runs a
command.

### 3. Bundle-local meaning before global summaries

Global docs and generated catalogs route work. A specific proof claim lives in
the bundle and its manifest.

### 4. Validation follows authority

Generated freshness checks follow generated changes. Schema checks follow
contract changes. Sibling-reference checks follow compatibility changes.
Proof-meaning checks need source refs, owner routes, generated parity, and
route-card coverage beyond presence.

### 5. Route maps before stop-lines

Cards should first say what a surface owns and how to move through it. Stop-lines
belong where overclaiming would otherwise be easy.

### 6. Legacy bridges active route

Old names should stay findable, but active cards should route by the living
operation whenever possible.

### 7. Public-safe by default

Eval examples, reports, receipts, and docs should avoid secrets, private logs,
and hidden operational topology unless a public-safe abstraction has been
reviewed.

### 8. Closeout is proof memory

A closeout should let the next agent tell what changed, what was checked, what
remains drifted, and where to resume from the closeout itself.

## Relationship to Other Root Surfaces

[`DESIGN.md`](DESIGN.md) describes the system form of the proof layer.
[`AGENTS.md`](AGENTS.md) is the active root route card.
[`docs/architecture/ARCHITECTURE.md`](docs/architecture/ARCHITECTURE.md) explains the technical proof
model.
[`docs/guides/EVAL_PHILOSOPHY.md`](docs/guides/EVAL_PHILOSOPHY.md) explains evaluation
posture and epistemic limits.
[`docs/architecture/PROOF_TOPOLOGY.md`](docs/architecture/PROOF_TOPOLOGY.md) maps proof authority
classes, active mechanics, and file-movement boundaries.
[`mechanics/EVIDENCE_CLUSTERS.md`](mechanics/EVIDENCE_CLUSTERS.md) records why
a mechanic parent is allowed and whether it is AoA-aligned or evals-native.
[`.agents/AGENTS.md`](.agents/AGENTS.md) routes maintained agent lanes.
[`skills/AGENTS.md`](skills/AGENTS.md) routes the canonical owner callable
procedure and its generated projection.
[`mechanics/README.md`](mechanics/README.md) is the operation atlas for active
mechanic packages.
`DESIGN.AGENTS.md` holds the agent-facing design form.

## Use by Agents

Consult this file when adding, moving, or refactoring:

- `AGENTS.md` cards;
- maintained agent lanes under `.agents/<lane>/`;
- the admitted owner skill under `skills/` or its `.agents/skills/` projection;
- proof bundle route rules;
- decision, quest, generated, receipt, runtime-candidate, or legacy guidance;
- future mechanic package cards;
- validators that enforce agent-facing topology.

This file gives the shape of agent guidance. The nearest `AGENTS.md` card gives
the active local route.
