# Proof Topology

## Role

`docs/PROOF_TOPOLOGY.md` maps the authority classes inside `aoa-evals`.

It is not the roadmap, architecture reference, eval bundle, decision log,
generated catalog, or mechanics atlas. It answers a narrower question:

Which kind of proof surface am I touching, and what may that surface own,
receive, transform, emit, or route onward?

## Topology Thesis

`aoa-evals` becomes safer to refactor when its topology is convex.

Convex topology means the main proof classes protrude clearly enough that a
reader can tell source proof objects, derived readers, candidate evidence,
receipts, quest obligations, decisions, sibling references, legacy lineage, and
mechanic-ready operations apart before editing.

The goal is not a decorative tree. The goal is a repository shape where correct
route choice is easier than overclaiming.

## Authority Classes

| Class | Primary surfaces | Owns | Receives or emits | Boundary |
| --- | --- | --- | --- | --- |
| Source proof objects | `bundles/*/EVAL.md`, `bundles/*/eval.yaml`, bundle-local notes and fixtures | bounded claim, object under evaluation, evidence posture, verdict logic, baseline or comparison posture, blind spots | receives selected evidence and review context; emits bundle-local report expectations and bounded interpretation | strongest local proof meaning for one eval claim |
| Source guidance | `DESIGN.md`, `docs/ARCHITECTURE.md`, `docs/EVAL_PHILOSOPHY.md`, score, verdict, portability, comparison, trace, and infra guides | repo form, proof philosophy, review vocabulary, guide-level interpretation rules | receives pressure from bundles, reports, decisions, and validators; emits routeable guidance | guides do not rewrite a specific bundle claim |
| Shared proof infrastructure | `fixtures/`, `runners/`, `scorers/`, `schemas/`, `templates/`, reusable report contracts | reusable contracts and execution support for proof work | receives bundle needs; emits fixtures, runner contracts, scorer helpers, schemas, and templates | stays weaker than bundle-local interpretation |
| Reports and examples | `reports/`, `examples/` | public-safe readouts, dry reviews, and example payloads | receive source bundle contracts and schemas; emit reviewable examples, bounded result artifacts, or non-publishing intake previews | examples illustrate; reports read one bounded result; dry reviews do not publish receipts |
| Derived readers | `generated/`, `EVAL_INDEX.md`, `EVAL_SELECTION.md`, generated quest readers | navigation, selection, compact projections, deterministic read models | receive authored source surfaces through builders; emit read-heavy routing surfaces | generated surfaces are companions, not proof authority |
| Candidate evidence | runtime evidence selections, artifact-to-verdict hooks, runtime candidate intake and template indexes | selected evidence packets and hook shapes that may support review | receive runtime, trace, machine, or sibling artifacts; emit candidate packets for bundle-local review | candidate evidence is not accepted verdict meaning |
| Receipts | `docs/EVAL_RESULT_RECEIPT_GUIDE.md`, `schemas/eval-result-receipt.schema.json`, `examples/eval_result_receipt.example.json`, `.aoa/live_receipts/` | publication facts for one bounded eval result | receive reviewed report facts; emit sidecar records for downstream readers | receipts do not outrank reports or bundles |
| Release publication | `docs/RELEASING.md`, `CHANGELOG.md`, `scripts/release_check.py`, `.github/workflows/repo-validation.yml`, `reports/proof-release-readiness-audit-v1.json`, Git tags and GitHub release notes | bounded release scope, public release narrative, release audit route, readiness review, and landing gate posture | receives changed proof surfaces and generated checks; emits readiness audit, release-prep handoff, tag, and release notes | release publication does not strengthen eval claims; readiness audit is not publication |
| Quest obligations | `QUESTBOOK.md`, `quests/`, generated quest catalog and dispatch | deferred proof, regression, and verdict-bridge obligations | receive unresolved proof pressure; emit return routes and dispatch hints | quests are obligations, not eval bundles |
| Decisions | `docs/decisions/` | durable rationale for topology, workflow, validation, compatibility, or authority changes | receive reviewed evidence and alternatives; emit why a route was chosen | decisions explain; they do not become source truth |
| Agent guidance | `AGENTS.md`, local `AGENTS.md` cards, `DESIGN.AGENTS.md`, `.agents/`, `.agents/skills/`, `.agents/spark/` | editing route, local risk, validation, closeout posture | receives topology and source-owner rules; emits bounded operating guidance | guidance routes proof work without owning verdict meaning |
| Sibling references | dependency refs and evidence refs into sibling repositories | cited inputs to local proof review | receive stronger owner truth from sibling repos; emit local proof references | no sibling authority transfer |
| Legacy lineage | Agon, wave, phase-alpha, old path names, historical bundle-family names, accepted legacy inputs | provenance, compatibility, and historical routeability | receives old names and old paths; emits current owner routes or containment notes | legacy preserves lineage without steering active topology |
| Mechanic-ready operations | `mechanics/*` packages | repeatable proof-layer operations once they have a real owner, inputs, outputs, and validation | receive recurring operations from the current root districts; emit package-local route cards and validators | no empty package taxonomy |

