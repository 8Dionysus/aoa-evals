# Changelog

All notable changes to `aoa-evals` will be documented in this file.

The format is intentionally simple and human-first.
Tracking starts with the community-docs baseline for this repository.

## [Unreleased]

## [0.4.0] - 2026-05-25

### Summary

- releases the accumulated proof-organ refactor from `v0.3.3` through the
  current `main`: 196 first-parent commits, merged PRs #148 through #343,
  1721 changed tracked paths, and the completed move from the old flat
  `bundles/` surface into the source-proof `evals/` tree.
- makes the repository legible as an agent-facing proof canon: root entry,
  authority topology, proof operations, mechanic parents, mechanic parts,
  payloads, generated/readout surfaces, and validation routes now have explicit
  owner paths instead of relying on scattered prose.
- keeps the release narrative below proof authority. This release records the
  route and topology work; source bundle meaning still lives in
  `evals/**/EVAL.md` and `evals/**/eval.yaml`, and mechanics keep their own
  proof-operation boundaries.

### Reconciliation Basis

- checked the release against `git log --first-parent v0.3.3..HEAD`,
  `git diff --name-status v0.3.3..HEAD`, merged GitHub PR metadata, the
  release-support readiness and handoff reports, and the current repository
  route cards instead of trusting this file alone.
- current public proof corpus: 37 source eval bundles under `evals/`.
- current proof-operation topology: 19 active mechanic parents under
  `mechanics/`, with parent route cards, direction surfaces, provenance
  bridges, part indexes, and 90 part or fixture README contracts.
- largest changed surfaces in the release window are `mechanics/`, `evals/`,
  `.agents/`, and `docs/`, matching the intended strategic refactor rather
  than an unrelated code-only release.

### Final Route Sweep

- root entry surfaces now route as a compact proof-organ map:
  `README.md`, `ROADMAP.md`, `DESIGN.md`, `DESIGN.AGENTS.md`,
  `docs/architecture/ARCHITECTURE.md`, `docs/architecture/PROOF_TOPOLOGY.md`, and
  `docs/architecture/AGENT_INDEX.md` point agents toward owner surfaces instead of carrying
  detailed operational ledgers.
- eval-facing guides now use owner routes for selection, review, score
  semantics, blind spots, baseline comparison, repeated windows, fixture
  surfaces, verdict interpretation, portable eval boundaries, proof guides,
  and closeout writeback ingress.
- mechanics closure tightened route language for audit, proof-object,
  antifragility, proof-loop, boundary-bridge, Agon, generated readers,
  readouts, legacy archives, source eval validation, and lower part indexes.
- AGENTS route cards now carry executable validation ownership across root,
  docs, decisions, evals, generated readers, mechanics, scripts, tests,
  GitHub, validator surfaces, and source eval entries.

### Proof Authority And Memory Boundary

- clarified the eval memory-consumer boundary: reviewed `aoa-memo` memory and
  `.aoa` session evidence may provide cited recall context, but proof authority
  stays with eval bundles, selected evidence, reports, mechanics, and validators.
- added validator coverage and a decision note for the route_only memory
  posture so `aoa-evals` does not imply local memo candidate/export authority.
- named the `aoa_memo` MCP access-plane boundary in proof guidance: brief,
  search, status, validation, and landing-plan dry-runs are inspection evidence,
  not proof authority or direct durable memory writes.

### Added

- root design spine for the bounded proof organ:
  `DESIGN.md`, `DESIGN.AGENTS.md`, and route-card links from `AGENTS.md`
- durable decision lane under `docs/decisions/`, including initial decisions
  for root design, proof-object authority, and sibling proof-reference
  compatibility
- quest route surfaces in `quests/README.md` and `quests/AGENTS.md`, plus a
  questbook topology decision
- proof topology map in `docs/architecture/PROOF_TOPOLOGY.md`, plus a decision recording why
  topology mapping precedes mechanics creation and file movement
- mechanics atlas plus the first live `questbook` package for quest source law,
  human open-obligation indexing, generated readers, and deferred promotion
  routing
- questbook `source-record-contract` and `dispatch-reader` parts, moving quest
  schemas behind the active `questbook` mechanic while preserving old root
  schema paths as legacy vocabulary
- questbook part owner-split contract guard, keeping source quest records,
  human `QUESTBOOK.md` visibility, generated quest readers, later proof
  verdicts, owner acceptance, harvest triage, live task assignment, and
  proof-surface promotion in separate authority lanes
- `proof-object` mechanic package for source proof-object completeness,
  bundle lifecycle posture, generated-reader derivation, part-local
  eval-authoring/template and eval-contract/schema support, and
  bundle-local review boundaries without moving `evals/`
- proof-object part owner-split contract guard, keeping eval-authoring as
  scaffold support and eval-contracts as schema validation support below
  source bundle meaning, bundle-local review, evidence acceptance, generated
  readers, receipts, runtime candidates, sibling refs, quests, and release
  readiness
- `comparison-spine` mechanic package for fixed-baseline, peer-compare,
  longitudinal-window, generated comparison reader, part-local fixture and
  report routes, and anti-overread boundaries without moving bundles or
  generated readers
