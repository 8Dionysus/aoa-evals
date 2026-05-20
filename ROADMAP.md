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
- decision memory is present in `docs/decisions/`;
- sibling proof references have been repaired against the current `aoa-memo`
  topology;
- `ROADMAP.md`, `QUESTBOOK.md`, and `quests/` now need to hold separate,
  routeable roles before mechanics or agent-lane moves begin.

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
- `bundles/aoa-diagnosis-cause-discipline/EVAL.md`
- `bundles/aoa-repair-boundedness/EVAL.md`
- `generated/eval_catalog.min.json`
- `generated/eval_capsules.json`
- `generated/eval_sections.full.json`
- `generated/runtime_candidate_template_index.min.json`
- `generated/runtime_candidate_intake.min.json`
- `generated/eval_report_index.min.json`
- `generated/phase_alpha_eval_matrix.min.json`
- `docs/PROGRESSION_EVIDENCE_MODEL.md`
- `docs/SELF_AGENT_CHECKPOINT_EVAL_POSTURE.md`
- `docs/RECURRENCE_PROOF_PROGRAM.md`
- `docs/TRACE_EVAL_BRIDGE.md`
- `docs/EVAL_RESULT_RECEIPT_GUIDE.md`
- `docs/RUNTIME_BENCH_PROMOTION_GUIDE.md`

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

- `docs/decisions/0001-root-design-spine.md`
- `docs/decisions/0002-proof-object-authority-contract.md`
- `docs/decisions/0003-sibling-proof-reference-compatibility.md`

Near-term additions:

- questbook topology decision;
- mechanics and legacy topology decision before any package creation or move;
- runtime-evidence intake decision before any stronger runtime seam is added.

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
- `quests/agon/captured/AOE-Q-AGON-*.md` files are
  legacy/source-compatible Agon alignment notes.
- `generated/quest_catalog.min.json` and `generated/quest_dispatch.min.json`
  are derived read models.

Near-term work:

- add and maintain `quests/README.md` and `quests/AGENTS.md`;
- keep old top-level quest paths as legacy path vocabulary, not active source
  files;
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

Goal: classify source, derived, candidate, receipt, sibling, legacy, and
mechanic-ready artifact classes before moving files.

Current state:

- `docs/PROOF_TOPOLOGY.md` maps authority classes and current root technical
  districts.
- `docs/decisions/0005-proof-topology-map.md` records why topology mapping
  comes before mechanics creation or file movement.
- `scripts/validate_repo.py` checks that the topology map and decision stay
  discoverable during full repository validation.

Near-term work:

- use the topology map to decide which surfaces stay as root technical
  districts and which need future mechanic packages;
- preserve public-safe sibling references and legacy aliases as explicit
  compatibility surfaces.

Exit gate:

- no major source/derived/candidate/receipt/legacy confusion remains unnamed;
- the first mechanics package has a real operation to own.

### Phase 5: Mechanics Atlas

Goal: create `mechanics/` only when it routes repeatable proof-layer operations.

Current state:

- `mechanics/README.md` is the active operation atlas.
- `mechanics/proof-object/` is the active package for source proof-object
  completeness, bundle lifecycle posture, generated-reader derivation, and
  bundle-local review boundaries.
- `mechanics/comparison-spine/` is the active package for fixed-baseline,
  peer-compare, and longitudinal-window semantics, generated comparison
  readers, and anti-overread boundaries.
- `mechanics/proof-infra/` is the active package for shared fixture, runner,
  scorer, schema, report, template, and generated proof-artifact contract
  routing.
- `mechanics/publication-receipts/` is the active package for optional eval
  result receipts, the local stats envelope mirror, receipt publisher, and
  owner-local live receipt route while keeping reports and bundles stronger.
- `mechanics/proof-release/` is the active package for bounded release scope,
  changelog narrative, release audit, GitHub `Repo Validation`, tag/release-note
  posture, and post-release proof boundaries.
- `mechanics/titan-canaries/` is the active package for Titan seed canary
  shape, incarnation and summon discipline guides, `evals/titan_*` seeds, and
  validator-backed boundaries without claiming full incarnation proof.
- `mechanics/agon-proof/` is the active package for Agon pre-protocol proof
  alignment: seed configs, generated registries, observe-only recurrence
  components and hooks, quest notes, recurrence-control-plane stop-lines, and
  owner handoffs without granting live verdict authority.
- `mechanics/questbook/` is the first package because the obligation layer
  already has source records, generated projections, route docs, post-session
  harvest boundaries, and validation pressure.
- `mechanics/runtime-evidence/` is the second live package because runtime
  candidate intake already has examples, schemas, generated readers, builders,
  tests, and a fragile `abyss-stack` authority boundary.