## Root Technical Districts

The current root districts remain valid while Phase 4 maps the topology.
Movement should happen only when a district has a clearer owner route, a
provenance plan, and a validator that can detect drift.

| District | Current role | Current posture |
| --- | --- | --- |
| `bundles/` | source proof object district | stays root-owned; package movement is not planned |
| `docs/` | source guidance, topology maps, decisions, bridge guides, legacy-heavy Agon and wave docs | stays root technical district while proof families are mapped |
| `generated/` | deterministic derived readers | stays generated-only; rebuild through builders |
| `examples/` | public-safe examples, candidate packets, receipts, hook payloads | stays example district; candidate-only posture must remain visible |
| `fixtures/`, `runners/`, `scorers/`, `schemas/`, `templates/` | shared proof infrastructure | stays shared infra; later `proof-infra` mechanic may own recurring operation |
| `reports/` | bounded readouts and reusable proof-flow examples | stays report district; reports remain below bundle-local meaning |
| `quests/` | lane/state source quest records and legacy/source-compatible quest notes | uses `quests/<lane>/<state>/` paths; generated quest readers must mirror current source paths |
| `config/` and `manifests/` | recurrence, Agon, and seed configuration surfaces | stays compatibility/provenance district until a specific mechanic owns the operation |
| `evals/` | Titan canary proof seeds | stays canary district routed by `mechanics/titan-canaries/`; seed canaries are not full incarnation proof |
| `.agents/` | maintained agent lanes and exported support skills | durable agent-facing district; not proof canon |
| `.agents/skills/` | installed local skills that support repo work | supports agent operation; not proof canon |
| `.agents/spark/` | maintained Spark fast-loop lane | routes narrow proof-surface work without owning proof meaning |
| `.aoa/live_receipts/` | owner-local live receipt log | receipt sidecar only; not a verdict source |
| `mechanics/` | operation atlas for repeatable proof-layer operations | active only where a package owns a real operation; currently `proof-object`, `proof-loop`, `comparison-spine`, `proof-infra`, `publication-receipts`, `proof-release`, `titan-canaries`, `agon-proof`, `questbook`, `runtime-evidence`, and `sibling-proof-refs` |

## Mechanic Readiness

A future `mechanics/` package is ready only when the operation has all of these:

- one recurring proof-layer operation;
- source artifacts it can route without stealing their authority;
- clear inputs and outputs;
- a stronger-owner or sibling-owner split when applicable;
- legacy or accepted-input posture if old names remain;
- local `AGENTS.md` guidance or package card shape;
- at least one validator, builder, or review check that constrains the route.

Active mechanic packages:

- `proof-object`
- `proof-loop`
- `comparison-spine`
- `proof-infra`
- `publication-receipts`
- `proof-release`
- `titan-canaries`
- `agon-proof`
- `questbook`
- `runtime-evidence`
- `sibling-proof-refs`

Candidate mechanic families are currently empty. The next package should still
be chosen by live operation pressure, not by symmetry with sibling
repositories.

## Legacy and Naming

Active names should describe the living proof operation.

Legacy names remain useful when they preserve:

- old public paths;
- historical Agon or wave context;
- accepted source inputs;
- generated or external references that still point at earlier vocabulary;
- proof lineage needed to understand why a current surface exists.

Each accepted legacy name should eventually have a current owner route,
provenance note, accepted-input reason, and containment or retirement posture.
Until then, legacy-heavy surfaces should stay visibly marked rather than being
renamed by convenience.

Use `docs/LEGACY_NAMING.md` as the active map for naming posture. It separates
`active`, `historical`, `accepted-input`, `generated-projection`,
`candidate-only`, and `retire-after` names so Agon, wave, phase-alpha,
runtime-candidate, artifact-to-verdict, bundle-family, Titan canary, historical
Spark root-path vocabulary, and source quest path vocabulary remain traceable
without steering active topology by habit.

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

If those answers are unclear, do not move the file yet. Clarify the topology
first.

## Validation

Current checks that keep this topology visible:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

When generated readers change, run the owning builder in `--check` mode. When a
mechanic package is later introduced, add package-shape checks only after that
package owns a real operation.