- `proof-infra` mechanic package for shared fixture, runner, scorer, schema,
  report, template, and generated proof-artifact contract routing, plus a
  `fixture-families` part for generic shared fixture support and a
  `reportable-contracts` part for shared runner/scorer/schema contracts
  without moving whole infrastructure districts by theme
- comparison-spine part-level contract guard, making spine-overview,
  fixed-baseline, peer-compare, and longitudinal-window README files expose
  inputs, outputs, stronger-owner split, stop-lines, and validation without
  turning comparison dossiers, fixture families, or generated comparison
  readers into bundle promotion, broad growth proof, or repo-global scoring
- `publication-receipts` mechanic package for optional eval-result receipt
  publication, stats-envelope mirroring, live publisher, report subordination,
  and owner-local live receipt boundaries without moving receipt data surfaces
- `release-support` mechanic package for bounded release scope, changelog
  narrative, release audit, GitHub `Repo Validation`, tag/release-note posture,
  and post-release proof boundaries without moving release or source proof
  surfaces
- release-support provenance bridge and legacy index for old `proof-release`
  parent, report, test, and decision wording, keeping release-support as the
  active mechanic
- `titan` mechanic package plus package-local seed guidance for Titan
  seed canary shape, incarnation and summon discipline guide routing, and
  validator-backed boundaries without claiming full incarnation proof
- Titan parts-index wording and validator coverage that keep canaries as the
  current seed-boundary payload form rather than a parent or parts-district
  name
- parent-level `DIRECTION.md` surfaces for every active mechanic, with
  validator coverage and a decision record keeping current operating direction
  separate from `README.md`, `PARTS.md`, `PROVENANCE.md`, legacy, and
  part-local contracts, plus parent `README.md` and `AGENTS.md` entry routes
  that expose `DIRECTION.md` before part growth or legacy lookup
- active parent evidence dimension ledger in `mechanics/EVIDENCE_CLUSTERS.md`,
  with validator coverage and a decision record requiring each active parent
  to show meaning/doctrine, proof pressure, contracts/payloads,
  builders/readouts, quest/deferred pressure, owner split and stop-lines, and
  legacy/provenance
- Mechanic Evidence Route Refs ledger in `mechanics/EVIDENCE_CLUSTERS.md`,
  with validator coverage and a decision record requiring each active parent
  to cite concrete local route refs, including an active parent route and at
  least one living non-mechanics evidence route ref, so parent evidence cannot
  be prose-only or rest on a generic root validator path or rationale-only
  decision ref
- repair/diagnosis route boundary wording and validation, keeping
  `aoa-repair-boundedness` under `antifragility/repair-proof` while
  `aoa-diagnosis-cause-discipline` routes through
  `growth-cycle/diagnosis-gate` instead of stale deferred Antifragility
  wording or a `repair` parent
- Active Mechanics Topology Wording decision and validator coverage that keeps
  `DESIGN.md`, `DESIGN.AGENTS.md`, and `docs/architecture/PROOF_TOPOLOGY.md` speaking about
  active mechanic packages rather than future or readiness-only pre-movement
  posture, now also covering `ROADMAP.md` and the proof-topology decision while
  leaving legacy archive details inside legacy
- legacy boundary wording guard that keeps `docs/architecture/LEGACY_NAMING.md`,
  `ROADMAP.md`, and `DESIGN.AGENTS.md` from treating legacy as a movement,
  deletion, or retirement route outside the owning archive
- legacy naming posture now stays free of concrete old-name inventories,
  active parent allowlists, wrong-parent maps, and old Spark path routing;
  those checks belong to active topology/evidence surfaces or owning
  `legacy/` archives behind `PROVENANCE.md`
- legacy archive accounting now stays inside `legacy/` while active surfaces
  route only through the current owner and `PROVENANCE.md`
- Titan owner-named evals-native boundary wording, clarifying that
  `mechanics/titan/` owns only the seed-boundary proof operation while
  `aoa-agents` keeps Titan role, bearer, summon, and incarnation law
- root-district reconnaissance ledger in `mechanics/EVIDENCE_CLUSTERS.md`,
  with validator coverage and a decision record requiring the goal-listed root
  districts plus current proof-infra route-card roots such as `runners/`,
  `scorers/`, and `templates/` to show root posture, route-card-only
  boundaries, mechanic-owned payload routes, and validation guards before
  further mechanic movement
- residual root-authored surface classification ledger in
  `mechanics/EVIDENCE_CLUSTERS.md`, with validator coverage and a decision
  record requiring top-level `docs/`, `scripts/`, and `tests/` files to remain
  explicitly root-owned or move behind the proper mechanic-owned payload route
- Mechanic Part Payload Inventory guard, with validator coverage and a decision
  record requiring each concrete part README to route every actual payload
  subdirectory while rejecting empty payload directories, unexpected payload
  classes, and unexpected part-root files
- the payload inventory guard now also covers eval-backed thin support
  routes, requiring any part with no part-local payload subdirectories to say
  why the source eval package stays under `evals/`
- Mechanic Part Source Surface Reference Guard, with validator coverage and a
  decision record requiring path-like `Source Surfaces` refs in concrete part
  README files to resolve as repo-relative paths, matching globs,
  repo-qualified sibling refs, or placeholder routes instead of stale source
  surface ref residue
