# Roadmap

## Role

`ROADMAP.md` is the active direction surface for `aoa-evals`.

It is not the changelog, questbook, architecture reference, design form,
decision log, or generated catalog. It names where the bounded proof organ is
trying to go next and which phase gates make that movement honest.

Detailed release history stays in [CHANGELOG.md](CHANGELOG.md).
Durable rationale stays in [docs/decisions/](docs/decisions/).
Deferred obligations stay in [QUESTBOOK.md](QUESTBOOK.md) and `quests/`.
Eval meaning stays in `bundles/*/EVAL.md` and `bundles/*/eval.yaml`.

## Current Posture

`aoa-evals` has moved beyond public bootstrap. The repository already carries
36 eval bundles plus generated readers, runtime-candidate templates, trace and
receipt bridges, phase-alpha matrices, Agon alignment surfaces, and public-safe
proof references into sibling owners.

The next work is not to add more bundles quickly.

The next work is to make the proof organ easier to enter, harder to overread,
and safer to refactor:

- root design spine is now present in `DESIGN.md` and `DESIGN.AGENTS.md`;
- `docs/ARCHITECTURE.md` now stays technical: it describes proof bundles,
  mechanics as operation support, and legacy bridge layering without replacing
  `DESIGN.md`, `docs/PROOF_TOPOLOGY.md`, or
  `mechanics/EVIDENCE_CLUSTERS.md`; `scripts/validate_repo.py` now guards that
  Architecture proof-model contract.
- decision memory is present in `docs/decisions/`;
- sibling proof references have been repaired against the current `aoa-memo`
  topology;
- `ROADMAP.md`, `QUESTBOOK.md`, and `quests/` hold separate routeable roles;
- mechanics movement has begun only where a package owns a real operation,
  part-local topology, and validation route.
- the mechanics evidence map now has an Active Parent Evidence Dimension Ledger,
  so every active parent is tied to visible meaning/doctrine, proof
  pressure, contracts/payloads, builders/readouts, quest/deferred pressure,
  owner split and stop-lines, and legacy/provenance rather than only a name
  allowlist.
- Mechanic Evidence Route Refs now make those parent rows auditable through
  concrete route refs: every active parent must point at an active parent
  route and at least one living non-mechanics evidence route ref that resolves
  in the current worktree, while generic root validator files and
  rationale-only decision refs cannot stand in as parent evidence.
- mechanic-payload route residue is now guarded for active mechanics payload:
  fixtures, schemas, manifests, scripts, tests, and hook bindings must use
  part-local paths, active repo paths, repo-qualified sibling refs, or root
  route cards instead of stale root payload routes.
- mechanic parent direction is now explicit: every active parent mechanic has
  `DIRECTION.md` for current operating direction, source-of-truth split,
  growth rule, stop-lines, and validation, while `README.md`, `PARTS.md`,
  `PROVENANCE.md`, and part-local contracts keep their separate jobs; parent
  `README.md` and `AGENTS.md` route `DIRECTION.md` from their Entry Route so
  future edits encounter active direction before part growth or legacy lookup.
- parent-level `docs/` under mechanics is now guarded as explicit
  mechanic-wide guidance only; part-owned payload docs must live under the
  owning `parts/<part>/docs/` route, allowlisted parent guidance must expose
  role, mechanic-wide scope, source surfaces, stronger owner split, stop-lines,
  and validation, and Titan canary guides now sit under
  `mechanics/titan/parts/seed-boundary/docs/`.
- `recurrence` is active for control-plane integrity, anchor-return,
  memory-recall, recursor-boundary, stats-regrounding boundary support, and
  portable-proof beacons; continuity-anchor and self-reanchor remain
  bundle-local until their support artifacts prove active parts.
- `antifragility` is now active only for the proven posture, stress-window, and
  repair-proof support route; diagnosis-gate pressure now routes through
  `growth-cycle`, while broader repair-cycle growth claims remain deferred.
- `method-growth` is now active for the proven candidate-lineage and
  owner-landing support route; diagnosis, repair, and non-distillation growth
  pressure remains outside that parent until separate evidence passes prove
  those routes.
- `rpg` is now active for the proven progression-unlocks support route;
  diagnosis, repair, harvest, closeout, and longitudinal growth pressure
  remain outside that parent; only diagnosis-gate has moved into
  `growth-cycle` in this slice.
- `distillation` is now active for the proven compost-provenance and reviewed
  runtime distillation candidate adoption support route; memo recall routes
  through `recurrence/memory-recall`, while memo contradiction, confirmed
  writeback-act proof, witness trace integrity, audit hook metadata, and
  generic Experience adoption remain outside that parent.
- Distillation parts now expose local contracts directly; validator coverage
  keeps compost-provenance and runtime-candidate-adoption below ToS canon,
  memory canon, runtime promotion, receipt publication, Experience adoption,
  KAG lift, bridge-ready truth, owner acceptance, and generic artifact-quality
  or live memory-ledger claims.
