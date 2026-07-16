# Proof Topology

## Role

`docs/architecture/PROOF_TOPOLOGY.md` maps the authority classes inside `aoa-evals`.

Use this map for authority-class routing. Use `ROADMAP.md` for sequencing,
`docs/architecture/ARCHITECTURE.md` for the proof model, source eval packages for bundle
meaning, `docs/decisions/` for rationale, generated readers for compact
projections, and `mechanics/README.md` for the operation atlas.

This topology map answers one question:

Which kind of proof surface am I touching, and what may that surface own,
receive, transform, emit, or route onward?

## Operating Card

| Field | Route |
| --- | --- |
| role | authority-class topology map for the bounded proof organ |
| entry | use when a path, payload, generated reader, receipt, quest, decision, legacy name, or mechanic operation needs authority classification |
| input | touched surface, old root path, proposed mechanic parent, generated ref, receipt, candidate evidence packet, or route residue |
| output | authority class, stronger owner route, allowed transformation, next route, and validation guard |
| owner | `docs/AGENTS.md` for docs law; this map for authority classes; `mechanics/EVIDENCE_CLUSTERS.md` for parent evidence |
| next route | `docs/architecture/AGENT_INDEX.md`, `mechanics/README.md`, parent route cards, source eval packages, generated builders, or `docs/decisions/` |
| validation | `docs/AGENTS.md#validation` and the nearest route card for the touched authority class |

## Topology Thesis

`aoa-evals` becomes safer to refactor when its topology is convex.

Convex topology means the main proof classes protrude clearly enough that a
reader can tell source proof objects, derived readers, candidate evidence,
receipts, quest obligations, decisions, sibling references, legacy lineage, and
mechanic operations apart before editing.

The goal is a repository shape where correct route choice is easier than
overclaiming.

## Authority Classes

