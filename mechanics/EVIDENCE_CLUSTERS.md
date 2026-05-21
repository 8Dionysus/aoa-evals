# Mechanics Evidence Clusters

## Role

`mechanics/EVIDENCE_CLUSTERS.md` is the refactor map for
`aoa-evals/mechanics`.

It answers whether a top-level mechanic parent has enough evidence to exist,
which root districts prove the cluster, and whether the parent name routes as
AoA-aligned or evals-native.

## Operating Card

| Field | Route |
| --- | --- |
| role | parent-mechanic evidence gate and cross-root evidence map |
| entry | use before moving root-district artifacts into or between mechanics |
| input | proposed parent name, old root path family, artifact class, report/canary/form cluster, or payload movement pressure |
| output | allowed parent class, evidence dimensions, root-district posture, mechanic boundary, and validation guard |
| owner | `mechanics/AGENTS.md` for mutation law; this map for parent evidence; parent `README.md`/`DIRECTION.md`/`PARTS.md` for local operation |
| next route | `docs/PROOF_TOPOLOGY.md`, `mechanics/README.md`, parent route cards, part READMEs, and `docs/decisions/` |
| validation | `scripts/validate_repo.py`, `tests/test_validate_repo.py`, and the nearest mechanics route card |

## Evidence Standard

Create or keep a mechanic parent when a recurring proof-side operation has
enough cross-root evidence to name:

- meaning or doctrine;
- proof claim or bounded evaluation pressure;
- schema, contract, example, fixture, or seed input;
- builder, validator, test, generated reader, report, or receipt output;
- stronger-owner split and stop-lines;
- legacy or provenance posture when old names remain.

Single documents, reports, and canary forms route as parts under the right parent.
They justify a parent only when the surrounding evidence proves an independent
operation.

Owner-named parents stay valid when the local proof operation is real, artifact
forms stay below the parent as parts, and the stronger-owner split is explicit.
That keeps an owner-named proof boundary from becoming a proof-organ-invented
doctrine route.

## Root District Reconnaissance Ledger

This root-district ledger is the first gate before package growth. It records
what each named root district currently owns, which payloads are mechanic-owned
or bundle-owned, and which guard prevents old root placement from steering
active topology.

| District | Authority class | Current root posture | Mechanics relationship | Validation guard |
| --- | --- | --- | --- | --- |
| `docs` | source guidance, topology, decisions, and repo-wide proof interpretation | root-owned source guidance stays in `docs/`; mechanic-owned docs live under the owning part when a narrower operation owns the read | mechanics may route docs as evidence, but mechanic-owned docs stay part-local and root docs remain guidance or provenance | `validate_root_authored_route_residue_surfaces`, `validate_proof_topology_surfaces`, and decision-token checks |
| `evals` | source proof object district | `evals/**/EVAL.md` and `evals/**/eval.yaml` stay root-owned source proof objects; source eval packages stay out of mechanics | mechanics provide proof-object, infra, comparison, audit, quest, or report support around eval packages without stealing eval meaning | per-eval validation, source-eval route residue, catalog builders, and root route-card validation |
| `fixtures` | shared proof infrastructure compatibility district | route-card-only compatibility posture; active fixture families live under proof-infra or domain mechanic parts | generic fixtures route to `mechanics/proof-infra/parts/fixture-families/fixtures/`, while domain fixtures live under owning mechanic parts | root route-card guard plus active-mechanic and mechanic-payload route residue checks |
| `schemas` | proof contract compatibility district | route-card-only compatibility posture; active schema payloads live under proof-object, proof-infra, questbook, or domain mechanic parts | eval contract schemas route to `mechanics/proof-object/parts/eval-contracts/schemas/`, shared contracts to proof-infra, quest schemas to questbook, and domain schemas to owning parts | root route-card guard plus schema-aware bundle, quest, and mechanic validation |
| `examples` | public-safe example compatibility district | route-card-only compatibility posture; active example payloads live beside their owning source | bundle examples stay in `evals/**/examples/`; audit, receipt, bridge, and domain examples live under owning mechanic parts | root route-card guard plus active route residue checks |
| `scripts` | repo-wide builders, validators, and release helpers | root scripts stay repo-wide and deterministic; mechanic-owned scripts live under the owning part | mechanics call or own part-local builders only when the operation owns the payload, while root `scripts/validate_repo.py` guards topology | touched-command checks, catalog-check route, and root repository validation route |
| `tests` | repo-wide validation district | root tests stay repo-wide for repository contracts, catalogs, generated readers, semantic cards, and topology guards | mechanic-owned tests live under `mechanics/<mechanic>/parts/<part>/tests/` next to the operation they constrain | focused pytest commands, part-local test placement guard, and full `tests/test_validate_repo.py` |
| `config` | configuration compatibility district | route-card-only compatibility posture; active config payloads live with the owning operation | Agon configs route to `mechanics/agon/parts/*/config/`; sibling canary config routes to boundary-bridge | root route-card guard and repo-config route residue checks |
| `manifests` | recurrence/component manifest compatibility district | route-card-only compatibility posture; active manifest payloads live with the owning lifecycle part | Agon manifests route to Agon parts; recurrence manifests route to `mechanics/recurrence/parts/` such as control-plane and portable-proof-beacons | root route-card guard plus mechanic-payload route residue checks |
| `generated` | repo-wide derived readers | root generated surfaces remain derived readers only; they are not source proof objects | part-local generated readers live under the owning mechanic part when the part owns the source and builder | generated route residue checks, builder check modes, and catalog-check route |
| `reports` | report compatibility district | route-card-only compatibility posture; active report payloads live with bundle or mechanic owners | bundle reports stay bundle-local; proof-loop, comparison, receipts, and release-support reports live under owning mechanic parts such as `mechanics/release-support/parts/` | root route-card guard, report index validation, and release-support report checks |
| `runners` | shared runner contract compatibility district | route-card-only compatibility posture; active runner contracts live under proof-infra or bundle-local pointers | active shared runner contract lives under `mechanics/proof-infra/parts/reportable-contracts/runners/`, while bundle-local runner contracts point to it through `runner_surface_path` | root route-card guard, bundle runner contract checks, and proof-infra reportable-contract validation |
| `scorers` | shared scorer helper compatibility district | route-card-only compatibility posture; active scorer helpers live under proof-infra or owning mechanic parts | active shared scorer helper lives under `mechanics/proof-infra/parts/reportable-contracts/scorers/`, while domain scorers live under owning mechanic parts | root route-card guard, scorer helper checks, schema validation, and proof-infra reportable-contract validation |
| `templates` | eval template compatibility district | route-card-only compatibility posture; active template payloads live under proof-object eval authoring | active eval authoring template lives under `mechanics/proof-object/parts/eval-authoring/templates/` | root route-card guard, proof-object eval-authoring checks, and root repository validation route |
| `quests` | source quest record district | schema-backed lane/state source quest records stay under `quests/`; generated quest readers remain derived; markdown quest-note lineage belongs behind the owning mechanic `PROVENANCE.md` | `mechanics/questbook/parts/` owns source-record schemas and dispatch-reader contracts without moving source quest records | quest route validation, generated quest catalog checks, and catalog-check route |
| `mechanics` | operation atlas | active only for proven parent operations with route cards, `DIRECTION.md`, parts, provenance, and validation | `mechanics/EVIDENCE_CLUSTERS.md` gates parent names and cross-root evidence before payload movement | parent allowlist, part README contracts, direction/provenance guards, and legacy/accounting checks |