- Proof-object bundle-authoring and bundle-contracts now expose stronger-owner
  splits directly; validator coverage keeps templates and schemas below source
  bundle meaning, bundle-local review, evidence acceptance, generated readers,
  receipts, runtime candidates, sibling refs, quests, and release readiness.
- Questbook source-record-contract and dispatch-reader now expose
  stronger-owner splits directly; validator coverage keeps source quest truth,
  human `QUESTBOOK.md` visibility, generated quest navigation, later proof
  verdicts, owner acceptance, harvest triage, live task assignment, and
  proof-surface promotion separated.
- `growth-cycle` is now active only for the proven diagnosis-gate support
  route; repair stays under `antifragility`, longitudinal movement under
  `comparison-spine`, RPG progression under `rpg`, and closeout or harvest
  pressure remains deferred until separate evidence proves active parts.
- growth-cycle diagnosis-gate now exposes its local contract directly;
  validator coverage keeps diagnosis-cause discipline below repair success,
  owner-fit proof, final object quality, broad growth score, closeout
  acceptance, donor harvest approval, quest promotion, memory canon, runtime
  activation, and owner-local landing.
- Method-growth candidate-lineage and owner-landing now expose stronger-owner
  splits directly; validator coverage keeps lineage proof separate from
  owner-fit routing proof and keeps both below final object quality,
  owner-local acceptance, hidden promotion, derivative first-authoring, seed
  truth, memory canon, and universal growth scores.
- recurrence control-plane-integrity now exposes its local contract directly
  and names current part-local payload homes; validator coverage keeps
  recurrence dossiers below runtime status, promotion readiness, downstream
  projection truth, owner review acceptance, Agon source truth, beacon verdict
  authority, hidden continuity, and portable-proof acceptance by manifest.
- RPG progression-unlocks now exposes its local contract directly; validator
  coverage keeps progression evidence and unlock cards below quest acceptance,
  universal rank, role/skill/technique/playbook authority, runtime equip state,
  generated-card authority, and growth-cycle diagnosis or longitudinal
  movement claims.
- `proof-infra` now owns generic shared fixture-family support through
  `mechanics/proof-infra/parts/fixture-families/` and shared reportable
  runner/scorer/schema contracts through
  `mechanics/proof-infra/parts/reportable-contracts/`; root `fixtures/`,
  `runners/`, `scorers/`, and `schemas/` are compatibility route cards, while
  bundle-local contracts and source proof bundles remain stronger.
- Every active mechanic parent now has a validator-backed legacy/provenance
  skeleton: `PROVENANCE.md` as the active-side bridge and a package-local
  `legacy/` archive behind it. This keeps legacy as lineage behind the active
  route instead of a trash folder or new-work entrypoint.
- Legacy route cards are now active-first: every `mechanics/*/legacy/README.md`
  points back through `../PROVENANCE.md`, and validator coverage keeps archive
  accounting inside legacy instead of active routes.
- `docs/LEGACY_NAMING.md` now acts as a thin legacy naming posture guide:
  old names route through current active routes and package `PROVENANCE.md`;
  archive details stay inside the owning `legacy/` archive.
- Mechanic Provenance Bridge Posture now requires every mechanic
  `PROVENANCE.md` to say it is a bridge, not an active route, and to route
  readers through `README.md`, `DIRECTION.md`, `PARTS.md`, and `parts/` before
  archive lookup.
- Legacy Naming Single-Bridge Language now keeps `docs/LEGACY_NAMING.md`
  consistent with that route: old names enter through package `PROVENANCE.md`
  as the single controlled bridge from active mechanic surfaces, while
  archive detail stays inside the owning `legacy/` archive.
- Legacy Naming Posture Guide now keeps `docs/LEGACY_NAMING.md` thin: posture
  and active-route discipline only, not a global archive map. It no longer
  carries concrete old-name inventories, active parent allowlists,
  wrong-parent maps, or old agent-lane path routing; those belong to active
  topology/evidence surfaces or inside owning `legacy/` archives after
  `PROVENANCE.md`.
- Compatibility root route cards now follow the same single-bridge rule:
  old root path lineage routes to the owning mechanic `PROVENANCE.md`, while
  archive-internal index and accounting surfaces stay inside `legacy/`.
- Legacy archive accounting stays inside `legacy/`; active surfaces name only
  the current owner route and `PROVENANCE.md` bridge, so provenance cannot
  become a second active route.
- Active Legacy Parent Wording Boundary now keeps active route wording from
  re-promoting legacy parent forms. Runtime evidence remains audit-owned
  evidence class and schema vocabulary, not a `runtime-evidence` parent or
  boundary-bridge/recurrence owner.