- Mechanic Part Source Surfaces Section Contract, with validator coverage and a
  decision record requiring every concrete part README to use the plural
  `## Source Surfaces` section with at least one path-like source ref rather
  than hiding active source paths under `Role`, `Source Surface`, or
  `Active Surfaces`
- Mechanic Part Validation Command Reachability guard, with validator coverage
  and a decision record requiring concrete part README validation commands to
  use repo-relative reachable paths instead of stale or absolute command
  targets, and requiring payload-bearing parts to carry a payload coverage
  anchor instead of only naked route-wide commands
- Mechanic PARTS Index Synchronization guard, with validator coverage and a
  decision record requiring parent `PARTS.md` maps to match actual local part
  directories while preserving cross-parent stop-line and handoff references
- Mechanic Parent Guidance Boundary guard, with validator coverage and a
  decision record keeping parent-level `docs/` limited to explicit
  mechanic-wide guidance with role, scope, source surfaces, owner split,
  stop-lines, and validation while moving Titan canary guides under the
  `seed-boundary` part-owned payload route
- Mechanic Legacy Single Bridge guard, with validator coverage and a decision
  record requiring active mechanic surfaces to use `PROVENANCE.md` as the
  single controlled bridge from active mechanic surfaces into the legacy
  archive instead of linking directly to archive internals, including active
  JSON/YAML manifests, hooks, and part-local helpers
- Mechanic Provenance Bridge Posture guard, with validator coverage and a
  decision record requiring every mechanic `PROVENANCE.md` to say it is a
  bridge, not an active route, and to route readers through active surfaces
  before opening the legacy archive
- Legacy Naming Single-Bridge Language guard, with validator coverage and a
  decision record requiring `docs/architecture/LEGACY_NAMING.md` to keep `PROVENANCE.md` as
  the single controlled bridge from active mechanic surfaces
- Legacy Naming Posture Guide guard, with validator coverage and a decision
  record requiring `docs/architecture/LEGACY_NAMING.md` to stay a posture guide rather than
  a global archive map
- compatibility root route-card legacy wording guard, keeping root route cards
  such as `schemas/` and `manifests/` on the owning mechanic `PROVENANCE.md`
  bridge instead of listing archive-internal index or accounting surfaces
- Active Legacy Parent Wording Boundary guard, with validator coverage and a
  decision record requiring active route wording to use runtime evidence as an
  audit-owned evidence class/schema vocabulary rather than reviving
  `runtime-evidence` as a parent-like route outside audit
- validator-backed legacy/provenance route cards for every active mechanic:
  `PROVENANCE.md` opens the archive through `legacy/README.md`, and archive
  accounting stays inside `legacy/`
- `agon` mechanic package for Agon pre-protocol proof alignment, seed
  configs, generated registries, observe-only recurrence components and hooks,
  quest notes, recurrence-control-plane stop-line review, and owner handoffs
  with part-local homes for Agon-owned docs, configs, schemas, examples,
  generated registries, scripts, tests, recurrence manifests, and observe-only
  hooks without granting live verdict authority
- `recurrence` mechanic package for eval-side recurrence proof, including the
  recurrence proof program, control-plane integrity docs, fixtures, schema,
  example dossier, runner, scorer, tests, manifest, provenance bridge, and
  legacy index while source proof bundles stay under `evals/`
- `checkpoint` mechanic package for eval-side checkpoint proof, including A2A
  summon return, restartable inquiry, and self-agent posture parts, with
  part-local fixture families, checkpoint-specific hook examples, validation
  tests, provenance bridge, and legacy index while source proof bundles stay
  under `evals/`
- checkpoint part-level contract guard for A2A summon return, restartable
  inquiry, and self-agent posture, updating source-surface lists to current
  part-local payload homes and keeping checkpoint proof below implementation,
  memory canon, runtime activation, owner acceptance, and broad long-horizon
  competence claims
- `experience` mechanic package for eval-side Experience proof, including
  protocol integrity, certification gate, adoption federation,
  governance/runtime-boundary, and office release-train parts, with part-local
  docs, fixtures, examples, schemas, tests, provenance bridge, and legacy index
  while source proof bundles stay under `evals/`
- Experience part-level contract guard for protocol integrity, certification
  gate, adoption federation, governance/runtime-boundary, and office
  release-train, keeping verdict support below live runtime, certification,
  adoption, governance, memory, routing, KAG, ToS, office, release,
  deployment, and broad Experience-success authority
- remaining Experience verdict residue for appeal review, stay-order
  enforcement, vote-seal integrity, replay-history integrity, replay audit, and
  service-mesh regression now lives under the existing
  `governance-runtime-boundary` or `office-release-train` parts instead of
  root `docs/`
- `antifragility` mechanic package for eval-side Antifragility proof, including
  posture review, stress-recovery window, and repair-proof parts, with
  part-local docs, fixture families, schemas, provenance bridge, and legacy
  index while source proof bundles stay under `evals/`, comparison readouts
  stay under `comparison-spine`, and runtime evidence selection stays under
  `audit`