## Residual Root-authored Surface Classification

This residual ledger covers root-authored files that remain under `docs/`,
`scripts/`, and `tests/` after mechanic-owned payload movement. These districts
are not route-card-only, so the guard is different: every top-level file must
be classified as root-owned guidance, root-owned builder/validator, or
root-owned test coverage, and every row must state where mechanic-owned payload
belongs instead.

| Surface | Root role | Mechanic boundary | Validation guard |
| --- | --- | --- | --- |
| `docs/AGENTS.md` | root-owned docs route card for proof-meaning edits | mechanic-owned payload guidance belongs in nearest `mechanics/*/AGENTS.md`, not this card | semantic and nested AGENTS validation |
| `docs/AGENTS_ROOT_REFERENCE.md` | root-owned preserved reference for full historical root guidance | mechanic-owned payload history must route through package `PROVENANCE.md` and legacy indexes | root design and route-residue validation |
| `docs/AGENT_INDEX.md` | root-owned agent-facing pass-through index from repo to authority class, operation, mechanic parent, part, payload, and validation | mechanic-owned payload details belong in `mechanics/EVIDENCE_CLUSTERS.md`, parent maps, part READMEs, and local route cards | agent-index surface validation and root-authored classification |
| `docs/ARCHITECTURE.md` | root-owned technical proof model | mechanic-owned payload architecture lives in parent `DIRECTION.md` and part READMEs | proof topology validation |
| `docs/ARTIFACT_PROCESS_SEPARATION_GUIDE.md` | root-owned guide for process/artifact reading | mechanic-owned payload examples and reports live under owning parts | root-authored route-residue validation |
| `docs/BASELINE_COMPARISON_GUIDE.md` | root-owned baseline comparison guide | mechanic-owned payload comparison fixtures and reports live under `mechanics/comparison-spine/parts/` | comparison-spine and root-authored route guards |
| `docs/BLIND_SPOT_DISCLOSURE_GUIDE.md` | root-owned blind-spot disclosure guide | mechanic-owned payload blind-spot evidence lives with bundles, reports, or owning mechanics | bundle and report validation |
| `docs/COMPARISON_SPINE_GUIDE.md` | root-owned comparison-spine interpretation guide | mechanic-owned payload comparison state lives under `mechanics/comparison-spine/parts/` | comparison-spine focused and route-residue checks |
| `docs/EVAL_PHILOSOPHY.md` | root-owned epistemic posture guide | mechanic-owned payload proof operations live in mechanic packages, not philosophy docs | root design validation |
| `docs/EVAL_REVIEW_GUIDE.md` | root-owned review posture guide | mechanic-owned payload review artifacts live under bundle-local or part-local reports | repo validation and report index checks |
| `docs/EVAL_RUBRIC.md` | root-owned rubric interpretation guide | mechanic-owned payload scoring helpers live under proof-infra or bundle-local contracts | schema and proof-infra validation |
| `docs/FIXTURE_SURFACE_GUIDE.md` | root-owned fixture interpretation guide | mechanic-owned payload fixture families live under proof-infra or owning mechanic parts | root route-card guard and fixture-family checks |
| `docs/LEGACY_NAMING.md` | root-owned legacy naming posture guide | mechanic-owned payload legacy details live inside package `legacy/` archives behind package `PROVENANCE.md` | legacy naming and provenance validators |
| `docs/PORTABLE_EVAL_BOUNDARY_GUIDE.md` | root-owned portability boundary guide | mechanic-owned payload portable beacons live under recurrence parts when proven | recurrence and root-authored route guards |
| `docs/PROOF_TOPOLOGY.md` | root-owned authority-class topology | mechanic-owned payload topology lives in `mechanics/EVIDENCE_CLUSTERS.md`, parent `DIRECTION.md`, and parts | proof topology validation |
| `docs/QUESTBOOK_EVAL_INTEGRATION.md` | root-owned quest/eval integration guide | mechanic-owned payload quest schemas and dispatch contracts live under `mechanics/questbook/parts/` | quest route and generated quest checks |
| `docs/README.md` | root-owned docs index | mechanic-owned payload docs route to owning mechanic docs and READMEs | root-authored route-residue validation |
| `docs/REGRESSION_PROOF_SURFACES.md` | root-owned regression proof guide | mechanic-owned payload regression fixtures and reports live under comparison-spine or bundles | comparison and bundle validation |
| `docs/RELEASING.md` | root-owned release process guide | mechanic-owned payload release state artifacts live under `mechanics/release-support/parts/` | release-support and release_check validation |
| `docs/REPEATED_WINDOW_DISCIPLINE_GUIDE.md` | root-owned repeated-window discipline guide | mechanic-owned payload repeated-window reports live under comparison-spine parts | comparison-spine validation |
| `docs/REVIEWED_CLOSEOUT_WRITEBACK_PROOF_INGRESS.md` | root-owned ingress note for deferred closeout/writeback pressure | mechanic-owned payload activates only through a proven growth-cycle, distillation, audit, or questbook part | root-authored route guards and future decision review |
| `docs/SCORE_SEMANTICS_GUIDE.md` | root-owned score semantics guide | mechanic-owned payload scorers live under proof-infra or owning parts | scorer and schema validation |
| `docs/SHARED_PROOF_INFRA_GUIDE.md` | root-owned shared proof infrastructure guide | mechanic-owned payload shared contracts live under `mechanics/proof-infra/parts/` | proof-infra validation |
| `docs/VERDICT_INTERPRETATION_GUIDE.md` | root-owned verdict interpretation guide | mechanic-owned payload verdict models live under source bundles or owning mechanic parts | bundle and root-authored route validation |
| `docs/VIA_NEGATIVA_CHECKLIST.md` | root-owned negative-boundary checklist | mechanic-owned payload stop-lines live in parent `DIRECTION.md`, `PARTS.md`, and part READMEs | direction and part README validators |
| `scripts/AGENTS.md` | root-owned scripts route card | mechanic-owned payload scripts live under owning `mechanics/*/parts/*/scripts/` | semantic AGENTS and script route validation |
| `scripts/build_catalog.py` | root-owned catalog builder | mechanic-owned payload builders live part-local and feed generated companions without owning root catalog truth | catalog check and repo validation |
| `scripts/eval_capsule_contract.py` | root-owned generated capsule contract helper | mechanic-owned payload capsule logic must not move into a mechanic part unless the part owns that generated reader | downstream feed tests |
| `scripts/eval_catalog_contract.py` | root-owned catalog contract helper | mechanic-owned payload bundle support remains part-local while root catalog remains repo-wide derived truth | catalog and downstream feed tests |
| `scripts/eval_comparison_spine_contract.py` | root-owned comparison-spine generated contract helper | mechanic-owned payload comparison reports and fixtures live under comparison-spine parts | comparison spine generated checks |
| `scripts/eval_proof_contract_helpers.py` | root-owned proof contract helper library | mechanic-owned payload validators may import helpers but belong under owning parts | full repo validation |
| `scripts/eval_section_contract.py` | root-owned section-reader contract helper | mechanic-owned payload section readers stay generated companions, not package source truth | downstream feed tests |
| `scripts/generate_eval_report_index.py` | root-owned report-index builder | mechanic-owned payload reports remain bundle-local or part-local and feed the root report index | report index check |
| `scripts/release_check.py` | root-owned release gate runner | mechanic-owned payload release audit artifacts live under release-support parts | release gate route in root `AGENTS.md#verify` |
| `scripts/validate_nested_agents.py` | root-owned nested AGENTS validator | mechanic-owned payload route cards are checked from root validation, not owned here | nested AGENTS validation |
| `scripts/validate_repo.py` | root-owned repository validator | mechanic-owned payload validators may live part-local, while this file guards cross-repo topology | focused and full repo validation |
| `scripts/validate_semantic_agents.py` | root-owned semantic AGENTS validator | mechanic-owned payload guidance lives in local route cards and is checked here | semantic AGENTS validation |
| `tests/AGENTS.md` | root-owned tests route card | mechanic-owned payload tests live under `mechanics/<mechanic>/parts/<part>/tests/` | semantic AGENTS validation |
| `tests/test_build_catalog.py` | root-owned catalog test coverage | mechanic-owned payload catalog inputs stay in bundles or parts and are checked through root builder tests | pytest catalog checks |
| `tests/test_current_direction_routes.py` | root-owned entrypoint route test | mechanic-owned payload direction lives in parent `DIRECTION.md` surfaces | focused direction tests |
| `tests/test_downstream_feed_contracts.py` | root-owned generated downstream feed contract tests | mechanic-owned payload generated readers remain part-local and feed root contracts only when derived | downstream feed tests |
| `tests/test_memo_contradiction_phase_alpha_gap_report.py` | root-owned bundle-report test for selected audit evidence | mechanic-owned payload selected evidence lives under `mechanics/audit/parts/selected-evidence-packets/` | bundle report schema test |
| `tests/test_memo_contradiction_phase_alpha_rerun_report.py` | root-owned bundle-report test for selected audit evidence | mechanic-owned payload selected evidence lives under `mechanics/audit/parts/selected-evidence-packets/` | bundle report schema test |
| `tests/test_memo_writeback_act_phase_alpha_report.py` | root-owned bundle-report test with sibling-evidence gating | mechanic-owned payload selected evidence lives under audit parts; sibling truth remains repo-qualified | bundle report and sibling-evidence skip checks |
| `tests/test_nested_agents_docs.py` | root-owned nested AGENTS test | mechanic-owned payload route cards are validated through root route tests | nested AGENTS pytest |
| `tests/test_roadmap_parity.py` | root-owned roadmap parity test | mechanic-owned payload status belongs in mechanics/roadmap surfaces, not ad hoc root notes | roadmap parity validation |
| `tests/test_validate_repo.py` | root-owned validator test suite | mechanic-owned payload contracts get focused tests here only when the root validator owns the cross-surface guard | full validator test suite |
| `tests/test_validate_semantic_agents.py` | root-owned semantic AGENTS test | mechanic-owned payload local cards remain under owning directories | semantic AGENTS pytest |
| `tests/test_verification_honesty_local_report.py` | root-owned bundle-local report test | mechanic-owned payload proof-loop report artifacts live under proof-loop parts, while this checks a source bundle report | bundle report schema test |

