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
- `scorer_helper_paths` may reference shared payload builders, but bundle-local schema and `EVAL.md` stay authoritative

## Naming discipline

Use these path shapes:
- fixture family: `fixtures/<family-name>/README.md`
- shared dossier: `reports/<readout-name>-vN.md`
- shared scorer helper: `scorers/<helper_name>.py`
- shared runner surface: `runners/<surface_name>.md`

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
