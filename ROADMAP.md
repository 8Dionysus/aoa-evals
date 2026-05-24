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

## Update Rule

Update this roadmap when a change moves repo-level proof direction, horizon
order, public contour, agent-entry posture, roadmap or quest route split,
mechanics atlas direction, validator-decomposition posture, or active proof-loop
direction.

Route local mechanic landings, release notes, quest lifecycle moves, decision
records, generated refreshes, payload relocations, and validator-token
maintenance to their owning surfaces unless the local change alters one of
those repo-level directions.

Before closeout, ask: did this change move proof-organ direction, or did it
only land a local surface?

## Operating Card

| Field | Route |
| --- | --- |
| input | proof-organ pressure, public contour shifts, horizon changes, or verification posture changes |
| output | direction, horizon order, current public contour, and exit gates |
| owner | root roadmap for sequencing; owner surfaces above for detail |
| next route | `docs/AGENT_INDEX.md`, `docs/PROOF_TOPOLOGY.md`, `mechanics/README.md`, then nearest local route card |
| validation | [AGENTS.md#verify](AGENTS.md#verify), `tests/test_roadmap_parity.py`, and roadmap contracts in `scripts/validate_repo.py` |

## Current Direction

`aoa-evals` is past bootstrap. The repository now carries the source eval
bundle corpus, generated proof readers, runtime-candidate templates, trace and
receipt bridges, phase-alpha matrices, Agon alignment surfaces, mechanics
packages, and public-safe proof references into sibling owners.

The current movement is proof-organ maturity:

- keep entry surfaces short enough to trust;
- keep the Agent index chain visible without making the roadmap the index;
- keep decision records as rationale crosswalks, not release notes or generated
  dumps;
- keep roadmap direction separate from release history, quest obligations, and
  validator chronology;
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

## Direction Anchors

These anchors keep direction recoverable without turning the roadmap into a
history ledger or validator-token ledger.

| Anchor | Owner surface | Directional use |
| --- | --- | --- |
| Root proof spine | `DESIGN.md`, `DESIGN.AGENTS.md`, `docs/ARCHITECTURE.md` | Keep root design compact and proof-bundle meaning bounded. |
| Agent index chain | `docs/AGENT_INDEX.md` | Keep the pass-through route from repo to authority class, operation, mechanic parent, part, payload, and validation visible. |
| Proof Topology Map | `docs/PROOF_TOPOLOGY.md` | Keep source, generated, candidate, receipt, sibling, legacy, and active mechanic authority classes separate. |
| Decision memory | `docs/decisions/README.md` | Keep decision records as rationale and crosswalks by surface class, mechanic parent, and validation guard family. |
| Legacy naming | `docs/LEGACY_NAMING.md` | Keep active names and legacy bridge posture explicit so active topology stays the first route. |
| Mechanics evidence | `mechanics/EVIDENCE_CLUSTERS.md` | Keep parent evidence, root district posture, and residual root-authored surface classification outside roadmap body detail. |
| Route residue guard family | `scripts/validate_repo.py`, route cards, and `docs/decisions/` | Keep generated/readout, active mechanic, root-authored, decision, repo-config, source-bundle, and mechanic-payload residue guards routed to their owner contracts. |
| Mechanic lower index | `mechanics/README.md`, parent `DIRECTION.md`, parent `PARTS.md`, part `README.md`, part `VALIDATION.md`, and parent `parts/AGENTS.md` | Keep parent direction, part/payload source surfaces, parts index synchronization, local validation routes, and payload coverage recoverable through owner surfaces instead of copied guard text. |
| Legacy bridge | parent `PROVENANCE.md` and `legacy/` | Keep single controlled bridge posture, active mechanic surfaces, and runtime evidence limits behind the active route. |
| Proof loop route | `mechanics/proof-loop/README.md` and bundle-local `reports/` | Keep schema-backed proof-loop evidence discoverable through the owning route instead of copying report paths into roadmap direction. |
| Generated report readers | `generated/README.md` | Keep report and receipt readers derived from source reports. |
| Publication receipt posture | `mechanics/publication-receipts/README.md` | Keep receipt publication status under the receipt mechanic and bundle-local review route. |
| Release-support posture | `mechanics/release-support/README.md` | Keep readiness, strategic closeout, and PR handoff under release-support ownership while roadmap carries only direction. |

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
