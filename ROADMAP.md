# Proof Direction Roadmap

## Role

`ROADMAP.md` is the active direction surface for `aoa-evals`.

It is not the changelog, questbook, architecture reference, design form,
decision log, validator ledger, or generated catalog. It names where the
bounded proof organ is trying to go next and which phase gates make that
movement honest.

Detailed release history stays in [CHANGELOG.md](CHANGELOG.md).
Durable rationale stays in [docs/decisions/](docs/decisions/).
Deferred obligations stay in [QUESTBOOK.md](QUESTBOOK.md) and `quests/`.
Eval meaning stays in `evals/**/EVAL.md` and `evals/**/eval.yaml`.

## Authority

The roadmap owns direction and sequencing.

It does not own source proof meaning, route law, validation implementation,
legacy archive accounting, runtime evidence acceptance, generated reader truth,
or sibling owner truth.

Use it to answer:

- what is the current contour of the proof organ?
- which horizon should be worked next?
- what must remain visible while implementation slices move detail elsewhere?

Use stronger surfaces for detail:

- root proof shape: `DESIGN.md`, `DESIGN.AGENTS.md`, and `docs/ARCHITECTURE.md`;
- agent pass-through index: `docs/AGENT_INDEX.md`;
- topology and authority classes: `docs/PROOF_TOPOLOGY.md`;
- durable rationale: `docs/decisions/README.md` and numbered decisions;
- mechanics evidence and package posture: `mechanics/EVIDENCE_CLUSTERS.md` and
  `mechanics/README.md`;
- validation contracts: `scripts/validate_repo.py` and `tests/test_validate_repo.py`.

## Update Rule

Update this file when the current direction, horizon order, public contour, or
standing verification posture changes.

Do not use this file as a status ledger for each guard added, each part exposed,
or each report recorded. Put those details in the owning decision, mechanic
index, generated/readout builder, report, receipt, or changelog surface.

## Current Direction

`aoa-evals` has moved beyond public bootstrap. The repository already carries
36 eval bundles, generated proof readers, runtime-candidate templates, trace and
receipt bridges, phase-alpha matrices, Agon alignment surfaces, mechanics
packages, and public-safe proof references into sibling owners.

The next work is structural maturity:

- keep entry surfaces short enough to trust;
- keep `docs/AGENT_INDEX.md` as the visible chain from repo root to payload
  validation;
- keep decisions as rationale crosswalks rather than generated dumps;
- keep roadmap direction separate from changelog and validator chronology;
- keep AGENTS law local to the nearest route card while preserving source
  meaning in authored design/topology docs;
- preserve mechanics topology without flattening active parent/part routes;
- split validation only after source and index surfaces make the domain
  boundaries obvious.

## Current Release Contour

Current release contour remains compact here so the roadmap keeps direction
instead of becoming a changelog.

Current release marker: `v0.3.3`.

Roadmap drift is controlled by keeping release anchors visible without turning
this file into release notes. This contour proves only bounded claims; it is not a claim that memo, runtime, release, sibling, or generated-reader surfaces are stronger than their owning proof objects.

The current release contour keeps these public anchors visible:

- `evals/capability/aoa-continuity-anchor-integrity/EVAL.md`
- `evals/workflow/aoa-reflective-revision-boundedness/EVAL.md`
- `evals/boundary/aoa-self-reanchor-correctness/EVAL.md`
- `evals/capability/aoa-candidate-lineage-integrity/EVAL.md`
- `evals/workflow/aoa-diagnosis-cause-discipline/EVAL.md`
- `evals/workflow/aoa-repair-boundedness/EVAL.md`
- `generated/eval_catalog.min.json`
- `generated/eval_capsules.json`
- `generated/eval_sections.full.json`
- `mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json`
- `mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json`
- `mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/generated/phase_alpha_eval_matrix.min.json`
- `mechanics/rpg/parts/progression-unlocks/docs/PROGRESSION_EVIDENCE_MODEL.md`
- `mechanics/checkpoint/parts/self-agent-posture/docs/SELF_AGENT_CHECKPOINT_EVAL_POSTURE.md`
- `mechanics/recurrence/docs/RECURRENCE_PROOF_PROGRAM.md`
- `mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md`
- `mechanics/publication-receipts/parts/receipt-payload/docs/EVAL_RESULT_RECEIPT_GUIDE.md`
- `mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md`

