# Decisions

This directory is the durable decision surface for `aoa-evals`.

Use it for meaningful choices about bounded proof topology, root surfaces,
agent-facing guidance, proof-object contracts, quest posture, mechanics, legacy,
validation, runtime-candidate intake, receipt posture, or sibling reference
compatibility.

Do not use it for ordinary edit summaries, generated output, release notes,
runtime logs, private evidence, or one-off planning thoughts.

## Authority

Decision notes explain why a route was chosen.

They are weaker than the source surface they describe:

- proof bundle meaning stays in `bundles/*/EVAL.md` and `eval.yaml`;
- system form stays in `DESIGN.md`;
- agent-facing shape stays in `DESIGN.AGENTS.md` and nearest `AGENTS.md` cards;
- technical proof model stays in `docs/ARCHITECTURE.md`;
- evaluation posture stays in `docs/EVAL_PHILOSOPHY.md`;
- generated readers stay derived from their builders;
- runtime candidates and receipts stay below bundle-local review;
- sibling repositories keep their own stronger truth.

## Current Decisions

- [0001 Root Design Spine](0001-root-design-spine.md)
- [0002 Proof Object Authority Contract](0002-proof-object-authority-contract.md)
- [0003 Sibling Proof Reference Compatibility](0003-sibling-proof-reference-compatibility.md)
- [0004 Questbook Topology](0004-questbook-topology.md)
- [0005 Proof Topology Map](0005-proof-topology-map.md)
- [0006 Questbook Mechanic Package](0006-questbook-mechanic-package.md)
- [0007 Runtime Evidence Mechanic Package](0007-runtime-evidence-mechanic-package.md)
- [0008 Sibling Proof Refs Mechanic Package](0008-sibling-proof-refs-mechanic-package.md)
- [0009 Legacy Naming Containment](0009-legacy-naming-containment.md)
- [0010 Proof Object Mechanic Package](0010-proof-object-mechanic-package.md)
- [0011 Comparison Spine Mechanic Package](0011-comparison-spine-mechanic-package.md)
- [0012 Proof Infra Mechanic Package](0012-proof-infra-mechanic-package.md)
- [0013 Publication Receipts Mechanic Package](0013-publication-receipts-mechanic-package.md)
- [0014 Proof Release Mechanic Package](0014-proof-release-mechanic-package.md)
- [0015 Titan Canaries Mechanic Package](0015-titan-canaries-mechanic-package.md)
- [0016 Agon Proof Mechanic Package](0016-agon-proof-mechanic-package.md)
- [0017 Spark Agent Lane Placement](0017-spark-agent-lane-placement.md)
- [0018 Quest Lane-State Source Layout](0018-quest-lane-state-source-layout.md)
- [0019 Proof Loop Mechanic Package](0019-proof-loop-mechanic-package.md)
- [0020 Proof Loop Local Smoke Report](0020-proof-loop-local-smoke-report.md)
- [0021 Quest Lifecycle Contract](0021-quest-lifecycle-contract.md)
- [0022 Proof Loop Bundle-Local Report](0022-proof-loop-bundle-local-report.md)
- [0023 Eval Report Index Reader](0023-eval-report-index-reader.md)
- [0024 Receipt Intake Dry Review](0024-receipt-intake-dry-review.md)
- [0025 Proof Release Readiness Audit](0025-proof-release-readiness-audit.md)
- [0026 Strategic Closeout Audit](0026-strategic-closeout-audit.md)
- [0027 Release Prep PR Handoff](0027-release-prep-pr-handoff.md)
- [0028 Repo Validation aoa-memo Pin Refresh](0028-repo-validation-aoa-memo-pin-refresh.md)

Canonical path: `docs/decisions/0020-proof-loop-local-smoke-report.md`.
Canonical path: `docs/decisions/0021-quest-lifecycle-contract.md`.
Canonical path: `docs/decisions/0022-proof-loop-bundle-local-report.md`.
Canonical path: `docs/decisions/0023-eval-report-index-reader.md`.
Canonical path: `docs/decisions/0024-receipt-intake-dry-review.md`.
Canonical path: `docs/decisions/0025-proof-release-readiness-audit.md`.
Canonical path: `docs/decisions/0026-strategic-closeout-audit.md`.
Canonical path: `docs/decisions/0027-release-prep-pr-handoff.md`.
Canonical path: `docs/decisions/0028-repo-validation-aoa-memo-pin-refresh.md`.

## Queued Decision Topics

These topics are known but should become decision notes only when they constrain
a concrete near-term change:

- Future maintained agent lanes beyond Spark.
- Stricter quest lifecycle transition rules after a real state movement needs
  them.
- Further proof-loop examples or checklists only after another reviewed local
  run needs them.
- A real eval-result receipt publication only after the dry-reviewed intake
  route from
  `reports/eval-result-receipt-intake-dry-review-v1.json` needs a live owner
  append.
- Further PR movement after the release-prep PR handoff only through current git
  and GitHub state; do not read
  `reports/release-prep-pr-handoff-v1.json` as live PR status after branch or PR
  creation.
- Goal completion only after `reports/strategic-closeout-audit-v1.json` is
  reread against the landed diff, GitHub `Repo Validation` is observed, and the
  owner-visible final closeout says the goal is actually complete.
- Future pinned sibling checkout refreshes only after the failing public CI lane
  is compared against current sibling truth and the local proof-reference map.

## Naming

Use monotonically increasing four-digit numbers:

`0016-short-decision-slug.md`

Prefer short titles that name the route, not the whole debate.

## Template

Start from [TEMPLATE.md](TEMPLATE.md) for new decisions. Keep notes concise, but
include enough context, alternatives, consequences, and validation for a future
agent to avoid repeating the same mistake.