- `mechanics/sibling-proof-refs/` is the third live package because sibling
  reference drift already happened, was repaired locally, and now has a
  compatibility map plus latest-sibling canary route.
- `docs/LEGACY_NAMING.md` now keeps active, historical, accepted-input,
  generated-projection, candidate-only, and retire-after names visible before
  future package moves or retirements.
- `docs/decisions/0006-questbook-mechanic-package.md` records why this package
  exists before other candidates.
- `docs/decisions/0007-runtime-evidence-mechanic-package.md` records why
  runtime evidence gets a proof-side package without gaining verdict authority.
- `docs/decisions/0008-sibling-proof-refs-mechanic-package.md` records why
  sibling refs get a package without transferring sibling authority.
- `docs/decisions/0010-proof-object-mechanic-package.md` records why the
  proof-object route gets a package while `bundles/` stays in place.
- `docs/decisions/0011-comparison-spine-mechanic-package.md` records why the
  comparison route gets a package while bundles, reports, fixtures, and
  generated readers stay in place.
- `docs/decisions/0012-proof-infra-mechanic-package.md` records why shared
  proof infrastructure gets a package while the shared directories stay in
  place.
- `docs/decisions/0013-publication-receipts-mechanic-package.md` records why
  publication receipts get a package while the receipt guide, schemas,
  examples, publisher, reports, and owner-local live receipt log stay in place.
- `docs/decisions/0014-proof-release-mechanic-package.md` records why release
  proof publication gets a package while release docs, changelog, release
  checks, GitHub workflow files, generated surfaces, and source proof bundles
  stay in place.
- `docs/decisions/0015-titan-canaries-mechanic-package.md` records why Titan
  canaries get a package while canary YAML files remain under `evals/` and stay
  seed-defined.
- `docs/decisions/0016-agon-proof-mechanic-package.md` records why Agon proof
  alignment gets a package while Agon docs, configs, generated registries,
  recurrence manifests, quest notes, and recurrence-control-plane bundle files
  stay in place.

Candidate next packages:

- none currently.

No additional candidate package is promoted here until the next source family
shows a narrower operation and validator pressure.

Exit gate:

- no empty package taxonomy;
- every package names owned operation, inputs, outputs, stronger owner split,
  must-not-claim boundaries, validation, and closeout.

### Phase 6: Legacy and Naming Containment

Goal: keep old names traceable without letting them steer active topology.

Current state:

- `docs/LEGACY_NAMING.md` maps Agon, wave, phase-alpha, runtime-candidate,
  artifact-to-verdict, bundle-family, Titan canary, historical Spark root-path
  vocabulary, and source quest path vocabulary to current routes and naming
  postures.
- `docs/decisions/0009-legacy-naming-containment.md` records why the map comes
  before physical movement, deletion, or retirement.
- `scripts/validate_repo.py` checks that the naming map and decision stay
  discoverable.

Near-term work:

- preserve Agon, wave, phase-alpha, runtime-candidate, bundle-family, and old
  Spark root-path names when they are source history or accepted external
  inputs;
- route old names through provenance, accepted-input maps, or package-local
  legacy homes once packages exist;
- use quiet active names for current proof operations.
- move any package-local legacy surface only after the package owns the
  operation and validators can follow the move.

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
- `reports/proof-loop-local-route-smoke-v1.md` records the first public-safe
  local route-smoke: a selected `aoa-verification-honesty` path that ends in a
  bounded report only, with no eval result receipt and no bundle promotion.
- `bundles/aoa-verification-honesty/reports/aoa-evals-slice-19-lifecycle-contract.report.json`
  records the first schema-backed bundle-local report for the active proof
  loop, still with no eval result receipt, no bundle promotion, and no quest
  closure.
- `generated/eval_report_index.min.json` routes readers to real bundle-local
  `*.report.json` artifacts while keeping the index below source reports,
  bundles, and receipt publication.
- `reports/eval-result-receipt-intake-dry-review-v1.json` dry-reviews the
  first report-to-receipt intake path by deriving a payload preview while
  keeping `receipt_status` `not_published`, with no envelope, no publisher run,
  and no live receipt append.
- `reports/proof-release-readiness-audit-v1.json` records local
  proof-release readiness for the accumulated strategic refactor diff while
  keeping tag, GitHub Release, PR approval, GitHub `Repo Validation`, live
  receipt publication, and goal completion explicitly open.
- `reports/strategic-closeout-audit-v1.json` records a
  requirement-by-requirement strategic closeout review for the local refactor
  while keeping the long goal not complete until the diff is landed, GitHub
  `Repo Validation` is observed, and the owner-visible final audit can honestly
  close the goal.
- `reports/release-prep-pr-handoff-v1.json` records the pre-PR owner landing handoff
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