- antifragility part-level contract guard for posture review,
  stress-recovery window, and repair proof, keeping those parts from becoming
  global resilience, runtime self-healing, permanent stability, repair-parent,
  or growth-cycle completion claims
- `method-growth` mechanic package for eval-side Method-growth proof,
  including candidate-lineage and owner-landing parts, with part-local shared
  fixture families, provenance bridge, and legacy index while source proof
  bundles stay under `evals/` while diagnosis, repair, and distillation
  surfaces stay outside the package until separate evidence passes prove those
  routes
- Method-growth part owner-split contract guard, keeping candidate-lineage as
  lineage proof only and owner-landing as owner-fit routing proof only, below
  final object quality, owner-local acceptance, hidden promotion, derivative
  first-authoring, seed truth, memory canon, and universal growth scores
- `rpg` mechanic package for eval-side RPG proof, including the
  `progression-unlocks` part, part-local progression/unlock docs, schemas,
  examples, generated example cards, provenance bridge, and legacy index while
  quest source records stay under `quests/` and role, skill, playbook, runtime,
  and stats truth stay with stronger owners
- `growth-cycle` mechanic package for eval-side Growth Cycle diagnosis proof,
  including the `diagnosis-gate` part, provenance bridge, and legacy index
  while source proof bundles stay under `evals/` and repair, longitudinal
  movement, RPG progression, closeout, harvest, quest promotion, and
  owner-followthrough pressure stay with their current owner routes until
  separate evidence passes prove active parts
- growth-cycle diagnosis-gate contract guard, keeping cause-hypothesis
  discipline below repair success, owner-fit proof, final object quality, broad
  growth score, closeout acceptance, donor harvest approval, quest promotion,
  memory canon, runtime activation, and owner-local landing
- `distillation` mechanic package for eval-side Distillation proof, including
  `compost-provenance` and `runtime-candidate-adoption` parts, provenance
  bridge, and legacy index while source proof bundles stay under `evals/`,
  runtime-pack hook metadata stays under `audit`, generic adoption stays under
  `experience`, memo recall routes through `recurrence/memory-recall`, and
  nearby contradiction, base writeback-act, and witness trace proof stay outside
  the parent until separate evidence proves active parts
- Distillation part-level contract guard for compost provenance and reviewed
  runtime candidate adoption, keeping those parts below ToS canon, memory
  canon, runtime promotion, receipt publication, Experience adoption, KAG lift,
  bridge-ready truth, owner acceptance, and generic artifact-quality or live
  memory-ledger claims
- recurrence support parts for `anchor-return`, `memory-recall`,
  `recursor-boundary`, and `stats-regrounding-boundary`, keeping source proof
  bundles under `evals/` while moving support fixtures, report tests, scorer,
  runner, and part route cards into `mechanics/recurrence/parts/`
- recurrence control-plane-integrity contract guard, updating source-surface
  lists to current part-local payload homes and keeping recurrence dossiers
  below runtime status, promotion readiness, downstream projection truth, owner
  review acceptance, Agon source truth, beacon verdict authority, hidden
  continuity, and portable-proof acceptance by manifest
- RPG progression-unlocks contract guard, keeping progression evidence and
  unlock cards below quest acceptance, universal rank, role/skill/technique/
  playbook authority, runtime equip state, generated-card authority, and
  growth-cycle diagnosis or longitudinal movement claims
- `portable-proof-beacons` recurrence support part for the portable-proof
  beacon manifest, hook binding, and recurrence decision-closure guidance,
  keeping runtime evidence, progression evidence, and overclaim alarms below
  bundle-local review instead of making `portable-proof-beacons` a parent
  mechanic
- `audit` mechanic package for runtime evidence selection,
  artifact-to-verdict hooks, generated candidate readers, integrity-review
  surfaces, part-local source homes, and bundle-local review boundaries
- audit provenance bridge and legacy index for old `runtime-evidence` parent
  and root runtime-evidence path vocabulary, keeping audit as the active
  mechanic
- sibling proof-reference compatibility map plus `boundary-bridge` mechanic
  package for current, legacy, rejected, and unresolved sibling ref posture
- `orchestrator-proof-anchors` part under `boundary-bridge`, moving the
  orchestrator proof alignment note out of root `docs/` while keeping
  `aoa-agents` class identity, playbook meaning, and memo truth with their
  stronger owners
- legacy naming map for active, historical, accepted-input,
  generated-projection, candidate-only, and provenance-bridge posture around old
  Agon, wave, phase-alpha, runtime-candidate, artifact-to-verdict,
  bundle-family, Titan canary, historical Spark root-path, or quest path names
  before they are moved, distilled, or removed
- Spark maintained agent lane placement under `.agents/spark/`, plus
  `.agents/AGENTS.md`, decision memory, and validator coverage for the agent
  district
- quest lane/state source layout under `quests/<lane>/<state>/`, generated
  quest-reader path parity, legacy top-level path mapping, and validator
  coverage rejecting stale root quest files
- quest lifecycle contract in `quests/LIFECYCLE.md` for state meaning,
  open-index visibility, return posture, proof-loop defer or handoff routing,
  and validator coverage across all schema states