## Active Parent Evidence Dimension Ledger

This ledger makes the evidence standard reviewable by parent. Each active
parent row names the same proof-side dimensions: meaning/doctrine, proof
pressure, contracts/payloads, builders/readouts, quest/deferred pressure, owner
split and stop-lines, and legacy/provenance.

| Parent | Class | Meaning/doctrine | Proof pressure | Contracts/payloads | Builders/readouts | Quest/deferred pressure | Owner split and stop-lines | Legacy/provenance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `agon` | AoA-aligned | Agon alignment, court/prebinding, CCS/VDS/KAG/SLC/Sophian threshold pressure | Agon proof-alignment and recurrence review pressure | part-local configs, schemas, examples, manifests, hooks | registry builders, validators, tests, generated registries | former Agon quest-note pressure behind provenance and recurrence-control-plane stop-line review | AoA keeps Agon law; evals keeps candidate-only proof alignment and observe-only hooks | wave landing receipts, former `AOE-Q-AGON-*` markdown notes, and old `agon-proof` placement route through provenance |
| `antifragility` | AoA-aligned | antifragility posture, stress recovery, bounded repair | posture review, stress-window, repair boundedness | stress/repair fixtures, schemas, runtime-chaos sidecars | tests, comparison readouts, audit evidence packets | diagnosis routes through `growth-cycle/diagnosis-gate`; other growth pressure remains routed or deferred | owners keep runtime repair and cleanup truth; evals keeps bounded proof | old root docs, fixture families, and repair pressure route through provenance |
| `audit` | AoA-aligned | audit as candidate-evidence intake and artifact-to-verdict bridge | runtime candidate, trace bridge, integrity review pressure | selected-evidence schemas, hook schemas, examples | candidate-reader builders, generated intake readers, tests | phase-alpha and runtime evidence pressure remain candidate-only | runtime owners keep facts; bundles accept or reject proof interpretation | old `runtime-evidence` parent and root paths route through provenance |
| `boundary-bridge` | AoA-aligned | boundary bridge for sibling refs and class-facing anchors | sibling path drift, orchestrator anchors, Phase Alpha matrix bridge | compatibility map, canary matrix, phase-alpha schema/example | canary runner, matrix generator, generated matrix, tests | quest proof anchors and unresolved sibling refs remain reviewable pressure | sibling repos keep owner truth; evals keeps compatibility evidence | old `sibling-proof-refs` and root bridge paths route through provenance |
| `checkpoint` | AoA-aligned | checkpoint return, restart, and self-agent posture | A2A summon return, long-horizon restart, self-agent checkpoint proof | checkpoint fixtures and hook examples | part-local tests plus audit candidate readers | checkpoint quest pressure stays source obligation | implementation, memory, runtime, and role truth stay with owners | old root checkpoint docs, fixtures, tests, and hook examples route through provenance |
| `comparison-spine` | evals-native | comparison posture for baseline, peer, and longitudinal reads | same-task regression, paired comparison, repeated-window movement | comparison fixtures and report contracts | generated comparison spine, report readouts, tests | growth and stress movement feed bounded comparison pressure | bundle meaning stays stronger; comparison does not promote bundles | old root comparison fixture/report paths route through provenance |
| `distillation` | AoA-aligned | distillation as provenance-preserving abstraction and candidate adoption | compost provenance and reviewed runtime candidate adoption | distillation fixtures and adoption guardrails | tests, reports, audit bridge references | writeback/closeout ingress remains root or quest pressure unless proven | ToS, memo, KAG, runtime, and owner acceptance stay stronger | old fixture placement and Experience-adjacent adoption route through provenance |
| `experience` | AoA-aligned | Experience protocol, certification, adoption, governance, office train | verdict support for protocol, certification, adoption, runtime-boundary, office | schemas, examples, fixtures, support docs | tests and generated references | office/release/governance pressure remains bounded proof support | Experience law, runtime, office, KAG, ToS, and adoption truth stay with owners | old Experience root docs/examples/schemas/tests route through provenance |
| `growth-cycle` | AoA-aligned | Growth Cycle diagnosis as first active stage | diagnosis-cause discipline and cause-hypothesis proof | diagnosis bundle notes/examples/checks and diagnosis-gate part | bundle integrity checks, tests, generated readers | repair, harvest, closeout, quest promotion, owner-followthrough remain routed or deferred | repair stays antifragility; progression stays RPG; longitudinal movement stays comparison | deferred stage pressure and ingress notes route through provenance |
| `method-growth` | AoA-aligned | method-growth lineage and owner landing | candidate-lineage integrity and owner-fit routing quality | bundle contracts, fixtures, reports, examples | tests, generated catalogs, validation routes | diagnosis/repair/progression/distillation pressure routes to owning parents | owner repos keep final object and acceptance truth | old shared fixture placement routes through provenance |
| `proof-infra` | evals-native | reusable proof infrastructure below bundle meaning | shared fixtures, runners, scorers, schemas, templates, report contracts | fixture families and reportable contracts | scorers, tests, generated proof-artifact readers | domain-specific pressure routes to narrower mechanics | source bundles and domain mechanics stay stronger | old root infra district paths remain route cards or provenance |
| `proof-loop` | evals-native | local proof loop coordination across source, evidence, report, receipt | route-smoke and bundle-local proof-loop materialization | route-smoke report, report schema, receipt dry-review inputs | report index, validators, release-support checks | open proof questions and receipt publication stay separate | step owners keep meaning; proof-loop coordinates only | old route-smoke root report path routes through provenance |
| `proof-object` | evals-native | source proof object completeness and eval authority | eval claim, eval manifest, frontmatter, lifecycle, completeness review | authoring template, schemas, eval-local contracts | catalog/capsule/section builders, validators, tests | proof pressure remains with source evals and quests | eval packages stay source authority; generated/readout surfaces stay weaker | old root template/schema placement routes through provenance |
| `publication-receipts` | evals-native | optional publication receipt sidecar below reviewed reports | eval-result receipt publication and intake dry-review pressure | receipt schema/example, stats-envelope mirror, live publisher | receipt tests, intake dry-review report, live publisher checks | live receipt publication remains optional and separate | reports and bundles stay stronger; stats envelope owner stays `aoa-stats` | old receipt docs/schema/example/publisher/test paths route through provenance |
| `questbook` | AoA-aligned | quest obligations, lifecycle, returnability, deferred proof | source quest records and generated dispatch pressure | quest schemas, lifecycle docs, source records | generated quest catalog/dispatch and validators | captured/triaged/deferred obligations remain reviewable | quests are obligations, not bundle verdicts or live tasks | old top-level quest/schema paths route through provenance |
| `recurrence` | AoA-aligned | recurrence proof, return anchors, memo recall, recursor boundary, beacons | control-plane, anchor-return, memory-recall, stats-regrounding, portable-proof-beacon proof | fixtures, schemas, manifests, hooks, scorer/runner cases | runners, scorers, tests, generated/readout support | continuity-anchor and self-reanchor remain bundle-local until parts are proven | runtime, memory, stats, Agon, and owner decisions stay stronger | old recurrence root paths and support placement route through provenance |
| `release-support` | AoA-aligned | bounded release support and publication posture | readiness audit, strategic closeout, PR handoff, release check pressure | release-support reports, changelog, release docs, workflow refs | release_check, tests, GitHub validation route, generated freshness checks | goal completion and public release stay open until landing proof | release does not strengthen eval claims or GitHub status | old `proof-release` wording and report/test paths route through provenance |
| `rpg` | AoA-aligned | RPG progression and unlock proof support | progression evidence and unlock proof bridge | progression schemas, examples, generated unlock cards | validators, tests, generated card checks | quest unlock pressure remains source obligation | roles, skills, techniques, playbooks, runtime, and stats stay with owners | old progression/unlock root paths route through provenance |
| `titan` | evals-native | owner-named Titan proof-seed boundary, not proof-organ doctrine | incarnation, summon, memory, gate, runtime roster, bridge, and closeout seed pressure | Titan canary YAML seeds and seed AGENTS route | canary shape validator and tests; future scorer route is not active | Titan boundary pressure stays seed-level until executable proof exists | `aoa-agents` owns Titan role/bearer/summon/incarnation law; `aoa-memo` and runtime owners keep memory and activation truth | old `titan-canaries` parent and root `evals/` placement route through provenance |

