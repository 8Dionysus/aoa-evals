# Shared Proof Infra Guide

This guide defines how shared fixture, runner, scorer, and dossier contracts should grow without hiding bundle-local meaning.

Use it when the question is:
- when should a repeated contract become shared infrastructure?
- how do primary and additional shared paths stay readable?
- how do shared helpers stay weaker than bundle-local interpretation boundaries?

## Shared contract rules

Use shared infrastructure only when the same pattern is already stable across more than one bundle family.

Keep these public rules:
- `shared_fixture_family_path` is the primary shared family for the bundle
- `additional_shared_fixture_family_paths` records extra reusable families without replacing the primary one
- `paired_readout_path` is the primary shared dossier for the bundle
- `additional_paired_readout_paths` records extra dossiers without replacing the primary one
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

Do not use shared names to imply stronger truth than the bundle already supports.

## Boundary discipline

Shared infrastructure should:
- reduce duplicated contract plumbing
- keep replacement rules explicit
- keep path validation deterministic
- keep report schemas and example artifacts bundle-local

Shared infrastructure should not:
- create a repo-global score
- erase bundle-local interpretation guidance
- promote draft surfaces by abstraction
- force a single readout shape across unrelated bundles