- `proof-loop` mechanic package for the active pick-inspect-expand-candidate
  review-report-receipt route, keeping source bundles, generated readers,
  candidate evidence, sibling refs, reports, and receipts in their existing
  owner lanes
- proof-loop provenance bridge and legacy index for the old root route-smoke
  report path, keeping route-smoke artifacts inside the active proof-loop part
- first proof-loop local route-smoke report, validating that one
  `aoa-verification-honesty` path can land in a bounded report without receipt
  emission, bundle promotion, runtime intake, or sibling-owner transfer
- proof-loop route-smoke part contract, keeping the first route-smoke report as
  routeability evidence only with explicit inputs, outputs, stronger-owner
  split, stop-lines, and validation
- first schema-backed bundle-local proof-loop report at
  `evals/workflow/aoa-verification-honesty/reports/aoa-evals-slice-19-lifecycle-contract.report.json`,
  plus bundle-local report validation for real `*.report.json` artifacts
  without receipt publication or bundle promotion
- generated eval report index at `generated/eval_report_index.min.json`, plus
  `scripts/generate_eval_report_index.py`, validator coverage, and
  release-check coverage so real bundle-local reports are routeable without
  becoming receipt or verdict authority
- receipt-intake dry review at
  `mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json`, plus decision and
  validator coverage proving the first report-to-receipt payload preview stays
  `not_published` with no envelope, publisher run, or live receipt append
- publication-receipts provenance bridge and legacy index for old root receipt
  guide, schema, example, publisher, test, and dry-review paths, keeping
  receipt work in active parts while `.aoa/live_receipts/` remains owner-local
  live memory
- publication-receipts part-level contract guard, making receipt payload, stats
  envelope mirror, live publisher, and intake dry-review README files expose
  inputs, outputs, stronger-owner split, stop-lines, and validation without
  turning any part into a parent mechanic or strengthening receipts over
  bundle-local reports
- release-support readiness audit at
  `mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json`, plus decision and validator
  coverage proving local release-prep reviewability without claiming tag,
  GitHub Release, PR approval, GitHub `Repo Validation`, or goal completion
- strategic closeout audit at `mechanics/release-support/parts/strategic-closeout/reports/strategic-closeout-audit-v1.json`,
  plus decision and validator coverage mapping the original refactor plan to
  repo-local evidence while keeping current objective completion open until
  both the objective audit and requested GitHub landing route complete; tag,
  release, receipt publication, runtime acceptance, and sibling mutation remain
  outside this goal
- release-prep PR handoff at `mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json`, plus
  decision and validator coverage preparing candidate branch, commit, PR
  title/body, changed surfaces, validation, and landing steps as a pre-PR
  snapshot that current git and GitHub state supersede after branch or PR
  creation
- release-support part-level contract guard, making readiness-audit,
  strategic-closeout, and pr-handoff README files expose inputs, outputs,
  stronger-owner split, stop-lines, and validation without treating local
  readiness, closeout, or handoff artifacts as release, GitHub, tag, or goal
  completion authority
- decision `docs/decisions/0028-repo-validation-aoa-memo-pin-refresh.md` for
  the pinned public CI lane after GitHub `Repo Validation` exposed stale
  `aoa-memo` checkout drift
- validator coverage that keeps the new root design and decision surfaces
  discoverable, including the proof topology and mechanics surfaces
- route-card guard for cleaned root districts, including new or tightened
  README cards for `config/`, `examples/`, `manifests/`, `reports/`,
  `schemas/`, and `templates/`, decision
  `docs/decisions/0051-root-route-card-guard.md`, and validator coverage that
  rejects active payload and stray directory drift across every route-card-only
  root district
- mechanic parent allowlist guard, decision
  `docs/decisions/0052-mechanic-parent-allowlist.md`, and validator coverage
  that rejects undeclared `mechanics/<parent>/` directories before they become
  invented active topology; the same guard now requires every allowed parent to
  expose `AGENTS.md`, `README.md`, `PARTS.md`, and part-contract wording
- mechanic legacy archive boundary guard, decision
  `docs/decisions/0071-mechanic-legacy-skeleton-contract.md`, and validator
  coverage requiring every active parent to expose `PROVENANCE.md` and a
  package-local legacy archive behind it so legacy remains provenance behind
  active mechanics
- mechanic parent class guard, decision
  `docs/decisions/0072-mechanic-parent-class-contract.md`, and validator
  coverage that keeps AoA-aligned and evals-native parent sets disjoint,
  complete, and tied to `mechanics/EVIDENCE_CLUSTERS.md`, while keeping
  `agon-proof`, `titan-canaries`, `proof-release`, `runtime-evidence`,
  `sibling-proof-refs`, and `repair` as wrong parent forms
- generated route residue guard, decision
  `docs/decisions/0073-generated-route-residue-guard.md`, and validator
  coverage that rejects stale structured generated/readout references to former
  wrong mechanic parents or route-card-only root districts without blocking
  valid part-local generated references to sibling `config/`, `schemas/`, or
  report surfaces
- active mechanic route residue guard, decision
  `docs/decisions/0076-active-mechanic-route-residue-guard.md`, and validator
  coverage that rejects stale authored mechanics route-card references to
  former wrong mechanic parents or route-card-only root payload paths without
  blocking root route cards or same-part local references