- Mechanics parent class membership is now validator-backed: AoA-aligned and
  evals-native parent sets must stay disjoint, cover the allowlist, and remain
  present in `mechanics/EVIDENCE_CLUSTERS.md`; wrong parent forms such as
  `agon-proof`, `titan-canaries`, `proof-release`, `runtime-evidence`,
  `sibling-proof-refs`, and `repair` stay out of active topology.
- comparison-spine parts now expose local contracts directly; validator
  coverage keeps spine overview, fixed baseline, peer compare, and
  longitudinal windows as comparison-support parts rather than generated truth,
  broad growth proof, repo-global scoring, or bundle promotion.
- root route-card-only districts now have an explicit guard: `config/`,
  `examples/`, `fixtures/`, `manifests/`, `reports/`, `runners/`, `schemas/`,
  `scorers/`, and `templates/` may not silently regain active payload files or
  stray payload directories without a topology decision and validator allowlist
  update.
- `mechanics/EVIDENCE_CLUSTERS.md` now carries a Root District Reconnaissance Ledger
  for the goal-listed root-district set plus current proof-infra route-card
  roots: `docs`, `bundles`,
  `fixtures`, `schemas`, `examples`, `scripts`, `tests`, `config`,
  `manifests`, `generated`, `reports`, `runners`, `scorers`, `templates`,
  `quests`, and `mechanics`; it records root posture, route-card-only
  boundaries, mechanic-owned payload routes, and validation guards before more
  mechanic movement begins.
- `mechanics/EVIDENCE_CLUSTERS.md` now also carries a Residual Root-authored Surface Classification
  ledger for top-level `docs/`,
  `scripts/`, and `tests/` files, so root-owned guides, builders, validators,
  and tests stay explicit while mechanic-owned payload drift is rejected.
- generated/readout route residue now has an explicit guard: root generated
  readers cannot preserve former wrong mechanic parents or route-card-only root
  district paths as structured active references, while part-local generated
  readers may still use local sibling paths that resolve inside the same part.
- active mechanic route residue now has an explicit guard: authored route cards
  cannot preserve former wrong mechanic parent paths or root payload paths as
  active navigation, while same-part local paths and root route cards remain
  valid.
- root-authored route residue now has an explicit guard: root-facing authored surfaces
  cannot preserve route-card-only root payload paths as current
  guidance, while historical context and root route cards remain valid.
- decision-route residue now has an explicit guard: decision records can
  preserve former root payload paths only with historical context, while
  current-looking routes must point at active mechanics,
  `bundles/<bundle>/...`, or root route cards.
- repo-config route residue now has an explicit guard: `.gitignore`,
  `pytest.ini`, and workflows cannot preserve former mechanic parent routes or
  route-card-only root payload paths as executable routing.
- source-bundle route residue now has an explicit guard: source proof bundles
  cannot carry ambiguous route-card-only root payload paths or former mechanic
  parent routes, while bundle-local paths, `bundles/<target>/...`, and
  repo-qualified sibling refs remain valid.
- top-level mechanics parents now have an explicit allowlist from
  `mechanics/EVIDENCE_CLUSTERS.md`; new parent packages must prove an
  AoA-aligned or evals-native cross-root cluster before becoming active
  topology, and every allowed parent must keep `AGENTS.md`, `README.md`,
  `PARTS.md`, and part-contract wording current.
- concrete mechanic parts now have a generic README contract: each active
  `mechanics/<parent>/parts/<part>/README.md` must expose inputs, outputs,
  stronger owner split, stop-lines, validation, and a parent `PARTS.md` route
  by README path or exact part slug.
- Mechanic Part Payload Inventory now guards the next layer below the part
  README: every actual payload subdirectory under a mechanic part must be
  named by that part README, while empty payload directories, unexpected
  payload classes, and unexpected part-root files are rejected.
- The same inventory guard now rejects unexplained thin parts: a part with no
  payload subdirectories must declare a bundle-backed thin support route and
  explain that the source proof bundle stays under `bundles/`.
- Mechanic Part Source Surface Reference Guard now keeps part `Source Surfaces`
  reachable: every path-like source-surface ref must resolve as a
  repo-relative path, matching glob, repo-qualified sibling ref, or placeholder
  route, so a stale source surface ref cannot survive a mechanics move.
- Mechanic Part Source Surfaces Section Contract now makes the source entry
  shape explicit: every concrete part README must use the plural section
  `## Source Surfaces` with at least one path-like source ref, so `Role`,
  singular source-surface, or active-surface lists cannot bypass the guard.
- Mechanic Part Validation Command Reachability now guards the part validation
  route itself: every concrete part README must carry at least one python
  command whose referenced path is repo-relative and reachable, while
  payload-bearing parts must also carry a payload coverage anchor, so a stale
  validation path or naked route-wide command cannot survive a mechanics move.
- Mechanic PARTS Index Synchronization now guards the parent part map: every
  actual part directory must be declared as a local route in its parent
  `PARTS.md`, stale local part routes are rejected, and cross-parent references
  remain allowed as stop-lines or handoff routes instead of local topology.
