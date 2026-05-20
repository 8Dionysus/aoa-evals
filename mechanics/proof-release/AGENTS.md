# AGENTS.md

## Applies to

`mechanics/proof-release/` and release proof publication route guidance.

## Role

This package routes bounded `aoa-evals` release preparation and release audit
work.

It does not own bundle meaning, changelog authority over source proof,
GitHub-native workflow law, release approval for sibling repos, or status
promotion by tag.

## Read before editing

1. repository root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/PROOF_TOPOLOGY.md`
5. `mechanics/README.md`
6. `mechanics/proof-release/README.md`
7. `docs/RELEASING.md`
8. `CHANGELOG.md`
9. `scripts/release_check.py`
10. `reports/proof-release-readiness-audit-v1.json` when auditing an
    accumulated release-prep diff
11. `reports/strategic-closeout-audit-v1.json` when auditing strategic
    completion readiness
12. `reports/release-prep-pr-handoff-v1.json` when reading the pre-PR owner
    landing handoff snapshot without mistaking it for live PR or GitHub `Repo Validation` state
13. `.github/AGENTS.md` when GitHub workflows or PR templates change
14. affected source proof bundles, docs, schemas, generated builders, or
    mechanics packages

## Local Law

- Keep release scope bounded and reviewable.
- Keep `CHANGELOG.md` as public narrative, not proof authority.
- Keep `scripts/release_check.py` as release audit glue, not a replacement for
  bundle-local review.
- Keep GitHub `Repo Validation` aligned with the root landing route.
- Keep release titles plain tag-shaped when publishing, for example `v0.3.3`.
- Keep sibling compatibility claims tied to CI or latest-sibling canary
  evidence.
- Keep readiness audits below tags, GitHub releases, PR approval, and goal
  completion.

## Boundaries

- Do not tag, publish, or edit GitHub Releases from a docs-only mechanics
  update.
- Do not weaken validation to land a release.
- Do not treat a green release audit as proof that every eval claim grew
  stronger.
- Do not treat a readiness audit as GitHub `Repo Validation` or release
  publication.
- Do not hide skipped checks in a release handoff.
- Do not mutate sibling repositories during an `aoa-evals` release route.
- Do not promote bundle status by changelog wording alone.

## Validation

Run the narrow package route checks:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
python scripts/release_check.py
```

Run generated and sibling checks when the release scope includes those
surfaces:

```bash
python scripts/build_catalog.py --check
python scripts/generate_eval_report_index.py --check
python scripts/generate_runtime_candidate_template_index.py --check
python scripts/generate_runtime_candidate_intake.py --check
python scripts/generate_phase_alpha_eval_matrix.py --check
python scripts/run_sibling_canary.py --repo-root . --format json
```

## Closeout

Report the release scope, which changelog section carries the narrative,
whether generated surfaces were rebuilt or checked, what `release_check.py` and
GitHub `Repo Validation` cover, which checks were skipped, whether sibling
compatibility was current or pinned, and which bundle-local proof boundaries
remain stronger than the release publication.
