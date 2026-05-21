# Boundary Bridge Mechanic

## Entry Route

Start with this README for role and owned operation. Then read [DIRECTION.md](DIRECTION.md) for current operating direction, [PARTS.md](PARTS.md) for active parts, and [PROVENANCE.md](PROVENANCE.md) only for legacy or former placement.

## Role

`mechanics/boundary-bridge/` routes the recurring operation that keeps
repo-qualified proof references and sibling-owned proof anchors current,
compatibility-aware, and bounded by owner truth.

It is not a sibling repo owner, migration tool, generated catalog, or proof
bundle.

## Owned Operation

The owned operation is:

`repo-qualified ref or class-facing proof anchor -> sibling owner route -> current/legacy/rejected/unresolved posture -> latest-sibling canary or quest validator -> bundle-local review or quest review`

This package turns sibling path drift into a reviewable compatibility boundary
instead of a one-off broken-link chore. It also keeps orchestrator-facing proof
anchors as a bridge part rather than creating an `orchestrator` parent package
or importing role identity from `aoa-agents`. It also keeps the Phase Alpha
eval matrix as a bridge from sibling-owned playbook run truth to local eval
anchors rather than leaving the matrix builder as a loose root script.

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
- `docs/decisions/0003-sibling-proof-reference-compatibility.md`
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
  anchors and support refs without importing playbook authority;
- legacy sibling refs that still preserve provenance or accepted input.

## Outputs

- current local proof refs;
- compatibility notes for legacy or accepted-input refs;
- rejected or unresolved posture for refs that should not feed proof;
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
runtime evidence schema refs resolve against the source checkout rather than a
deployed `Configs` mirror.

## Boundaries

- Do not edit sibling repositories from this package.
- Do not treat path existence as sibling owner acceptance.
- Do not treat generated readers as the source of sibling truth.
- Do not use legacy refs as active topology without a current owner route.
- Do not treat orchestrator proof anchors as orchestrator identity, role
  policy, playbook authority, or memo truth.
- Do not treat Phase Alpha eval matrix entries as playbook approval, runtime
  verdicts, or bundle-local eval results.
- Do not let a sibling ref promote a bundle, receipt, runtime candidate, or
  quest by itself.

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

The next honest movement is to add a machine-readable compatibility ledger only
after repeated sibling drift proves the current docs and canary matrix are not
enough.
