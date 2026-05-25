# Shared Proof Infra Guide

This guide routes shared fixture, runner, scorer, and dossier contracts so
reusable support grows while bundle-local meaning stays in the source bundle.

Use it when the question is:
- when should a repeated contract become shared infrastructure?
- how do primary and additional shared paths stay readable?
- how do shared helpers stay weaker than bundle-local interpretation boundaries?

## Shared contract rules

Use shared infrastructure only when the same pattern is already stable across more than one bundle family.

Keep these public rules:
- `shared_fixture_family_path` is the primary shared family for the bundle
- `additional_shared_fixture_family_paths` records extra reusable families alongside the primary one
- `paired_readout_path` is the primary shared dossier for the bundle
- `additional_paired_readout_paths` records extra dossiers alongside the primary one
- `runner_surface_path` should reference the active reportable-contract runner
  surface when a bundle exposes machine-readable report artifacts
- `scorer_helper_paths` may reference shared payload builders under the active
  reportable-contract part, but bundle-local schema and `EVAL.md` stay
  authoritative

## Naming discipline

Use these path shapes:
- generic fixture family:
  `mechanics/proof-infra/parts/fixture-families/fixtures/<family-name>/README.md`
- mechanic-owned fixture family:
  `mechanics/<mechanic>/parts/<part>/fixtures/<family-name>/README.md`
- shared reportable runner surface:
  `mechanics/proof-infra/parts/reportable-contracts/runners/<surface-name>.md`
- shared scorer helper:
  `mechanics/proof-infra/parts/reportable-contracts/scorers/<helper_name>.py`
- shared runner, fixture-contract, and report-summary schemas:
  `mechanics/proof-infra/parts/reportable-contracts/schemas/<schema-name>.json`
- shared dossier: `mechanics/<mechanic>/parts/<part>/reports/<readout-name>-vN.md`
  when a mechanic owns it, or `evals/<family>/<eval>/reports/<artifact>.json` when
  the bundle owns it

Use shared names as support labels. Stronger-truth pressure routes back to
bundle-local `EVAL.md`, `eval.yaml`, and reviewed reports.

## Boundary discipline

Shared infrastructure keeps:
- duplicated contract plumbing reduced
- replacement rules explicit
- path validation deterministic
- report schemas and example artifacts bundle-local

| Pressure | Route |
| --- | --- |
| repo-global score pressure | bundle-specific verdict or scoring logic |
| bundle-local interpretation disappears behind shared plumbing | bundle `EVAL.md`, `eval.yaml`, and report schema |
| draft surface looks promoted by shared infrastructure | bundle lifecycle review and release-support route |
| one readout shape spreads across unrelated bundles | bundle-owned report route or mechanic-owned report route |