| Class | Primary surfaces | Owns | Receives or emits | Boundary |
| --- | --- | --- | --- | --- |
| Source proof objects | `evals/**/EVAL.md`, `evals/**/eval.yaml`, `mechanics/proof-object/parts/eval-authoring/`, `mechanics/proof-object/parts/eval-contracts/`, bundle-local notes and fixtures | bounded claim, object under evaluation, evidence posture, verdict logic, baseline or comparison posture, blind spots | receives selected evidence and review context; emits bundle-local report expectations and bounded interpretation | strongest local proof meaning for one eval claim |
| Source guidance | `DESIGN.md`, `docs/architecture/ARCHITECTURE.md`, `docs/guides/EVAL_PHILOSOPHY.md`, score, verdict, portability, comparison, trace, and infra guides | repo form, proof philosophy, review vocabulary, guide-level interpretation rules | receives pressure from bundles, reports, decisions, and validators; emits routeable guidance | specific bundle claims stay with bundle-local `EVAL.md` and `eval.yaml` |
| Shared proof infrastructure | `fixtures/`, `mechanics/proof-infra/parts/fixture-families/fixtures/`, `mechanics/proof-infra/parts/reportable-contracts/`, `runners/`, `scorers/`, `schemas/`, `templates/`, reusable report contracts | reusable contracts and execution support for proof work | receives bundle needs; emits fixtures, runner contracts, scorer helpers, schemas, and templates | stays weaker than bundle-local interpretation |
| Repo-local suite execution contracts | sibling `evals/suites/*.suite.json` validated by `mechanics/proof-object/parts/eval-authoring/schemas/local-eval-suite-execution.schema.json` | canonical PORT/Git owner identity, typed `python_pytest` argv/cwd/timeout/exit source contract, and tracked-source freshness state | receives a matching suite note plus reviewed source hashes; emits `absent`/`invalid`/`stale`/source-contract-`ready` routing metadata | `.suite.md` alone is non-runnable; ready does not prove runtime reproducibility; discovery/readiness/MCP never execute; only repo owner or `aoa-eval-apply` JIT-revalidates, invokes exact argv, and captures environment/receipt; no verdict or proof authority |
| Reports and examples | `reports/`, `examples/`, and mechanic-local `parts/*/reports/` where a narrower mechanic owns the readout | public-safe readouts and example payloads | receive source bundle contracts and schemas; emit reviewable examples or bounded result artifacts | examples illustrate; reports read one bounded result |
| Derived readers | `generated/`, `EVAL_INDEX.md`, `EVAL_SELECTION.md`, generated quest readers | navigation, selection, compact projections, deterministic read models | receive authored source surfaces through builders; emit read-heavy routing surfaces | generated surfaces are companions that route to authored source owners |
| Local KAG provider | `kag/` | compact source-linked provider records for KAG registry, composition, and MCP consumers | receives eval report index and owner-route refs; emits portable provider packet records and validation receipts | proof meaning stays with eval bundles and generated readers; shared KAG schema, registry, and provider validation stay with `aoa-kag` |
| Candidate evidence | runtime evidence selections, artifact-to-verdict hooks, runtime candidate intake and template indexes | selected evidence packets and hook shapes that may support review | receive runtime, trace, machine, or sibling artifacts; emit candidate packets for bundle-local review | candidate packets enter bundle-local review before verdict meaning |
| Memory evidence context | reviewed `aoa-memo` object ids, provenance, lifecycle, generated memory read models, `.aoa` session evidence refs, local `memo/` port packets, and `aoa_memo` MCP access-plane dry-runs | recall context, source refs, and `write_candidate_only` proof-layer memory candidates used by bounded proof review | receives reviewed memory read models; emits source refs into candidate evidence, local memo candidates, or bundle-local review | reviewed memory provides recall context; local proof authority stays with the eval bundle or owning mechanic; local `memo/` packets are review material, not proof authority; MCP output remains inspection evidence; durable memory lands only in `aoa-memo` |
| Owner-local statistics | `stats/port.manifest.json` and `stats/packets/*.json` | eval-local statistical questions and source-backed measurement packets | receives facts whose meaning remains with `aoa-evals`; emits a discoverable local port for shared validation and cross-owner composition | `aoa-stats` owns shared grammar and composition; the source eval bundle or owning mechanic keeps proof and verdict meaning |
| MCP access-plane contract | `docs/architecture/AOA_EVALS_MCP_CONTRACT.md` | resources, tools, prompts, owner split, stop-lines, local-port write gates, inspect-only suite execution metadata, and candidate-only runtime evidence posture for `aoa_evals` | receives generated readers, runtime-candidate readers, proof questions, sibling local-port pressure, and v1/v2 inventory packets; emits compact proof/candidate read access plus narrow gated sibling-local note writes for the stack-owned MCP implementation | MCP output remains inspection support; MCP neither writes `.suite.json` nor executes argv; source bundles and manifests keep proof authority; sibling repos own local port files; `abyss-stack` owns runtime service code only |
| Receipts | `mechanics/publication-receipts/parts/receipt-payload/docs/EVAL_RESULT_RECEIPT_GUIDE.md`, `mechanics/publication-receipts/parts/receipt-payload/schemas/eval-result-receipt.schema.json`, `mechanics/publication-receipts/parts/stats-envelope-mirror/schemas/stats-event-envelope.schema.json`, `mechanics/publication-receipts/parts/receipt-payload/examples/eval_result_receipt.example.json`, `mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json`, `.aoa/live_receipts/` | publication facts for one bounded eval result and non-publishing receipt-intake review | receive reviewed report facts; emit sidecar records for downstream readers or dry-review payload previews | reports and bundle-local sources remain the stronger route for verdict meaning |
| Release publication | `docs/operations/RELEASING.md`, `CHANGELOG.md`, `scripts/release_check.py`, `scripts/validate_abyss_machine_report_index_bundle.py`, `.github/workflows/repo-validation.yml`, `mechanics/release-support/parts/artifact-bundles/manifests/report_index.bundle.json`, `mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json`, `mechanics/release-support/parts/strategic-closeout/reports/strategic-closeout-audit-v1.json`, `mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json`, Git tags and GitHub release notes | bounded release scope, public release narrative, release audit route, OS Abyss report-index artifact bundle identity/provenance, readiness review, strategic handoff, and landing gate posture | receives changed proof surfaces, generated checks, and `abyss-machine` artifact policy verification; emits readiness audit, strategic closeout, release-prep handoff, tag, and release notes | source bundles keep eval-claim strength; generated report-index bundle validation proves the release carrier, not proof meaning |
| Quest obligations | `QUESTBOOK.md`, `quests/`, `mechanics/questbook/parts/source-record-contract/`, `mechanics/questbook/parts/dispatch-reader/`, generated quest catalog and dispatch | deferred proof, regression, and verdict-bridge obligations | receive unresolved proof pressure; emit return routes and dispatch hints | quest records carry obligation return routes; eval bundle meaning stays with source proof objects |
| Decisions | `docs/decisions/` | durable rationale for topology, workflow, validation, compatibility, or authority changes | receive reviewed evidence and alternatives; emit why a route was chosen | source truth stays with the source surface; decisions preserve route rationale |
| Agent guidance | `AGENTS.md`, local `AGENTS.md` cards, `DESIGN.AGENTS.md`, `.agents/`, `.agents/spark/` | editing route, local risk, validation, closeout posture | receives topology and source-owner rules; emits bounded operating guidance | source proof surfaces keep verdict meaning; guidance owns edit route and validation |
| Sibling references | dependency refs and evidence refs into sibling repositories | cited inputs to local proof review | receive stronger owner truth from sibling repos; emit local proof references | sibling owner retains stronger authority |
| Legacy lineage | old names, old paths, and accepted legacy inputs | provenance, compatibility, and historical routeability | receives historical vocabulary; emits the active owner route and the `PROVENANCE.md` bridge | active topology starts at the current owner route; legacy keeps lineage and the `PROVENANCE.md` bridge |
| Mechanic operations | `mechanics/*` packages | repeatable proof-layer operations with a real owner, inputs, outputs, and validation | receive recurring operations from root districts or part-local payloads; emit package-local route cards and validators | package topology is backed by owned operation, inputs, outputs, and validation |