## Active Parent Evidence Route Refs

This ledger keeps the dimension rows auditable. Each active parent must carry
concrete local route refs: repo-relative refs that resolve in the current
worktree, include the active parent route, and include at least one
living non-mechanics route ref, meaning a non-mechanics route ref that points
at current evidence. This living non-mechanics evidence keeps the parent from
being justified by
package-local prose alone. A generic root validator file is not enough here,
and a rationale-only decision ref is not enough by itself; use a concrete
source, bundle, generated readout, quest, workflow/config, root entry, or
part-local validator route for parent evidence.

| Parent | Route refs |
| --- | --- |
| `agon` | `mechanics/agon/README.md`, `mechanics/agon/parts/ccs-alignment/README.md`, `mechanics/agon/parts/ccs-alignment/config/agon_ccs_eval_alignment.seed.json`, `evals/boundary/aoa-recurrence-control-plane-integrity/EVAL.md` |
| `antifragility` | `mechanics/antifragility/README.md`, `mechanics/antifragility/parts/repair-proof/README.md`, `evals/stress/aoa-antifragility-posture/EVAL.md`, `evals/workflow/aoa-repair-boundedness/EVAL.md` |
| `audit` | `mechanics/audit/README.md`, `mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json`, `evals/capability/aoa-eval-integrity-check/EVAL.md`, `docs/decisions/0007-audit-mechanic-package.md` |
| `boundary-bridge` | `mechanics/boundary-bridge/README.md`, `mechanics/boundary-bridge/parts/latest-sibling-canary/README.md`, `.github/workflows/latest-sibling-canary.yml`, `quests/orchestrator/captured/AOA-EV-Q-0006.yaml` |
| `checkpoint` | `mechanics/checkpoint/README.md`, `mechanics/checkpoint/parts/a2a-summon-return/README.md`, `evals/workflow/aoa-a2a-summon-return-checkpoint/EVAL.md`, `mechanics/checkpoint/parts/a2a-summon-return/tests/test_a2a_summon_return_checkpoint_fixture.py` |
| `comparison-spine` | `mechanics/comparison-spine/README.md`, `mechanics/comparison-spine/parts/fixed-baseline/fixtures/frozen-same-task-v1/README.md`, `docs/COMPARISON_SPINE_GUIDE.md`, `generated/comparison_spine.json` |
| `distillation` | `mechanics/distillation/README.md`, `mechanics/distillation/parts/compost-provenance/README.md`, `evals/artifact/aoa-compost-provenance-preservation/EVAL.md`, `evals/workflow/aoa-memo-reviewed-candidate-adoption-integrity/EVAL.md` |
| `experience` | `mechanics/experience/README.md`, `mechanics/experience/parts/protocol-integrity/README.md`, `evals/boundary/aoa-experience-protocol-integrity/EVAL.md`, `mechanics/experience/parts/protocol-integrity/fixtures/experience-verdict-protocol-integrity-v1/README.md` |
| `growth-cycle` | `mechanics/growth-cycle/README.md`, `mechanics/growth-cycle/parts/diagnosis-gate/README.md`, `evals/workflow/aoa-diagnosis-cause-discipline/EVAL.md`, `docs/REVIEWED_CLOSEOUT_WRITEBACK_PROOF_INGRESS.md` |
| `method-growth` | `mechanics/method-growth/README.md`, `mechanics/method-growth/parts/candidate-lineage/README.md`, `evals/capability/aoa-candidate-lineage-integrity/EVAL.md`, `evals/boundary/aoa-owner-fit-routing-quality/EVAL.md` |
| `proof-infra` | `mechanics/proof-infra/README.md`, `mechanics/proof-infra/parts/fixture-families/README.md`, `docs/SHARED_PROOF_INFRA_GUIDE.md`, `mechanics/proof-infra/parts/reportable-contracts/schemas/report-summary.schema.json` |
| `proof-loop` | `mechanics/proof-loop/README.md`, `mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md`, `evals/workflow/aoa-verification-honesty/EVAL.md`, `generated/eval_catalog.json` |
| `proof-object` | `mechanics/proof-object/README.md`, `mechanics/proof-object/parts/eval-contracts/schemas/eval-manifest.schema.json`, `evals/workflow/aoa-verification-honesty/EVAL.md`, `generated/eval_catalog.json` |
| `publication-receipts` | `mechanics/publication-receipts/README.md`, `mechanics/publication-receipts/parts/receipt-payload/docs/EVAL_RESULT_RECEIPT_GUIDE.md`, `mechanics/publication-receipts/parts/receipt-payload/schemas/eval-result-receipt.schema.json`, `.aoa/live_receipts/AGENTS.md` |
| `questbook` | `mechanics/questbook/README.md`, `mechanics/questbook/parts/source-record-contract/schemas/quest.schema.json`, `quests/README.md`, `generated/quest_catalog.min.json` |
| `recurrence` | `mechanics/recurrence/README.md`, `mechanics/recurrence/parts/control-plane-integrity/README.md`, `evals/boundary/aoa-recurrence-control-plane-integrity/EVAL.md`, `mechanics/recurrence/parts/control-plane-integrity/tests/test_recurrence_control_plane_integrity_eval_seed.py` |
| `release-support` | `mechanics/release-support/README.md`, `mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json`, `docs/RELEASING.md`, `scripts/release_check.py` |
| `rpg` | `mechanics/rpg/README.md`, `mechanics/rpg/parts/progression-unlocks/README.md`, `mechanics/rpg/parts/progression-unlocks/schemas/progression_evidence.schema.json`, `quests/unlock/triaged/AOA-EV-Q-0009.yaml` |
| `titan` | `mechanics/titan/README.md`, `mechanics/titan/parts/seed-boundary/docs/TITAN_INCARNATION_CANARIES.md`, `mechanics/titan/parts/seed-boundary/seeds/titan_incarnation_spine_canary.yaml`, `README.md` |

