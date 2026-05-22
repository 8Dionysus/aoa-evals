# aoa-evals System Design

## Role

`DESIGN.md` describes the system form of `aoa-evals`.

Use it when the question is the bounded proof organ's shape, authority classes,
growth constraints, or how proof bundles, reports, receipts, generated readers,
mechanics, and legacy bridges cooperate.

Adjacent routes:

- public entry: `README.md`
- repo direction: `ROADMAP.md`
- technical proof model: `docs/ARCHITECTURE.md`
- eval-package meaning: `evals/**/EVAL.md` and `evals/**/eval.yaml`
- durable rationale: `docs/decisions/`
- agent-facing route shape: `DESIGN.AGENTS.md` and `AGENTS.md`

It answers one question:

What shape should the bounded proof organ preserve while it grows as an AoA
repository?

## Design Thesis

`aoa-evals` is the bounded proof organ of AoA.

It turns claims about agent-shaped work into reviewable proof objects: claims
with an object under evaluation, evidence substrate, verdict logic, baseline or
comparison posture, report contract, blind spots, and interpretation limits.

The bundle owns the proof object.
The report carries one bounded reading.
The receipt records publication.
The generated surface helps navigation.
The sibling owner keeps its stronger truth.

## Design as Appearance

`aoa-evals` should appear as a proof atlas, not a flat benchmark attic.

A healthy proof layer has:

- a compact public entry route;
- source proof bundles under `evals/`;
- human-readable guides for verdicts, scores, comparison, portability, and
  blind spots;
- shared proof infrastructure for fixtures, runners, scorers, schemas, reports,
  and examples;
- generated companions that route readers back to source bundles;
- quest and decision surfaces that preserve obligations and durable rationale;
- runtime-candidate and receipt surfaces that remain visibly subordinate to
  bundle-local review;
- local agent cards that keep low-context changes inside the nearest proof
  owner lane.

The repository should feel useful without requiring a full local AoA deployment.
AoA federation routes may enrich a proof object, but the public proof surface
must remain understandable from the authored bundle and its public-safe support
artifacts.

## Design as Anatomy

`aoa-evals` is composed of different source classes:

- root public entry and owner-boundary surfaces;
- source-authored eval bundles under `evals/`;
- proof philosophy, architecture, review, score, verdict, comparison,
  portability, and bridge docs under `docs/`;
- shared fixtures, examples, reports, runners, scorers, schemas, and templates;
- generated reader and runtime selection companions under `generated/`;
- quest source records and quest read models for deferred proof obligations;
- decision records that preserve why proof topology or workflow routes moved;
- public-safe receipt and runtime-candidate surfaces;
- agent-facing route cards and maintained agent lanes under `.agents/`;
- mechanics packages for repeatable proof-layer operations;
- legacy and provenance bridges when old names remain accepted inputs.

Each class supports the others. No class should silently steal authority from
another class.

## Design as Operation

The current public use path remains:

`pick -> inspect -> expand -> object use`

As the repository matures into active proof work, the fuller route is:

`pick proof question -> inspect source bundle -> expand fixture/report contract -> select candidate evidence -> review against bundle -> publish bounded report -> emit optional receipt`

A good proof operation has:

- one named bounded claim;
- one object under evaluation;
- a source bundle or explicit proof-object draft;
- evidence whose source and limits are visible;
- verdict logic that can be reviewed;
- baseline, comparison, or repeat-window posture when comparison is claimed;
- blind spots that travel with the claim;
- validation that checks the changed source and derived surfaces;
- a return route to sibling owners when the claim depends on their truth.

Runtime candidates, machine evidence, sibling references, generated catalogs,
and receipts may help the operation. They do not become proof acceptance without
bundle-local review.

## Design as Aim

The long aim is a proof canon that helps AoA grow without lying to itself.

`aoa-evals` should support:

- portable public eval bundles;
- bounded workflow, boundary, artifact, regression, comparison, longitudinal,
  and stress proof surfaces;
- compact reports that humans can review and agents can consume;
- disciplined baseline and comparison semantics;
- proof-pressure quests that can return across long work;
- runtime and machine evidence intake without runtime authority transfer;
- sibling compatibility references without absorbing sibling meaning;
- legacy provenance that keeps old names traceable without steering the active
  topology.

The repository grows well when every new surface makes proof honesty,
routeability, evidence review, or return clearer than before.

## Design Principles

### 1. Bounded proof before confidence

An eval should say what claim is supported, under which conditions, through
which evidence and verdict logic, with which blind spots. Confidence without
that shape is theater.

### 2. Source bundle before generated reader

`evals/**/EVAL.md` and `evals/**/eval.yaml` own bundle meaning. Generated
catalogs, capsules, section indexes, dispatch views, and runtime selectors help
readers orient.