- root authored route residue guard, decision
  `docs/decisions/0077-root-authored-route-residue-guard.md`, and validator
  coverage that rejects stale root-facing guide references to route-card-only
  root payload paths without blocking root route cards, historical context, or
  active `evals/<family>/<eval>/...` and `mechanics/...` routes
- decision route residue guard, decision
  `docs/decisions/0078-decision-route-residue-guard.md`, and validator coverage
  that rejects unmarked current-looking decision references to former root
  payload paths without blocking historical context, root route cards, or
  active `evals/<family>/<eval>/...` and `mechanics/...` routes
- repo config route residue guard, decision
  `docs/decisions/0079-repo-config-route-residue-guard.md`, `.gitignore`
  migration from the rejected `mechanics/titan-canaries/seeds/` unignore to
  `mechanics/titan/parts/seed-boundary/seeds/`, and validator coverage that
  keeps repo config from preserving former parent routes or route-card-only
  root payload paths as executable routing
- source bundle route residue guard, decision
  `docs/decisions/0080-source-bundle-route-residue-guard.md`, repo-qualified
  `aoa-sdk` fixture wording in `aoa-a2a-summon-return-checkpoint`, target-bundle
  fixture checklist wording in `aoa-eval-integrity-check`, and validator
  coverage that keeps source proof bundles from carrying ambiguous root payload
  paths or former mechanic parent routes
- mechanic payload route residue guard, decision
  `docs/decisions/0081-mechanic-payload-route-residue-guard.md`,
  repo-qualified recursor refs to `repo:aoa-agents/config/codex_subagent_wiring.v2.json`,
  portable-proof hook cleanup from stale root runtime globs, and validator
  coverage that keeps active mechanics payload from carrying ambiguous root
  payload paths or former mechanic parent routes
- mechanic part README contract guard, decision
  `docs/decisions/0074-mechanic-part-readme-contract.md`, and validator coverage
  that requires every active `mechanics/<parent>/parts/<part>/README.md` to
  expose inputs, outputs, stronger-owner split, stop-lines, validation, and a
  parent `PARTS.md` route by README path or exact part slug
- mechanic provenance entry contract guard, decision
  `docs/decisions/0075-mechanic-provenance-entry-contract.md`, and validator
  coverage that requires every active `PROVENANCE.md` to name the active route
  first and bridge only to `legacy/README.md` without carrying archive details
- legacy route notes for every active mechanic parent, plus validator coverage
  that keeps legacy archive detail out of active-side bridge surfaces
- audit part-level contract guard, making selected evidence packets,
  artifact-to-verdict hooks, candidate readers, and integrity-review README
  files expose inputs, outputs, stronger-owner split, stop-lines, and
  validation directly
- Agon part-level contract guard, making every active Agon part README expose
  inputs, outputs, stronger-owner split, stop-lines, and validation so Agon can
  grow inside `mechanics/agon/` without spawning proof-suffix parents
- Titan seed-boundary part contract, keeping canary YAML files as
  seed-boundary artifacts inside `mechanics/titan/` with explicit inputs,
  outputs, stronger-owner split, stop-lines, and validation
- Boundary Bridge part-level contract guard, making compatibility map,
  latest-sibling canary, and orchestrator proof-anchor parts expose inputs,
  outputs, stronger-owner split, stop-lines, and validation without importing
  sibling authority

### Changed

- clarified `docs/architecture/ARCHITECTURE.md` as the technical proof model, distinct from
  `DESIGN.md`, `docs/architecture/PROOF_TOPOLOGY.md`, and
  `mechanics/EVIDENCE_CLUSTERS.md`, with mechanics and legacy bridge layering
  described as proof-operation support rather than bundle authority, plus a
  validator-backed decision contract that keeps that role visible
- refreshed `aoa-memo` proof-reference paths to the current sibling topology
  while keeping `aoa-evals` as the local bounded proof owner
- refreshed GitHub `Repo Validation`'s pinned `aoa-memo` checkout to
  `97f19698c94ebbebabe8b1b6f22e5ccff3bc5f1f` without weakening validation or
  mutating the sibling repo
- reframed `mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json` as a pre-PR snapshot so
  local git and GitHub state supersede it after branch or PR creation
- rebuilt `ROADMAP.md` and `QUESTBOOK.md` around active proof-organ direction,
  open obligations, source quest records, and generated quest readers
- moved Agon, Titan canary, recurrence, checkpoint, Experience, and audit runtime-evidence source surfaces into
  package-local mechanic homes where those mechanics now own real operations,
  while leaving source proof bundles and stronger-owner truth in their owning
  routes
- moved former `AOE-Q-AGON-*` markdown quest notes behind
  `mechanics/agon/PROVENANCE.md` so `quests/` remains a schema-backed source
  record district instead of an active route for legacy note forms

### Validation

- `python scripts/validate_repo.py`
- `python scripts/validate_semantic_agents.py`
- `python scripts/build_catalog.py --check`
- `python scripts/generate_eval_report_index.py --check`
- `python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check`
- `python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check`
- `python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py --check`
- `python mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py --repo-root . --format json`
- `python scripts/release_check.py`
- GitHub `Repo Validation` on the release PR