Memo pilot surfaces may describe future scar or retention readiness, but they do
not claim live memory-ledger readiness.

## Current Checked Contour

The following anchors must remain visible while roadmap, README, docs, decision,
mechanics, and validator cleanup proceeds. This is an anchor ledger, not a
history log.

| Anchor family | Current owner | Roadmap contour |
| --- | --- | --- |
| Root proof spine | `DESIGN.md`, `DESIGN.AGENTS.md`, `docs/ARCHITECTURE.md` | Root design stays compact, proof-bundle meaning remains bounded, and architecture describes mechanics as support rather than replacing source proof objects. |
| Agent index chain | `docs/AGENT_INDEX.md` | The pass-through index keeps the path from repo to authority class, operation, mechanic parent, part, payload, and validation visible without owning source truth or route law. |
| Proof topology | `docs/PROOF_TOPOLOGY.md`, `docs/decisions/0005-proof-topology-map.md` | The Proof Topology Map keeps source, generated, candidate, receipt, sibling, legacy, and active mechanic classes separate. |
| Decision memory | `docs/decisions/README.md` | Decision records explain durable rationale; decision-route residue keeps decision records from presenting former root payload paths as current routes. |
| Mechanics evidence | `mechanics/EVIDENCE_CLUSTERS.md` | Active Parent Evidence Dimension Ledger and Mechanic Evidence Route Refs keep parent evidence tied to contracts/payloads and living route refs. |
| Root district posture | `mechanics/EVIDENCE_CLUSTERS.md` | Root District Reconnaissance Ledger keeps route-card-only districts visible before mechanic-owned payload movement. |
| Residual root-authored surfaces | `mechanics/EVIDENCE_CLUSTERS.md` | Residual Root-authored Surface Classification keeps top-level docs, scripts, and tests explicit while mechanic-owned payload drift is rejected. |
| Generated/readout residue | validator and generated readers | generated/readout route residue keeps root generated readers away from route-card-only active paths while part-local generated readers may use same part paths. |
| Active route residues | validator and route cards | active mechanic route residue protects authored route cards; root-authored route residue protects root-facing authored surfaces. |
| Repo config and source bundle residues | `.gitignore`, `pytest.ini`, workflows, bundles | repo-config route residue includes `.gitignore`; source-bundle route residue keeps source proof bundles on bundle-local or repo-qualified sibling paths. |
| Mechanic payload residue | mechanics parts | mechanic-payload route residue keeps active mechanics payload references part-local, active, or repo-qualified. |
| Parent direction | parent `DIRECTION.md` files | mechanic parent direction keeps current operating direction visible between parent README, PARTS, PROVENANCE, and part contracts. |
| Part payload inventory | part READMEs and `PARTS.md` | Mechanic Part Payload Inventory names every payload subdirectory and rejects unexpected payload classes. |
| Part source and validation shape | part README, `VALIDATION.md`, parent `parts/AGENTS.md` | Mechanic Part Source Surface Reference Guard rejects a stale source surface ref; Mechanic Part Source Surfaces Section Contract requires the plural section; Mechanic Part Validation Command Reachability requires a payload coverage anchor; Mechanic Part Validation Command Ownership keeps executable commands in route cards. |
| Parent part map | parent `PARTS.md` | Mechanic PARTS Index Synchronization rejects a stale local part route while allowing cross-parent handoff references. |
| Legacy route | `docs/LEGACY_NAMING.md`, parent `PROVENANCE.md`, `legacy/` | Legacy and Naming Containment, Legacy Naming Single-Bridge Language, and Legacy Naming Posture Guide keep old names behind active routes. Mechanic Legacy Single Bridge keeps a single controlled bridge from active mechanic surfaces. Mechanic Provenance Bridge Posture says `PROVENANCE.md` is a bridge, not an active route. Active Legacy Parent Wording Boundary keeps runtime evidence from becoming a legacy parent route. |
| Proof loop reports | proof-loop and release-support mechanics | `mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md` remains routeability evidence, and `evals/workflow/aoa-verification-honesty/reports/aoa-evals-slice-19-lifecycle-contract.report.json` remains the first schema-backed bundle-local report. |
| Generated report index | `generated/eval_report_index.min.json` | The report index is a derived reader for reports and receipts; it routes to source reports without adding verdict authority. |
| Receipt dry review | `mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json` | The dry-review receipt stays at `not_published` posture and remains publication-boundary evidence, not proof-strengthening evidence. |
| Release readiness | `mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json` | Readiness audit evidence may inform release preparation, while goal completion remains governed by the active goal, validation, and owner review. |
| Strategic closeout | `mechanics/release-support/parts/strategic-closeout/reports/strategic-closeout-audit-v1.json` | The strategic closeout audit records that the long goal not complete posture can be explicit until all required owner gates land. |
| PR handoff | `mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json` | The PR handoff report carries owner landing handoff context without becoming live PR or GitHub status authority. |