- Mechanic Parent Guidance Boundary now guards parent-level mechanic docs:
  `mechanics/<parent>/docs/` is allowed only for explicit mechanic-wide
  guidance, while part-owned payload docs must stay below the owning
  `parts/<part>/docs/` route.
- Mechanic Legacy Single Bridge now guards active package surfaces: active
  route cards, part maps, directions, docs, part READMEs, JSON/YAML manifests,
  hooks, and part-local helpers may point to `PROVENANCE.md` as the single
  controlled bridge from active mechanic surfaces, while archive internals
  remain inside legacy.
- mechanic provenance entries now have a generic contract: each active
  `PROVENANCE.md` must name the active route first and then open the legacy
  archive without making it an active route.
- `audit` and `release-support` now have explicit provenance bridges for the
  old `runtime-evidence` and `proof-release` parent forms; those names remain
  lineage and accepted vocabulary where needed, not active parent topology.
- `proof-loop` and `publication-receipts` now have explicit provenance bridges
  for moved root report, receipt guide, schema, example, publisher, test, and
  dry-review paths; those old paths are lookup lineage, not active placement.
- proof-loop route-smoke now exposes its local part contract directly;
  validator coverage keeps the first route-smoke report as routeability
  evidence rather than eval-result run, receipt publication, bundle promotion,
  runtime intake, sibling approval, or full proof-loop completeness.
- antifragility parts now expose local contracts directly; validator coverage
  keeps posture review, stress-recovery windows, and repair proof as bounded
  antifragility evidence rather than global resilience, live self-healing,
  permanent stability, repair-parent topology, or growth-cycle completion.
- checkpoint parts now expose local contracts directly and name current
  part-local payload homes; validator coverage keeps A2A summon return,
  restartable inquiry, and self-agent checkpoint posture below implementation,
  memory canon, runtime activation, owner acceptance, and broad long-horizon
  competence claims.
- Experience parts now expose local contracts directly; validator coverage
  keeps protocol integrity, certification gate, adoption federation,
  governance/runtime-boundary, and office release-train verdict support below
  live runtime, certification, adoption, governance, memory, routing, KAG, ToS,
  office, release, deployment, and broad Experience-success authority.
- publication receipt parts now expose local contracts directly; validator
  coverage keeps receipt payload, stats envelope mirror, live publisher, and
  intake dry-review as parts of `publication-receipts`, with reports and
  bundles remaining stronger than receipts.
- release-support parts now expose local contracts directly; validator coverage
  keeps readiness-audit, strategic-closeout, and pr-handoff as local
  release-support artifacts rather than release publication, GitHub status, tag
  authority, or goal completion.
- every active mechanic parent now has a package-local legacy archive behind
  `PROVENANCE.md`, so raw legacy cannot become an unbounded active work area.
- audit parts now expose part-level contracts directly and validator coverage
  keeps selected evidence, artifact hooks, candidate readers, and integrity
  review candidate-only.
- Agon parts now expose part-level contracts directly; validator coverage keeps
  court prebinding, CCS, VDS, mechanical-trial suites, retention/rank,
  epistemic, SLC, KAG, and Sophian threshold pressure inside the `agon` parent
  instead of letting future growth split into invented proof-suffix mechanics.
- Titan seed-boundary now exposes its part-level contract directly; validator
  coverage keeps `titan*.yaml` canaries as seed-boundary artifacts inside the
  `titan` parent instead of letting the canary form become active topology.
- Boundary Bridge parts now expose local contracts for compatibility-map,
  latest-sibling-canary, and orchestrator-proof-anchors; validator coverage
  keeps sibling refs, canary output, and class-facing proof anchors as bridge
  evidence rather than sibling-owner authority.
- `boundary-bridge` now owns orchestrator proof anchors through
  `mechanics/boundary-bridge/parts/orchestrator-proof-anchors/`; the anchors
  keep quest proof obligations tied to `aoa-agents` class refs without creating
  an `orchestrator` parent mechanic or importing sibling identity.

## Current release contour

The current public release contour remains `v0.3.3`.

This is not a claim that `aoa-evals` owns runtime truth, memory truth, role
policy, or broad autonomy proof. Roadmap drift is an eval-layer risk: if this
file forgets the current proof contour, readers may over- or under-read the
boundary. The repository proves only bounded claims.

Current contour surfaces that must remain visible while the roadmap is being
refactored:

- `bundles/aoa-continuity-anchor-integrity/EVAL.md`
- `bundles/aoa-reflective-revision-boundedness/EVAL.md`
- `bundles/aoa-self-reanchor-correctness/EVAL.md`
- `bundles/aoa-candidate-lineage-integrity/EVAL.md`
- `bundles/aoa-owner-fit-routing-quality/EVAL.md`
- `bundles/aoa-diagnosis-cause-discipline/EVAL.md`
- `bundles/aoa-repair-boundedness/EVAL.md`
- `generated/eval_catalog.min.json`
- `generated/eval_capsules.json`
- `generated/eval_sections.full.json`
- `mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json`
- `mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json`
- `generated/eval_report_index.min.json`
- `mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/generated/phase_alpha_eval_matrix.min.json`
- `mechanics/rpg/parts/progression-unlocks/docs/PROGRESSION_EVIDENCE_MODEL.md`
- `mechanics/checkpoint/parts/self-agent-posture/docs/SELF_AGENT_CHECKPOINT_EVAL_POSTURE.md`
- `mechanics/recurrence/docs/RECURRENCE_PROOF_PROGRAM.md`
- `mechanics/recurrence/parts/portable-proof-beacons/manifests/recurrence/component.evals.portable-proof-beacons.json`
- `mechanics/antifragility/README.md`
- `mechanics/method-growth/README.md`
- `mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md`
- `mechanics/publication-receipts/parts/receipt-payload/docs/EVAL_RESULT_RECEIPT_GUIDE.md`
- `mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md`
- `mechanics/boundary-bridge/parts/orchestrator-proof-anchors/docs/ORCHESTRATOR_PROOF_ALIGNMENT.md`

Memo-pilot proof surfaces keep future scar and retention language bounded. They
do not certify live memory-ledger readiness, and they do not turn memo evidence
into proof authority.

## Directional Invariants

- `aoa-evals` owns bounded proof meaning, not skill execution, technique canon,
  memory truth, runtime health, routing policy, stats dashboards, role rights,
  playbook scenario authority, or AoA constitutional law.
- Source proof objects remain stronger than generated readers, runtime
  candidates, receipts, and sibling references.
- A proof claim must name claim boundary, object under evaluation, evidence
  substrate, verdict or score logic, baseline or comparison posture, blind
  spots, and interpretation limits.
- Runtime, machine, trace, and sibling artifacts enter as candidate evidence
  until a bundle-local review accepts their bounded interpretation.
- Quests track obligations to return. They do not become eval bundles, roadmap
  direction, or verdict authority.
- Legacy names preserve lineage and accepted inputs; active names should expose
  the living proof operation.

## Active Phases

### Phase 1: Root Proof Spine

Goal: keep repository-level proof identity visible before topology movement.

Current state:

- `DESIGN.md` describes the system form of the bounded proof organ.
- `DESIGN.AGENTS.md` describes the agent-facing guidance form.
- root `AGENTS.md` routes to the design spine and decision lane.
- `scripts/validate_repo.py` checks the root design and decision surfaces during
  full repository validation.

Exit gate:

- root design surfaces stay aligned with `docs/ARCHITECTURE.md` and
  `docs/EVAL_PHILOSOPHY.md`;
- root `AGENTS.md` remains a route card rather than a doctrine warehouse;
- maintained agent lanes route through `.agents/`, with Spark at
  `.agents/spark/`;
- `python scripts/validate_repo.py` stays green.

### Phase 2: Decision Memory

Goal: keep durable reasons separate from evidence, generated readers, runtime
facts, and ordinary edit summaries.

Current state:

- `docs/decisions/README.md` is the current decision index.
- Decisions now cover root design, proof topology, quest routes, mechanics
  parent creation, legacy/provenance posture, route residue guards, part
  contracts, parent-class allowlists, and active-mechanics wording.
- New decision notes are added when a structural, topology, validation,
  workflow, legacy, runtime-candidate, sibling-reference, or agent-route change
  would otherwise be easy to repeat incorrectly.

Maintained work:

- keep each decision weaker than the source surface it explains;
- add decisions for future topology movement only when the route needs durable
  rationale;
- avoid turning decisions into changelog entries, archive maps, or generated
  status reports.

Exit gate:

- every topology or authority change that future agents could misunderstand has
  a concise decision note;
- decision notes explain why, not just what changed;
- decisions do not replace source proof objects or validators.

### Phase 3: Roadmap, Questbook, and Quest Route

Goal: separate direction, obligations, source quest records, and generated quest
readers.

Current state:

- `ROADMAP.md` is this active direction surface.
- `QUESTBOOK.md` is the human tracked surface for open proof obligations.
- `quests/<lane>/<state>/*.yaml` are source quest records for `AOA-EV-Q-*`.
- `quests/LIFECYCLE.md` is the state contract for open-index visibility,
  return posture, promotion posture, and proof-loop defer or handoff endings.
- former `AOE-Q-AGON-*` markdown notes are Agon lineage behind
  `mechanics/agon/PROVENANCE.md`, not active quest lifecycle source records.
- quest source and dispatch schemas live under
  `mechanics/questbook/parts/source-record-contract/` and
  `mechanics/questbook/parts/dispatch-reader/`.
- `generated/quest_catalog.min.json` and `generated/quest_dispatch.min.json`
  are derived read models.

Near-term work:

