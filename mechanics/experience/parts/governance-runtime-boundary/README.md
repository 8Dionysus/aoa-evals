# Experience / Governance Runtime Boundary Part

## Role

This part owns the support route for Experience governance and runtime-boundary
verdict proof.

It keeps governance, charter, appeal, veto, stay-order, authority-resolution,
constitution-runtime, sealed-vote, runtime-integrity, replay-history, and ToS
governance verdict support together.

## Source Surfaces

- `mechanics/experience/parts/governance-runtime-boundary/docs/`
- `mechanics/experience/parts/governance-runtime-boundary/examples/`
- `mechanics/experience/parts/governance-runtime-boundary/schemas/`
- `mechanics/experience/parts/governance-runtime-boundary/tests/test_experience_wave4_seed_contracts.py`
- `mechanics/experience/parts/governance-runtime-boundary/docs/APPEAL_REVIEW_VERDICT.md`
- `mechanics/experience/parts/governance-runtime-boundary/docs/STAY_ORDER_ENFORCEMENT_VERDICT.md`
- `mechanics/experience/parts/governance-runtime-boundary/docs/VOTE_SEAL_INTEGRITY_VERDICT.md`
- `mechanics/experience/parts/governance-runtime-boundary/docs/REPLAY_HISTORY_INTEGRITY_VERDICT.md`

## Inputs

- governance verdict packets;
- charter amendment and appeal refs;
- stay-order authority and expiry refs;
- authority-resolution refs;
- runtime-boundary verdict packets;
- sealed-vote, replay-history, and ToS governance refs.

## Outputs

- bounded governance and runtime-boundary proof readings;
- schema/example contracts for governance verdict packets;
- owner handoff route when verdict packets require governance, runtime, or ToS
  authority.

## Stronger Owner Split

`Agents-of-Abyss` owns center law, constitution posture, governance language,
and Experience stop-lines. `abyss-stack` owns runtime behavior and runtime
enforcement. Tree-of-Sophia keeps authored meaning and canon. Owner
repositories own local authority resolution, appeal disposition, stay-order
execution, sealed-vote acceptance, and replay-history acceptance.

`aoa-evals` owns only bounded governance and runtime-boundary proof readings,
schema/example contracts, and bundle-local interpretation of verdict packets.

## Stop-Lines

This part must claim no governance authority, runtime enforcement, direct ToS
write, settled constitution interpretation, sealed-vote authority, appeal
authority, stay-order execution, or replay acceptance.

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
