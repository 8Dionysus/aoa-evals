# Mechanics Operation Atlas

## Role

`mechanics/` is the operation atlas for repeatable proof-layer operations in
`aoa-evals`.

It receives recurring proof pressure and routes it to the parent operation,
part contract, payload home, and validation lane that owns the work. A mechanic
exists only when a recurring operation has source surfaces, inputs, outputs,
boundaries, and validation.

Package taxonomy requires source surfaces, inputs, outputs, boundaries,
validation, and parent evidence.

## Operating Card

| Field | Route |
| --- | --- |
| role | operation atlas for repeatable proof-layer work |
| entry | choose a parent from `Active Packages`, or recover it bottom-up from a payload |
| input | source proof pressure, support artifact movement, route-card drift, or mechanic-owned payload work |
| output | parent route, part contract, payload location, validation lane, or stronger-owner handoff |
| owner | mechanic parent `README.md`, `DIRECTION.md`, `PARTS.md`, part `README.md`, and nearest `AGENTS.md` |
| next route | `mechanics/EVIDENCE_CLUSTERS.md` for parent evidence, `docs/PROOF_TOPOLOGY.md` for authority class |
| validation | [mechanics/AGENTS.md#validation](AGENTS.md#validation) and the nearest package card |

## Traversal Index

Use mechanics as a lower proof index that turns parent names and payload paths
into routeable operations.

Top-down route:

`mechanics/README.md -> mechanics/<parent>/README.md -> DIRECTION.md -> PARTS.md -> parts/<part>/README.md -> payload subdirectory -> validation route`

Bottom-up route:

`payload file -> nearest part README -> parent PARTS.md -> parent DIRECTION.md -> parent README -> mechanics/EVIDENCE_CLUSTERS.md -> docs/PROOF_TOPOLOGY.md`

| Layer | Primary route | What it answers |
| --- | --- | --- |
| parent operation | `mechanics/<parent>/README.md` | what repeatable proof operation this parent owns |
| current contour | `mechanics/<parent>/DIRECTION.md` | what is active now, what is deferred, and what stop-lines apply |
| part set | `mechanics/<parent>/PARTS.md` | which parts exist and how they relate to inputs, outputs, owner split, stop-lines, and validation |
| local part contract | `mechanics/<parent>/parts/<part>/README.md` | source surfaces, payload classes, local validation, and part-specific boundaries |
| payload | `docs/`, `examples/`, `fixtures/`, `schemas/`, `scripts/`, `tests/`, `reports/`, `generated/`, or other part-local payload homes | the actual proof-support material owned by the part |
| route law | nearest `AGENTS.md` | how an agent may edit the surface and what to verify before closeout |
| evidence class | `mechanics/EVIDENCE_CLUSTERS.md` and `docs/PROOF_TOPOLOGY.md` | why the parent exists and what authority class the artifact belongs to |

When starting from a payload, recover the nearest part first. When starting from
a parent, read `DIRECTION.md` before part details. When a path looks legacy,
enter through `PROVENANCE.md` before opening archive internals.

## Evidence Atlas

Use [`mechanics/EVIDENCE_CLUSTERS.md`](EVIDENCE_CLUSTERS.md) before moving
root-district artifacts into or between packages. It owns the parent evidence
gate for this atlas:

- parent class: which parent names are AoA-aligned and which are evals-native;
- Root District Reconnaissance Ledger: which root districts remain
  route-card-only and where their active payload moved;
- residual root-authored surfaces: which top-level `docs/`, `scripts/`, and
  `tests/` files stay root-owned;
- Active Parent Evidence Dimension Ledger: meaning/doctrine, proof pressure,
  contracts/payloads, builders/readouts, quest/deferred pressure, owner split,
  stop-lines, and legacy/provenance;
- Active Parent Evidence Route Refs: at least one active parent route and at
  least one living non-mechanics evidence route for every parent.

Use the evidence gate as an operating checklist:

| Need | Required route |
| --- | --- |
| parent activation | `mechanics/<new-parent>/` starts from a cross-root cluster, package contract, topology update, decision record, and validator allowlist entry |
| parent route shape | every active parent exposes `AGENTS.md`, `README.md`, `DIRECTION.md`, and `PARTS.md`; `DIRECTION.md` owns the current operating direction, growth rule, stop-lines, source split, and validation posture; each parent `README.md` and `AGENTS.md` routes `DIRECTION.md` from its Entry Route |
| part contract | each part README names inputs, outputs, stronger owner split, stop-lines, validation, payload homes, and the source surfaces that make the part real |
| parent part map | parent `PARTS.md` keeps the declared part route set synchronized with actual `parts/` directories; stale local part route checks keep removed parts from staying active by name; cross-parent references stay owner-split, stop-line, or handoff routes |
| payload coverage | every actual payload subdirectory is routed from the part README; a bundle-backed thin support route points to the source eval package under `evals/` as its payload |
| source refs | every concrete mechanic part README exposes plural `## Source Surfaces` with at least one path-like source ref that resolves as an existing repo-relative path, matching repo-relative glob, repo-qualified sibling ref, or explicit placeholder route; stale source surface ref checks keep old root payload names from steering current work |
| validation route | every part `## Validation` section routes to part-local `VALIDATION.md`; every `VALIDATION.md` routes to the parent `parts/AGENTS.md` centralized child validation block; that block owns reachable repo-relative executable checks, stale validation path checks keep the route current, and payload-bearing parts carry a payload coverage anchor |
| parent-level docs | parent-level `docs/` carries explicitly allowlisted mechanic-wide guidance; part-owned payload docs live under `parts/<part>/docs/`; allowed parent guides expose role, mechanic-wide scope, source surfaces, stronger owner split, stop-lines, and validation |

Rationale-only decisions and generic root validator refs can support context.
The Active Parent Evidence Route Refs ledger supplies the living route evidence
that makes a parent operational.

## Provenance Bridge And Archive Boundary

Every active parent must expose the same active-to-archive boundary:

- `PROVENANCE.md` as the bridge from active route to former placement;
- a legacy archive behind that bridge, with its own route card and
  archive-local accounting.

Archive boundary route: active work starts from parent `README.md`,
`DIRECTION.md`, `PARTS.md`, parts, owner split, stop-lines, and validation.
Legacy explains lineage after the active form exists, and the archive explains
its own internal route.
Every `PROVENANCE.md` is the active-to-archive bridge for its mechanic.

Use active surfaces first:

- parent `README.md`;
- parent `DIRECTION.md`;
- parent `PARTS.md`;
- part-local `parts/` contracts and payloads.

Every `PROVENANCE.md` is the single controlled bridge from active mechanic surfaces into the legacy archive.
Active mechanic surfaces route to archive internals through `PROVENANCE.md`;
the legacy directory explains itself after the reader crosses that bridge.
Archive-local indexes, raw lineage, distillation logs, and accounting rules
belong inside `legacy/`; this active atlas names only the bridge and the
current owner route.

## Parent Class Summary

The active parent set is split by `mechanics/EVIDENCE_CLUSTERS.md`:

- AoA-aligned parents: `agon`, `release-support`, `audit`,
  `boundary-bridge`, `questbook`, `recurrence`, `checkpoint`, `experience`,
  `antifragility`, `method-growth`, `rpg`, `growth-cycle`, and
  `distillation`.
- Evals-native parents: `proof-object`, `proof-infra`,
  `comparison-spine`, `publication-receipts`, `proof-loop`, and `titan`.

`titan` is the owner-named evals-native case: `aoa-evals` owns the
seed-boundary proof operation, while `aoa-agents` keeps Titan role, bearer,
summon, and incarnation law. The parent is `titan` because the proof subject is
Titan; canaries are only the current `seed-boundary` payload form.

Concrete wrong-parent mappings live in
[`mechanics/EVIDENCE_CLUSTERS.md`](EVIDENCE_CLUSTERS.md), where the validator
checks them against the active parent-class map. This README keeps the route:
legacy, artifact-form, evidence-class, and stage-pressure vocabulary stay in
the evidence cluster map and provenance bridge until an evidence-backed parent
route promotes them.

## Active Packages

### `proof-object`

`mechanics/proof-object/` owns the operation that keeps source proof objects
complete, bounded, and stronger than generated or emitted companions:

`origin proof pressure -> source proof bundle -> proof-object completeness review -> generated reader derivation -> bundle-local report or downstream route`

It routes `evals/**/EVAL.md`, `evals/**/eval.yaml`, the
`eval-authoring` template part, the `eval-contracts` schema part, proof
review guides, generated catalog readers, and lifecycle posture while `evals/`
stays the source proof object district.

### `proof-loop`

`mechanics/proof-loop/` owns the route that makes one active proof loop locally
followable:

`proof question -> selection route -> source proof object -> support contract -> candidate evidence packet -> bundle-local review -> bounded report -> optional receipt`

It coordinates `proof-object`, `proof-infra`, `audit`, `boundary-bridge`, and
`publication-receipts` while each step owner stays authoritative for its own
route. Its first bounded route-smoke report lives in
`mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md`.

### `comparison-spine`

`mechanics/comparison-spine/` owns the operation that keeps baseline,
peer-compare, and longitudinal-window proof claims bounded:

`comparison claim -> bundle comparison_surface -> shared proof artifacts -> generated comparison spine -> bounded comparison read`

It routes comparison guides, `comparison_surface`, part-local comparison
fixture families and reports, `generated/comparison_spine.json`, and shared
proof artifact contracts while source bundles and generated readers stay in
their owner lanes.

### `proof-infra`

`mechanics/proof-infra/` owns the operation that keeps shared proof contracts
reusable and bundle-local meaning visible:

`bundle proof need -> shared proof contract -> bundle-local contract -> generated proof_artifacts -> bounded review`

It routes shared fixture families, runner contracts, scorer helpers, schemas,
report contracts, templates, and generated catalog `proof_artifacts`. Generic
shared fixture families now live
under `mechanics/proof-infra/parts/fixture-families/fixtures/`; shared
reportable runner/scorer/schema contracts now live under
`mechanics/proof-infra/parts/reportable-contracts/`. Whole infrastructure
districts move only through owner operation, evidence, and validation.

### `publication-receipts`

`mechanics/publication-receipts/` owns the operation that keeps optional eval
result publication receipts subordinate to reviewed reports:

`reviewed bounded report -> eval-result receipt payload -> stats-event-envelope sidecar -> owner-local live receipt log -> downstream derived reader`

It keeps the eval result receipt guide, payload schema, local stats envelope
mirror, public example, live publisher, and intake dry review in package-local
parts while `.aoa/live_receipts/` remains the owner-local append surface.

### `release-support`

`mechanics/release-support/` owns the operation that keeps bounded release
publication coherent and eval claims bounded:

`bounded release scope -> changelog narrative -> release audit -> Repo Validation -> tag and GitHub release notes -> post-release proof posture`

It routes `docs/RELEASING.md`, `CHANGELOG.md`, `scripts/release_check.py`,
GitHub `Repo Validation`, generated freshness checks, release-note posture, and
part-local readiness/closeout/handoff reports while root release entrypoints,
CI, generated surfaces, and source proof bundles stay in their owner lanes.

### `titan`

`mechanics/titan/` owns the operation that keeps Titan seed canary
surfaces shaped and bounded:

`Titan boundary pressure -> seed canary YAML -> shape validation -> future executable scorer route -> bounded proof or owner handoff`

It routes Titan incarnation and summon discipline guides,
`mechanics/titan/parts/seed-boundary/seeds/titan*.yaml`,
`mechanics/titan/parts/seed-boundary/seeds/AGENTS.md`, legacy naming posture,
and `validate_titan_canary_surfaces`. Full Titan incarnation proof routes to
the stronger Titan owner.

### `agon`

`mechanics/agon/` owns the operation that keeps Agon proof-alignment artifacts
part-local, generated from source, candidate-only, observe-only, and
stop-line bounded:

`Agon pressure -> part-local seed/config/docs -> deterministic registry -> candidate-only checks -> observe-only recurrence hooks -> bundle-local review or owner handoff`

It routes Agon docs, seed configs, generated registries, schemas, examples,
scripts, tests, recurrence manifests, observe-only hooks, quest notes, and
recurrence-control-plane stop-line review through candidate-only eval support;
live verdict authority stays outside this package.

### `recurrence`

`mechanics/recurrence/` owns the operation that keeps recurrence proof work
bounded on the eval side:

`recurrence pressure -> bounded recurrence proof question -> control-plane, anchor-return, memory-recall, recursor-boundary, regrounding, or portable-proof-beacon evidence -> bundle-local review -> bounded report, decision packet, or owner handoff`

It routes the recurrence proof program, control-plane integrity support,
return-anchor fixtures, memo-recall fixtures and phase-alpha report checks,
recursor readiness boundary fixture, scorer, runner, and test surfaces, stats
re-grounding fixture/report checks, recurrence component manifests, and
portable-proof beacon hook bindings while keeping source proof bundles under
`evals/`.

### `checkpoint`

`mechanics/checkpoint/` owns the operation that keeps checkpoint proof work
bounded on the eval side:

`checkpoint pressure -> bounded checkpoint proof question -> part-local support surface -> bundle-local review -> bounded report or owner handoff`

It routes A2A summon return checkpoint support, restartable-inquiry checkpoint
support, self-agent checkpoint posture, checkpoint-specific hook examples, and
part-local fixture/test surfaces while keeping source proof bundles under
`evals/` and hook schema/readers under `mechanics/audit/`.

### `experience`

`mechanics/experience/` owns the operation that keeps Experience proof work
bounded on the eval side:

`experience pressure -> bounded experience proof question -> part-local verdict support -> bundle-local review -> bounded report or owner handoff`

It routes experience protocol integrity, certification gate, adoption
federation, governance/runtime-boundary, and office release-train support
surfaces through active parts while keeping source proof bundles under
`evals/` and stronger owner truth in its owning repositories.

### `antifragility`

`mechanics/antifragility/` owns the operation that keeps Antifragility proof
work bounded on the eval side:

`stress or repair pressure -> bounded antifragility proof question -> owner-first evidence -> bundle-local review -> bounded report or owner handoff`

It routes first-wave posture review, repeated-window stress recovery support,
and bounded repair-proof support through active parts while keeping source
proof bundles under `evals/`, comparison readout discipline under
`comparison-spine`, runtime-chaos selected evidence under `audit`, and
diagnosis-cause discipline routed through `growth-cycle/diagnosis-gate`.

### `method-growth`

`mechanics/method-growth/` owns the operation that keeps Method-growth proof
work bounded on the eval side:

`growth-refinery pressure -> lineage or owner-landing proof question -> part-local fixture family -> bundle-local review -> bounded verdict or owner handoff`

It routes candidate-lineage and owner-landing support through active parts while
keeping source proof bundles under `evals/`, final object truth with owner
repositories, repair proof under `antifragility`, and diagnosis-cause
discipline routed through `growth-cycle/diagnosis-gate`.

### `rpg`

`mechanics/rpg/` owns the operation that keeps RPG progression and unlock proof
work bounded on the eval side:

`progression or unlock pressure -> multi-axis evidence -> bounded unlock proof -> owner handoff or held gate`

It routes progression evidence and unlock proof support through
`progression-unlocks` while keeping role truth with `aoa-agents`, skill truth
with `aoa-skills`, technique truth with `aoa-techniques`, campaign and party
method with `aoa-playbooks`, quest acceptance with quest owners, runtime equip
state with `abyss-stack`, and derived summaries with `aoa-stats`.

### `growth-cycle`

`mechanics/growth-cycle/` owns the operation that keeps Growth Cycle diagnosis
proof work bounded on the eval side:

`diagnosis pressure -> cause-hypothesis proof question -> bundle-local diagnosis review -> repair eligibility or owner handoff`

It routes `aoa-diagnosis-cause-discipline` through `diagnosis-gate` while
keeping repair proof under `antifragility`, repeated-window movement under
`comparison-spine`, RPG progression/unlock proof under `rpg`, and closeout,
harvest, quest, and owner-followthrough pressure deferred until separate
evidence proves active parts.

### `distillation`

`mechanics/distillation/` owns the operation that keeps Distillation proof work
bounded on the eval side:

`distillation pressure -> provenance-preserving or candidate-preserving proof question -> part-local support surface -> bundle-local review -> bounded abstraction/adoption read or owner handoff`

It routes `aoa-compost-provenance-preservation` through
`compost-provenance` and `aoa-memo-reviewed-candidate-adoption-integrity`
through `runtime-candidate-adoption` while keeping source proof bundles under
`evals/`, runtime-pack bridge metadata under `audit`, generic Experience
adoption under `experience`, and memo recall, memo contradiction, and base
writeback-act proof outside this package until separate evidence proves a
Distillation part.

### `questbook`

`mechanics/questbook/` owns the operation that keeps quest obligations
routeable:

`source quest record -> human index -> generated quest reader -> deferred return or reviewed promotion`

It routes the current lane/state quest source paths, `QUESTBOOK.md`,
part-local quest schemas, generated quest readers, lifecycle posture, and
post-session harvest boundary while keeping old top-level quest paths and
former root schema placement as legacy vocabulary only.

### `audit`

`mechanics/audit/` owns the operation that keeps runtime and trace
artifacts candidate-only until bundle-local review:

`runtime or trace artifact -> selected evidence packet -> runtime candidate reader -> bundle-local review`

It routes runtime evidence selection examples, artifact-to-verdict hooks,
generated candidate readers, runtime promotion guides, integrity-review
surfaces, and stronger-owner boundaries through part-local homes. Verdict
authority stays with bundle-local review.

### `boundary-bridge`

`mechanics/boundary-bridge/` owns the operation that keeps proof references and
class-facing proof anchors into sibling repositories compatibility-aware:

`repo-qualified ref or class-facing proof anchor -> sibling owner route -> compatibility posture -> latest-sibling canary or quest validator -> bundle-local or quest review`

It routes `mechanics/boundary-bridge/parts/compatibility-map/docs/SIBLING_PROOF_REFS.md`, `mechanics/boundary-bridge/parts/latest-sibling-canary/config/sibling_canary_matrix.json`,
`mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py`,
`mechanics/boundary-bridge/parts/orchestrator-proof-anchors/docs/ORCHESTRATOR_PROOF_ALIGNMENT.md`,
`mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/generated/phase_alpha_eval_matrix.min.json`,
and local proof refs with sibling repositories read as owners, orchestrator
identity routed to `aoa-agents`, and `aoa-playbooks` run truth kept upstream
from eval verdict authority.

## Candidate Families

Candidate families stay evidence-only until a parent route has source surfaces,
contracts, owner split, and validation.

Current candidate promotion state: empty.
Future candidates must come from
[`mechanics/EVIDENCE_CLUSTERS.md`](EVIDENCE_CLUSTERS.md), local proof pressure,
and a validator, builder, or review check that can catch drift.

## Package Shape

Each active package should name:

- owned operation;
- source surfaces;
- inputs;
- outputs;
- stronger-owner split;
- legacy or accepted-input posture when relevant;
- boundaries;
- validation;
- next route.

Package cards route recurring work and hand off to `DESIGN.md`, eval bundles,
decision records, generated builders, or sibling-owner truth when those
surfaces own the stronger meaning.

## Validation

Executable commands for this mechanics atlas live in
[mechanics/AGENTS.md#validation](AGENTS.md#validation).

For package-local work, start with the nearest package `AGENTS.md` and add the
central mechanics lane only when registry, parent topology, part topology,
generated readers, public route surfaces, or release-bound proof claims move.