- add and maintain `quests/README.md` and `quests/AGENTS.md`;
- keep old top-level quest paths as legacy path vocabulary, not active source
  files;
- keep former root quest schema paths as legacy vocabulary behind
  `mechanics/questbook/PROVENANCE.md`;
- keep lane/state paths aligned with source `state` and generated projections;
- keep every schema state covered by `quests/LIFECYCLE.md`;
- keep `QUESTBOOK.md` aligned with active, non-closed quest IDs.

Exit gate:

- a low-context agent can distinguish `ROADMAP.md`, `QUESTBOOK.md`, `quests/`,
  generated quest readers, and eval bundle meaning;
- `python scripts/build_catalog.py --check` proves quest projections are fresh;
- `python scripts/validate_repo.py` proves quest route docs and projections are
  aligned.

### Phase 4: Proof Topology Map

Goal: classify source, derived, candidate, receipt, sibling, legacy, and active
mechanic artifact classes during current work and before further package
movement.

Current state:

- `docs/PROOF_TOPOLOGY.md` maps authority classes and current root technical
  districts.
- `docs/decisions/0005-proof-topology-map.md` records why topology mapping
  preceded the first broad mechanics movement and continues to constrain file
  movement after active mechanics exist.
- `scripts/validate_repo.py` checks that the topology map and decision stay
  discoverable during full repository validation.

Maintained work:

- use the topology map to decide which surfaces stay root technical districts,
  which belong to existing mechanic parts, and which need later
  evidence-backed parent packages or parts;
- preserve public-safe sibling references and legacy aliases as explicit
  compatibility surfaces.

Exit gate:

- no major source/derived/candidate/receipt/legacy confusion remains unnamed;
- every mechanics move names the operation, stronger-owner stop-lines, and
  validator-backed route that made the move safe.

### Phase 5: Mechanics Atlas

Goal: create `mechanics/` only when it routes repeatable proof-layer operations.

Current state:

- `mechanics/README.md` is the active operation atlas.
- `mechanics/proof-object/` is the active package for source proof-object
  completeness, bundle lifecycle posture, generated-reader derivation,
  bundle-local review boundaries, bundle authoring template, and eval
  frontmatter/manifest contracts.
- `mechanics/comparison-spine/` is the active package for fixed-baseline,
  peer-compare, and longitudinal-window semantics, generated comparison
  readers, part-local comparison fixture/report support, and anti-overread
  boundaries.
- `mechanics/proof-infra/` is the active package for shared fixture, runner,
  scorer, schema, report, template, and generated proof-artifact contract
  routing, with generic shared fixture families now under the
  `fixture-families` part, reportable runner/scorer/schema contracts under
  `reportable-contracts`, and root infrastructure districts kept as
  compatibility route cards.
- `mechanics/publication-receipts/` is the active package for optional eval
  result receipts, the local stats envelope mirror, receipt publisher, and
  owner-local live receipt route while keeping reports and bundles stronger.
- `mechanics/release-support/` is the active package for bounded release scope,
  changelog narrative, release audit, GitHub `Repo Validation`, tag/release-note
  posture, and post-release proof boundaries.
- `mechanics/titan/` is the active package for Titan seed canary
  shape, incarnation and summon discipline guides, `mechanics/titan/parts/seed-boundary/seeds/titan*` seeds, and
  validator-backed boundaries without claiming full incarnation proof.
- `mechanics/agon/` is the active package for Agon pre-protocol proof
  alignment: seed configs, generated registries, observe-only recurrence
  components and hooks, quest notes, recurrence-control-plane stop-lines, and
  owner handoffs without granting live verdict authority.
- `mechanics/recurrence/` is the active package for eval-side recurrence proof:
  the recurrence proof program, control-plane integrity support machinery,
  part-local fixture/schema/example/runner/scorer/test/manifest surfaces,
  portable-proof beacon hooks, and return-aware bundle routing without claiming
  global recurrence completeness or portable proof acceptance.
- `mechanics/checkpoint/` is the active package for eval-side checkpoint proof:
  A2A summon return, restartable inquiry, and self-agent posture support
  surfaces, with checkpoint-specific hook examples under checkpoint parts while
  audit keeps hook schema and candidate-reader builders.
- `mechanics/experience/` is the active package for eval-side Experience
  proof: protocol integrity, certification gate, adoption federation,
  governance/runtime-boundary, and office release-train support surfaces while
  source proof bundles and stronger-owner truth stay outside the package.
- `mechanics/antifragility/` is the active package for eval-side Antifragility
  proof: posture review, stress-recovery window, and repair-proof support while
  source proof bundles, comparison readouts, runtime evidence, and diagnosis
  pressure stay with their owning routes.
- `mechanics/method-growth/` is the active package for eval-side Method-growth
  proof: candidate-lineage and owner-landing support while final object truth,
  diagnosis-cause discipline, repair proof, and RPG progression stay outside
  the package.