## Parent Classes

### Class Membership Contract

AoA-aligned active parents are:

- `agon`
- `release-support`
- `audit`
- `boundary-bridge`
- `questbook`
- `recurrence`
- `checkpoint`
- `experience`
- `antifragility`
- `method-growth`
- `rpg`
- `growth-cycle`
- `distillation`

Evals-native active parents are:

- `proof-object`
- `proof-infra`
- `comparison-spine`
- `publication-receipts`
- `proof-loop`
- `titan`

These two sets are intentionally disjoint. A parent may move between classes
only through the same evidence-backed slice that updates this map, route cards,
topology docs, decisions, and validator constants.

`titan` is the owner-named evals-native case. The class is evals-native because
`aoa-evals` owns only the local proof-seed boundary operation. The parent name
is kept as `titan` because the proof subject is the Titan role/bearer axis;
canaries remain the `seed-boundary` part, and `aoa-agents` keeps stronger Titan law.

### AoA-aligned parents

When a proof-side operation in `aoa-evals` materializes a named center mechanic
from `Agents-of-Abyss`, the parent mechanic keeps the center name. Eval-specific
forms live below it as parts.

| Parent | Evidence cluster | Current route decision |
| --- | --- | --- |
| `agon` | Agon docs, seed configs, examples, schemas, generated registries, scripts, tests, recurrence manifests, observe-only hooks, and quest pressure span `docs/`, `config/`, `examples/`, `schemas/`, `generated/`, `scripts/`, `tests/`, `manifests/`, and `quests/`. | Parent is `agon`. Proof alignment, candidate-only registries, recurrence hooks, and wave provenance are parts and legacy behind the active route. |
| `release-support` | Release, rollback, replay, release readiness, closeout, PR handoff, changelog, release checks, and GitHub validation posture span `docs/`, `reports/`, `schemas/`, `examples/`, `scripts/`, `tests/`, and root release surfaces. | Parent must be `release-support`, not `proof-release`. Proof-release wording is artifact history or report vocabulary, not active parent topology. |
| `audit` | Runtime candidate intake, trace bridge, selected evidence packets, integrity review, artifact-to-verdict examples, runtime evidence schemas, generated candidate readers, and audit/readout reports span `docs/`, `examples/`, `schemas/`, `generated/`, `scripts/`, `tests/`, `reports/`, and source eval packages. | Parent must be `audit`. `runtime-evidence` is an evidence class and part family, not the parent mechanic. |
| `boundary-bridge` | Sibling proof refs, repo-qualified compatibility, latest-sibling canary, source-checkout resolution, orchestrator proof anchors, Phase Alpha playbook-to-eval matrix bridging, KAG/ToS/federation boundary refs, and owner handoff posture span `docs/`, `scripts/`, config, tests, examples, schemas, generated quest readers, generated matrix readers, quest source records, and sibling route references. | Parent must be `boundary-bridge`. `sibling-proof-refs`, `latest-sibling-canary`, orchestrator proof anchors, and Phase Alpha eval matrix bridging are parts inside the bridge; no `orchestrator`, `playbook-matrix`, or `phase-alpha` parent is created from class-facing proof anchors or sibling-derived matrix artifacts. |
| `questbook` | Quest source records, lifecycle docs, part-local quest schemas, generated quest catalog and dispatch, validators, human open-obligation index, and questbook decisions span `quests/`, `mechanics/questbook/parts/`, `docs/`, `generated/`, `scripts/`, and tests. | Parent remains `questbook`. Source-record and dispatch-reader schemas are parts; generated readers stay root derived companions; quest records stay source obligations, not proof verdicts. |
| `recurrence` | Recurrence control-plane bundle, return-anchor pressure, memo-recall proof pressure, recursor-readiness boundary cases, stats re-grounding boundary pressure, portable-proof beacon pressure, recurrence proof program docs, portable eval boundary guidance, control-plane eval docs, live-observation producer notes, fixtures, schema, example dossier, runner, scorer, tests, component manifests, hook bindings, generated/readout support, and neighboring return-aware bundles span `evals/`, `docs/`, `fixtures/`, `manifests/`, `schemas/`, `scripts/`, `scorers/`, `tests/`, `examples/`, and generated readers. | Parent is `recurrence`. Control-plane integrity, anchor-return, memory-recall, recursor-boundary, stats-regrounding-boundary, and portable-proof-beacons support artifacts are active part-local surfaces; source proof bundles stay under `evals/`; continuity-anchor and self-reanchor remain bundle-local until their support artifacts justify parts. |
| `checkpoint` | A2A summon return checkpoint bundle, long-horizon checkpoint restart bundle, self-agent checkpoint posture, fixture families, tests, artifact-to-verdict checkpoint examples, generated candidate readers, and quest pressure span `evals/`, `docs/`, `examples/`, `fixtures/`, `tests/`, `generated/`, `mechanics/audit/`, and `quests/`. | Parent is `checkpoint`. A2A summon return, restartable inquiry, and self-agent posture are active parts; source proof bundles stay under `evals/`; audit owns hook schema and candidate-reader builders. |
| `experience` | Experience protocol, certification gate, adoption, governance, appeal, stay-order, sealed-vote, replay-history, runtime-boundary, office, service-mesh, replay-audit, release-train, shadow, and assistant certification surfaces span `evals/`, docs, fixtures, examples, schemas, tests, and generated references. | Parent is `experience`. Protocol integrity, certification gate, adoption federation, governance/runtime boundary, and office release-train support are parts under the active route; source proof bundles stay under `evals/`. |
| `antifragility` | Antifragility posture, stress recovery, bounded repair proof, chaos/remediation sidecars, degraded-mode and recovery reports span bundles, docs, examples, fixtures, reports, schemas, audit sidecars, comparison readouts, and eval seeds. | Parent is `antifragility`. First-wave posture, stress-recovery window, and repair-proof support are parts; comparison readouts stay in `comparison-spine`; runtime evidence selection stays in `audit`; diagnosis-cause discipline routes through `growth-cycle/diagnosis-gate`, not this parent. |
| `method-growth` | Candidate-lineage integrity, owner-fit routing quality, growth-refinery selection wording, shared fixture families, bundle-local contracts, report schemas, example reports, generated catalogs, tests, and roadmap/changelog pressure span `evals/`, `fixtures/`, `generated/`, `tests/`, root selection docs, and mechanics provenance. | Parent is `method-growth`. Candidate lineage and owner landing are parts; source proof bundles stay under `evals/`; former root shared fixture families live behind active parts; diagnosis-cause discipline routes through `growth-cycle/diagnosis-gate`, repair proof stays under `antifragility`, and RPG progression/unlock surfaces route through `rpg/progression-unlocks`. |
| `rpg` | Progression evidence and unlock proof bridge surfaces span root docs, schemas, examples, generated cards, quest source records, validators, tests, recurrence manifests, and AoA center `progression-unlocks` owner split. | Parent is `rpg`. Progression evidence and unlock proof are active `progression-unlocks` support surfaces under the RPG parent; quest records stay in `quests/`; old root paths are provenance only. |
| `growth-cycle` | Diagnosis-cause discipline, deferred repair, closeout, harvest, writeback, repeated-window, progression, and quest pressure span `evals/`, `docs/`, `mechanics/`, `quests/`, generated readers, and tests. The first active proof operation is `aoa-diagnosis-cause-discipline`, with support notes, example report, integrity check, and existing deferrals from `method-growth`. | Parent is `growth-cycle`. `diagnosis-gate` is the active part. Repair proof stays under `antifragility/repair-proof`; longitudinal movement stays under `comparison-spine`; RPG progression/unlock proof stays under `rpg`; closeout, harvest, quest-promotion, and owner-followthrough stay deferred until separate eval-side operations exist. |
| `distillation` | Compost provenance preservation and reviewed runtime distillation candidate adoption span `evals/`, former `fixtures/`, `mechanics/experience/`, `docs/`, `generated/`, reports, tests, and audit bridge references. The proof-side operation is not generic memo quality: it checks whether abstraction or candidate adoption preserves provenance, review state, candidate posture, receipt visibility, recall inspectability, and promotion boundaries. | Parent is `distillation`. `compost-provenance` and `runtime-candidate-adoption` are active parts. Source proof bundles stay under `evals/`; runtime-pack hook metadata stays under `audit`; generic adoption/consent/compatibility stays under `experience`; memo recall, memo contradiction, and confirmed writeback-act proof stay outside this parent until separate evidence proves a Distillation operation. |

