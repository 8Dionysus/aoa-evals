# Boundary Bridge Mechanic

## Entry Route

Start with this README for role and owned operation. Then read [DIRECTION.md](DIRECTION.md) for current operating direction, [PARTS.md](PARTS.md) for active parts, and [PROVENANCE.md](PROVENANCE.md) as the active-to-archive bridge for legacy or former-placement lookup.

## Role

`mechanics/boundary-bridge/` routes the recurring operation that keeps
repo-qualified proof references and sibling-owned proof anchors current,
compatibility-aware, and bounded by owner truth.

Sibling repositories keep owner truth, migration authority, and source proof
meaning. This package keeps compatibility maps, sibling references, canary
matrices, orchestrator proof anchors, and Phase Alpha bridge readouts current
for local review.

## Owned Operation

The owned operation is:

`repo-qualified ref or class-facing proof anchor -> sibling owner route -> current/legacy/rejected/unresolved posture -> latest-sibling canary or quest validator -> bundle-local review or quest review`

This package gives sibling path drift a standing compatibility boundary:
posture vocabulary, latest-sibling canary evidence, sibling owner route, and
bundle-local review. Orchestrator-facing proof anchors stay in the bridge part,
with role identity routed to `aoa-agents`. The Phase Alpha eval matrix stays as
the bridge from sibling-owned playbook run truth to local eval anchors, with
its builder owned by the matrix part.

## Source Surfaces

- `mechanics/boundary-bridge/PARTS.md`
- `mechanics/boundary-bridge/PROVENANCE.md`
- `mechanics/boundary-bridge/parts/README.md`
- `mechanics/boundary-bridge/parts/compatibility-map/docs/SIBLING_PROOF_REFS.md`
- `mechanics/boundary-bridge/parts/compatibility-map/README.md`
- `mechanics/boundary-bridge/parts/orchestrator-proof-anchors/docs/ORCHESTRATOR_PROOF_ALIGNMENT.md`
- `mechanics/boundary-bridge/parts/orchestrator-proof-anchors/README.md`
- `mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/README.md`
- `mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/examples/phase_alpha_eval_matrix.example.json`
- `mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/schemas/phase-alpha-eval-matrix.schema.json`
- `mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py`
- `mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/generated/phase_alpha_eval_matrix.min.json`
- `docs/decisions/AOA-EV-D-0003-sibling-proof-reference-compatibility.md`
- `mechanics/boundary-bridge/parts/latest-sibling-canary/config/sibling_canary_matrix.json`
- `mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py`
- `mechanics/boundary-bridge/parts/latest-sibling-canary/tests/test_sibling_canary.py`
- `mechanics/boundary-bridge/parts/latest-sibling-canary/README.md`
- `scripts/validate_repo.py`
- `.github/workflows/repo-validation.yml` for pinned public sibling checkouts
- bundle-local `EVAL.md`, `eval.yaml`, notes, reports, and examples that cite
  `repo:<sibling>/...` refs
- generated readers that carry sibling refs from source proof surfaces

## Inputs

- dependency refs into `aoa-techniques` and `aoa-skills`;
- proof evidence refs into `aoa-agents`, `aoa-playbooks`, `aoa-memo`,
  `aoa-routing`, `aoa-kag`, `aoa-sdk`, `aoa-stats`, and `abyss-stack`;
- path drift detected by `validate_repo.py` or the latest-sibling canary;
- path drift detected by GitHub `Repo Validation` because a pinned sibling
  checkout is older than current local proof refs;
- orchestrator-facing quest records that cite `aoa-agents` class refs,
  playbook family refs, and memo surface refs;
- Phase Alpha run matrix entries from `aoa-playbooks` that need local eval
  anchors and support refs with playbook authority routed back to
  `aoa-playbooks`;
- legacy sibling refs that still preserve provenance or accepted input.

## Outputs

- current local proof refs;
- compatibility notes for legacy or accepted-input refs;
- rejected or unresolved posture for refs that route to owner review before proof use;
- latest-sibling canary evidence;
- orchestrator proof-anchor guidance and quest owner-surface bindings;
- generated Phase Alpha eval matrix entries for release and recurrence checks;
- owner-route guidance for future repair.

## Stronger Owner Split

`aoa-evals` owns bounded proof wording, local proof interpretation, local
compatibility posture, local orchestrator proof-anchor posture, and whether a
sibling ref may support a local proof claim.

The sibling repo owns the referenced object meaning.

`abyss-stack` is special: the canary uses the `abyss-stack-source` resolver so
runtime evidence schema refs resolve against the source checkout; the deployed
`Configs` mirror remains runtime artifact territory.

## Boundaries

| Pressure | Route |
| --- | --- |
| sibling repository needs an edit | route through the sibling owner before changing it |
| path existence looks like sibling owner acceptance | keep it as compatibility evidence below owner acceptance |
| generated reader carries a sibling ref | trace back to source surfaces and the sibling owner route |
| legacy ref appears in active topology | pair it with a current owner route before proof use |
| orchestrator proof anchor reads as orchestrator identity, role policy, playbook authority, or memo truth | route identity, role, playbook, and memo meaning to their stronger owners |
| Phase Alpha eval matrix entry reads as playbook approval, runtime verdict, or bundle-local eval result | keep it as a bridge entry below those owner surfaces |
| sibling ref appears to promote a bundle, receipt, runtime candidate, or quest | route promotion through bundle-local review, receipt, runtime-candidate, or quest owner surfaces |

## Legacy Posture

Old sibling paths may stay only when they preserve source lineage or accepted
input. They should be marked `legacy` and paired with a current route or repair
plan when the current owner surface is known.

Former root paths and rejected parent names are mapped through
`mechanics/boundary-bridge/PROVENANCE.md`; archive indexes stay behind that
single bridge.

The first repaired drift in this refactor was `aoa-memo` path movement. That
repair stays local to `aoa-evals` unless the user explicitly routes work to
`aoa-memo`.

The first pinned public-lane refresh was the `aoa-memo` checkout in
`.github/workflows/repo-validation.yml`, moved to
`97f19698c94ebbebabe8b1b6f22e5ccff3bc5f1f` after GitHub `Repo Validation`
failed against stale memo paths.

## Validation

Use [AGENTS](AGENTS.md#validation) for executable validation commands. This
README names the mechanic role, routes, and boundaries; the nearest route card
owns command execution.

When generated or source-support surfaces change, follow the same AGENTS
validation lane before closeout.

## Next Route

The next honest movement is a machine-readable compatibility ledger when
repeated sibling drift shows the current docs and canary matrix need a shared
ledger surface.
