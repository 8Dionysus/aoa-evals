# Spark and Legacy Surface Retirement

- Decision ID: AOA-EV-D-0257
- Status: Accepted
- Date: 2026-09-04
- Owner surface: retired Spark lane and mechanics legacy scaffolding

## Index Metadata

- Original date: 2026-09-04
- Surface classes: legacy, validation guard, source/topology
- Mechanic parents: cross-parent
- Guard families: source/topology, observability/audit
- Posture: active rationale

## Decision

Retire the tracked `.agents/spark/` lane and all `mechanics/*/legacy/`
subtrees from the current `aoa-evals` tree. Remove validators and tests whose
only purpose was archive skeleton, route-language, or raw-payload accounting.
Keep active mechanic `PROVENANCE.md` checks as a narrow bridge: active routes
remain authoritative and historical details are reachable only through the
pinned immutable Git links below. Eval statuses, categories, baselines, and
proof meaning are unchanged.

## Recovery

Every retired subtree is recoverable from the exact baseline commit
`f44dbe693d1236d4e3adf7ab61bf21a444fcb929`; each link is immutable and every
baseline blob was verified before retirement:

- [.agents/spark](https://github.com/8Dionysus/aoa-evals/tree/f44dbe693d1236d4e3adf7ab61bf21a444fcb929/.agents/spark)
- [mechanics/agon/legacy](https://github.com/8Dionysus/aoa-evals/tree/f44dbe693d1236d4e3adf7ab61bf21a444fcb929/mechanics/agon/legacy)
- [mechanics/antifragility/legacy](https://github.com/8Dionysus/aoa-evals/tree/f44dbe693d1236d4e3adf7ab61bf21a444fcb929/mechanics/antifragility/legacy)
- [mechanics/audit/legacy](https://github.com/8Dionysus/aoa-evals/tree/f44dbe693d1236d4e3adf7ab61bf21a444fcb929/mechanics/audit/legacy)
- [mechanics/boundary-bridge/legacy](https://github.com/8Dionysus/aoa-evals/tree/f44dbe693d1236d4e3adf7ab61bf21a444fcb929/mechanics/boundary-bridge/legacy)
- [mechanics/checkpoint/legacy](https://github.com/8Dionysus/aoa-evals/tree/f44dbe693d1236d4e3adf7ab61bf21a444fcb929/mechanics/checkpoint/legacy)
- [mechanics/comparison-spine/legacy](https://github.com/8Dionysus/aoa-evals/tree/f44dbe693d1236d4e3adf7ab61bf21a444fcb929/mechanics/comparison-spine/legacy)
- [mechanics/distillation/legacy](https://github.com/8Dionysus/aoa-evals/tree/f44dbe693d1236d4e3adf7ab61bf21a444fcb929/mechanics/distillation/legacy)
- [mechanics/experience/legacy](https://github.com/8Dionysus/aoa-evals/tree/f44dbe693d1236d4e3adf7ab61bf21a444fcb929/mechanics/experience/legacy)
- [mechanics/growth-cycle/legacy](https://github.com/8Dionysus/aoa-evals/tree/f44dbe693d1236d4e3adf7ab61bf21a444fcb929/mechanics/growth-cycle/legacy)
- [mechanics/method-growth/legacy](https://github.com/8Dionysus/aoa-evals/tree/f44dbe693d1236d4e3adf7ab61bf21a444fcb929/mechanics/method-growth/legacy)
- [mechanics/proof-infra/legacy](https://github.com/8Dionysus/aoa-evals/tree/f44dbe693d1236d4e3adf7ab61bf21a444fcb929/mechanics/proof-infra/legacy)
- [mechanics/proof-loop/legacy](https://github.com/8Dionysus/aoa-evals/tree/f44dbe693d1236d4e3adf7ab61bf21a444fcb929/mechanics/proof-loop/legacy)
- [mechanics/proof-object/legacy](https://github.com/8Dionysus/aoa-evals/tree/f44dbe693d1236d4e3adf7ab61bf21a444fcb929/mechanics/proof-object/legacy)
- [mechanics/publication-receipts/legacy](https://github.com/8Dionysus/aoa-evals/tree/f44dbe693d1236d4e3adf7ab61bf21a444fcb929/mechanics/publication-receipts/legacy)
- [mechanics/questbook/legacy](https://github.com/8Dionysus/aoa-evals/tree/f44dbe693d1236d4e3adf7ab61bf21a444fcb929/mechanics/questbook/legacy)
- [mechanics/recurrence/legacy](https://github.com/8Dionysus/aoa-evals/tree/f44dbe693d1236d4e3adf7ab61bf21a444fcb929/mechanics/recurrence/legacy)
- [mechanics/release-support/legacy](https://github.com/8Dionysus/aoa-evals/tree/f44dbe693d1236d4e3adf7ab61bf21a444fcb929/mechanics/release-support/legacy)
- [mechanics/rpg/legacy](https://github.com/8Dionysus/aoa-evals/tree/f44dbe693d1236d4e3adf7ab61bf21a444fcb929/mechanics/rpg/legacy)
- [mechanics/titan/legacy](https://github.com/8Dionysus/aoa-evals/tree/f44dbe693d1236d4e3adf7ab61bf21a444fcb929/mechanics/titan/legacy)

## Boundaries

This decision does not change eval status, category, baseline mode, claim
meaning, proof verdicts, or runtime/owner acceptance. It does not recreate an
archive directory or make Git history an active topology route.

## Validation

Regenerate decision and validation inventories through their canonical
builders. Run the full source owner gate; CI, merge, deployment, runtime, and
cross-owner acceptance remain outside this local decision.