### Notes

- `v0.4.0` publishes the proof topology, mechanics topology, agent route mesh,
  generated-reader parity, release-support route, and eval-source tree
  refactor. It does not promote `aoa-evals` into runtime, memory, role,
  routing, sibling-release, or broad agent-capability authority.

## [0.3.3] - 2026-04-23

### Summary

- this patch expands proof coverage across reviewed closeout carry, Agon
  prebindings, contradiction closure, verdict-delta scars, mechanical trials,
  retention rank, schools/lineages/campaigns, KAG/Sophian alignment, and
  Wave XV epistemic evals
- recurrence control-plane integrity, recursor readiness, stats re-grounding,
  Titan canaries/incarnation checks, Experience protocol integrity,
  certification gates, adoption verdicts, governance refs, and post-W10
  runtime integrity review surfaces are added or tightened
- `aoa-evals` remains the bounded proof layer: it carries verdict and
  integrity evidence without becoming owner truth for runtime, memory, roles,
  routing, or source-authored meaning

### Added

- reviewed workspace closeout proof-pressure and carry-note surfaces
- Agon eval prebindings and alignment surfaces across contradiction closure,
  verdict-delta scar, mechanical trial, retention rank, schools/lineages,
  campaigns, KAG/Sophian, and epistemic waves
- recurrence integrity, recursor readiness, stats re-grounding boundary,
  Titan runtime and incarnation canaries, Experience protocol integrity,
  certification gates, adoption verdicts, governance verdict refs, and
  post-W10 runtime integrity proof surfaces

### Changed

- eval review follow-up drift, validator follow-ups, recurrence scorer
  evidence checks, Experience verdict metadata, adoption/gateway metadata, and
  wave4 governance verdict references were tightened

### Validation

- `python scripts/release_check.py`

### Notes

- this patch adds proof and integrity surfaces only; it does not promote evals
  into source, runtime, memory, routing, or role authority

## [0.3.2] - 2026-04-19

### Summary

- this patch adds chaos-wave trace and proof lanes, A2A summon return
  coverage, and a bounded memo writeback-act proof surface
- proof gates, receipt loops, playbook pinning, and sibling-root-aware memo
  evidence handling are tightened across the eval layer
- `aoa-evals` remains the bounded proof and audit layer without absorbing
  owner truth

### Added

- `aoa-memo-writeback-act-integrity` as a bounded draft proof surface for one
  real Phase Alpha runtime-to-memo writeback act
- `runtime_evidence_selection.phase-alpha-memo-writeback-act.example.json`
  plus schema-backed report artifacts for the new writeback-act lane
- chaos wave 1 trace eval bridge surfaces, early proof-pressure evidence,
  A2A summon return checkpoint coverage, and reviewed candidate adoption eval
  lanes

### Changed

- refreshed memo-pilot roadmap, selector, and runtime-promotion guidance so the
  writeback-act lane sits beside recall and contradiction without overclaiming
- eval proof gates, receipt loops, release-audit playbooks pinning, memo
  report sibling-root handling, and proof-carry notes are tightened for the
  current wave

### Validation

- `python scripts/release_check.py`

### Notes

- this patch keeps the release line focused on bounded proof surfaces for
  memo, playbook, A2A, and chaos-wave follow-through


## [0.3.1] - 2026-04-12

### Summary

- this patch adds continuity-oriented eval bundles, diagnosis-cause-discipline
  coverage, and checkpoint proof follow-through
- proof publication and catalog surfaces are refreshed for the current wave
  without widening eval ownership
- `aoa-evals` remains the bounded proof and audit layer

### Added

- checkpoint proof follow-through quest capture, growth-refinery lineage eval
  bundles, diagnosis-cause-discipline coverage, and self-agency continuity
  eval bundles.

### Changed

- proof-artifact publication, catalog surfaces, and dependency alignment are
  refreshed for the current continuity wave.

### Validation

- `python scripts/release_check.py`

### Notes

- detailed continuity-oriented bundle, catalog, and checkpoint-proof changes for this patch remain enumerated below under `Added` and `Changed`

## [0.3.0] - 2026-04-10

### Summary

- this release adds local-text and ring-discipline eval bundles, live eval-result receipt contracts, and latest-sibling canary support
- proof validation, portable-eval expectations, and compact proof lineage readers are hardened across the public corpus
- `aoa-evals` remains the bounded proof and audit layer rather than turning into generic runtime QA ownership

### Validation

- `python scripts/release_check.py`

### Notes

- detailed bundle, report, generated-surface, and operating-surface coverage for this release remains enumerated below under `Added`, `Changed`, and `Included in this release`

### Added

- local-text and ring-discipline eval bundles plus antifragility posture and
  fourth-wave stress-recovery evals
- live eval-result receipt contracts and publisher support together with a
  latest-sibling canary workflow
- repo-local project-foundation, session-harvest, and automation-opportunity
  skill surfaces for proof-repo follow-through

### Changed

- hardened proof validation, portable-eval expectations, and compact proof
  lineage readers across the current public corpus
- clarified proof-route, validator, and AGENTS guidance around the next-wave
  bounded proof posture

### Included in this release

