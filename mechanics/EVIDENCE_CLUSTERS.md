# Mechanics Evidence Clusters

## Role

`mechanics/EVIDENCE_CLUSTERS.md` is the parent-mechanic evidence gate for the
`aoa-evals` mechanics atlas. It answers one routing question:

`proposed parent or moved payload -> evidence class -> parent route -> part route -> validation guard`

Use it when an agent needs to classify root-district pressure, prove that a
parent operation is real, or recover why an active parent is AoA-aligned or
evals-native.

## Operating Card

| Field | Route |
| --- | --- |
| role | parent-mechanic evidence gate and cross-root evidence map |
| entry | use before moving root-district artifacts into or between mechanics |
| input | proposed parent name, old root path family, artifact class, report/canary/form cluster, or payload movement pressure |
| output | allowed parent class, evidence dimensions, root-district posture, mechanic boundary, and validation guard |
| owner | `mechanics/AGENTS.md` for mutation law; this map for parent evidence; parent `README.md`/`DIRECTION.md`/`PARTS.md` for local operation |
| next route | `docs/architecture/PROOF_TOPOLOGY.md`, `mechanics/README.md`, parent route cards, part READMEs, and `docs/decisions/` |
| tools | root validator, semantic route-card validator, package-local builders, and focused validator tests named by the touched parent |
| validation | [mechanics/AGENTS.md#validation](AGENTS.md#validation) and the nearest mechanics route card |

## Evidence Standard

Read parent readiness as an operating checklist:

| Evidence dimension | Parent-ready route |
| --- | --- |
| meaning | the recurring proof-side operation has doctrine, posture, or route language |
| proof pressure | bounded claims or evaluation pressure repeat across more than one source surface |
| contracts and payloads | schemas, contracts, examples, fixtures, seeds, reports, receipts, or support docs need a shared operation home |
| builders and readouts | validators, tests, builders, generated readers, reports, or receipts exercise the operation |
| owner split | stronger-owner truth and eval-side proof support are named together |
| lineage | old names have a current provenance bridge and active route |

Single documents, reports, and canary forms route as parts under the right parent;
parent status comes from the repeated operation around them. Owner-named
parents stay valid when the local proof operation is real, artifact forms stay
below the parent as parts, and the stronger-owner split is explicit.

## Root District Reconnaissance Ledger

This root-district ledger is the first gate before package growth. It records
what each named root district currently owns, where active payloads route, and
which validation guard keeps the route anchored to current topology.

| District | Authority class | Current root posture | Mechanics relationship | Validation guard |
| --- | --- | --- | --- | --- |
| `docs` | source guidance, topology, decisions, and repo-wide proof interpretation | root-owned source guidance stays in `docs/`; mechanic-owned docs live under the owning part when a narrower operation owns the read | mechanics may route docs as evidence, but mechanic-owned docs stay part-local and root docs remain guidance or provenance | `validate_root_authored_route_residue_surfaces`, `validate_proof_topology_surfaces`, and decision-token checks |
| `evals` | source proof object district | `evals/**/EVAL.md` and `evals/**/eval.yaml` stay root-owned source proof objects; source eval packages stay out of mechanics | mechanics provide proof-object, infra, comparison, audit, quest, or report support around eval packages while eval meaning stays on source proof objects | per-eval validation, source-eval route residue, catalog builders, and root route-card validation |
| `fixtures` | shared proof infrastructure compatibility district | route-card-only compatibility posture; active fixture families live under proof-infra or domain mechanic parts | generic fixtures route to `mechanics/proof-infra/parts/fixture-families/fixtures/`, while domain fixtures live under owning mechanic parts | root route-card guard plus active-mechanic and mechanic-payload route residue checks |
| `schemas` | proof contract compatibility district | route-card-only compatibility posture; active schema payloads live under proof-object, proof-infra, questbook, or domain mechanic parts | eval contract schemas route to `mechanics/proof-object/parts/eval-contracts/schemas/`, shared contracts to proof-infra, quest schemas to questbook, and domain schemas to owning parts | root route-card guard plus schema-aware bundle, quest, and mechanic validation |
| `examples` | public-safe example compatibility district | route-card-only compatibility posture; active example payloads live beside their owning source | bundle examples stay in `evals/**/examples/`; audit, receipt, bridge, and domain examples live under owning mechanic parts | root route-card guard plus active route residue checks |
| `scripts` | repo-wide builders, validators, and release helpers | root scripts stay repo-wide and deterministic; mechanic-owned scripts live under the owning part | mechanics call or own part-local builders only when the operation owns the payload, while root `scripts/validate_repo.py` guards topology | touched-command checks, catalog-check route, and root repository validation route |
| `tests` | repo-wide validation district | root tests stay repo-wide for repository contracts, catalogs, generated readers, semantic cards, and topology guards | mechanic-owned tests live under `mechanics/<mechanic>/parts/<part>/tests/` next to the operation they constrain | focused pytest commands, part-local test placement guard, and full `tests/test_validate_repo.py` |
| `config` | configuration compatibility district | route-card-only compatibility posture; active config payloads live with the owning operation | Agon configs route to `mechanics/agon/parts/*/config/`; sibling canary config routes to boundary-bridge | root route-card guard and repo-config route residue checks |
| `manifests` | recurrence/component manifest compatibility district | route-card-only compatibility posture; active manifest payloads live with the owning lifecycle part | Agon manifests route to Agon parts; recurrence manifests route to `mechanics/recurrence/parts/` such as control-plane and portable-proof-beacons | root route-card guard plus mechanic-payload route residue checks |
| `generated` | repo-wide derived readers | root generated surfaces remain derived readers tied to source proof objects | part-local generated readers live under the owning mechanic part when the part owns the source and builder | generated route residue checks, builder check modes, and catalog-check route |
| `reports` | report compatibility district | route-card-only compatibility posture; active report payloads live with bundle or mechanic owners | bundle reports stay bundle-local; proof-loop, comparison, receipts, and release-support reports live under owning mechanic parts such as `mechanics/release-support/parts/` | root route-card guard, report index validation, and release-support report checks |
| `runners` | shared runner contract compatibility district | route-card-only compatibility posture; active runner contracts live under proof-infra or bundle-local pointers | active shared runner contract lives under `mechanics/proof-infra/parts/reportable-contracts/runners/`, while bundle-local runner contracts point to it through `runner_surface_path` | root route-card guard, bundle runner contract checks, and proof-infra reportable-contract validation |
| `scorers` | shared scorer helper compatibility district | route-card-only compatibility posture; active scorer helpers live under proof-infra or owning mechanic parts | active shared scorer helper lives under `mechanics/proof-infra/parts/reportable-contracts/scorers/`, while domain scorers live under owning mechanic parts | root route-card guard, scorer helper checks, schema validation, and proof-infra reportable-contract validation |
| `templates` | eval template compatibility district | route-card-only compatibility posture; active template payloads live under proof-object eval authoring | active eval authoring template lives under `mechanics/proof-object/parts/eval-authoring/templates/` | root route-card guard, proof-object eval-authoring checks, and root repository validation route |
| `quests` | source quest record district | schema-backed lane/state source quest records stay under `quests/`; generated quest readers remain derived; markdown quest-note lineage belongs behind the owning mechanic `PROVENANCE.md` | `mechanics/questbook/parts/` owns source-record schemas and dispatch-reader contracts; source quest records stay under `quests/` | quest route validation, generated quest catalog checks, and catalog-check route |
| `mechanics` | operation atlas | active only for proven parent operations with route cards, `DIRECTION.md`, parts, provenance, and validation | `mechanics/EVIDENCE_CLUSTERS.md` gates parent names and cross-root evidence before payload movement | parent allowlist, part README contracts, direction/provenance guards, and legacy/accounting checks |

## Residual Root-authored Surface Classification

This residual ledger covers root-authored files that remain under `docs/`,
`scripts/`, and `tests/` after mechanic-owned payload movement. These districts
carry authored guidance, builders, validators, and tests, so every top-level
file plus the focused root validator modules are classified as root-owned
guidance, root-owned builder/validator, or root-owned test coverage, and every
row states where mechanic-owned payload belongs.

| Surface | Root role | Mechanic boundary | Validation guard |
| --- | --- | --- | --- |
| `docs/AGENTS.md` | root-owned docs route card for proof-meaning edits | mechanic-owned payload guidance belongs in nearest `mechanics/*/AGENTS.md` | semantic and nested AGENTS validation |
| `docs/operations/AGENTS_ROOT_REFERENCE.md` | root-owned preserved reference for full historical root guidance | mechanic-owned payload history must route through package `PROVENANCE.md` and legacy indexes | root design and route-residue validation |
| `docs/architecture/AGENT_INDEX.md` | root-owned agent-facing pass-through index from repo to authority class, operation, mechanic parent, part, payload, and validation | mechanic-owned payload details belong in `mechanics/EVIDENCE_CLUSTERS.md`, parent maps, part READMEs, and local route cards | agent-index surface validation and root-authored classification |
| `docs/architecture/AOA_EVALS_MCP_CONTRACT.md` | root-owned MCP access-plane contract for bounded proof selection, inspection, runtime-candidate templates, and report skeletons | mechanic-owned payload remains in source bundles, generated-reader builders, and active mechanics; runnable MCP service code belongs in `abyss-stack:mcp/services/aoa-evals-mcp/` | MCP contract route, proof topology validation, and runtime-candidate reader checks |
| `docs/architecture/ARCHITECTURE.md` | root-owned technical proof model | mechanic-owned payload architecture lives in parent `DIRECTION.md` and part READMEs | proof topology validation |
| `docs/architecture/ROUTE_RESIDUE_GUARDS.md` | root-owned route-residue guard contract map | mechanic-owned payload route details remain under active mechanics, source bundles, or generated builders instead of hidden root paths | route-residue validation family |
| `docs/architecture/topology_contract.yaml` | root-owned docs topology contract | mechanic-owned payload docs stay under owning mechanic parts; this contract only classifies docs authority folders | docs topology validation |
| `docs/guides/ARTIFACT_PROCESS_SEPARATION_GUIDE.md` | root-owned guide for process/artifact reading | mechanic-owned payload examples and reports live under owning parts | root-authored route-residue validation |
| `docs/guides/BASELINE_COMPARISON_GUIDE.md` | root-owned baseline comparison guide | mechanic-owned payload comparison fixtures and reports live under `mechanics/comparison-spine/parts/` | comparison-spine and root-authored route guards |
| `docs/guides/BLIND_SPOT_DISCLOSURE_GUIDE.md` | root-owned blind-spot disclosure guide | mechanic-owned payload blind-spot evidence lives with bundles, reports, or owning mechanics | bundle and report validation |
| `docs/guides/COMPARISON_SPINE_GUIDE.md` | root-owned comparison-spine interpretation guide | mechanic-owned payload comparison state lives under `mechanics/comparison-spine/parts/` | comparison-spine focused and route-residue checks |
| `docs/guides/EVAL_PHILOSOPHY.md` | root-owned epistemic posture guide | mechanic-owned payload proof operations live in mechanic packages | root design validation |
| `docs/guides/EVAL_REVIEW_GUIDE.md` | root-owned review posture guide | mechanic-owned payload review artifacts live under bundle-local or part-local reports | repo validation and report index checks |
| `docs/guides/EVAL_RUBRIC.md` | root-owned rubric interpretation guide | mechanic-owned payload scoring helpers live under proof-infra or bundle-local contracts | schema and proof-infra validation |
| `docs/guides/FIXTURE_SURFACE_GUIDE.md` | root-owned fixture interpretation guide | mechanic-owned payload fixture families live under proof-infra or owning mechanic parts | root route-card guard and fixture-family checks |
| `docs/architecture/LEGACY_NAMING.md` | root-owned legacy naming posture guide | mechanic-owned payload legacy details live inside package `legacy/` archives behind package `PROVENANCE.md` | legacy naming and provenance validators |
| `docs/guides/PORTABLE_EVAL_BOUNDARY_GUIDE.md` | root-owned portability boundary guide | mechanic-owned payload portable beacons live under recurrence parts when proven | recurrence and root-authored route guards |
| `docs/architecture/PROOF_TOPOLOGY.md` | root-owned authority-class topology | mechanic-owned payload topology lives in `mechanics/EVIDENCE_CLUSTERS.md`, parent `DIRECTION.md`, and parts | proof topology validation |
| `docs/operations/QUESTBOOK_EVAL_INTEGRATION.md` | root-owned quest/eval integration guide | mechanic-owned payload quest schemas and dispatch contracts live under `mechanics/questbook/parts/` | quest route and generated quest checks |
| `docs/README.md` | root-owned docs index | mechanic-owned payload docs route to owning mechanic docs and READMEs | root-authored route-residue validation |
| `docs/testing/AGENTS.md` | root-owned testing route card for test-topology edits | mechanic-owned payload tests stay under owning `mechanics/*/parts/*/tests/` or source-bundle reports | semantic AGENTS and test topology validation |
| `docs/testing/TEST_TOPOLOGY.md` | root-owned test topology map for boundary coverage | mechanic-owned payload test fixtures, traces, and reports remain under owning mechanics or eval bundles | test topology inventory validation |
| `docs/testing/test_inventory.json` | root-owned descriptive test inventory read model | mechanic-owned payload fixtures and expected evidence stay in owning parts and bundles | test topology inventory validation |
| `docs/validation/AGENTS.md` | root-owned validation route card for validator and lane topology edits | mechanic-owned payload validation commands remain part-local when the mechanic owns the source and generated companions | semantic AGENTS and validation topology checks |
| `docs/validation/COMMAND_AUTHORITY.md` | root-owned validation command authority map | mechanic-owned payload command details stay in owning part `VALIDATION.md`, scripts, and route cards | validation lane manifest tests |
| `docs/validation/SCRIPT_TOPOLOGY.md` | root-owned script topology map for builders, validators, audits, gates, and canaries | mechanic-owned payload scripts stay under owning part `scripts/` directories | script topology inventory validation |
| `docs/validation/VALIDATOR_TOPOLOGY.md` | root-owned validator layer topology map | mechanic-owned payload validators stay part-local unless promoted to root cross-surface guards | validation topology inventory checks |
| `docs/validation/script_inventory.json` | root-owned descriptive script inventory read model | mechanic-owned payload script implementation remains under owning parts and is only referenced here by boundary | script topology inventory validation |
| `docs/validation/validation_lanes.json` | root-owned validation lane command manifest | mechanic-owned payload commands are referenced by lane but owned by their local scripts and part route cards | lane loader, CI gate, and release gate tests |
| `docs/validation/validator_inventory.json` | root-owned descriptive validator inventory read model | mechanic-owned payload validator meaning stays in source docs, bundles, and part-local validation files | validation topology inventory checks |
| `docs/guides/REGRESSION_PROOF_SURFACES.md` | root-owned regression proof guide | mechanic-owned payload regression fixtures and reports live under comparison-spine or bundles | comparison and bundle validation |
| `docs/operations/RELEASING.md` | root-owned release process guide | mechanic-owned payload release state artifacts live under `mechanics/release-support/parts/` | release-support and release_check validation |
| `docs/guides/REPEATED_WINDOW_DISCIPLINE_GUIDE.md` | root-owned repeated-window discipline guide | mechanic-owned payload repeated-window reports live under comparison-spine parts | comparison-spine validation |
| `docs/operations/REVIEWED_CLOSEOUT_WRITEBACK_PROOF_INGRESS.md` | root-owned ingress note for deferred closeout/writeback pressure | mechanic-owned payload activates only through a proven growth-cycle, distillation, audit, or questbook part | root-authored route guards and future decision review |
| `docs/guides/SCORE_SEMANTICS_GUIDE.md` | root-owned score semantics guide | mechanic-owned payload scorers live under proof-infra or owning parts | scorer and schema validation |
| `docs/guides/SHARED_PROOF_INFRA_GUIDE.md` | root-owned shared proof infrastructure guide | mechanic-owned payload shared contracts live under `mechanics/proof-infra/parts/` | proof-infra validation |
| `docs/guides/VERDICT_INTERPRETATION_GUIDE.md` | root-owned verdict interpretation guide | mechanic-owned payload verdict models live under source bundles or owning mechanic parts | bundle and root-authored route validation |
| `docs/guides/BOUNDARY_ROUTE_CHECKLIST.md` | root-owned boundary route checklist | mechanic-owned payload stop-lines live in parent `DIRECTION.md`, `PARTS.md`, and part READMEs | direction and part README validators |
| `scripts/AGENTS.md` | root-owned scripts route card | mechanic-owned payload scripts live under owning `mechanics/*/parts/*/scripts/` | semantic AGENTS and script route validation |
| `scripts/build_catalog.py` | root-owned catalog builder | mechanic-owned payload builders live part-local and feed generated companions; root catalog truth stays with the root builder | catalog check and repo validation |
| `scripts/eval_capsule_contract.py` | root-owned generated capsule contract helper | mechanic-owned payload capsule logic moves into a mechanic part only when the part owns that generated reader | downstream feed tests |
| `scripts/eval_catalog_contract.py` | root-owned catalog contract helper | mechanic-owned payload bundle support remains part-local while root catalog remains repo-wide derived truth | catalog and downstream feed tests |
| `scripts/eval_comparison_spine_contract.py` | root-owned comparison-spine generated contract helper | mechanic-owned payload comparison reports and fixtures live under comparison-spine parts | comparison spine generated checks |
| `scripts/eval_proof_contract_helpers.py` | root-owned proof contract helper library | mechanic-owned payload validators may import helpers but belong under owning parts | full repo validation |
| `scripts/eval_section_contract.py` | root-owned section-reader contract helper | mechanic-owned payload section readers stay generated companions tied to source truth | downstream feed tests |
| `scripts/generate_decision_indexes.py` | root-owned decision-index read-model builder | mechanic-owned payload lookup belongs in owning decision notes and generated `docs/decisions/indexes/` read models | decision index generated parity check |
| `scripts/generate_eval_report_index.py` | root-owned report-index builder | mechanic-owned payload reports remain bundle-local or part-local and feed the root report index | report index check |
| `scripts/ci_gate.py` | root-owned lane execution entrypoint for CI and local gate selection | mechanic-owned payload commands remain in their owning scripts and part-local validation surfaces | validation lane and release command tests |
| `scripts/release_check.py` | root-owned release gate runner | mechanic-owned payload release audit artifacts live under release-support parts | release gate route in root `AGENTS.md#verify` |
| `scripts/validation_lanes.py` | root-owned validation lane manifest loader | mechanic-owned payload command meaning stays in docs/validation manifest entries and owning scripts | validation lane loader tests |
| `scripts/validate_nested_agents.py` | root-owned nested AGENTS validator | mechanic-owned payload route cards live locally and are checked from root validation | nested AGENTS validation |
| `scripts/validate_repo.py` | root-owned repository validator | mechanic-owned payload validators may live part-local, while this file guards cross-repo topology | focused and full repo validation |
| `scripts/validate_semantic_agents.py` | root-owned semantic AGENTS validator | mechanic-owned payload guidance lives in local route cards and is checked here | semantic AGENTS validation |
| `scripts/validators/__init__.py` | root-owned validator module package marker | mechanic-owned payload validators belong under owning mechanic parts unless the root validator owns the cross-surface guard | validator module import smoke through repo validation |
| `scripts/validators/agon.py` | root-owned Agon route validator module | mechanic-owned payload Agon parent route cards, part README contracts, and Agon decisions stay under Agon; this module checks bounded part-contract posture without owning live verdicts, center law, rank/trust mutation, arena execution, KAG promotion, Tree of Sophia canon writes, or part-local generated registry parity | Agon route/part-contract validation and repo validation |
| `scripts/validators/antifragility.py` | root-owned Antifragility route validator module | mechanic-owned payload Antifragility route cards, parts index, posture, stress recovery, repair proof, stress-window doc, provenance, and Antifragility decisions stay under Antifragility; this module checks bounded stress/repair support posture without owning runtime repair, cleanup authority, stats truth, memory truth, or growth-cycle completion | Antifragility route validation and repo validation |
| `scripts/validators/audit.py` | root-owned audit route validator module | mechanic-owned payload selected evidence packets, artifact verdict hooks, candidate readers, integrity review route cards, provenance, and legacy bridge stay under audit; this module checks audit route posture below runtime owners and source bundle review | audit route validation and repo validation |
| `scripts/validators/artifact_hooks.py` | root-owned artifact hook contract-ref validator module | mechanic-owned payload examples stay under audit/checkpoint parts while sibling truth remains repo-qualified | trace/eval hook validation and sibling-ref resolution |
| `scripts/validators/boundary_bridge.py` | root-owned boundary-bridge route validator module | mechanic-owned payload compatibility maps, sibling canary route cards and matrix shape, orchestrator proof anchors, provenance, legacy bridge, and repo-validation workflow-pin hygiene stay under boundary-bridge; live canary execution remains a separate latest-sibling gate | boundary-bridge route, workflow-pin, matrix shape, and repo validation |
| `scripts/validators/checkpoint.py` | root-owned checkpoint route validator module | mechanic-owned payload checkpoint route cards, A2A summon return, restartable-inquiry, self-agent-posture, posture doc, provenance, and checkpoint decisions stay under checkpoint; this module checks checkpoint support posture without owning runtime activation, memory canon, self-repair acceptance, or child-output quality | checkpoint route validation and repo validation |
| `scripts/validators/common.py` | root-owned shared validator helper module | mechanic-owned payload stays with focused validators and owning mechanics; this helper carries only shared issue, JSON, schema, and mapping helpers without mechanic meaning ownership | validator topology validation and repo validation |
| `scripts/validators/comparison_spine.py` | root-owned comparison-spine validator module | mechanic-owned payload comparison route cards, fixtures, readouts, provenance, and anti-overread boundaries stay under comparison-spine; this module checks comparison support posture below source bundle meaning and generated projection parity | comparison-spine route validation and repo validation |
| `scripts/validators/distillation.py` | root-owned Distillation route validator module | mechanic-owned payload Distillation route cards, compost provenance, runtime-candidate adoption, provenance, and Distillation decisions stay under Distillation; this module checks bounded distillation support posture without owning ToS canon, memory canon, runtime promotion, live receipt append behavior, KAG lift, or owner-local acceptance | Distillation route validation and repo validation |
| `scripts/validators/docs_decisions.py` | root-owned decision-index read-model validator module | mechanic-owned payload decision meaning stays in source decisions; this module checks metadata and generated lookup parity | decision index generated parity and repo validation |
| `scripts/validators/docs_routes.py` | root-owned docs route-map validator module | mechanic-owned payload docs route to owning mechanics or bundles; this module checks root docs routes and links | docs route contracts and repo validation |
| `scripts/validators/docs_topology.py` | root-owned docs topology validator module | mechanic-owned payload docs stay under owning mechanics; this module checks docs folder topology and topology contract | docs topology contract and repo validation |
| `scripts/validators/eval_bundles.py` | root-owned source eval tree validator module | mechanic-owned payload support parts remain outside bundle-local claim truth; this module checks eval source topology | eval source topology validation and repo validation |
| `scripts/validators/evidence_readouts.py` | root-owned evidence/readout orchestrator module | mechanic-owned payload reports, runtime evidence, receipt logs, release-support reports, phase-alpha matrices, Titan canaries, and generated read models stay with focused validators and owning mechanic parts; this module only wires repo-wide and target-eval readout checks with injected context | evidence/readout validation and repo validation |
| `scripts/validators/experience.py` | root-owned Experience route validator module | mechanic-owned payload Experience route cards, protocol, certification, adoption, governance/runtime-boundary, office release-train, provenance, and Experience decisions stay under Experience; this module checks bounded Experience support posture without owning runtime activation, operator certification, adoption truth, routing authorship, memory canon, or KAG/ToS truth | Experience route validation and repo validation |
| `scripts/validators/generated_parity.py` | root-owned generated/read-model parity validator module | mechanic-owned payload generated companions stay part-local unless promoted through root readers; this module checks catalog, capsule, section, comparison-spine, report-index route, quest-reader route, and decision-index projections without defining source meaning | generated parity contracts and repo validation |
| `scripts/validators/growth_cycle.py` | root-owned Growth-cycle diagnosis validator module | mechanic-owned payload Growth-cycle route cards, parts index, diagnosis-gate, provenance, Growth-cycle decisions, and repair-diagnosis boundary rationale stay under Growth-cycle and decisions; this module checks diagnosis support posture without owning repair success, progression score, closeout acceptance, memory canon, runtime activation, hidden automation, or owner-local landing | Growth-cycle route validation and repo validation |
| `scripts/validators/mechanic_legacy.py` | root-owned mechanic legacy/provenance boundary validator module | mechanic-owned payload archive details stay in `legacy/`; this module checks active-to-archive PROVENANCE bridges, archive route language, raw payload accounting, and active legacy parent wording without defining mechanic payload truth | mechanic legacy/provenance validation and repo validation |
| `scripts/validators/mechanic_parents.py` | root-owned mechanic parent route validator module | mechanic-owned payload meaning stays with owning parent and part surfaces; this module checks parent route-card coverage, direction contracts, guidance doc allowlists, mechanics parent allowlist, and lower parts index command hygiene without defining payload truth | mechanic parent route/guidance validation and repo validation |
| `scripts/validators/mechanic_parts.py` | root-owned mechanic part contract validator module | mechanic-owned payload meaning stays with the owning mechanic part; this module checks part README contracts, payload inventory, source refs, PARTS index synchronization, index/route heading roles, and validation command reachability without defining payload truth | mechanic part contract, payload inventory, parts index, index-role, validation command, and repo validation |
| `scripts/validators/mechanics.py` | root-owned mechanics topology validator module | mechanic-owned payload classification stays in owning mechanic surfaces; this module checks mechanics root route tokens, parent class/evidence ledgers, root-district reconnaissance, part-local test placement route, and residual root-authored surface classification | mechanics root route, mechanic parent topology, root-district reconnaissance, root-authored classification, and repo validation |
| `scripts/validators/mechanics_routes.py` | root-owned mechanics route-domain orchestrator module | mechanic-owned payload stays in focused mechanic validators, route cards, parts, provenance, and local test surfaces; this module only aggregates mechanic route-domain checks and injected route-token context without defining payload truth | mechanics route-domain validation and repo validation |
| `scripts/validators/method_growth.py` | root-owned Method-growth route validator module | mechanic-owned payload Method-growth route cards, candidate-lineage, owner-landing, provenance, and Method-growth decisions stay under Method-growth; this module checks bounded lineage/owner-fit support posture without owning final owner truth, derivative first-authoring, memory canon, seed truth, stats truth, diagnosis-cause ownership, or repair success | Method-growth route validation and repo validation |
| `scripts/validators/phase_alpha_matrix.py` | root-owned Phase Alpha matrix validator module | mechanic-owned payload matrix plan stays under boundary-bridge and sibling truth stays in aoa-playbooks; this module checks generated matrix parity and strict sibling compatibility | phase-alpha matrix parity and repo validation |
| `scripts/validators/proof_infra.py` | root-owned proof-infra validator module | mechanic-owned payload reusable fixture families, runner/scorer/schema contracts, provenance, and shared proof-infra guidance stay under proof-infra; this module checks reusable support posture below source bundle meaning | proof-infra route/shared-support validation and repo validation |
| `scripts/validators/proof_loop.py` | root-owned proof-loop validator module | mechanic-owned payload route-smoke and bundle-local report support stay under proof-loop and source eval bundles; this module checks loop routeability without promoting receipts, runtime evidence, or sibling truth | proof-loop route/report validation and repo validation |
| `scripts/validators/proof_object.py` | root-owned proof-object validator module | mechanic-owned payload authoring templates, eval contract schemas, source-authority route cards, provenance, and part decisions stay under proof-object; this module checks source proof-object routeability without owning generated catalog parity | proof-object route validation and repo validation |
| `scripts/validators/publication_receipts.py` | root-owned publication receipt validator module | mechanic-owned payload route cards, receipt shape, stats-envelope mirror, dry-review report, and live append log stay under publication-receipts and `.aoa/live_receipts/`; this module checks receipt sidecar posture below reviewed reports | publication receipt route/boundary validation and repo validation |
| `scripts/validators/questbook.py` | root-owned Questbook source, projection, route, and part-contract validator module | mechanic-owned payload source records, route cards, part owner-split contracts, generated dispatch readers, and RPG progression bridge surfaces stay under Questbook/RPG; this module checks source/projection and route posture without owning live task assignment, proof-surface promotion, owner acceptance, or runtime dispatch | questbook source/projection/route validation and repo validation |
| `scripts/validators/recurrence.py` | root-owned recurrence route validator module | mechanic-owned payload recurrence route cards, part contracts, portable-proof beacon posture, provenance, and recurrence decisions stay under recurrence; this module checks recurrence proof-support posture without accepting runtime activation, owner promotion, or source bundle meaning | recurrence route validation and repo validation |
| `scripts/validators/release_support.py` | root-owned release-support validator module | mechanic-owned payload readiness, strategic closeout, PR handoff, route, and legacy artifacts stay under release-support; this module checks release publication support posture below live git, GitHub, tag, and release evidence | release-support boundary validation and repo validation |
| `scripts/validators/report_index.py` | root-owned generated report-index validator module | mechanic-owned payload reports remain bundle-local or part-local; this module checks the generated reader stays derived and non-authoritative | report index parity and repo validation |
| `scripts/validators/root_authority.py` | root-owned root authority/design validator module | mechanic-owned payload architecture details, legacy archive payloads, generated projections, source eval contracts, runtime outcomes, and release publication evidence stay with owning surfaces; this module checks root design, proof topology, legacy naming, agent index, audit/GitHub route, agent lane, memory proof boundary, read-model command ownership, decision status, and validator/index posture | root authority route validation and repo validation |
| `scripts/validators/root_context.py` | root-owned validation context module | mechanic-owned payload and source proof meaning stay with focused validators; this helper owns sibling root resolution, `repo:` reference parsing, strict sibling compatibility context, and route-token companion lookup without defining source, generated, mechanic, runtime, or release truth | runtime/ref parser tests, sibling canary override tests, and repo validation |
| `scripts/validators/root_guidance.py` | root-owned guidance and README route validator module | mechanic-owned payload guide examples, release-support evidence, and proof-operation details stay with source bundles or owning mechanic parts; this module checks root guidance/readme/operations route posture without owning generated parity, source eval contract meaning, release publication state, or runtime outcomes | root guidance route validation and repo validation |
| `scripts/validators/root_route_cards.py` | root-owned root route-card-only district validator module | mechanic-owned payloads and source eval payloads belong under their owning mechanics or bundles; this module checks root compatibility districts remain route cards instead of payload homes | root route-card district validation and repo validation |
| `scripts/validators/root_topology.py` | root-owned source/topology orchestrator module | mechanic-owned payload meaning stays with focused validators, active mechanic route cards, source bundles, generated builders, and runtime/release support owners; this module only wires root source/topology checks and injected route context | root source/topology validation and repo validation |
| `scripts/validators/route_residue.py` | root-owned route residue validator module | mechanic-owned payload source meaning stays with owning mechanics or eval bundles; this module checks generated/readout, source, config, decision, and mechanic payload references do not use route-card-only or legacy parent paths as current authority | route residue validation and repo validation |
| `scripts/validators/rpg.py` | root-owned RPG route validator module | mechanic-owned payload RPG route cards, progression-unlocks support, provenance, and RPG decisions stay under RPG; this module checks bounded progression/unlock support posture without owning quest acceptance, universal score, runtime equip state, generated-card authority, or growth-cycle movement | RPG route validation and repo validation |
| `scripts/validators/runtime_audit.py` | root-owned runtime audit validator module | mechanic-owned payload trace bridge schema files, trace bridge example files, selected evidence packets, runtime integrity review docs, replay fields, and evidence refs stay under audit parts; this module checks trace/eval, runtime evidence selection, and candidate-only runtime review boundaries through injected repo-ref context without accepting runtime activation or proof canon | runtime audit boundary validation and repo validation |
| `scripts/validators/runtime_candidates.py` | root-owned runtime-candidate generated reader validator module | mechanic-owned payload templates and review examples stay under audit/checkpoint parts; this module checks generated candidate-reader parity and review posture | runtime-candidate reader parity and repo validation |
| `scripts/validators/source_eval_domains.py` | root-owned source-eval doctrine orchestrator module | mechanic-owned payload support artifacts stay in source bundles, proof-infra parts, focused source doctrine validators, and sibling source refs; this module only wires source-eval dependency roots and doctrine checks without owning source proof meaning | source-eval doctrine validation and repo validation |
| `scripts/validators/source_doctrine.py` | root-owned source doctrine validator module | mechanic-owned payload guides, source bundles, comparison posture, artifact/process separation, repeated-window wording, and integrity taxonomy stay in authored source; this module checks doctrine alignment without owning generated or runtime truth | source doctrine and guide alignment validation |
| `scripts/validators/source_eval_contracts.py` | root-owned source eval proof-object contract validator module | mechanic-owned payload support artifacts stay under proof-object and proof-infra parts while bundle-local `EVAL.md`, `eval.yaml`, reports, fixtures, runners, proof artifacts, dependency refs, and command ownership keep source truth; this module checks contract shape, command ownership, and dependency reachability without owning generated reader freshness, public entry topology, release packaging, or runtime outcomes | source eval proof-object contract validation and repo validation |
| `scripts/validators/titan.py` | root-owned Titan route and canary validator module | mechanic-owned payload Titan route cards, seed-boundary docs, Titan canary YAML seeds, and seed-boundary decision stay under Titan; this module checks seed-level route posture and YAML shape without owning Titan role/bearer/summon/incarnation law, memory sovereignty, runtime activation, or executable proof scoring | Titan route/seed-boundary validation and repo validation |
| `scripts/validators/validation_topology.py` | root-owned validation/test/script topology validator module | mechanic-owned payload command, script, and test details stay in owning parts while this module checks root inventories and lane authority | validation topology contracts and repo validation |
| `tests/AGENTS.md` | root-owned tests route card | mechanic-owned payload tests live under `mechanics/<mechanic>/parts/<part>/tests/` | semantic AGENTS validation |
| `tests/test_build_catalog.py` | root-owned catalog test coverage | mechanic-owned payload catalog inputs stay in bundles or parts and are checked through root builder tests | pytest catalog checks |
| `tests/test_comparison_surface_contracts.py` | root-owned comparison surface contract test | mechanic-owned payload comparison fixtures, runner contracts, support notes, and paired readouts stay under comparison-spine or source eval packages while root validation checks source-to-support alignment | comparison surface contract validation |
| `tests/test_current_direction_routes.py` | root-owned entrypoint route test | mechanic-owned payload direction lives in parent `DIRECTION.md` surfaces | focused direction tests |
| `tests/test_decision_indexes.py` | root-owned decision-index read-model contract test | mechanic-owned payload decision meaning stays in source decisions and generated indexes remain root read models | decision index read-model validation |
| `tests/test_docs_topology.py` | root-owned docs topology contract test | mechanic-owned payload docs stay under owning mechanics while this test checks root docs route and topology contracts | docs topology validation |
| `tests/test_downstream_feed_contracts.py` | root-owned generated downstream feed contract tests | mechanic-owned payload generated readers remain part-local and feed root contracts only when derived | downstream feed tests |
| `tests/test_eval_source_topology.py` | root-owned source eval topology, manifest/frontmatter parity, and dependency-ref contract test | mechanic-owned payload support parts remain outside bundle-local claim truth while eval bundles, dependency metadata, and source entry cards stay rooted in evals surfaces | eval source topology validation |
| `tests/test_generated_parity.py` | root-owned generated/read-model parity contract test | mechanic-owned payload generated companions remain part-local unless promoted through root readers; generated catalog, capsule, section, and min projections stay derived from source eval packages | generated parity validation |
| `tests/test_generated_route_residue.py` | root-owned generated route residue contract test | mechanic-owned payload generated companions may point to part-local config while generated readers cannot claim route-card-only or legacy parent paths as source truth | generated route residue validation |
| `tests/test_guidance_surface_routes.py` | root-owned public and docs guidance route contract test | mechanic-owned payload proof criteria stay with bundles or owning mechanics while guidance surfaces route review without becoming source truth | guidance surface route validation |
| `tests/test_index_surface_roles.py` | root-owned root/mechanic index role contract test | mechanic-owned payload index rows stay in owning parent `PARTS.md` and parts routes while headings keep index/route roles explicit | index surface role validation |
| `tests/test_mechanic_evidence_ledger.py` | root-owned mechanic evidence ledger and class-map contract test | mechanic-owned payload parent rows keep evidence dimensions, class partition, and route refs grounded in living source surfaces instead of generic root validator refs | mechanic evidence ledger validation |
| `tests/test_memo_contradiction_phase_alpha_gap_report.py` | root-owned bundle-report test for selected audit evidence | mechanic-owned payload selected evidence lives under `mechanics/audit/parts/selected-evidence-packets/` | bundle report schema test |
| `tests/test_memo_contradiction_phase_alpha_rerun_report.py` | root-owned bundle-report test for selected audit evidence | mechanic-owned payload selected evidence lives under `mechanics/audit/parts/selected-evidence-packets/` | bundle report schema test |
| `tests/test_memo_writeback_act_phase_alpha_report.py` | root-owned bundle-report test with sibling-evidence gating | mechanic-owned payload selected evidence lives under audit parts; sibling truth remains repo-qualified | bundle report and sibling-evidence skip checks |
| `tests/test_mechanic_legacy_bridge.py` | root-owned mechanic legacy single-bridge and provenance posture test | mechanic-owned payload active surfaces route legacy archive detail through PROVENANCE bridges instead of direct legacy indexes or raw archives | mechanic legacy bridge validation |
| `tests/test_mechanic_legacy_archive_routes.py` | root-owned mechanic legacy archive route contract test | mechanic-owned payload archive surfaces stay route/readout records without executable command blocks or negative active-package scaffold wording | mechanic legacy archive validation |
| `tests/test_mechanic_manifest_routes.py` | root-owned mechanic manifest route-field contract test | mechanic-owned payload manifests may name part-local surfaces, but unresolved root docs globs and root route-card-only payload paths stay outside part payload truth | mechanic manifest route validation |
| `tests/test_mechanic_part_contracts.py` | root-owned mechanic part README, payload inventory, and source-surface contract test | mechanic-owned payload parts must be routed from parent `PARTS.md`, name source surfaces, explain local payload dirs, and keep owner split explicit | mechanic part contract validation |
| `tests/test_mechanic_part_validation_commands.py` | root-owned mechanic part validation-command ownership test | mechanic-owned payload executable commands stay in nearest AGENTS validation blocks and must reach repo-relative, part-local or bundle-specific anchors | mechanic part validation-command validation |
| `tests/test_mechanic_parent_direction.py` | root-owned mechanic parent direction and provenance negative contract test | mechanic-owned payload parent READMEs, AGENTS cards, DIRECTION cards, and PROVENANCE bridges keep active-to-archive routes explicit while root validation rejects stale package wording | mechanic parent direction validation |
| `tests/test_mechanic_parent_topology.py` | root-owned mechanic parent topology contract test | mechanic-owned payload parents keep allowlisted docs, direction cards, PARTS indexes, and legacy skeletons in active parent homes while root validation checks coverage | mechanic parent topology validation |
| `tests/test_mechanic_parts_index.py` | root-owned mechanic PARTS and lower-parts index synchronization test | mechanic-owned payload part directories must be declared by owning indexes, keep command ownership in AGENTS, and allow explicit cross-parent references only as route context | mechanic parts index validation |
| `tests/test_mechanic_root_district_recon.py` | root-owned mechanic root-district reconnaissance contract test | mechanic-owned payload roots keep active source trees superseding old flat districts while route-card-only root districts stay compatibility maps | mechanic root-district reconnaissance validation |
| `tests/test_mechanic_surface_contracts.py` | root-owned mechanic surface contract smoke test | mechanic-owned payload route cards, part readmes, and provenance bridges stay in owning mechanic surfaces while root validation checks current contract coverage | mechanic surface contract validation |
| `tests/test_mechanics_topology.py` | root-owned mechanics topology contract test | mechanic-owned payload tests remain part-local while this test checks the root-authored surface classification guard | mechanics topology validation |
| `tests/test_nested_agents_docs.py` | root-owned nested AGENTS test | mechanic-owned payload route cards are validated through root route tests | nested AGENTS pytest |
| `tests/test_roadmap_parity.py` | root-owned roadmap parity, current-contour, starter-surface, and targeted non-starter selection test | mechanic-owned payload status routes through mechanics/roadmap surfaces and current-contour cards | roadmap parity validation |
| `tests/test_read_model_command_ownership.py` | root-owned read-model command ownership contract test | mechanic-owned payload read models keep executable commands in nearest AGENTS surfaces instead of guidance/read-model pages | read-model command ownership validation |
| `tests/test_repo_validation_workflow.py` | root-owned GitHub repo-validation workflow contract test | mechanic-owned payloads do not infer sibling truth from moving repositories; sibling checkout pins remain explicit workflow release evidence | repo-validation workflow pin validation |
| `tests/test_quest_and_reader_surfaces.py` | root-owned questbook, quest route, runtime-candidate reader, and eval-report-index contract test | mechanic-owned payload quest schemas and candidate-reader sources stay under owning mechanics while generated readers remain derived companions | quest and generated reader surface validation |
| `tests/test_root_surface_roles.py` | root-owned root, design, proof-topology, agent-index, legacy-naming, and memory-consumer route contract test | mechanic-owned payload route cards stay under owning mechanics while public README, design spine, proof topology, agent lane, legacy naming, scripts, tests, and memory-consumer boundaries keep their distinct owner roles | root surface role validation |
| `tests/test_route_residue.py` | root-owned route residue and root route-card district contract test | mechanic-owned payload paths remain bundle-local, part-local, or repo-qualified while root route-card-only districts stay route surfaces instead of source payload homes | route residue validation |
| `tests/test_runtime_evidence_surfaces.py` | root-owned runtime evidence, integrity review, trace bridge, and artifact-hook contract test | mechanic-owned payload runtime evidence packets, integrity review docs, schemas, examples, and hook examples stay under audit/checkpoint parts while root validation checks owner refs | runtime evidence surface validation |
| `tests/test_report_schema_contracts.py` | root-owned report schema, actual-report alignment, integrity taxonomy, and overclaim helper contract test | mechanic-owned payload report schemas stay with source eval packages or owning mechanic parts while root tests check schema acceptance, actual report alignment, integrity taxonomy, and overclaim boundary helpers | report schema contract validation |
| `tests/test_script_topology.py` | root-owned script topology contract test | mechanic-owned payload scripts stay under owning parts while this test checks inventory and lane references | script topology inventory validation |
| `tests/test_test_topology.py` | root-owned test topology contract test | mechanic-owned payload fixtures and owner surfaces stay under bundles or parts while this test checks coverage inventory | test topology inventory validation |
| `tests/test_validate_repo.py` | root-owned validator test suite | mechanic-owned payload contracts get focused tests here only when the root validator owns the cross-surface guard | full validator test suite |
| `tests/test_validation_topology.py` | root-owned validation lane and validator topology contract test | mechanic-owned payload validator details stay with source surfaces while this test checks lane and inventory coherence | validation topology inventory validation |
| `tests/test_validate_semantic_agents.py` | root-owned semantic AGENTS test | mechanic-owned payload local cards remain under owning directories | semantic AGENTS pytest |
| `tests/test_verification_honesty_local_report.py` | root-owned bundle-local report test | mechanic-owned payload proof-loop report artifacts live under proof-loop parts, while this checks a source bundle report | bundle report schema test |
| `tests/validate_repo_fixtures.py` | root-owned validator fixture helper | mechanic-owned payload fixtures are synthesized only for tests while source payload homes stay under owning bundles or parts | validator fixture support |

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
| `comparison-spine` | evals-native | comparison posture for baseline, peer, and longitudinal reads | same-task regression, paired comparison, repeated-window movement | comparison fixtures and report contracts | generated comparison spine, report readouts, tests | growth and stress movement feed bounded comparison pressure | bundle meaning stays stronger than comparison readouts | old root comparison fixture/report paths route through provenance |
| `distillation` | AoA-aligned | distillation as provenance-preserving abstraction and candidate adoption | compost provenance and reviewed runtime candidate adoption | distillation fixtures and adoption guardrails | tests, reports, audit bridge references | writeback/closeout ingress remains root or quest pressure unless proven | ToS, memo, KAG, runtime, and owner acceptance stay stronger | old fixture placement and Experience-adjacent adoption route through provenance |
| `experience` | AoA-aligned | Experience protocol, certification, adoption, governance, office train | verdict support for protocol, certification, adoption, runtime-boundary, office | schemas, examples, fixtures, support docs | tests and generated references | office/release/governance pressure remains bounded proof support | Experience law, runtime, office, KAG, ToS, and adoption truth stay with owners | old Experience root docs/examples/schemas/tests route through provenance |
| `growth-cycle` | AoA-aligned | Growth Cycle diagnosis as first active stage | diagnosis-cause discipline and cause-hypothesis proof | diagnosis bundle notes/examples/checks and diagnosis-gate part | bundle integrity checks, tests, generated readers | repair, harvest, closeout, quest promotion, owner-followthrough remain routed or deferred | repair stays antifragility; progression stays RPG; longitudinal movement stays comparison | deferred stage pressure and ingress notes route through provenance |
| `method-growth` | AoA-aligned | method-growth lineage and owner landing | candidate-lineage integrity and owner-fit routing quality | bundle contracts, fixtures, reports, examples | tests, generated catalogs, validation routes | diagnosis/repair/progression/distillation pressure routes to owning parents | owner repos keep final object and acceptance truth | old shared fixture placement routes through provenance |
| `proof-infra` | evals-native | reusable proof infrastructure below bundle meaning | shared fixtures, runners, scorers, schemas, templates, report contracts | fixture families and reportable contracts | scorers, tests, generated proof-artifact readers | domain-specific pressure routes to narrower mechanics | source bundles and domain mechanics stay stronger | old root infra district paths remain route cards or provenance |
| `proof-loop` | evals-native | local proof loop coordination across source, evidence, report, receipt | route-smoke and bundle-local proof-loop materialization | route-smoke report, report schema, receipt dry-review inputs | report index, validators, release-support checks | open proof questions and receipt publication stay separate | step owners keep meaning; proof-loop coordinates only | old route-smoke root report path routes through provenance |
| `proof-object` | evals-native | source proof object completeness and eval authority | eval claim, eval manifest, frontmatter, lifecycle, completeness review | authoring template, schemas, eval-local contracts | catalog/capsule/section builders, validators, tests | proof pressure remains with source evals and quests | eval packages stay source authority; generated/readout surfaces stay weaker | old root template/schema placement routes through provenance |
| `publication-receipts` | evals-native | optional publication receipt sidecar below reviewed reports | eval-result receipt publication and intake dry-review pressure | receipt schema/example, stats-envelope mirror, live publisher | receipt tests, intake dry-review report, live publisher checks | live receipt publication remains optional and separate | reports and bundles stay stronger; stats envelope owner stays `aoa-stats` | old receipt docs/schema/example/publisher/test paths route through provenance |
| `questbook` | AoA-aligned | quest obligations, lifecycle, returnability, deferred proof | source quest records and generated dispatch pressure | quest schemas, lifecycle docs, source records | generated quest catalog/dispatch and validators | captured/triaged/deferred obligations remain reviewable | quests are obligation source records before bundle verdicts or live tasks | old top-level quest/schema paths route through provenance |
| `recurrence` | AoA-aligned | recurrence proof, return anchors, memo recall, recursor boundary, beacons | control-plane, anchor-return, memory-recall, stats-regrounding, portable-proof-beacon proof | fixtures, schemas, manifests, hooks, scorer/runner cases | runners, scorers, tests, generated/readout support | continuity-anchor and self-reanchor remain bundle-local until parts are proven | runtime, memory, stats, Agon, and owner decisions stay stronger | old recurrence root paths and support placement route through provenance |
| `release-support` | AoA-aligned | bounded release support and publication posture | readiness audit, strategic closeout, PR handoff, release check pressure | release-support reports, changelog, release docs, workflow refs | release_check, tests, GitHub validation route, generated freshness checks | goal completion and public release stay open until landing proof | release support preserves eval-claim and GitHub-status authority boundaries | old `proof-release` wording and report/test paths route through provenance |
| `rpg` | AoA-aligned | RPG progression and unlock proof support | progression evidence and unlock proof bridge | progression schemas, examples, generated unlock cards | validators, tests, generated card checks | quest unlock pressure remains source obligation | roles, skills, techniques, playbooks, runtime, and stats stay with owners | old progression/unlock root paths route through provenance |
| `titan` | evals-native | owner-named Titan proof-seed boundary with proof-organ claim limits | incarnation, summon, memory, gate, runtime roster, bridge, and closeout seed pressure | Titan canary YAML seeds and seed AGENTS route | canary shape validator and tests; future scorer route remains deferred | Titan boundary pressure stays seed-level until executable proof exists | `aoa-agents` owns Titan role/bearer/summon/incarnation law; `aoa-memo` and runtime owners keep memory and activation truth | old `titan-canaries` parent and root `evals/` placement route through provenance |

## Active Parent Evidence Route Refs

This ledger keeps the dimension rows auditable. Each active parent must carry
concrete local route refs: repo-relative refs that resolve in the current
worktree, include the active parent route, and include at least one
living non-mechanics route ref, meaning a non-mechanics route ref that points
at current evidence. This living non-mechanics evidence keeps the parent tied
to source, bundle, generated readout, quest, workflow/config, root entry, or
part-local validator routes. Package-local prose, rationale-only decisions, and
generic root validator files can support route context; the parent evidence row
still needs living evidence.

| Parent | Route refs |
| --- | --- |
| `agon` | `mechanics/agon/README.md`, `mechanics/agon/parts/ccs-alignment/README.md`, `mechanics/agon/parts/ccs-alignment/config/agon_ccs_eval_alignment.seed.json`, `evals/boundary/aoa-recurrence-control-plane-integrity/EVAL.md` |
| `antifragility` | `mechanics/antifragility/README.md`, `mechanics/antifragility/parts/repair-proof/README.md`, `evals/stress/aoa-antifragility-posture/EVAL.md`, `evals/workflow/aoa-repair-boundedness/EVAL.md` |
| `audit` | `mechanics/audit/README.md`, `mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json`, `evals/capability/aoa-eval-integrity-check/EVAL.md`, `docs/decisions/AOA-EV-D-0007-audit-mechanic-package.md` |
| `boundary-bridge` | `mechanics/boundary-bridge/README.md`, `mechanics/boundary-bridge/parts/latest-sibling-canary/README.md`, `.github/workflows/latest-sibling-canary.yml`, `quests/orchestrator/captured/AOA-EV-Q-0006.yaml` |
| `checkpoint` | `mechanics/checkpoint/README.md`, `mechanics/checkpoint/parts/a2a-summon-return/README.md`, `evals/workflow/aoa-a2a-summon-return-checkpoint/EVAL.md`, `mechanics/checkpoint/parts/a2a-summon-return/tests/test_a2a_summon_return_checkpoint_fixture.py` |
| `comparison-spine` | `mechanics/comparison-spine/README.md`, `mechanics/comparison-spine/parts/fixed-baseline/fixtures/frozen-same-task-v1/README.md`, `docs/guides/COMPARISON_SPINE_GUIDE.md`, `generated/comparison_spine.json` |
| `distillation` | `mechanics/distillation/README.md`, `mechanics/distillation/parts/compost-provenance/README.md`, `evals/artifact/aoa-compost-provenance-preservation/EVAL.md`, `evals/workflow/aoa-memo-reviewed-candidate-adoption-integrity/EVAL.md` |
| `experience` | `mechanics/experience/README.md`, `mechanics/experience/parts/protocol-integrity/README.md`, `evals/boundary/aoa-experience-protocol-integrity/EVAL.md`, `mechanics/experience/parts/protocol-integrity/fixtures/experience-verdict-protocol-integrity-v1/README.md` |
| `growth-cycle` | `mechanics/growth-cycle/README.md`, `mechanics/growth-cycle/parts/diagnosis-gate/README.md`, `evals/workflow/aoa-diagnosis-cause-discipline/EVAL.md`, `docs/operations/REVIEWED_CLOSEOUT_WRITEBACK_PROOF_INGRESS.md` |
| `method-growth` | `mechanics/method-growth/README.md`, `mechanics/method-growth/parts/candidate-lineage/README.md`, `evals/capability/aoa-candidate-lineage-integrity/EVAL.md`, `evals/boundary/aoa-owner-fit-routing-quality/EVAL.md` |
| `proof-infra` | `mechanics/proof-infra/README.md`, `mechanics/proof-infra/parts/fixture-families/README.md`, `docs/guides/SHARED_PROOF_INFRA_GUIDE.md`, `mechanics/proof-infra/parts/reportable-contracts/schemas/report-summary.schema.json` |
| `proof-loop` | `mechanics/proof-loop/README.md`, `mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md`, `evals/workflow/aoa-verification-honesty/EVAL.md`, `generated/eval_catalog.json` |
| `proof-object` | `mechanics/proof-object/README.md`, `mechanics/proof-object/parts/eval-contracts/schemas/eval-manifest.schema.json`, `evals/workflow/aoa-verification-honesty/EVAL.md`, `generated/eval_catalog.json` |
| `publication-receipts` | `mechanics/publication-receipts/README.md`, `mechanics/publication-receipts/parts/receipt-payload/docs/EVAL_RESULT_RECEIPT_GUIDE.md`, `mechanics/publication-receipts/parts/receipt-payload/schemas/eval-result-receipt.schema.json`, `.aoa/live_receipts/AGENTS.md` |
| `questbook` | `mechanics/questbook/README.md`, `mechanics/questbook/parts/source-record-contract/schemas/quest.schema.json`, `quests/README.md`, `generated/quest_catalog.min.json` |
| `recurrence` | `mechanics/recurrence/README.md`, `mechanics/recurrence/parts/control-plane-integrity/README.md`, `evals/boundary/aoa-recurrence-control-plane-integrity/EVAL.md`, `mechanics/recurrence/parts/control-plane-integrity/tests/test_recurrence_control_plane_integrity_eval_seed.py` |
| `release-support` | `mechanics/release-support/README.md`, `mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json`, `docs/operations/RELEASING.md`, `scripts/release_check.py` |
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
| `release-support` | Release, rollback, replay, release readiness, closeout, PR handoff, changelog, release checks, and GitHub validation posture span `docs/`, `reports/`, `schemas/`, `examples/`, `scripts/`, `tests/`, and root release surfaces. | Parent route is `release-support`. Proof-release wording stays artifact history or report vocabulary behind the active parent topology. |
| `audit` | Runtime candidate intake, trace bridge, selected evidence packets, integrity review, artifact-to-verdict examples, runtime evidence schemas, generated candidate readers, and audit/readout reports span `docs/`, `examples/`, `schemas/`, `generated/`, `scripts/`, `tests/`, `reports/`, and source eval packages. | Parent route is `audit`. `runtime-evidence` routes as an evidence class and part family inside the audit mechanic. |
| `boundary-bridge` | Sibling proof refs, repo-qualified compatibility, latest-sibling canary, source-checkout resolution, orchestrator proof anchors, Phase Alpha playbook-to-eval matrix bridging, KAG/ToS/federation boundary refs, and owner handoff posture span `docs/`, `scripts/`, config, tests, examples, schemas, generated quest readers, generated matrix readers, quest source records, and sibling route references. | Parent route is `boundary-bridge`. `sibling-proof-refs`, `latest-sibling-canary`, orchestrator proof anchors, and Phase Alpha eval matrix bridging route as parts inside the bridge. |
| `questbook` | Quest source records, lifecycle docs, part-local quest schemas, generated quest catalog and dispatch, validators, human open-obligation index, and questbook decisions span `quests/`, `mechanics/questbook/parts/`, `docs/`, `generated/`, `scripts/`, and tests. | Parent remains `questbook`. Source-record and dispatch-reader schemas are parts; generated readers stay root derived companions; quest records stay source obligations before proof verdicts. |
| `recurrence` | Recurrence control-plane bundle, return-anchor pressure, memo-recall proof pressure, recursor-readiness boundary cases, stats re-grounding boundary pressure, portable-proof beacon pressure, recurrence proof program docs, portable eval boundary guidance, control-plane eval docs, live-observation producer notes, fixtures, schema, example dossier, runner, scorer, tests, component manifests, hook bindings, generated/readout support, and neighboring return-aware bundles span `evals/`, `docs/`, `fixtures/`, `manifests/`, `schemas/`, `scripts/`, `scorers/`, `tests/`, `examples/`, and generated readers. | Parent is `recurrence`. Control-plane integrity, anchor-return, memory-recall, recursor-boundary, stats-regrounding-boundary, and portable-proof-beacons support artifacts are active part-local surfaces; source proof bundles stay under `evals/`; continuity-anchor and self-reanchor remain bundle-local until their support artifacts justify parts. |
| `checkpoint` | A2A summon return checkpoint bundle, long-horizon checkpoint restart bundle, self-agent checkpoint posture, fixture families, tests, artifact-to-verdict checkpoint examples, generated candidate readers, and quest pressure span `evals/`, `docs/`, `examples/`, `fixtures/`, `tests/`, `generated/`, `mechanics/audit/`, and `quests/`. | Parent is `checkpoint`. A2A summon return, restartable inquiry, and self-agent posture are active parts; source proof bundles stay under `evals/`; audit owns hook schema and candidate-reader builders. |
| `experience` | Experience protocol, certification gate, adoption, governance, appeal, stay-order, sealed-vote, replay-history, runtime-boundary, office, service-mesh, replay-audit, release-train, shadow, and assistant certification surfaces span `evals/`, docs, fixtures, examples, schemas, tests, and generated references. | Parent is `experience`. Protocol integrity, certification gate, adoption federation, governance/runtime boundary, and office release-train support are parts under the active route; source proof bundles stay under `evals/`. |
| `antifragility` | Antifragility posture, stress recovery, bounded repair proof, chaos/remediation sidecars, degraded-mode and recovery reports span bundles, docs, examples, fixtures, reports, schemas, audit sidecars, comparison readouts, and eval seeds. | Parent is `antifragility`. First-wave posture, stress-recovery window, and repair-proof support are parts; comparison readouts stay in `comparison-spine`; runtime evidence selection stays in `audit`; diagnosis-cause discipline routes through `growth-cycle/diagnosis-gate` as the active diagnosis lane. |
| `method-growth` | Candidate-lineage integrity, owner-fit routing quality, growth-refinery selection wording, shared fixture families, bundle-local contracts, report schemas, example reports, generated catalogs, tests, and roadmap/changelog pressure span `evals/`, `fixtures/`, `generated/`, `tests/`, root selection docs, and mechanics provenance. | Parent is `method-growth`. Candidate lineage and owner landing are parts; source proof bundles stay under `evals/`; former root shared fixture families live behind active parts; diagnosis-cause discipline routes through `growth-cycle/diagnosis-gate`, repair proof stays under `antifragility`, and RPG progression/unlock surfaces route through `rpg/progression-unlocks`. |
| `rpg` | Progression evidence and unlock proof bridge surfaces span root docs, schemas, examples, generated cards, quest source records, validators, tests, recurrence manifests, and AoA center `progression-unlocks` owner split. | Parent is `rpg`. Progression evidence and unlock proof are active `progression-unlocks` support surfaces under the RPG parent; quest records stay in `quests/`; old root paths are provenance only. |
| `growth-cycle` | Diagnosis-cause discipline, deferred repair, closeout, harvest, writeback, repeated-window, progression, and quest pressure span `evals/`, `docs/`, `mechanics/`, `quests/`, generated readers, and tests. The first active proof operation is `aoa-diagnosis-cause-discipline`, with support notes, example report, integrity check, and existing deferrals from `method-growth`. | Parent is `growth-cycle`. `diagnosis-gate` is the active part. Repair proof stays under `antifragility/repair-proof`; longitudinal movement stays under `comparison-spine`; RPG progression/unlock proof stays under `rpg`; closeout, harvest, quest-promotion, and owner-followthrough stay deferred until separate eval-side operations exist. |
| `distillation` | Compost provenance preservation and reviewed runtime distillation candidate adoption span `evals/`, former `fixtures/`, `mechanics/experience/`, `docs/`, `generated/`, reports, tests, and audit bridge references. The proof-side operation checks whether abstraction or candidate adoption preserves provenance, review state, candidate posture, receipt visibility, recall inspectability, and promotion boundaries. | Parent is `distillation`. `compost-provenance` and `runtime-candidate-adoption` are active parts. Source proof bundles stay under `evals/`; runtime-pack hook metadata stays under `audit`; generic adoption/consent/compatibility stays under `experience`; memo recall, memo contradiction, and confirmed writeback-act proof stay outside this parent until separate evidence proves a Distillation operation. |

### Evals-native parents

These parents use proof-organ operation names. They are allowed because
`aoa-evals` owns the proof organ operation itself. Most names are local proof
operations such as `proof-object` or
`comparison-spine`; `titan` is the
owner-named evals-native exception, where the local operation is the proof-seed
boundary and the stronger Titan truth stays outside `aoa-evals`.

| Parent | Evidence cluster | Current route decision |
| --- | --- | --- |
| `proof-object` | Source eval claims, `EVAL.md`, `eval.yaml`, authoring template, frontmatter and manifest schemas, proof-surface contracts, generated catalogs, capsule/section readers, lifecycle checks, and completeness review span `evals/`, `mechanics/proof-object/parts/`, `docs/`, `scripts/`, `tests/`, and `generated/`. | Valid evals-native parent. `eval-authoring` and `eval-contracts` are parts; source eval packages stay under `evals/`; generated readers stay derived companions. |
| `proof-infra` | Shared fixtures, runners, scorers, schemas, templates, report contracts, generic fixture-family support, reportable runner/scorer/schema contracts, generated proof artifact readers, validators, tests, and bundle-local contracts span root infrastructure districts, mechanic-local parts, and source eval packages. | Valid evals-native parent. It routes shared proof infrastructure while keeping bundle meaning stronger. Generic shared fixture families may live under `parts/fixture-families`; shared reportable contracts may live under `parts/reportable-contracts`; domain-specific families and schemas stay under their owning mechanic parts. |
| `comparison-spine` | Baseline, regression, same-task, output-vs-process, peer compare, repeated-window, stress-recovery, comparison guide, generated spine, fixture families, reports, examples, schemas, and tests form a cross-root comparison operation. | Valid evals-native parent. It owns comparison posture plus fixed-baseline, peer-compare, and longitudinal-window fixture/report parts. |
| `publication-receipts` | Eval result receipt guide, receipt schema, stats envelope mirror, receipt example, live publisher, local live receipt log, intake dry review, and receipt tests form the publication sidecar operation. | Valid evals-native parent. Receipts stay weaker than reports and source eval packages. |
| `proof-loop` | Selection route, source proof object, proof infra, candidate evidence, sibling refs, bundle-local report, optional receipt, route-smoke report, decisions, and tests form a local proof loop operation. | Valid evals-native parent while it remains a coordinator and preserves the step-owner meaning of each package. |
| `titan` | Titan incarnation and summon discipline docs plus 37 Titan seed canaries in the former `evals/` district form an owner-named proof-seed boundary operation. Stronger Titan role, bearer, summon, and incarnation law belongs to `aoa-agents`; memo posture belongs to `aoa-memo`; runtime belongs to `abyss-stack`. | Parent route is `titan`; `titan-canaries` stays historical canary-parent vocabulary. Canary YAML files are seed-boundary parts, and the local parent preserves the Titan authority boundary outside `aoa-evals`. |

## Former Wrong Parent Forms

The following names are accepted as legacy vocabulary, artifact forms, or
evidence-class wording. Each row names the active route that receives the
pressure:

| Wrong parent | Correct parent | Reason |
| --- | --- | --- |
| `agon-proof` | `agon` | Active route keeps the AoA-aligned Agon mechanic name. |
| `titan-canaries` | `titan` | Active route keeps the Titan proof-seed mechanic; canaries are the artifact form below it. |
| `proof-release` | `release-support` | Active route keeps the AoA-aligned release-support mechanic name. |
| `runtime-evidence` | `audit` | Active route sends runtime evidence through the audit mechanic that receives, constrains, and routes it. |
| `sibling-proof-refs` | `boundary-bridge` | Active route sends sibling proof refs through the boundary-bridge mechanic. |
| `repair` | `antifragility/repair-proof` | Active route sends bounded repair pressure through the repair-proof part; future Growth Cycle repair stages still need separate evidence. |

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

This list is an active topology allowlist; candidate brainstorming belongs in a
future evidence pass until evidence makes a parent route ready.
`scripts/validate_repo.py` rejects undeclared top-level
`mechanics/<parent>/` directories. A future parent must first prove an
AoA-aligned or evals-native cross-root evidence cluster, then update this file,
the package route cards, `docs/architecture/PROOF_TOPOLOGY.md`, `docs/decisions/`, and the
validator allowlist in one slice.

Allowed parents must keep their active route form complete: `AGENTS.md`,
`README.md`, and `PARTS.md` must exist, and `PARTS.md` must describe inputs,
outputs, owner split, stop-lines, and validation for the package parts.
Every concrete `mechanics/<parent>/parts/<part>/README.md` must also expose
`## Inputs`, `## Outputs`, `## Stronger Owner Split`, `## Stop-Lines`, and
`## Validation`, and the parent `PARTS.md` must route that part by README path
or exact part slug so the validator keeps parts attached to parent topology.
Every parent `PROVENANCE.md` must route readers through the active form first
and then bridge only into the owning legacy archive. Archive details belong
inside `legacy/`.

## Next Evidence Pass

Next package growth starts from local proof pressure and evidence shape. Use
this route table before promoting a new parent or Growth Cycle/Distillation
part:

| Pressure | Current route | Activation condition |
| --- | --- | --- |
| repair-cycle | `mechanics/antifragility/parts/repair-proof/` | a Growth Cycle repair stage needs its own source surfaces, contracts, stop-lines, and validation before entering `mechanics/growth-cycle/parts/` |
| progression-lift | `mechanics/rpg/parts/progression-unlocks/` and `mechanics/comparison-spine/parts/longitudinal-window/` | a Growth Cycle progression part needs distinct eval-side operation evidence |
| reviewed-closeout-chain | `docs/operations/REVIEWED_CLOSEOUT_WRITEBACK_PROOF_INGRESS.md` plus the relevant closeout, audit, questbook, or distillation route | active part status needs source refs, payload contract, owner split, and validation |
| donor-harvest | current owner mechanic plus provenance bridge | active part status needs reusable proof operation evidence beyond a one-off harvest note |
| quest-promotion | `mechanics/questbook/parts/` and source quest records under `quests/` | active part status needs a schema-backed promotion contract and generated-reader route |
| owner-followthrough | stronger-owner handoff route plus local proof receipt or report | active part status needs owner-visible evidence and bounded eval-side validation |

### Current route reading

| Family | Active route | Current reading |
| --- | --- | --- |
| Experience | `mechanics/experience/` | active AoA-aligned package |
| Antifragility | `mechanics/antifragility/` | active AoA-aligned package; bounded repair proof routes through `repair-proof` |
| Method Growth | `mechanics/method-growth/` | active AoA-aligned package for candidate lineage and owner landing |
| RPG | `mechanics/rpg/` | active AoA-aligned package for progression and unlock proof support |
| Growth Cycle | `mechanics/growth-cycle/parts/diagnosis-gate/` | `aoa-diagnosis-cause-discipline` cause-hypothesis discipline |
| Distillation | `mechanics/distillation/parts/compost-provenance/` and `mechanics/distillation/parts/runtime-candidate-adoption/` | compost provenance and reviewed runtime-candidate adoption proof support |
| Memo recall pressure | `mechanics/recurrence/parts/memory-recall/` | memo recall integrity proof |
| Memo contradiction pressure | lifecycle-aware contradiction visibility proof surfaces | read as contradiction visibility; Distillation adoption needs reviewed-candidate route evidence |
| Memo writeback-act pressure | confirmed base writeback-act proof surfaces | read as writeback-act proof; reviewed-candidate adoption needs Distillation source refs |
| witness trace pressure | upstream witness trace integrity surfaces | route through the owning witness/audit boundary before Distillation adoption |
| artifact-to-verdict `distillation_pack` metadata | audit bridge support | a Distillation part accepts it only through a specific bundle-local read |

Route invariant: diagnosis-cause discipline routes through `growth-cycle/diagnosis-gate` as the active diagnosis lane.

## Legacy Rule

Legacy is provenance behind an active mechanic.

Active route comes first: `README.md`, `PARTS.md` or `DIRECTION.md`, parts,
owner split, stop-lines, and validation. Legacy is entered through the single
`PROVENANCE.md` bridge; after that bridge, the legacy archive owns its own
details.

Use legacy for:

- historical name and path lookup;
- raw provenance that still needs archive-local accounting;
- accepted compatibility vocabulary with a current active route;
- distillation logs that explain how old placement became active topology.

Start current work in the active package or part. Route unresolved files through
the owning roadmap, quest, decision queue, or parent evidence pass before they
enter legacy.

When old path or name compatibility remains, keep it mapped to the current
active part and validation route.