### Evals-native parents

These parents are not named center AoA mechanics. They are allowed only because
`aoa-evals` owns the proof organ operation itself. Most names are local proof
operations such as `proof-object` or `comparison-spine`; `titan` is the
owner-named evals-native exception, where the local operation is the proof-seed
boundary and the stronger Titan truth stays outside `aoa-evals`.

| Parent | Evidence cluster | Current route decision |
| --- | --- | --- |
| `proof-object` | Source eval claims, `EVAL.md`, `eval.yaml`, authoring template, frontmatter and manifest schemas, proof-surface contracts, generated catalogs, capsule/section readers, lifecycle checks, and completeness review span `evals/`, `mechanics/proof-object/parts/`, `docs/`, `scripts/`, `tests/`, and `generated/`. | Valid evals-native parent. `eval-authoring` and `eval-contracts` are parts; source eval packages stay under `evals/`; generated readers stay derived companions. |
| `proof-infra` | Shared fixtures, runners, scorers, schemas, templates, report contracts, generic fixture-family support, reportable runner/scorer/schema contracts, generated proof artifact readers, validators, tests, and bundle-local contracts span root infrastructure districts, mechanic-local parts, and source eval packages. | Valid evals-native parent. It routes shared proof infrastructure while keeping bundle meaning stronger. Generic shared fixture families may live under `parts/fixture-families`; shared reportable contracts may live under `parts/reportable-contracts`; domain-specific families and schemas stay under their owning mechanic parts. |
| `comparison-spine` | Baseline, regression, same-task, output-vs-process, peer compare, repeated-window, stress-recovery, comparison guide, generated spine, fixture families, reports, examples, schemas, and tests form a cross-root comparison operation. | Valid evals-native parent. It owns comparison posture plus fixed-baseline, peer-compare, and longitudinal-window fixture/report parts. |
| `publication-receipts` | Eval result receipt guide, receipt schema, stats envelope mirror, receipt example, live publisher, local live receipt log, intake dry review, and receipt tests form the publication sidecar operation. | Valid evals-native parent. Receipts stay weaker than reports and source eval packages. |
| `proof-loop` | Selection route, source proof object, proof infra, candidate evidence, sibling refs, bundle-local report, optional receipt, route-smoke report, decisions, and tests form a local proof loop operation. | Valid evals-native parent if it remains a coordinator and does not steal meaning from the packages that own each step. |
| `titan` | Titan incarnation and summon discipline docs plus 37 Titan seed canaries in the former `evals/` district form an owner-named proof-seed boundary operation. Stronger Titan role, bearer, summon, and incarnation law belongs to `aoa-agents`; memo posture belongs to `aoa-memo`; runtime belongs to `abyss-stack`. | Parent is `titan`, not `titan-canaries`. Canary YAML files are seed-boundary parts, not the package name, and the local parent does not transfer Titan authority into `aoa-evals`. |