## Horizons

### Horizon: Index Chain And Decision Memory

Goal: make the agent index chain reliable before slimming entry surfaces.

Current contour:

- `docs/decisions/README.md` is the decision crosswalk by number, surface
  class, mechanic parent, validation guard family, and active posture.
- Decisions stay weaker than source surfaces, generated readers, runtime facts,
  receipts, and sibling owner truth.

Next work:

- keep the decision index compact as new decisions are added;
- add a decision only when a future agent needs rationale, not when a diff is
  self-explanatory.

Exit gate:

- a future agent can find why a route exists without reading a changelog or
  validator token list.

### Horizon: Roadmap, Questbook, And Quest Route

Goal: separate direction, obligations, source quest records, and generated quest
readers.

Current contour:

- `ROADMAP.md` is this active direction surface.
- `QUESTBOOK.md` is the human tracked surface for open proof obligations.
- `quests/<lane>/<state>/*.yaml` are source quest records.
- generated quest readers remain derived navigation.

Next work:

- keep old quest-note lineage behind owning provenance bridges;
- keep lane/state source records aligned with generated projections;
- keep quest obligations from becoming eval bundle meaning or roadmap direction.

Exit gate:

- a low-context agent can distinguish direction, obligation, source quest, and
  generated quest reader without chat memory.

### Horizon: Root README And Docs Map

Goal: make entry and docs maps concise, beautiful, and route-safe.

Current contour:

- `README.md` introduces the proof organ but still carries too much dispatcher
  detail.
- `docs/README.md` maps docs but still contains validation placement noise.

Next work:

- rewrite the root README as a short public proof-organ entry;
- move detailed route matrices to docs or mechanics indexes;
- relocate `docs/README.md` validation guidance so reader paths remain clean.

Exit gate:

- public entry is readable without becoming shallow;
- detailed navigation remains recoverable from canonical index surfaces.

### Horizon: AGENTS Law And Source Meaning

Goal: distinguish operating law from authored source meaning.

Current contour:

- root and nested `AGENTS.md` cards already cover root, docs, decisions,
  route-card-only districts, mechanics parents, legacy, selected parts,
  `.agents`, `.aoa`, and `.github`.
- ordinary docs still legitimately carry authority-class and topology meaning.

Next work:

- audit law-like text by nearest owner rather than moving every boundary phrase
  into root `AGENTS.md`;
- keep route commands and mutation/validation posture in local route cards;
- keep proof meaning in design, topology, bundle, and mechanic source surfaces.

Exit gate:

- a future edit can tell whether to read AGENTS, README, DESIGN, topology,
  decisions, mechanics, or validator first.

### Horizon: Mechanics Atlas And Lower Index

Goal: keep `mechanics/` as an operation atlas, not a taxonomy attic.

Current contour:

- 19 active parent mechanics exist because each owns a repeatable proof-layer
  operation.
- Parent `README.md`, `DIRECTION.md`, `PARTS.md`, `PROVENANCE.md`, local
  `AGENTS.md`, part READMEs, payload homes, and legacy bridges form the lower
  index.

Next work:

- improve wayfinding before any parent split or removal;
- preserve valid legacy archives and generated/readout surfaces as subordinate
  route supports;
- add no new parent without evidence cluster, decision, route cards, topology,
  and validator movement in the same slice.

Exit gate:

- a future agent can start at one payload and recover parent operation,
  authority class, rationale, and validation route.

### Horizon: Legacy And Naming Containment

Goal: keep old names traceable without letting them steer active topology.

Current contour:

- `docs/LEGACY_NAMING.md` is a posture guide, not a global archive map.
- Parent `PROVENANCE.md` files open the active-to-archive bridge.
- Archive detail stays inside owning `legacy/` routes.

Next work:

- use active names for living proof operations;
- preserve old names as lineage, accepted input, generated projection, or
  provenance bridge context;
- update active owner routes before archive accounting.

Exit gate:

- a reader can tell whether a name is active topology, historical lineage,
  accepted input, generated projection, or archive vocabulary.

### Horizon: Validator Domain Split

Goal: make validation easier to maintain without weakening proof topology.

Current contour:

- `scripts/validate_repo.py` is still the central contract mesh.
- `tests/test_validate_repo.py` protects many domain invariants and should not
  be split before source/index owners are clearer.

Next work:

- group validator responsibilities by authority domain after README, roadmap,
  docs, decisions, AGENTS, mechanics, and naming surfaces are clear;
- update validator tokens and tests in lockstep with wording changes.

Exit gate:

- validators can name the invariant they protect;
- green validation means more than file presence;
- proof topology remains constrained after decomposition.

### Horizon: Active Proof Loop

Goal: make the repository actively usable for bounded proof work without
requiring runtime, stack, or sibling authority.

Target route:

`pick proof question -> inspect source bundle -> expand fixture/report contract -> select candidate evidence -> review against bundle -> publish bounded report -> emit optional receipt`

Exit gate:

- this route can be followed locally from `aoa-evals`;
- receipts, runtime candidates, generated summaries, and sibling refs remain
  subordinate to bundle-local review;
- release-support reports remain handoff and readiness artifacts, not GitHub
  status, tag authority, or goal-completion authority.

## Current Public Surface

Use [EVAL_INDEX.md](EVAL_INDEX.md) and [EVAL_SELECTION.md](EVAL_SELECTION.md)
for the current public eval map and selection route.

No additional planned starter bundles are currently named publicly.

The current roadmap focus is structural maturity, not bundle-count expansion.

## Standing Direction

Keep the proof organ honest and legible:

- source proof bundles own bounded claims;
- generated readers route back to authored sources;
- runtime, machine, trace, and sibling artifacts remain candidate evidence
  until bundle-local review accepts a bounded interpretation;
- receipts record publication after review; they do not strengthen proof;
- quests track return obligations; they do not become verdicts;
- decisions explain why; they do not replace source truth;
- mechanics route repeatable operations; they do not steal bundle meaning;
- legacy preserves lineage behind active owner routes.

## Verification Posture

This roadmap names when a change should trigger proof-surface verification. It
does not own the command list.

For roadmap, questbook, decision, source quest, generated-reader, runtime
candidate, or broader proof-surface changes, follow
[AGENTS.md#verify](AGENTS.md#verify) and the nearest local route card. When the
verification posture itself changes, update this section only to preserve the
directional gate, not to mirror every executable command.