- `mechanics/rpg/` is the active package for eval-side RPG proof:
  progression-unlocks support while role, skill, technique, playbook, quest,
  runtime, stats, and broad growth truth stay outside the package.
- `mechanics/growth-cycle/` is the active package for eval-side Growth Cycle
  diagnosis proof: `diagnosis-gate` support for
  `aoa-diagnosis-cause-discipline` while repair-cycle, progression-lift,
  reviewed-closeout-chain, donor-harvest, quest-promotion, and
  owner-followthrough remain deferred.
- `mechanics/questbook/` is the first package because the obligation layer
  already has source records, generated projections, route docs, post-session
  harvest boundaries, and validation pressure.
- `mechanics/audit/` is the second live package because runtime
  candidate intake already has examples, schemas, generated readers, builders,
  tests, and a fragile `abyss-stack` authority boundary.
- `mechanics/boundary-bridge/` is the third live package because sibling
  reference drift already happened, was repaired locally, and now has a
  compatibility map plus latest-sibling canary route. It also owns
  orchestrator proof anchors as a part, not as an `orchestrator` parent.
- `docs/LEGACY_NAMING.md` now keeps active, historical, accepted-input,
  generated-projection, candidate-only, and provenance-bridge names visible before
  future package moves, distillation, or removals.
- `docs/decisions/0006-questbook-mechanic-package.md` records why this package
  exists before other candidates.
- `docs/decisions/0007-audit-mechanic-package.md` records why
  runtime evidence gets a proof-side package without gaining verdict authority.
- `docs/decisions/0008-boundary-bridge-mechanic-package.md` records why
  sibling refs get a package without transferring sibling authority.
- `docs/decisions/0010-proof-object-mechanic-package.md` records why the
  proof-object route gets a package while `bundles/` stays in place.
- `docs/decisions/0011-comparison-spine-mechanic-package.md` records why the
  comparison route gets a package while bundles and generated readers stay in
  place.
- `docs/decisions/0040-comparison-spine-fixture-parts.md` records why
  fixed-baseline, peer-compare, and longitudinal-window fixture families now
  live under active comparison-spine parts.
- `docs/decisions/0059-comparison-spine-part-contract-guard.md` records why
  spine-overview, fixed-baseline, peer-compare, and longitudinal-window need
  local contracts before further comparison growth.
- `docs/decisions/0012-proof-infra-mechanic-package.md` records why shared
  proof infrastructure gets a package while the shared directories stay in
  place.
- `docs/decisions/0013-publication-receipts-mechanic-package.md` records why
  publication receipts get a package while the receipt guide, schemas,
  examples, publisher, reports, and owner-local live receipt log stay in place.
- `docs/decisions/0057-publication-receipts-part-contract-guard.md` records why
  receipt payload, stats envelope mirror, live publisher, and intake dry-review
  are contract-bearing parts rather than parent mechanics or proof authority.
- `docs/decisions/0014-release-support-mechanic-package.md` records why release
  proof publication gets a package while release docs, changelog, release
  checks, GitHub workflow files, generated surfaces, and source proof bundles
  stay in place.
- `docs/decisions/0058-release-support-part-contract-guard.md` records why
  readiness-audit, strategic-closeout, and pr-handoff are contract-bearing
  parts rather than release, GitHub, tag, or goal completion authority.
- `docs/decisions/0015-titan-mechanic-package.md` records why Titan
  canaries get a package-local seed home and stay seed-defined.
- `docs/decisions/0016-agon-mechanic-package.md` records why Agon
  proof-alignment artifacts move into part-local mechanic homes while quest
  notes and recurrence proof bundles stay with their owning routes.
- `docs/decisions/0031-recurrence-mechanic-package.md` records why recurrence
  control-plane support surfaces moved into `mechanics/recurrence/` while
  source proof bundles and stronger-owner truth stay outside the package.
- `docs/decisions/0032-checkpoint-mechanic-package.md` records why checkpoint
  support surfaces moved into `mechanics/checkpoint/` while source proof
  bundles, audit hook schema, and stronger-owner truth stay outside the
  package.
- `docs/decisions/0033-experience-mechanic-package.md` records why Experience
  support surfaces moved into `mechanics/experience/` while source proof
  bundles and stronger-owner truth stay outside the package.
- `docs/decisions/0034-antifragility-mechanic-package.md` records why
  Antifragility support surfaces moved into `mechanics/antifragility/` while
  diagnosis/growth-cycle pressure stays outside the package.
- `docs/decisions/0035-method-growth-mechanic-package.md` records why
  Method-growth support surfaces moved into `mechanics/method-growth/` while
  diagnosis, repair, and progression pressure stay outside the package.
- `docs/decisions/0036-rpg-mechanic-package.md` records why progression and
  unlock support moved into `mechanics/rpg/` while growth-cycle pressure stays
  outside the package.
- `docs/decisions/0037-growth-cycle-mechanic-package.md` records why Growth
  Cycle activates only `diagnosis-gate` in this slice while other center stages
  stay deferred.