## Root Technical Districts

Root districts remain valid after mechanics movement when their owner route,
provenance posture, and drift validator are visible. Use these companion routes
before any additional root path becomes mechanic-owned payload:

| Companion route | Owner | Use |
| --- | --- | --- |
| `mechanics/EVIDENCE_CLUSTERS.md` | mechanics evidence gate | Root District Reconnaissance Ledger, residual root-authored surface classification for every unclassified root-authored surface, mechanic-owned payload routes, and validation guards |
| `docs/architecture/AGENT_INDEX.md` | agent-facing pass-through reader | path name -> authority class -> stronger owner surface |
| nearest `AGENTS.md` | route law | editing law, command lane, validation posture, and closeout route |
| source eval package or mechanic part | stronger owner surface | bundle meaning, payload ownership, part-local contracts, and proof interpretation |

| District | Current role | Current posture |
| --- | --- | --- |
| `evals/` | source proof object district | stays root-owned; active package routes point back to bundle source meaning |
| `docs/` | source guidance, topology maps, decisions, and repo-wide guides | stays root technical district unless a live mechanic owns the narrower operation; recurrence proof-program guidance now routes through `mechanics/recurrence/`, and orchestrator proof-anchor alignment now routes through `mechanics/boundary-bridge/parts/orchestrator-proof-anchors/` |
| `generated/` | deterministic repo-wide derived readers | stays generated-only for repo-wide readers; package-owned generated readers may live under their mechanic part and still rebuild through builders; the Phase Alpha eval matrix now lives under `mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/generated/` |
| `kag/` | compact local KAG provider records | stays root technical district for portable provider records over eval report index and owner-return routes; records route to `aoa-kag` validation and MCP consumers while eval bundles and generated readers keep proof meaning |
| `examples/` | compatibility route card for former root public-safe examples | active examples payloads route to bundle-local `evals/**/examples/` or package-owned candidate packets, hooks, bridge source plans, receipts, and mechanic examples under their owning mechanic parts |
| `fixtures/`, `runners/`, `scorers/`, `schemas/`, `templates/` | shared proof infrastructure and compatibility route cards | root `fixtures/`, `runners/`, `scorers/`, `schemas/`, and `templates/` are now compatibility route cards where their active payloads have narrower owners; generic active fixture families live under `mechanics/proof-infra/parts/fixture-families/fixtures/`; reportable runner/scorer/schema contracts live under `mechanics/proof-infra/parts/reportable-contracts/`; package-owned fixture families, schemas, builders, templates, or validation helpers may live under mechanic parts; quest source and dispatch schemas now live under `mechanics/questbook/parts/`; eval frontmatter/manifest schemas and `EVAL.template.md` now live under `mechanics/proof-object/parts/` |
| `reports/` | compatibility route card for former root shared dossiers and reports | active root reports payload routes require a topology decision and validator allowlist update; bundle-local reports stay under `evals/**/reports/`, and package-owned proof-loop, comparison, receipt, and release-support reports live under their mechanic parts |
| `tests/` | repo-wide validator, catalog, generated-reader, and semantic route-card tests | stays root-owned for repository-wide checks; part-owned tests live under `mechanics/<mechanic>/parts/<part>/tests/` next to the active operation they constrain |
| `quests/` | lane/state schema-backed source quest records | uses `quests/<lane>/<state>/` YAML paths; generated quest readers must mirror current source paths; former markdown quest-note lineage belongs behind the owning mechanic `PROVENANCE.md` |
| `memo/` | proof-layer local memory port | holds `write_candidate_only` candidates, receipts, exports, local notes, and generated local port indexes before any reviewed `aoa-memo` landing; it is not proof authority, durable memory, or eval verdict support |
| `stats/` | owner-local statistics port | holds the port manifest and source-backed measurement packets whose local meaning stays with `aoa-evals`; shared grammar, validation, and cross-owner composition stay with `aoa-stats` |
| `config/` and `manifests/` | compatibility and provenance route for former root recurrence and seed configuration surfaces | active root config or manifest payload routes require a topology decision; Agon-owned configs, latest-sibling canary config, recurrence control-plane manifests, and portable-proof-beacon recurrence manifests with part-local validation now live under their mechanic parts |
| `skills/` | owner-admitted repo-specific callable procedures | currently absent; may appear only after manual trigger, ABI, composition, coexistence, and no-skill evidence plus an owner decision; shared workflows remain with `aoa-skills` |
| `.agents/` | maintained agent lanes | durable agent-facing district; proof canon stays with source proof objects |
| `.agents/spark/` | maintained Spark fast-loop lane | routes narrow proof-surface work; source proof objects keep proof meaning |
| `.aoa/live_receipts/` | owner-local live receipt log | receipt sidecar route; verdict meaning stays with reviewed reports and source bundles |
| `mechanics/` | operation atlas for repeatable proof-layer operations | active where a package owns a real operation; top-level mechanics parents are validator allowlisted from `mechanics/EVIDENCE_CLUSTERS.md`; parent and part routes are owned by `mechanics/README.md`, parent `README.md`, `DIRECTION.md`, `PARTS.md`, part README, part `VALIDATION.md`, and nearest `AGENTS.md`; part-owned tests live under `mechanics/<mechanic>/parts/<part>/tests/`; parent-level `docs/` is only for explicit mechanic-wide guidance, while part-owned payload docs live under `parts/<part>/docs/` |

