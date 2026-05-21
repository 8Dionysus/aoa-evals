# Vote Seal Integrity Verdict

## Role

This note scopes vote-seal integrity verdicts for governance/runtime proof.

Vote seal verdicts compare a commit hash, reveal payload, and expected
disclosure route as bounded evidence.

## Reads

Use this surface when a governance packet cites sealed-vote evidence and needs a
proof read before owner acceptance.

## Boundary

`aoa-evals` may verify the vote-seal evidence shape. Governance owners keep
vote authority, ballot acceptance, reveal acceptance, and final decision
meaning.

Runtime law remains reviewable. Owner meaning remains owner-local.

## Validation

Use the governance-runtime-boundary README. The verdict should preserve the
commit/reveal distinction and route acceptance questions to the owner.