No additional candidate package is promoted here until the source family shows
a narrower operation, part split, owner split, stop-lines, and validator
pressure.

Exit gate:

- no empty package taxonomy;
- every package names owned operation, inputs, outputs, stronger owner split,
  must-not-claim boundaries, validation, and closeout.

### Phase 6: Legacy and Naming Containment

Goal: keep old names traceable without letting them steer active topology.

Current state:

- `docs/LEGACY_NAMING.md` is now a thin posture guide for old and overloaded
  names. It names posture and active-route discipline without carrying archive
  detail.
- `docs/decisions/0009-legacy-naming-containment.md` records why external
  legacy wording stays thin: active route first, then `PROVENANCE.md`, with
  archive detail explained only inside the owning `legacy/` archive.
- `scripts/validate_repo.py` checks that the posture guide and decisions stay
  discoverable and do not become a second legacy route.

Near-term work:

- preserve Agon, wave, phase-alpha, runtime-candidate, bundle-family, and old
  Spark root-path names when they are source history or accepted external
  inputs;
- route old names through active package surfaces and package `PROVENANCE.md`
  when archive context is needed;
- use quiet active names for current proof operations.
- keep package-local archive accounting inside `legacy/`; when an active source
  route changes, update the active owner first and then adjust archive
  accounting from inside that package.

Exit gate:

- a future reader can tell whether a name is active topology, historical
  lineage, accepted input, or generated projection.

### Phase 7: Validation as Meaning Protection

Goal: constrain stable proof invariants rather than file presence alone.

Near-term work:

- root design and decision checks;
- quest route checks;
- sibling-reference compatibility checks;
- generated derivation checks;
- runtime-candidate and receipt subordination checks;
- later mechanics package shape checks.

Exit gate:

- each validator can name the invariant it protects;
- green validation means more than "the files exist".

### Phase 8: Active Proof Loop

Goal: make the repository actively usable for bounded proof work without
requiring machine, stack, or sibling authority.

Target route:

`pick proof question -> inspect source bundle -> expand fixture/report contract -> select candidate evidence -> review against bundle -> publish bounded report -> emit optional receipt`

Exit gate:

- this route can be followed locally from `aoa-evals`;
- receipts, runtime candidates, generated summaries, and sibling refs remain
  subordinate to bundle-local review.
- `mechanics/proof-loop/` routes the active proof loop without becoming proof
  authority over the packages that own each step.
- `mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md` records the first public-safe
  local route-smoke: a selected `aoa-verification-honesty` path that ends in a
  bounded report only, with no eval result receipt and no bundle promotion.
- `docs/decisions/0060-proof-loop-route-smoke-contract.md` records why the
  route-smoke part carries its own local contract while remaining routeability
  evidence only.
- `bundles/aoa-verification-honesty/reports/aoa-evals-slice-19-lifecycle-contract.report.json`
  records the first schema-backed bundle-local report for the active proof
  loop, still with no eval result receipt, no bundle promotion, and no quest
  closure.
- `generated/eval_report_index.min.json` routes readers to real bundle-local
  `*.report.json` artifacts while keeping the index below source reports,
  bundles, and receipt publication.
- `mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json` dry-reviews the
  first report-to-receipt intake path by deriving a payload preview while
  keeping `receipt_status` `not_published`, with no envelope, no publisher run,
  and no live receipt append.
- `mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json` records local
  release-support readiness for the accumulated strategic refactor diff while
  keeping tag, GitHub Release, PR approval, GitHub `Repo Validation`, live
  receipt publication, and goal completion explicitly open.
- `mechanics/release-support/parts/strategic-closeout/reports/strategic-closeout-audit-v1.json` records a
  requirement-by-requirement strategic closeout review for the local refactor
  while keeping the long goal not complete until a current objective audit
  proves the mechanics-refactor definition of done and the requested GitHub
  landing route completes: commit, push, PR, GitHub `Repo Validation`, merge,
  fast-forward `main`, and clean worktree.
- `mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json` records the pre-PR owner landing handoff
  snapshot: candidate branch, commit, PR title/body, changed surface
  groups, validation, and landing steps while noting that live git/GitHub state
  supersedes the snapshot after branch or PR creation.

## Current Public Surface

Use [EVAL_INDEX.md](EVAL_INDEX.md) and [EVAL_SELECTION.md](EVAL_SELECTION.md)
for the current public eval map and selection route.

No additional planned starter bundles are currently named publicly.

The current roadmap focus is structural maturity, not bundle-count expansion.

## Verification Posture

After roadmap, questbook, decision, source quest, or generated quest changes,
run:

```bash
python scripts/build_catalog.py --check
python scripts/generate_eval_report_index.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

When builder logic, generated readers, runtime candidates, or broader proof
surfaces change, add the relevant targeted checks and `python -m pytest -q
tests`.