### 3. Review before receipt

A receipt records that a bounded eval result was emitted. It does not outrank
the bundle, the report contract, or the review that interprets evidence.

### 4. Candidate evidence before verdict

Runtime, machine, trace, and sibling artifacts enter as candidate evidence until
a proof object accepts their bounded interpretation.

### 5. Comparison before growth claims

Growth, regression, baseline, and repeated-window claims need explicit
comparison posture. A polished single run is not enough.

### 6. Blind spots travel with proof

Blind spots are part of the proof contract. If a proof surface cannot name its
limits, it is not ready to make a strong claim.

### 7. Self-contained before connected

Sibling routes and AoA law matter, but an eval bundle should remain
public-safe, portable, and reviewable from its own source surfaces.

### 8. Topology should expose authority

Docs, quests, decisions, generated readers, runtime candidates, receipts,
mechanics, and legacy bridges should sit where their authority class is easy to
see.

### 9. Legacy preserves lineage

Old wave, Agon, phase-alpha, runtime-candidate, and bundle-family names may stay
as provenance or accepted input. Active topology should use names that describe
the living proof operation.

### 10. Validation protects meaning

Checks should constrain source truth visibility, generated derivation,
candidate-only posture, sibling-ref status, quest state, receipt subordination,
and proof-object completeness. Green file presence alone is not proof.

## Good Design Feels Like

A reader can find one eval and understand its bounded claim.
An agent can find the nearest route card.
A report can find its bundle.
A generated surface can find its source.
A runtime candidate can find its review boundary.
A sibling reference can find its owner.
A quest can find its obligation and return route.
A future maintainer can find why the topology exists.

## Bad Design Smells Like

- flat benchmark accumulation;
- root docs repeating every guide and bundle;
- generated files cited as proof authority;
- runtime candidates presented as accepted verdicts;
- receipts treated as stronger than reports;
- sibling path drift patched without a compatibility decision;
- quests replacing roadmap direction or bundle meaning;
- old wave names used as active topology because they are familiar;
- broad intelligence, safety, autonomy, or selfhood claims without bounded
  proof objects.

## Relationship to Other Root Surfaces

[`README.md`](README.md) introduces the public repository.
[`AGENTS.md`](AGENTS.md) routes agent work.
[`DESIGN.AGENTS.md`](DESIGN.AGENTS.md) holds the design form of the
agent-facing guidance mesh.
[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) explains the technical proof
model and bundle layering.
[`docs/EVAL_PHILOSOPHY.md`](docs/EVAL_PHILOSOPHY.md) explains the epistemic
posture and limits of evaluation.
[`docs/PROOF_TOPOLOGY.md`](docs/PROOF_TOPOLOGY.md) maps source, derived,
candidate, receipt, quest, decision, sibling, legacy, and active mechanic
authority classes.
[`docs/LEGACY_NAMING.md`](docs/LEGACY_NAMING.md) maps active, historical,
accepted-input, generated-projection, candidate-only, and provenance-bridge
naming postures. It is a posture guide, not an archive map: old names route
through active surfaces and the `PROVENANCE.md` single controlled bridge from
active mechanic surfaces into the legacy archive. `PROVENANCE.md` is a bridge,
not an active route; archive details stay inside the archive. In short:
`PROVENANCE.md` is a bridge, not an active route.
[`mechanics/EVIDENCE_CLUSTERS.md`](mechanics/EVIDENCE_CLUSTERS.md) records the
root-district reconnaissance and cross-root evidence standard for parent
mechanics before files move into or between mechanic packages; it also classifies
residual top-level `docs/`, `scripts/`, and `tests/` surfaces that remain
root-owned after mechanic-owned payload movement.
[`mechanics/README.md`](mechanics/README.md) routes repeatable proof-layer
operations once they have real source surfaces and validation.
[`mechanics/proof-loop/README.md`](mechanics/proof-loop/README.md) routes the
active local proof loop without replacing the packages that own each step.
[`ROADMAP.md`](ROADMAP.md) points direction.
[`QUESTBOOK.md`](QUESTBOOK.md) tracks proof obligations.
[`docs/decisions/`](docs/decisions/) preserves durable structural and workflow
rationale.

`DESIGN.md` holds the system form of the proof layer.

## Use by Agents

Agents should consult this file when a change alters:

- repository shape;
- root surfaces;
- proof-object anatomy;
- source versus generated authority;
- runtime-candidate, receipt, or machine-evidence posture;
- sibling proof-reference compatibility;
- quest or decision topology;
- legacy naming posture;
- mechanics package boundaries;
- agent-facing layer design.

This file does not override local owner truth. It tells agents what kind of
shape the proof layer is preserving.