## Former Wrong Parent Forms

The following names are accepted only as legacy vocabulary, artifact forms, or
evidence-class wording. They must not return as active parent packages:

| Wrong parent | Correct parent | Reason |
| --- | --- | --- |
| `agon-proof` | `agon` | Replaces the AoA-aligned Agon mechanic with a proof-organ suffix. |
| `titan-canaries` | `titan` | Names the artifact form instead of the Titan proof-seed mechanic. |
| `proof-release` | `release-support` | Replaces the AoA-aligned release-support mechanic with proof-organ adjective. |
| `runtime-evidence` | `audit` | Names an evidence class instead of the audit mechanic that receives, constrains, and routes it. |
| `sibling-proof-refs` | `boundary-bridge` | Names one bridge payload instead of the boundary-bridge mechanic. |
| `repair` | `antifragility/repair-proof` | Names a stage or artifact pressure instead of the active bounded repair-proof part; future Growth Cycle repair stages still need separate evidence. |

The following parents are active and must stay constrained by their package
cards and validators:

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
- `release-support`
- `titan`
- `proof-object`
- `proof-infra`
- `comparison-spine`
- `publication-receipts`
- `proof-loop`

This list is an active topology allowlist, not a brainstorming list.
`scripts/validate_repo.py` rejects undeclared top-level
`mechanics/<parent>/` directories. A future parent must first prove an
AoA-aligned or evals-native cross-root evidence cluster, then update this file,
the package route cards, `docs/PROOF_TOPOLOGY.md`, `docs/decisions/`, and the
validator allowlist in one slice.

