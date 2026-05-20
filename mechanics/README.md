# Mechanics

## Role

`mechanics/` is the operation atlas for repeatable proof-layer operations in
`aoa-evals`.

It is not the doctrine center, roadmap, decision log, generated catalog, or
proof bundle directory. A mechanic exists only when a recurring operation has
source surfaces, inputs, outputs, boundaries, and validation.

The rule for this atlas is simple: no empty package taxonomy.

## Active Packages

### `proof-object`

`mechanics/proof-object/` owns the operation that keeps source proof objects
complete, bounded, and stronger than generated or emitted companions:

`origin proof pressure -> source proof bundle -> proof-object completeness review -> generated reader derivation -> bundle-local report or downstream route`

It routes `bundles/*/EVAL.md`, `bundles/*/eval.yaml`,
`templates/EVAL.template.md`, proof review guides, generated catalog readers,
and lifecycle posture without moving `bundles/`.

### `proof-loop`

`mechanics/proof-loop/` owns the route that makes one active proof loop locally
followable:

`proof question -> selection route -> source proof object -> support contract -> candidate evidence packet -> bundle-local review -> bounded report -> optional receipt`

It coordinates `proof-object`, `proof-infra`, `runtime-evidence`,
`sibling-proof-refs`, and `publication-receipts` without becoming stronger than
any of those owner routes.

### `comparison-spine`

`mechanics/comparison-spine/` owns the operation that keeps baseline,
peer-compare, and longitudinal-window proof claims bounded:

`comparison claim -> bundle comparison_surface -> shared proof artifacts -> generated comparison spine -> bounded comparison read`

It routes comparison guides, `comparison_surface`, shared proof artifacts,
`generated/comparison_spine.json`, and comparison reports without moving
bundles, reports, fixtures, or generated readers.

### `proof-infra`

`mechanics/proof-infra/` owns the operation that keeps shared proof contracts
reusable without hiding bundle-local meaning:

`bundle proof need -> shared proof contract -> bundle-local contract -> generated proof_artifacts -> bounded review`

It routes shared fixtures, runners, scorers, schemas, reports, templates, and
generated catalog `proof_artifacts` without moving those directories.

### `publication-receipts`

`mechanics/publication-receipts/` owns the operation that keeps optional eval
result publication receipts subordinate to reviewed reports:

`reviewed bounded report -> eval-result receipt payload -> stats-event-envelope sidecar -> owner-local live receipt log -> downstream derived reader`

It routes the eval result receipt guide, payload schema, local stats envelope
mirror, public example, live publisher, reports boundary, and owner-local live
receipt card without moving receipt, report, schema, example, or live-log
surfaces.

### `proof-release`

`mechanics/proof-release/` owns the operation that keeps bounded release
publication coherent without strengthening eval claims:

`bounded release scope -> changelog narrative -> release audit -> Repo Validation -> tag and GitHub release notes -> post-release proof posture`

It routes `docs/RELEASING.md`, `CHANGELOG.md`, `scripts/release_check.py`,
GitHub `Repo Validation`, generated freshness checks, and release-note posture
without moving release docs, changelog, CI, generated surfaces, or source proof
bundles.

### `titan-canaries`

`mechanics/titan-canaries/` owns the operation that keeps Titan seed canary
surfaces shaped and bounded:

`Titan boundary pressure -> seed canary YAML -> shape validation -> future executable scorer route -> bounded proof or owner handoff`

It routes Titan incarnation and summon discipline guides,
`evals/titan_*_canary.yaml`, `evals/AGENTS.md`, legacy naming posture, and
`validate_titan_canary_surfaces` without moving canary YAML files or claiming
full Titan incarnation proof.

### `agon-proof`

`mechanics/agon-proof/` owns the operation that keeps Agon pre-protocol proof
alignment generated, observe-only, and stop-line bounded:

`Agon proof pressure -> seed prebinding or alignment config -> deterministic generated registry -> observe-only recurrence component and hooks -> Agon stop-line review -> bundle-local proof or owner handoff`

It routes Agon docs, seed configs, generated registries, recurrence manifests,
observe-only hooks, quest notes, and recurrence-control-plane stop-line review
without moving those surfaces or granting live verdict authority.

### `questbook`

`mechanics/questbook/` owns the operation that keeps quest obligations
routeable:

`source quest record -> human index -> generated quest reader -> deferred return or reviewed promotion`

It routes the current lane/state quest source paths, `QUESTBOOK.md`, schemas,
generated quest readers, and post-session harvest boundary while keeping old
top-level quest paths as legacy vocabulary only.

### `runtime-evidence`

`mechanics/runtime-evidence/` owns the operation that keeps runtime and trace
artifacts candidate-only until bundle-local review:

`runtime or trace artifact -> selected evidence packet -> runtime candidate reader -> bundle-local review`

It routes runtime evidence selection examples, artifact-to-verdict hooks,
generated candidate readers, runtime promotion guides, and stronger-owner
boundaries without moving verdict authority into runtime.

### `sibling-proof-refs`

`mechanics/sibling-proof-refs/` owns the operation that keeps proof references
into sibling repositories compatibility-aware:

`repo-qualified ref -> sibling owner route -> compatibility posture -> latest-sibling canary -> bundle-local review`

It routes `docs/SIBLING_PROOF_REFS.md`, `scripts/sibling_canary_matrix.json`,
`scripts/run_sibling_canary.py`, and local proof refs without editing sibling
repositories.

## Candidate Families

Candidate families remain named here without package directories until they own
a real proof-layer operation:

Current candidate set: none.

Create a new package only when the candidate has source artifacts to route and
a validator, builder, or review check that can catch drift.

## Package Shape

Each active package should name:

- owned operation;
- source surfaces;
- inputs;
- outputs;
- stronger-owner split;
- legacy or accepted-input posture when relevant;
- boundaries;
- validation;
- next route.

Package cards route recurring work. They do not replace `DESIGN.md`, eval
bundles, decision records, generated builders, or sibling-owner truth.

## Validation

After editing mechanics surfaces, run:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

If the changed package touches generated quest readers, also run:

```bash
python scripts/build_catalog.py --check
```