Detailed route-residue guard contracts live in
[`ROUTE_RESIDUE_GUARDS.md`](ROUTE_RESIDUE_GUARDS.md). This topology map keeps
the authority classes and the guard family map:

| Guard family | Contract owner | Protects |
| --- | --- | --- |
| generated route residue | `docs/architecture/ROUTE_RESIDUE_GUARDS.md` | derived readers route to current source owners and same part root paths |
| active mechanic route residue | `docs/architecture/ROUTE_RESIDUE_GUARDS.md` | active route cards avoid former legacy parent routes |
| mechanic payload route residue | `docs/architecture/ROUTE_RESIDUE_GUARDS.md` | part-local payload paths resolve under the owning mechanic or part root |
| root authored route residue | `docs/architecture/ROUTE_RESIDUE_GUARDS.md` | root-facing guidance uses source eval, active mechanic, or route-card paths |
| decision route residue | `docs/architecture/ROUTE_RESIDUE_GUARDS.md` | current decision navigation avoids old root payload paths unless marked historical |
| repo config route residue | `docs/architecture/ROUTE_RESIDUE_GUARDS.md` | executable routes point at active owners |
| source bundle route residue | `docs/architecture/ROUTE_RESIDUE_GUARDS.md` | bundle-local paths stay under their bundle and sibling refs stay repo-qualified |

## Mechanic Readiness

A new `mechanics/` parent is ready only when the operation has all of these:

- one recurring proof-layer operation;
- source artifacts it can route while source owners keep authority;
- clear inputs and outputs;
- a stronger-owner or sibling-owner split when applicable;
- legacy or accepted-input posture if old names remain;
- local `AGENTS.md` guidance or package card shape;
- parent `DIRECTION.md` for current operating direction;
- at least one validator, builder, or review check that constrains the route.

Use `mechanics/EVIDENCE_CLUSTERS.md` as the parent evidence gate before
creating or renaming a parent. The topology map needs only the gate shape; the
ledger detail lives in mechanics:

| Evidence gate | Lives in | Topology use |
| --- | --- | --- |
| Active Parent Evidence Dimension Ledger | `mechanics/EVIDENCE_CLUSTERS.md` | keeps every parent tied to meaning/doctrine, proof pressure, contracts/payloads, builders/readouts, quest/deferred pressure, owner split and stop-lines, and legacy/provenance |
| Active Parent Evidence Route Refs | `mechanics/EVIDENCE_CLUSTERS.md` | keeps every parent tied to concrete local route refs, including at least one living non-mechanics evidence route in addition to validator and rationale refs |
| Root District Reconnaissance Ledger | `mechanics/EVIDENCE_CLUSTERS.md` | keeps root districts visible as source, derived, route-card-only, repo-wide validation, or mechanic-owned payload routes before another root path becomes mechanic-owned payload |
| Residual Root-authored Surface Classification | `mechanics/EVIDENCE_CLUSTERS.md` | keeps remaining top-level `docs/`, `scripts/`, and `tests/` files classified as root-owned surfaces so an unclassified root-authored surface cannot drift into hidden mechanic payload |

The parent-class split is validator-backed. AoA-aligned parents keep the named
AoA mechanic form; evals-native parents name proof-organ operations that belong
to `aoa-evals` itself. `titan` is the owner-named evals-native case: the local
operation is seed-boundary proof, while `aoa-agents` keeps Titan role, bearer,
summon, and incarnation law. Concrete wrong-parent mappings live in
`mechanics/EVIDENCE_CLUSTERS.md`, not in the legacy posture guide.

Active mechanic packages:

- `proof-object`
- `proof-loop`
- `comparison-spine`
- `proof-infra`
- `publication-receipts`
- `release-support`
- `titan`
- `agon`
- `recurrence`
- `checkpoint`
- `experience`
- `antifragility`
- `method-growth`
- `rpg`
- `growth-cycle`
- `distillation`
- `questbook`
- `audit`
- `boundary-bridge`

No remaining named candidate family is promoted by symmetry in this slice. The
mechanics atlas names active packages, but package-specific activations,
deferred stages, part contracts, payload homes, and validation routes belong in
`mechanics/README.md`, parent route cards, `PARTS.md`, part READMEs, and
`mechanics/EVIDENCE_CLUSTERS.md`.

## Legacy and Naming

Active names should describe the living proof operation.

Legacy names remain useful only as provenance, accepted-input, generated
projection, or candidate-only vocabulary behind a current active owner.

Each accepted legacy name needs an active owner route before it can influence
new work. The archive may preserve more history, but active topology should
not repeat that archive inventory.

Use `docs/architecture/LEGACY_NAMING.md` as a thin posture guide for naming posture and
provenance routing. It separates `active`, `historical`, `accepted-input`,
`generated-projection`, `candidate-only`, and `provenance-bridge` names, then
routes old names through current active routes and package `PROVENANCE.md`.
Each mechanic `PROVENANCE.md` is the active-to-archive bridge for its mechanic.

Use active surfaces first: parent `README.md`, `DIRECTION.md`, `PARTS.md`, and
part-local `parts/` contracts. `PROVENANCE.md` is the single controlled bridge
from active mechanic surfaces into the legacy archive; archive details belong
inside legacy, not in active mechanic route cards or root guidance.
Concrete archive contents and old-name inventories belong inside the owning
legacy archive after the bridge. Active topology surfaces may name only the
current owner, posture, and stop-line needed to prevent old names from steering
new work.

## Runtime and Machine Intake

Runtime, trace, machine, and stack artifacts enter the topology as candidate
evidence:

`machine or runtime evidence packet -> runtime candidate -> bundle-local review -> bounded report -> optional receipt`

This route keeps `aoa-evals` self-contained while allowing host or runtime
facts to support bounded proof. The proof owner still accepts or rejects the
interpretation through a source proof object and review surface.

## Use by Future Agents

Before moving a file, creating a mechanic, changing a generated reader, or
strengthening a runtime or receipt seam, answer:

- which authority class owns this surface now?
- which class should own it after the change?
- what source surface remains stronger?
- what generated, candidate, receipt, sibling, or legacy surface stays weaker?
- what validator or builder will notice drift?

Unclear answers route back to topology clarification before file movement.

## Validation

Executable checks that keep this topology visible live in
[docs/AGENTS.md#validation](../AGENTS.md#validation) and root
[AGENTS.md#verify](../../AGENTS.md#verify).

When generated readers change, run the owning builder in `--check` mode. When a
mechanic package is later introduced, add package-shape checks only after that
package owns a real operation.