Allowed parents must keep their active route form complete: `AGENTS.md`,
`README.md`, and `PARTS.md` must exist, and `PARTS.md` must describe inputs,
outputs, owner split, stop-lines, and validation for the package parts.
Every concrete `mechanics/<parent>/parts/<part>/README.md` must also expose
`## Inputs`, `## Outputs`, `## Stronger Owner Split`, `## Stop-Lines`, and
`## Validation`, and the parent `PARTS.md` must route that part by README path
or exact part slug so parts cannot become orphan topology.
Every parent `PROVENANCE.md` must route readers through the active form first
and then bridge only into the owning legacy archive. Archive details belong
inside `legacy/`.

## Next Evidence Pass

The next package must still come from local proof pressure, not symmetry.
There is no remaining named candidate promoted by this slice.

Future Growth Cycle parts remain possible, but each must prove its own local
eval-side operation before entering `mechanics/growth-cycle/parts/`:

- `repair-cycle` must not steal `antifragility/repair-proof`;
- `progression-lift` must not steal `rpg/progression-unlocks` or
  `comparison-spine/longitudinal-window`;
- `reviewed-closeout-chain`, `donor-harvest`, `quest-promotion`, and
  `owner-followthrough` must not promote quest or ingress pressure into active
  topology without source surfaces, contracts, stop-lines, and validation.

### Current next-route reading

`experience`, `antifragility`, `method-growth`, `rpg`, `growth-cycle`, and
`distillation` are
no longer next-route candidates; they are active AoA-aligned packages under
`mechanics/experience/`, `mechanics/antifragility/`,
`mechanics/method-growth/`, `mechanics/rpg/`, and
`mechanics/growth-cycle/`, and `mechanics/distillation/`.

The current `growth-cycle` package is deliberately narrow. It activates only:

- `aoa-diagnosis-cause-discipline` as `diagnosis-gate` cause-hypothesis
  discipline.

It keeps these separations explicit:

- `aoa-repair-boundedness` remains antifragility `repair-proof` support;
- `aoa-candidate-lineage-integrity` and `aoa-owner-fit-routing-quality` remain
  active method-growth parts rather than all-purpose growth-cycle evidence;
- `aoa-longitudinal-growth-snapshot` and repeated-window reports remain
  longitudinal movement under comparison-spine;
- `rpg/progression-unlocks` remains RPG progression and unlock proof support,
  not a generic growth-cycle proof score;
- closeout, harvest, and repeated blind-spot quest pressure remain obligations
  or ingress context until a later pass proves an active part;
- `docs/REVIEWED_CLOSEOUT_WRITEBACK_PROOF_INGRESS.md` is one such ingress
  anchor, not an active `reviewed-closeout-chain` or writeback stage part.

The current `distillation` package is deliberately narrow. It activates only:

- `aoa-compost-provenance-preservation` as `compost-provenance`;
- `aoa-memo-reviewed-candidate-adoption-integrity` as
  `runtime-candidate-adoption`.

It keeps these separations explicit:

- `aoa-memo-recall-integrity` routes through
  `recurrence/memory-recall` as memo recall integrity proof, not Distillation;
- `aoa-memo-contradiction-integrity` remains lifecycle-aware contradiction
  visibility proof, not Distillation;
- `aoa-memo-writeback-act-integrity` remains confirmed base writeback-act
  proof, not reviewed distillation candidate adoption;
- `docs/REVIEWED_CLOSEOUT_WRITEBACK_PROOF_INGRESS.md` may explain why the
  reviewed-candidate gap matters, but it is root ingress rather than an active
  Distillation source surface;
- `aoa-witness-trace-integrity` remains upstream witness trace integrity;
- artifact-to-verdict `distillation_pack` hook metadata remains audit bridge
  support until a bundle-local Distillation part accepts a specific read.

## Legacy Rule

Legacy is provenance behind an active mechanic.

Active route comes first: `README.md`, `PARTS.md` or `DIRECTION.md`, parts,
owner split, stop-lines, and validation. Legacy is entered through the single
`PROVENANCE.md` bridge; after that bridge, the legacy archive owns its own
details.

Legacy must not become:

- the active package name;
- a trash folder for unresolved files;
- a timebox table without provenance;
- the place where new work begins.

When old path or name compatibility remains, keep it mapped to the current
active part and validation route.