- proof-corpus expansions across `evals/`, `docs/`, `generated/`,
  `examples/`, `fixtures/`, `schemas/`, and `reports/`, including Phase Alpha
  routing surfaces, RPG unlock proof, runtime candidate hardening, and new
  bounded audit posture
- repo-local operating and follow-through surfaces under `.agents/`, `.github/`,
  `AGENTS.md`, `AUDIT.md`, `README.md`, `EVAL_INDEX.md`, `EVAL_SELECTION.md`,
  `QUESTBOOK.md`, `quests/`, `scripts/`, and `tests/`, including quest and
  automation harvest installs, latest-sibling canary support, and route
  clarifications

## [0.2.0] - 2026-04-01

Second public release of `aoa-evals`.

This changelog entry uses the release-prep merge date.

### Summary

- current public corpus now ships as `18` public eval bundles, up from `15` in `v0.1.0`
- this release extends the repo with progression evidence, downstream feed contracts, questbook source-proof surfaces, and runtime candidate intake/template-index surfaces
- review posture is stronger for operator-facing runtime audit and intake flows while the repository remains bounded proof canon rather than a generic benchmark dump

### Added

- progression evidence adjunct surfaces for the current public proof contour
- eval downstream feed contracts for sibling consumers
- questbook source-proof surfaces and live questbook projections from quest YAML
- runtime candidate template index surfaces under `mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json`
- runtime candidate intake surfaces under `mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json`

### Changed

- hardened runtime candidate template indexing for operator audit and review prep
- clarified portable-eval and contract wording across the public proof surface
- fixed source-root handling around `abyss-stack`-adjacent resolution in the local validation path

### Included in this release

- `18` public eval bundles under `evals/`
- current generated reader and comparison surfaces under `generated/`, including the runtime candidate template/index families

### Validation

- `python scripts/build_catalog.py`
- `python scripts/build_catalog.py --check`
- `python scripts/validate_repo.py`
- `python -m pytest`

### Notes

- this remains a bounded proof release, not a claim that every current public bundle is equally mature or that `aoa-evals` has become a generic runtime QA repository

## [0.1.0] - 2026-03-23

First public release of `aoa-evals` as the bounded proof-canon repository in the AOA public surface.

This changelog entry uses the release-prep merge date.

### Summary

- current public corpus now ships as one bounded release with `15` public eval bundles
- current public maturity is explicitly mixed rather than flattened:
  - `9` `bounded` bundles
  - `1` `baseline` bundle
  - `5` `draft` bundles
- release messaging remains intentionally modest:
  - only `aoa-regression-same-task` is a public `baseline` surface
  - `draft`, `comparative`, and `longitudinal` surfaces should not be read more strongly than their current status and wording support

### Added

- first public release of `aoa-evals` as a portable proof-surface repository for bounded claims about workflow quality, boundaries, artifact quality, regressions, and repeated-window movement
- public eval corpus across workflow, boundary, stress, artifact, regression, comparative, capability, and longitudinal surfaces
- derived reader and runtime surfaces:
  - `generated/eval_catalog.json`
  - `generated/eval_catalog.min.json`
  - `generated/eval_capsules.json`
  - `generated/comparison_spine.json`
  - `generated/eval_sections.full.json`
- shared proof-flow dossiers under `reports/` for same-task baseline, artifact/process paired reading, comparison-spine reading, and repeated-window reading
- repo-owned validation helpers under `scripts/` plus the GitHub Actions repo validation workflow under `.github/workflows/repo-validation.yml`
- public repository entry and governance surfaces including `README.md`, `docs/README.md`, `docs/architecture/ARCHITECTURE.md`, `docs/guides/EVAL_PHILOSOPHY.md`, `docs/operations/RELEASING.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `EVAL_INDEX.md`, and `EVAL_SELECTION.md`

### Included in this release

- eval bundles under `evals/` plus the current repository-wide chooser and index in `EVAL_SELECTION.md` and `EVAL_INDEX.md`
- shared fixtures, scorers, runner contracts, schemas, templates, examples, and report artifacts that keep the current eval corpus reviewable and portable
- the current comparison-spine layer anchored by:
  - `aoa-regression-same-task` as the only public `baseline` starter
  - `aoa-output-vs-process-gap` as a draft bridge surface
  - `aoa-longitudinal-growth-snapshot` as a draft repeated-window surface
  - `aoa-eval-integrity-check` as the bounded integrity sidecar
- the current artifact/process and trace-adjacent proof surfaces, including shared dossiers under `reports/` and bridge guidance in `mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md`

### Validation

Documented local validation path for this release:

- `python -m pip install -r requirements-dev.txt`
- `python scripts/build_catalog.py`
- `python scripts/validate_repo.py`
- `python -m pytest`

### Notes

- this is the first public release of the repository, not a claim that every current public bundle is equally mature
- only `aoa-regression-same-task` currently has public `baseline` status; the other comparative and longitudinal surfaces remain draft and should stay weaker than any broad growth or baseline-by-association reading
- this release remains a repository release of docs, eval bundles, schemas, generated reader surfaces, and validation helpers rather than a package or registry artifact
- publishing to PyPI, npm, or other registries is out of scope for `v0.1.0`
