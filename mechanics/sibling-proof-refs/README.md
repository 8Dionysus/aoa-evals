# Sibling Proof Refs Mechanic

## Role

`mechanics/sibling-proof-refs/` routes the recurring operation that keeps
repo-qualified proof references into sibling repositories current,
compatibility-aware, and bounded by owner truth.

It is not a sibling repo owner, migration tool, generated catalog, or proof
bundle.

## Owned Operation

The owned operation is:

`repo-qualified ref -> sibling owner route -> current/legacy/rejected/unresolved posture -> latest-sibling canary -> bundle-local review`

This package turns sibling path drift into a reviewable compatibility boundary
instead of a one-off broken-link chore.

## Source Surfaces

- `docs/SIBLING_PROOF_REFS.md`
- `docs/decisions/0003-sibling-proof-reference-compatibility.md`
- `scripts/sibling_canary_matrix.json`
- `scripts/run_sibling_canary.py`
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
- legacy sibling refs that still preserve provenance or accepted input.

## Outputs

- current local proof refs;
- compatibility notes for legacy or accepted-input refs;
- rejected or unresolved posture for refs that should not feed proof;
- latest-sibling canary evidence;
- owner-route guidance for future repair.

## Stronger Owner Split

`aoa-evals` owns bounded proof wording, local proof interpretation, local
compatibility posture, and whether a sibling ref may support a local proof
claim.

The sibling repo owns the referenced object meaning.

`abyss-stack` is special: the canary uses the `abyss-stack-source` resolver so
runtime-evidence schema refs resolve against the source checkout rather than a
deployed `Configs` mirror.

## Boundaries

- Do not edit sibling repositories from this package.
- Do not treat path existence as sibling owner acceptance.
- Do not treat generated readers as the source of sibling truth.
- Do not use legacy refs as active topology without a current owner route.
- Do not let a sibling ref promote a bundle, receipt, runtime candidate, or
  quest by itself.

## Legacy Posture

Old sibling paths may stay only when they preserve source lineage or accepted
input. They should be marked `legacy` and paired with a current route or repair
plan when the current owner surface is known.

The first repaired drift in this refactor was `aoa-memo` path movement. That
repair stays local to `aoa-evals` unless the user explicitly routes work to
`aoa-memo`.

The first pinned public-lane refresh was the `aoa-memo` checkout in
`.github/workflows/repo-validation.yml`, moved to
`97f19698c94ebbebabe8b1b6f22e5ccff3bc5f1f` after GitHub `Repo Validation`
failed against stale memo paths.

## Validation

After changing sibling refs, compatibility docs, canary matrix entries, or this
mechanic, run:

```bash
python scripts/validate_repo.py
python scripts/run_sibling_canary.py --repo-root . --format json
python scripts/validate_semantic_agents.py
```

When `.github/workflows/repo-validation.yml` changes, rerun the release route
and watch GitHub `Repo Validation` rather than treating the local canary as a
substitute for the pinned public lane.

If generated readers changed because source proof refs changed, run the owning
builder in `--check` mode too.

## Next Route

The next honest movement is to add a machine-readable compatibility ledger only
after repeated sibling drift proves the current docs and canary matrix are not
enough.
