# Proof Direction Roadmap

## Role

`ROADMAP.md` is the active direction surface for `aoa-evals`.

It names the current proof-organ direction, horizon order, public contour, and
phase gates that keep movement honest. This roadmap owns direction and sequencing.

Use the stronger owner surface when the work needs detail:

- release history: [CHANGELOG.md](CHANGELOG.md)
- tracked obligations: [QUESTBOOK.md](QUESTBOOK.md) and `quests/`
- route law and executable checks: [AGENTS.md](AGENTS.md) and nearest nested
  `AGENTS.md`
- durable rationale: [docs/decisions/](docs/decisions/)
- source proof meaning: `evals/**/EVAL.md` and `evals/**/eval.yaml`
- proof topology: [docs/PROOF_TOPOLOGY.md](docs/PROOF_TOPOLOGY.md)
- mechanics operations: [mechanics/README.md](mechanics/README.md),
  parent `README.md`, parent `DIRECTION.md`, parent `PARTS.md`, and part
  `README.md`
- validator contracts: `scripts/validate_repo.py` and
  `tests/test_validate_repo.py`

## Operating Card

| Field | Route |
| --- | --- |
| input | proof-organ pressure, public contour shifts, horizon changes, or verification posture changes |
| output | direction, horizon order, current public contour, and exit gates |
| owner | root roadmap for sequencing; owner surfaces above for detail |
| next route | `docs/AGENT_INDEX.md`, `docs/PROOF_TOPOLOGY.md`, `mechanics/README.md`, then nearest local route card |
| validation | [AGENTS.md#verify](AGENTS.md#verify), `tests/test_roadmap_parity.py`, and roadmap contracts in `scripts/validate_repo.py` |

## Current Direction

`aoa-evals` is past bootstrap. The repository now carries 36 eval bundles,
generated proof readers, runtime-candidate templates, trace and receipt
bridges, phase-alpha matrices, Agon alignment surfaces, mechanics packages, and
public-safe proof references into sibling owners.

The current movement is structural maturity:

- keep entry surfaces short enough to trust;
- keep the Agent index chain in `docs/AGENT_INDEX.md` visible from repo root to
  authority class, operation, mechanic parent, part, payload, and validation;
- keep decision records as rationale crosswalks, not generated dumps;
- keep roadmap direction separate from release history and validator chronology;
- keep route commands in local `AGENTS.md` cards while authored docs carry proof
  meaning, topology, and read models;
- preserve mechanics topology before splitting the validator mesh;
- use active names for living proof operations and keep legacy names behind
  provenance bridges.

## Current Public Contour

Current release marker: `v0.3.3`.

The public proof contour stays bounded: this roadmap keeps release anchors
visible while source bundles, reports, receipts, generated readers, runtime
candidates, and sibling references remain under their owning proof objects.
This contour proves only bounded claims.

Current public surface:

- No additional planned starter bundles are currently named publicly.

Use [EVAL_INDEX.md](EVAL_INDEX.md) and [EVAL_SELECTION.md](EVAL_SELECTION.md)
for the public eval map and starter selection route.

Memo pilot claim limit: future scar and retention remain outside current proof;
live memory-ledger readiness stays outside the public contour until a
bundle-local review accepts that claim.

## Directional Anchors

These anchors keep direction recoverable without turning the roadmap into a
history ledger.

| Anchor | Owner surface | Directional use |
| --- | --- | --- |
| Root proof spine | `DESIGN.md`, `DESIGN.AGENTS.md`, `docs/ARCHITECTURE.md` | Keep root design compact and proof-bundle meaning bounded. |
| Agent index chain | `docs/AGENT_INDEX.md` | Keep the pass-through route from repo to authority class, operation, mechanic parent, part, payload, and validation visible. |
| Proof Topology Map | `docs/PROOF_TOPOLOGY.md` | Keep source, generated, candidate, receipt, sibling, legacy, and active mechanic authority classes separate. |
| Decision memory | `docs/decisions/README.md` | Keep decision records as rationale and decision-route residue crosswalks. |
| Legacy naming | `docs/LEGACY_NAMING.md` | Preserve Legacy and Naming Containment, Legacy Naming Single-Bridge Language, and Legacy Naming Posture Guide as active-name support. |
| Mechanics evidence | `mechanics/EVIDENCE_CLUSTERS.md` | Keep the Active Parent Evidence Dimension Ledger and Mechanic Evidence Route Refs tied to contracts/payloads. |
| Root district posture | `mechanics/EVIDENCE_CLUSTERS.md` | Keep the Root District Reconnaissance Ledger visible for route-card-only districts before mechanic-owned payload movement. |
| Root residual classes | `mechanics/EVIDENCE_CLUSTERS.md` | Keep Residual Root-authored Surface Classification explicit for mechanic-owned payload boundaries. |
| Route residue guards | validator and route cards | Keep generated/readout route residue on the same part, active mechanic route residue on authored route cards, root-authored route residue on root-facing authored surfaces, decision-route residue on decision records, repo-config route residue on `.gitignore`, source-bundle route residue on source proof bundles, and mechanic-payload route residue on active mechanics payload. |
| Mechanic lower index | parent `DIRECTION.md`, parent `PARTS.md`, part `README.md` | Keep mechanic parent direction, Mechanic Part Payload Inventory, payload subdirectory inventory, Mechanic Part Source Surface Reference Guard, stale source surface ref detection, Mechanic Part Source Surfaces Section Contract, plural section checks, Mechanic PARTS Index Synchronization, and stale local part route checks visible before validator decomposition. |
| Legacy bridge | parent `PROVENANCE.md` and `legacy/` | Keep Mechanic Legacy Single Bridge, Mechanic Provenance Bridge Posture, bridge, not an active route, single controlled bridge, active mechanic surfaces, and Active Legacy Parent Wording Boundary tied to runtime evidence limits. |
| Part validation route | part `VALIDATION.md` and parent `parts/AGENTS.md` | Keep Mechanic Part Validation Command Reachability and payload coverage anchor visible while commands stay in route cards. |
| Proof loop report | `evals/workflow/aoa-verification-honesty/reports/aoa-evals-slice-19-lifecycle-contract.report.json` | Keep the first schema-backed bundle-local report visible as proof-loop evidence. |
| Generated report index | `generated/eval_report_index.min.json` | Keep report and receipt readers derived from source reports. |
| Publication receipt dry review | `mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json` | Keep the dry-review receipt at `not_published` posture. |
| Release-support readouts | `mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json`, `mechanics/release-support/parts/strategic-closeout/reports/strategic-closeout-audit-v1.json`, `mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json` | Keep release readiness tied to goal completion, strategic closeout tied to long goal not complete posture, and PR handoff tied to owner landing handoff context. |

## Horizons

### Horizon: Entry Surfaces

| Field | Direction |
| --- | --- |
| Current posture | `README.md`, `docs/README.md`, and `docs/AGENT_INDEX.md` now carry clearer entry and pass-through roles. |
| Next movement | Keep the root README public-readable while moving dense route matrices into docs and mechanics indexes. |
| Exit gate | A low-context agent can tell where to start, where detail lives, and which file owns validation commands. |

### Horizon: Decision Memory

| Field | Direction |
| --- | --- |
| Current posture | `docs/decisions/README.md` acts as a decision crosswalk by number, surface class, mechanic parent, validation guard family, and active posture. |
| Next movement | Add decisions only when future agents need rationale; keep decision records weaker than source surfaces and generated/runtime facts. |
| Exit gate | A future agent can find why a route exists without reading a changelog or validator token list. |

### Horizon: Roadmap, Questbook, And Quest Route

| Field | Direction |
| --- | --- |
| Current posture | `ROADMAP.md` owns direction, `QUESTBOOK.md` owns tracked proof obligations, `quests/<lane>/<state>/*.yaml` own source quest records, and generated quest readers remain derived navigation. |
| Next movement | Keep lane/state quest records aligned with generated projections without turning obligations into eval meaning or roadmap direction. |
| Exit gate | Direction, obligation, source quest, and generated quest reader are visibly separate. |

### Horizon: AGENTS Law And Source Meaning

| Field | Direction |
| --- | --- |
| Current posture | Root and nested `AGENTS.md` cards own commands, mutation gates, and local risk while authored docs own proof meaning and topology. |
| Next movement | Audit law-like text by nearest owner and route executable validation posture into route cards. |
| Exit gate | A future edit can tell whether to read `AGENTS.md`, `README.md`, `DESIGN.md`, topology, decisions, mechanics, or validator first. |

### Horizon: Mechanics Atlas And Lower Index

| Field | Direction |
| --- | --- |
| Current posture | Nineteen active parent mechanics own repeatable proof-layer operations through parent route cards, `DIRECTION.md`, `PARTS.md`, part READMEs, payload homes, and legacy bridges. |
| Next movement | Improve wayfinding before parent splits, removals, or validator decomposition. |
| Exit gate | A future agent can start at one payload and recover parent operation, authority class, rationale, and validation route. |

### Horizon: Validator Domain Split

| Field | Direction |
| --- | --- |
| Current posture | `scripts/validate_repo.py` and `tests/test_validate_repo.py` still carry the central contract mesh. |
| Next movement | Split guard classes by authority domain only after entry, roadmap, docs, decisions, AGENTS, mechanics, and naming surfaces make the owner boundaries obvious. |
| Exit gate | Validators can name the invariant they protect and green validation still constrains proof topology. |

### Horizon: Active Proof Loop

| Field | Direction |
| --- | --- |
| Current posture | The local proof loop already has source bundles, report schemas, generated readers, receipt dry review, and release-support readouts. |
| Next movement | Make the route usable locally: pick proof question -> inspect source bundle -> expand fixture/report contract -> select candidate evidence -> review against bundle -> publish bounded report -> emit optional receipt. |
| Exit gate | Receipts, runtime candidates, generated summaries, and sibling refs remain subordinate to bundle-local review. |

## Standing Direction

Keep the proof organ honest and legible:

- source proof bundles own bounded claims;
- generated readers route back to authored sources;
- runtime, machine, trace, and sibling artifacts remain candidate evidence until
  bundle-local review accepts a bounded interpretation;
- receipts record publication after review;
- quests track return obligations;
- decisions explain why;
- mechanics route repeatable operations;
- legacy preserves lineage behind active owner routes.

## Verification Posture

This roadmap names when a change should trigger proof-surface verification.
Executable commands live in route cards.

For roadmap, questbook, decision, source quest, generated-reader,
runtime-candidate, or broader proof-surface changes, follow
[AGENTS.md#verify](AGENTS.md#verify) and the nearest local route card. When the
verification posture itself changes, update this section as the directional
gate, then keep command detail in `AGENTS.md`.
