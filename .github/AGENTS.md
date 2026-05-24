# AGENTS.md

## Applies to

This card applies to `.github/` and GitHub-native workflow, pull request,
CODEOWNERS, and repository metadata files in this repository.

## Role

`.github/` is the GitHub platform route for `aoa-evals`: workflows, PR
templates, CODEOWNERS, and repository metadata that support the root landing
route.

GitHub automation stays public-safe and deterministic. Source-owned docs,
validators, mechanics cards, and bundle-local proof objects carry proof meaning.

## Operating Card

| Field | Route |
| --- | --- |
| role | GitHub platform route for workflows, templates, CODEOWNERS, and repository metadata |
| input | workflow, pull request template, CODEOWNERS, check-name, or repository-policy change |
| output | GitHub-native support surface aligned with the root landing route, validation evidence, or owner-route handoff |
| owner | `.github/AGENTS.md` owns GitHub-native support; root `AGENTS.md` owns branch/PR/CI/merge, owner boundaries, and the shortest validation path |
| next route | root `AGENTS.md`, `.github/workflows/`, `.github/pull_request_template.md`, `.github/CODEOWNERS`, `scripts/validate_repo.py`, `scripts/release_check.py` |
| tools | workflow YAML inspection, root validation lane, release check when Repo Validation or landing posture changes |
| validation | this card's `Verify` section |

## Boundary Routes

| Pressure | Route |
| --- | --- |
| sibling doctrine or workflow meaning | route to the owning sibling repository, then carry only explicit public handoff here |
| private workspace or hidden release behavior | route to root `AGENTS.md` or the owner-local non-public surface; checked-in GitHub files stay public-safe and deterministic |
| secret or private environment setup | route to GitHub, repository, or organization secret ownership; checked-in files name only the public contract |
| sibling repository mutation | route through explicit owner review before adding workflow behavior |
| CI-green pressure | fix the source guardrail, proof surface, or test evidence so `Repo Validation` keeps catching drift |

## Platform sync

Keep `.github/CODEOWNERS`, PR templates, and workflow names aligned with the root route card.
`Repo Validation` is the landing check expected by the root GitHub landing workflow. If that check is added, renamed, or its meaning changes, update the root route, PR expectations, and this file in the same change.

When workflow or repository-policy files change, report:

- GitHub surface touched
- local validation run
- whether `Repo Validation` was added, renamed, skipped, or changed
- remaining platform risk

## Verify

Use the root `AGENTS.md` verification path for the changed surface. For GitHub-only edits, inspect the workflow YAML and run the nearest repo-local static, release, or validation check when available.
