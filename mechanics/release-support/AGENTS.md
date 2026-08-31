# AGENTS.md

## Entry Route

When package semantics or direction are relevant, consult the package README and then the `mechanics/release-support/DIRECTION.md`, `mechanics/release-support/PARTS.md`, and `mechanics/release-support/PROVENANCE.md` routes as needed for the touched source.

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

## Local Law

- Keep release scope bounded and reviewable.
- Keep `CHANGELOG.md` as public narrative below proof authority.
- Keep `scripts/release_check.py` as release audit glue below bundle-local
  review.
- Keep GitHub `Repo Validation` aligned with the root landing route.
- Keep release titles plain tag-shaped when publishing, for example `v0.3.3`.
- Keep sibling compatibility claims tied to CI or latest-sibling canary
  evidence.
- Keep OS Abyss artifact bundle verification under the `abyss-machine`
  policy/verifier route; release-support manifests name the carried artifact,
  not a local signing doctrine.
- Keep readiness audits below tags, GitHub releases, PR approval, and goal
  completion.
- Keep package-owned audit and handoff artifacts under
  `mechanics/release-support/parts/`; keep `CHANGELOG.md`,
  `docs/operations/RELEASING.md`, `scripts/release_check.py`, and GitHub workflows in
  their root or GitHub-native lanes.

Each package keeps current operating direction in `DIRECTION.md`; the active-to-archive bridge in `PROVENANCE.md` is consulted only when legacy names are involved.

Readiness and handoff report routes remain
`mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json`
and `mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json`;
live PR or GitHub `Repo Validation` state stays owner-visible.

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

Use the on-demand [VALIDATION.md](VALIDATION.md) route for executable checks.

Run the narrow package route checks:

Run generated and sibling checks when the release scope includes those
surfaces:

## Closeout

Report the release scope, which changelog section carries the narrative,
whether generated surfaces were rebuilt or checked, what `release_check.py` and
GitHub `Repo Validation` cover, which checks were skipped, whether sibling
compatibility was current or pinned, and which bundle-local proof boundaries
remain stronger than the release publication.
