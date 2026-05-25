# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/release-support/DIRECTION.md` for current operating direction, `mechanics/release-support/PARTS.md` for active parts, and `mechanics/release-support/PROVENANCE.md` as the active-to-archive bridge for legacy or former-placement lookup.

## Applies to

`mechanics/release-support/` and release proof publication route guidance.

## Role

This package routes bounded `aoa-evals` release preparation and release audit
work.

It maps release-prep pressure to changelog narrative, release audit,
readiness/closeout/handoff parts, GitHub validation posture, or stronger-owner
handoff routes.

## Operating Card

| Field | Route |
| --- | --- |
| role | bounded `aoa-evals` release preparation and release audit route |
| input | release scope, `CHANGELOG.md` narrative, release audit, GitHub `Repo Validation` posture, PR handoff, readiness report, or sibling compatibility pressure |
| output | release-support part route, changelog route, release check, generated/sibling check, PR handoff, or stronger-owner handoff |
| owner | `aoa-evals` owns bounded release support; source bundles keep proof meaning, GitHub-native surfaces keep workflow law, and sibling repos keep release approval |
| next route | `mechanics/release-support/README.md`, `DIRECTION.md`, `PARTS.md`, affected part README, `CHANGELOG.md`, `docs/operations/RELEASING.md`, `scripts/release_check.py`, and `.github/AGENTS.md` when GitHub surfaces move |
| tools | root validator, semantic AGENTS validator, `scripts/release_check.py`, generated builders, latest-sibling canary runner |
| validation | this card's `Validation` section |

## Read before editing

1. repository root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/architecture/PROOF_TOPOLOGY.md`
5. `mechanics/README.md`
6. `mechanics/release-support/README.md`
7. `mechanics/release-support/PARTS.md`
8. `mechanics/release-support/parts/README.md`
9. the relevant part `README.md`
10. `docs/operations/RELEASING.md`
11. `CHANGELOG.md`
12. `scripts/release_check.py`
13. `mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json` when auditing an
    accumulated release-prep diff
14. `mechanics/release-support/parts/strategic-closeout/reports/strategic-closeout-audit-v1.json` when auditing strategic
    completion readiness
15. `mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json` when reading the pre-PR owner
    landing handoff snapshot without mistaking it for live PR or GitHub `Repo Validation` state
16. `.github/AGENTS.md` when GitHub workflows or PR templates change
17. affected source proof bundles, docs, schemas, generated builders, or
    mechanics packages

## Local Law

- Keep release scope bounded and reviewable.
- Keep `CHANGELOG.md` as public narrative below proof authority.
- Keep `scripts/release_check.py` as release audit glue below bundle-local
  review.
- Keep GitHub `Repo Validation` aligned with the root landing route.
- Keep release titles plain tag-shaped when publishing, for example `v0.3.3`.
- Keep sibling compatibility claims tied to CI or latest-sibling canary
  evidence.
- Keep readiness audits below tags, GitHub releases, PR approval, and goal
  completion.
- Keep package-owned audit and handoff artifacts under
  `mechanics/release-support/parts/`; keep `CHANGELOG.md`,
  `docs/operations/RELEASING.md`, `scripts/release_check.py`, and GitHub workflows in
  their root or GitHub-native lanes.

## Route Rules

- Tag, publish, or edit GitHub Releases only through an explicit release route.
- Fix evidence, scope, or checks rather than weakening validation to land a
  release.
- Treat a green release audit as release-support evidence below eval claim
  growth.
- Keep readiness audits below GitHub `Repo Validation` and release publication.
- Surface skipped checks explicitly in release handoffs.
- Mutate sibling repositories only through their owner routes.
- Promote bundle status through bundle-local review, with changelog wording as
  narrative evidence only.

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
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check
python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py --check
python mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py --repo-root . --format json
```

## Closeout

Report the release scope, which changelog section carries the narrative,
whether generated surfaces were rebuilt or checked, what `release_check.py` and
GitHub `Repo Validation` cover, which checks were skipped, whether sibling
compatibility was current or pinned, and which bundle-local proof boundaries
remain stronger than the release publication.
