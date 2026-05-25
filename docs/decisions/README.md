# Decision Records Index

This directory is the durable decision surface for `aoa-evals`.

Use it for meaningful choices about bounded proof topology, root surfaces,
agent-facing guidance, proof-object contracts, quest posture, mechanics, legacy,
validation, runtime-candidate intake, receipt posture, generated read models, or
sibling reference compatibility.

Ordinary edit summaries, generated output, release notes, runtime logs, private
evidence, and one-off planning thoughts route to their owning surfaces instead.

## Operating Card

| Field | Route |
| --- | --- |
| role | durable decision rationale entrypoint and agent-facing index chooser |
| entry | use when a structural, topology, validation, public-contract, legacy, runtime-candidate, sibling-reference, generated-index, or agent-route change needs recoverable rationale |
| input | changed source surface, owner boundary, rejected option, validation guard, or cross-surface route pressure |
| output | numbered decision note, metadata-backed lookup index, and route back to the source surface |
| owner | `docs/decisions/AGENTS.md` for lane law; numbered decisions for rationale; generated indexes for lookup only |
| next route | source surface first, then local route card, `docs/architecture/PROOF_TOPOLOGY.md`, `mechanics/EVIDENCE_CLUSTERS.md`, the generated lookup indexes, or the affected generated/runtime/sibling owner |
| validation | [docs/decisions/AGENTS.md#validation](AGENTS.md#validation), generated-index parity, and the owning route card for the changed surface |

## Authority

Decision notes explain why a route was chosen.

They are weaker than the source surface they describe:

- source eval package meaning stays in `evals/**/EVAL.md` and `eval.yaml`;
- system form stays in `DESIGN.md`;
- agent-facing shape stays in `DESIGN.AGENTS.md` and nearest `AGENTS.md` cards;
- technical proof model stays in `docs/architecture/ARCHITECTURE.md`;
- evaluation posture stays in `docs/guides/EVAL_PHILOSOPHY.md`;
- generated readers stay derived from their builders;
- runtime candidates and receipts stay below eval-package-local review;
- sibling repositories keep their own stronger truth.

Generated decision indexes are weaker than the numbered decision notes. They
exist to make lookup cheaper for agents, not to carry decision rationale.

## Index Shape

Each numbered decision owns its own `## Index Metadata` block:

- surface classes
- mechanic parents
- guard families
- posture

The lookup indexes under [indexes](indexes/README.md) are generated from that
metadata:

- [Decisions by number](indexes/by-number.md)
- [Decisions by surface class](indexes/by-surface.md)
- [Decisions by mechanic parent](indexes/by-mechanic.md)
- [Decisions by validation guard family](indexes/by-validation-guard.md)

Use them in both directions:

- top down: repo route -> authority class -> operation -> mechanic parent ->
  part -> validation guard -> decision rationale;
- bottom up: changed source surface -> local route card or part index ->
  validator guard -> decision rationale -> stronger owner surface.

Regenerate the read models after decision metadata changes:

`python scripts/generate_decision_indexes.py`

## Current Route

Open [Decisions by number](indexes/by-number.md) for the stable chronological
list. Open the grouped indexes only when the question starts from a surface
class, mechanic parent, or validation-guard family.

Do not hand-edit generated index files. Update the source decision metadata and
regenerate.

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
  `mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json` needs a live owner
  append.
- Further PR movement after the release-prep PR handoff only through current git
  and GitHub state; do not read
  `mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json` as live PR status after branch or PR
  creation.
- Goal completion only after `mechanics/release-support/parts/strategic-closeout/reports/strategic-closeout-audit-v1.json` is
  reread against the landed diff, GitHub `Repo Validation` is observed, and the
  owner-visible final closeout says the goal is actually complete.
- Future pinned sibling checkout refreshes only after the failing public CI lane
  is compared against current sibling truth and the local proof-reference map.

## Naming

Use monotonically increasing four-digit numbers:

`0107-short-decision-slug.md`

Prefer short titles that name the route, not the whole debate.

## Template

Start from [TEMPLATE.md](TEMPLATE.md) for new decisions. Keep notes concise, but
include enough context, alternatives, consequences, index metadata, and
validation for a future agent to avoid repeating the same mistake.
